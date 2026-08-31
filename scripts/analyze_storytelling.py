"""
Data Storytelling & Insight Narrative Demo Script
Demonstrates creating compelling data stories and insight narratives.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from src.storytelling.story_narrative import (
    generate_insight_narrative,
    create_story_structure,
    get_business_context,
    validate_story_data,
    extract_key_insights,
    format_narrative_text,
    get_storytelling_recommendations
)
from src.ingestion.load_data import load_csv


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    
    print("=" * 60)
    print("DATA STORYTELLING & INSIGHT NARRATIVE")
    print("=" * 60)
    
    # Load datasets
    print("\n--- Loading Data ---")
    datasets = {}
    for filename, label in [("timesheets_raw.csv", "Timesheets")]:
        file_path = data_dir / filename
        if file_path.exists():
            df = load_csv(str(file_path))
            datasets[label] = df
            print(f"Loaded {label}: {len(df)} rows")
    
    # Generate insight narrative
    print("\n" + "=" * 60)
    print("INSIGHT NARRATIVE")
    print("=" * 60)
    
    if 'Timesheets' in datasets:
        ts = datasets['Timesheets']
        narrative = generate_insight_narrative(ts, 'hours_logged')
        print(narrative[:200] + "...")
    
    # Create story structure
    print("\n" + "=" * 60)
    print("STORY STRUCTURE")
    print("=" * 60)
    
    structure = create_story_structure(
        "Employee Utilization Analysis",
        ["Introduction", "Key Metrics", "Trend Analysis", "Key Insights"],
        "Conclusion & Recommendations"
    )
    print(f"Title: {structure['title']}")
    print(f"Sections: {structure['total_sections']}")
    print(f"Has Conclusion: {structure['has_conclusion']}")
    
    # Business context
    print("\n" + "=" * 60)
    print("BUSINESS CONTEXT")
    print("=" * 60)
    
    context = get_business_context('utilization', 'Consulting')
    print(context)
    
    # Validate story data
    print("\n" + "=" * 60)
    print("DATA VALIDATION")
    print("=" * 60)
    
    validation = validate_story_data(ts, ['employee_id', 'hours_logged', 'task_category'])
    print(f"Valid: {validation['valid']}")
    print(f"Row count: {validation['row_count']}")
    print(f"Meets minimum: {validation['meets_minimum']}")
    print(f"Data quality score: {validation['data_quality_score']}")
    
    # Extract key insights
    print("\n" + "=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)
    
    insights = extract_key_insights(ts, 'hours_logged', 'task_category', top_n=3)
    for insight in insights:
        print(f"  {insight['rank']}. {insight['insight']}")
    
    # Storytelling recommendations
    print("\n" + "=" * 60)
    print("STORYTELLING RECOMMENDATIONS")
    print("=" * 60)
    
    recommendations = get_storytelling_recommendations(ts, 'hours_logged', 'task_category')
    print(f"Has trend: {recommendations['has_trend']}")
    print(f"Has groups: {recommendations['has_groups']}")
    print(f"Recommended structure: {recommendations['suggested_visualizations']}")
    print(f"Key message: {recommendations['key_message']}")
    
    # Format narrative
    print("\n" + "=" * 60)
    print("FORMATTED NARRATIVE")
    print("=" * 60)
    
    formatted = format_narrative_text(narrative, 500)
    print(formatted[:500] + "...")
    
    print(f"\n{'=' * 60}")
    print("DATA STORYTELLING COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()