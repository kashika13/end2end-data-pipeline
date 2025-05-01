# DPDzero DataOps Assignment

This project implements a full end-to-end data pipeline for daily collection of call data using Python and pandas. It fetches, validates, merges, transforms, and reports agent-level performance metrics with an optional Slack-style summary.

---

## Objective

Build a simplified data pipeline that:

- Ingests daily CSVs from different sources
- Validates and cleans the data
- Merge CSVs using agent_id, org_id, and call_date
- Perform feature engineering and compute performance
- Output the performance summary and give a slack like report

---

## Input Files

| File Name              | Description |
|------------------------|-------------|
| `call_logs.csv`        | Contains call-level data like agent_id, status, duration, call_date |
| `agent_roster.csv`     | Static metadata for agents (name, location, org_id) |
| `disposition_summary.csv` | Presence data showing login times per agent/date |

---

## Features

Data Ingestion and Validation  
Merge Logic (joins by `agent_id`, `org_id`, and `call_date`)  
Feature Engineering and performance metrics calculation  
Slack-Style Summary  
Logging & CLI Support

---

## Metrics Calculated

For each agent and each call date:
- Total Calls Made
- Unique Loans Contacted (`installment_id`)
- Connect Rate = Completed Calls / Total Calls
- Average Call Duration (in minutes)
- Presence (1 if login_time exists, else 0)

---

## Output 

- `agent_performance_summary.csv` – full per-agent performance report
- Printed summary in terminal for a particular date

---

## Project Breakdown

The repository contains the following files:
- `main.py`: Entry point of the pipeline.
- `src/`: Directory containing exception handling and logging.
  -  `__init__.py`: Marks the folder as a Python package.
  -  `logger.py` : Handles application logging for debugging and monitoring.
  -  `exception.py`: Defines custom exceptions for better error handling.
  -  `parse_cla.py`: Parses the argument.
- `collection_pipeline/`: Directory containing modules for data ingestion, preprocessing and report generation.
    - `__init__.py`: Marks the folder as a Python package.
    - `data_ingestion.py`: Fetches the data and validate it.
    - `data_preprocessing.py`: Joins the data and calculate performance metrics
    - `report_generation.py`: Generates report summary and save it.
- `notebook.ipynb` Jupyter Notebook used for exploring the dataset.
- `artifacts/`: Folder which stores input file and output file.
- `logs/` : Contains logging data

---

## How to Use

You can run the main file as:

```bash
python main.py.
```
In this case, it will use the files which are already stored in artifacts folder and save the the output file(agent_performance_summary) in artifacts folder.


or
```bash
python main.py \
  --call_logs /path/to/call_logs.csv \
  --agent_roster /path/to/agent_roster.csv \
  --disposition_summary /path/to/disposition_summary.csv \
  --output /path/to/output.csv
```
In this case, it will store the input csv files (call_logs,agent_roster, disposition_summary) into artifacts folder and save the output file (agent_performance_summary) in the specified path.

---

## How mismatches are handled in join logic?

The merging logic is designed to preserve all call records, even when corresponding agent or login data is missing. This is achieved using left join and proper handling of missing values.

### Merge Steps:

- call_logs is joined with agent_roster on agent_id and org_id.
- The result is then joined with disposition_summary on agent_id, org_id, and call_date.
- In both steps, an _merge indicator column is used to detect unmatched records, and mismatched are logged for any missing agent or login data and it is replaced with NaN in ther merged dataframe.

### Handling Missing Values:

- Missing fields are filled with defaults using .fillna(0).
- Presence is computed using .notna().astype(int).
- Aggregation functions like .mean() and .sum() automatically handle NaN values.




