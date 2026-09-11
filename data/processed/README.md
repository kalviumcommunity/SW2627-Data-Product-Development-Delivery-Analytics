# Processed Data

This directory contains cleaned and transformed data ready for analysis.

The CSV files are versioned pipeline outputs. The scheduled GitHub Actions job
regenerates them from `data/raw/` and opens a pull request with any changes.
Keeping the outputs in the repository gives the dashboard and reviewers a
stable, inspectable snapshot without requiring the pipeline to run locally.

**Rule:** Only use data from this directory for analysis. Do not edit the CSV
outputs manually; update the raw data or pipeline code and regenerate them.
