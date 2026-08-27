# Team GitHub Workflow

This document establishes the branching, commit, and review conventions for the Employee Utilization Analytics project.

---

## Branching Strategy

### Main Branch
- `main` holds releasable, production-ready code only
- Never commit directly to main
- All changes go through feature branches and pull requests

### Feature Branch Naming
```
<LU-Number>-<type>/<short-description>
```

**Types:**
- `feature` — New functionality
- `fix` — Bug fixes
- `docs` — Documentation only
- `refactor` — Code restructuring without behavior change
- `chore` — Maintenance tasks

**Examples:**
- `2.11-setup/dev-environment`
- `2.12-feature/github-workflow-setup`
- `2.15-ingestion/csv-json-load`
- `2.18-cleaning/missing-values`
- `2.34-analytics/kpi-definition`

### Branch Lifecycle
1. Create branch from `main`
2. Work on the branch with atomic commits
3. Push to remote
4. Open pull request for review
5. Merge to `main` after approval
6. Delete branch after merge

---

## Commit Message Convention

### Format
```
<type>(<scope>): <short description>

[optional body explaining why]
```

### Types
| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix or correction |
| `docs` | Documentation changes only |
| `refactor` | Code cleanup without behavior change |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks (dependencies, CI, etc.) |

### Examples
```
feat(ingestion): add CSV loader with encoding detection
fix(cleaning): handle null values in billable_hours column
docs(profiling): add data dictionary for timesheet columns
refactor(analytics): extract KPI calculations to separate module
test(cleaning): add unit tests for deduplication logic
chore(pipeline): add logging configuration
```

### Rules
- Keep description under 72 characters
- Use imperative mood ("add" not "added")
- Reference issue number when applicable

---

## Pull Request Process

### PR Title
Clear, action-oriented title describing the change:
```
Add data validation workflow and team branching guidelines
```

### PR Description Template
```markdown
## Summary
[What this PR does and why]

## What Changed
- [List of specific changes]
- [Files modified/created]

## Related Issue
Closes #[issue-number]

## Testing
[How the changes were tested]
```

### Review Requirements
- At least one approval required before merge
- Review focuses on: correctness, clarity, data integrity
- Commit messages are reviewed as part of code review
- Address all feedback before merging

---

## GitHub Issue Tracking

### Issue Structure
- **Title:** Clear, action-oriented (e.g., "Implement data validation script")
- **Description:** Context, requirements, and done criteria
- **Labels:** Categorize work type
- **Assignee:** One person accountable

### Issue Lifecycle
1. Create issue before starting work
2. Link issue to branch and PR
3. PR auto-closes issue on merge
4. Issue provides permanent record of why code was written

---

## Workflow Summary

```
1. Pick/Create Issue
2. Create Feature Branch
3. Write Code + Commit (atomic commits)
4. Push Branch
5. Open PR (link issue)
6. Code Review
7. Merge to Main
8. Delete Branch
9. Issue Auto-Closes
```
