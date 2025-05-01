'''Function for loading and validating csv files'''


import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException
import os
artifacts_path = "./artifacts"
os.makedirs(artifacts_path, exist_ok=True)

def load_and_validate_data(file_path,expected_columns,file_type):
    try:
        logging.info(f"Loading {file_type} data from {file_path}")
        df=pd.read_csv(file_path)

        # Check if all expected columns are present
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            logging.error(f"Missing columns in {file_type}: {missing_columns}")
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check for duplicate entries
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            logging.warning(f"Found {duplicate_count} duplicate rows in {file_type}")

        # Check for missing values in key columns
        key_columns = ["agent_id", "org_id"]
        if "call_date" in expected_columns:
            # Ensure date colums are in correct format
            df["call_date"] = pd.to_datetime(df["call_date"]).dt.date
            
        for col in key_columns:
            if col in df.columns:
                missing_count = df[col].isna().sum()
                if missing_count > 0:
                    logging.warning(f"Found {missing_count} missing values in {col} column")

        # Save the dataframe to artifacts folder
        output_file_path = os.path.join(artifacts_path, f"{file_type.replace(' ', '_')}.csv")
        df.to_csv(output_file_path, index=False)
        logging.info(f"Saved {file_type} data to {output_file_path}")


        return df
    
    except Exception as e:
        raise CustomException(e,sys)


def load_all_data(call_logs_path,agent_roster_path,disposition_summary_path):

    # Define expected columns for each file
    call_logs_columns = ["call_id", "agent_id", "org_id", "installment_id", 
                        "status", "duration", "created_ts", "call_date"]
    agent_roster_columns = ["agent_id", "users_first_name", "users_last_name", 
                           "users_office_location", "org_id"]
    disposition_columns = ["agent_id", "org_id", "call_date", "login_time"]

    # Load and validate each file
    call_logs_df = load_and_validate_data(call_logs_path, call_logs_columns, "call logs")
    agent_roster_df = load_and_validate_data(agent_roster_path, agent_roster_columns, "agent roster")
    disposition_df = load_and_validate_data(disposition_summary_path, disposition_columns, "disposition summary")
    
    return call_logs_df, agent_roster_df, disposition_df