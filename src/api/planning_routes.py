"""Work Planning and employee lookup endpoints."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field

from src.api.dependencies import get_current_user, require_roles
from src.database import connection


router = APIRouter(tags=["work planning"])


class AssignmentInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    employee_id: str = Field(min_length=1, max_length=80)
    work_date: date
    start_time: time
    duration_hours: float = Field(gt=0, le=24)


class AssignmentResponse(AssignmentInput):
    id: int
    employee_name: str
    created_by: int | None
    created_at: str
    updated_at: str
    warnings: list[str] = []


class EmployeeResponse(BaseModel):
    employee_id: str
    employee_name: str
    team: str | None = None
    department: str | None = None
    capacity_hours_monthly: float | None = None


def _assignment_row(row, warnings: list[str] | None = None) -> AssignmentResponse:
    return AssignmentResponse(
        id=row["id"],
        title=row["title"],
        employee_id=row["employee_id"],
        employee_name=row["employee_name"],
        work_date=date.fromisoformat(row["work_date"]),
        start_time=time.fromisoformat(row["start_time"]),
        duration_hours=row["duration_hours"],
        created_by=row["created_by"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        warnings=warnings or [],
    )


def _warnings(conn, employee_id: str, work_date: date, start_time: time, duration: float, exclude_id: int | None = None) -> list[str]:
    start = datetime.combine(work_date, start_time)
    end = start + timedelta(hours=duration)
    query = """
        SELECT id, start_time, duration_hours
        FROM assignments
        WHERE employee_id = ? AND work_date = ?
    """
    params: list[object] = [employee_id, work_date.isoformat()]
    if exclude_id is not None:
        query += " AND id != ?"
        params.append(exclude_id)
    warnings: list[str] = []
    for row in conn.execute(query, params).fetchall():
        other_start = datetime.combine(work_date, time.fromisoformat(row["start_time"]))
        other_end = other_start + timedelta(hours=row["duration_hours"])
        if start < other_end and end > other_start:
            warnings.append("This assignment overlaps an existing assignment.")
            break

    capacity = conn.execute(
        "SELECT capacity_hours_monthly FROM employees WHERE employee_id = ?", (employee_id,)
    ).fetchone()
    if capacity and capacity["capacity_hours_monthly"]:
        month_start = work_date.replace(day=1).isoformat()
        total = conn.execute(
            """SELECT COALESCE(SUM(duration_hours), 0) AS total
               FROM assignments
               WHERE employee_id = ? AND work_date >= ? AND work_date < date(?, '+1 month')""",
            (employee_id, month_start, month_start),
        ).fetchone()["total"]
        if exclude_id is not None:
            old = conn.execute("SELECT duration_hours FROM assignments WHERE id = ?", (exclude_id,)).fetchone()
            total -= old["duration_hours"] if old else 0
        if total + duration > capacity["capacity_hours_monthly"]:
            warnings.append("This assignment exceeds the employee's monthly capacity.")
    return warnings


def _get_assignment(conn, assignment_id: int):
    return conn.execute(
        """SELECT a.*, e.employee_name
           FROM assignments a JOIN employees e ON e.employee_id = a.employee_id
           WHERE a.id = ?""",
        (assignment_id,),
    ).fetchone()


@router.get("/employees", response_model=list[EmployeeResponse])
def list_employees(_: dict = Depends(get_current_user)) -> list[EmployeeResponse]:
    with connection() as conn:
        rows = conn.execute(
            """SELECT employee_id, employee_name, team, department, capacity_hours_monthly
               FROM employees WHERE is_active = 1 ORDER BY employee_name"""
        ).fetchall()
    return [EmployeeResponse(**dict(row)) for row in rows]


@router.get("/assignments", response_model=list[AssignmentResponse])
def list_assignments(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    _: dict = Depends(get_current_user),
) -> list[AssignmentResponse]:
    query = """SELECT a.*, e.employee_name FROM assignments a
               JOIN employees e ON e.employee_id = a.employee_id WHERE 1 = 1"""
    params: list[object] = []
    if start_date:
        query += " AND a.work_date >= ?"
        params.append(start_date.isoformat())
    if end_date:
        query += " AND a.work_date <= ?"
        params.append(end_date.isoformat())
    query += " ORDER BY a.work_date, a.start_time, e.employee_name"
    with connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [_assignment_row(row) for row in rows]


@router.post("/assignments", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(request: AssignmentInput, user: dict = Depends(require_roles("admin", "manager"))) -> AssignmentResponse:
    with connection() as conn:
        employee = conn.execute("SELECT employee_id FROM employees WHERE employee_id = ? AND is_active = 1", (request.employee_id,)).fetchone()
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        warnings = _warnings(conn, request.employee_id, request.work_date, request.start_time, request.duration_hours)
        cursor = conn.execute(
            """INSERT INTO assignments
               (title, employee_id, work_date, start_time, duration_hours, created_by)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (request.title.strip(), request.employee_id, request.work_date.isoformat(), request.start_time.isoformat(), request.duration_hours, user["id"]),
        )
        row = _get_assignment(conn, cursor.lastrowid)
    return _assignment_row(row, warnings)


@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(assignment_id: int, request: AssignmentInput, _: dict = Depends(require_roles("admin", "manager"))) -> AssignmentResponse:
    with connection() as conn:
        if _get_assignment(conn, assignment_id) is None:
            raise HTTPException(status_code=404, detail="Assignment not found")
        employee = conn.execute("SELECT employee_id FROM employees WHERE employee_id = ? AND is_active = 1", (request.employee_id,)).fetchone()
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        warnings = _warnings(conn, request.employee_id, request.work_date, request.start_time, request.duration_hours, assignment_id)
        conn.execute(
            """UPDATE assignments SET title = ?, employee_id = ?, work_date = ?, start_time = ?,
               duration_hours = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?""",
            (request.title.strip(), request.employee_id, request.work_date.isoformat(), request.start_time.isoformat(), request.duration_hours, assignment_id),
        )
        row = _get_assignment(conn, assignment_id)
    return _assignment_row(row, warnings)


@router.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: int, _: dict = Depends(require_roles("admin", "manager"))) -> Response:
    with connection() as conn:
        cursor = conn.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Assignment not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
