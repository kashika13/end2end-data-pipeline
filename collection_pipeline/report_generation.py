"""Function for generating report and saving performance report"""

from src.logger import logging
import sys
from src.exception import CustomException


def save_performance_report(performance_df, output_path):

    try:
        performance_df.to_csv(output_path, index=False)
        logging.info(f"Performance summary saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to save performance report: {e}")
        raise CustomException(e,sys)



def generate_report(performance_df,date=None):

    logging.info("Generating Report")

    if date is None:
        # Get latest date
        date=performance_df["call_date"].max()

    # Filter for just the specified date
    daily_df = performance_df[performance_df["call_date"] == date]
    
    if daily_df.empty:
        return f"No data available for {date}"
    
    # Find Top Performer
    top_performer = performance_df.loc[performance_df["connect_rate"].idxmax()]
    top_name = f"{top_performer['users_first_name']} {top_performer['users_last_name']}"
    top_rate = top_performer["connect_rate"] * 100

    # Calculate summary metrics
    active_agents = daily_df[daily_df["presence"] == 1].shape[0]
    avg_duration = daily_df["avg_duration"].mean()

    # Create the summary message
    summary = f"""
    Agent Summary for {date}
    Top Performer: {top_name} ({top_rate:.0f}% connect rate)
    Total Active Agents: {active_agents}
    Average Duration: {avg_duration:.1f} min
    """
    return summary




