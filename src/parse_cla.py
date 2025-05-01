import argparse
import os
artifacts_path = "./artifacts"
os.makedirs(artifacts_path, exist_ok=True)



def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process collection call data")
    parser.add_argument("--call_logs", type=str, default=os.path.join(artifacts_path,'call_logs.csv'),
                        help="Path to call logs CSV file")
    parser.add_argument("--agent_roster", type=str, default=os.path.join(artifacts_path,'agent_roster.csv'),
                        help="Path to agent roster CSV file")
    parser.add_argument("--disposition_summary", type=str, default=os.path.join(artifacts_path,'disposition_summary.csv'),
                        help="Path to disposition summary CSV file")
    parser.add_argument("--output", type=str, default=os.path.join(artifacts_path,'agent_performance_summary.csv'),
                        help="Path to output the performance summary CSV")
    return parser.parse_args()