from datetime import datetime

async def generate_unique_name(prefix='Report_'):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_report_name = f"{prefix}{timestamp}"
    return unique_report_name

# Convert Unix timestamp to datetime
async def unix_to_datetime(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')



