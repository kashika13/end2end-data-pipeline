"""Function for preprocessing the data"""

import pandas as pd
from src.logger import logging


def merge_datasets(call_logs_df,agent_roster_df,disposition_df):
    """Merge the 3 datasets based on agent_id,org_id and call_data"""

    logging.info("Merging datasets")

    # First merge call logs with agent roster
    merged_df = pd.merge(
        call_logs_df,
        agent_roster_df,
        on=["agent_id", "org_id"],
        how="left",
        indicator=True
    )

    # Check for unmatched records
    unmatched_calls = merged_df[merged_df["_merge"] == "left_only"].shape[0]
    if unmatched_calls > 0:
        logging.warning(f"Found {unmatched_calls} call records with no matching agent info")

    # Remove the indicator column
    merged_df = merged_df.drop(columns=["_merge"])

    # Now merge with disposition summary
    full_merged_df = pd.merge(
        merged_df,
        disposition_df,
        on=["agent_id", "org_id", "call_date"],
        how="left",
        indicator=True
    )
    
    # Check for unmatched records after second merge
    unmatched_records = full_merged_df[full_merged_df["_merge"] == "left_only"].shape[0]
    if unmatched_records > 0:
        logging.warning(f"Found {unmatched_records} call records with no disposition data")
    
    # Remove the indicator column
    full_merged_df = full_merged_df.drop(columns=["_merge"])
    
    return full_merged_df



def calculate_agent_metrics(merged_df):
    """Calculate performance metrics for each agent on each date."""

    logging.info("Calculating agent performance metrics")

    # Create presence indicator
    merged_df["presence"] = merged_df["login_time"].notna().astype(int)

    # Group by agent, org, and date
    performance_df = merged_df.groupby(["agent_id", "org_id", "call_date", "users_first_name", "users_last_name", "users_office_location"]).agg(
        total_calls=("call_id", "count"),
        unique_loans=("installment_id", pd.Series.nunique),
        completed_calls=("status", lambda x: (x == "completed").sum()),
        total_duration=("duration", "sum"),
        avg_duration=("duration", "mean"),
        presence=("presence", "max")
    ).reset_index()
    
    # Calculate connect rate
    performance_df["connect_rate"] = (performance_df["completed_calls"] / performance_df["total_calls"]).fillna(0)
    
    return performance_df


def process_data(call_logs_df, agent_roster_df, disposition_df):
    """Process the data through the full pipeline."""

    # Merge the datasets
    merged_df = merge_datasets(call_logs_df, agent_roster_df, disposition_df)
    
    # Calculate the metrics
    performance_df = calculate_agent_metrics(merged_df)
    
    return performance_df
