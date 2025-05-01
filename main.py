"""Main entry point for the data collection pipeline"""

import sys
import os
from src.logger import logging
from src.exception import CustomException
from src.parse_cla import parse_arguments
from collection_pipeline.data_ingestion import load_all_data
from collection_pipeline.data_preprocessing import process_data
from collection_pipeline.report_generation import generate_report, save_performance_report


def main():
    args=parse_arguments()
    if os.path.isdir(args.output):
        args.output = os.path.join(args.output, "agent_performance_summary.csv")

    try:
        # Step 1: Load and validate data
        logging.info("Starting data pipeline")
        call_logs_df, agent_roster_df, disposition_df = load_all_data(
            args.call_logs, 
            args.agent_roster, 
            args.disposition_summary
        )
        
        # Step 2: Process data
        performance_df = process_data(call_logs_df, agent_roster_df, disposition_df)
        
        # Step 3: Generate and save reports
        save_performance_report(performance_df, args.output)
        
        # Step 4: Print summary
        summary = generate_report(performance_df)
        print(summary)
        
        logging.info("Pipeline completed successfully")
    
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise CustomException(e,sys)


if __name__ == "__main__":
    main()