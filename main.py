import json
import os
import structlog

logger = structlog.get_logger()


def process_raw_log_data(raw_log_data: str) -> list:
    """converts the raw log data to readable format.

    Args:
        raw_log_data (str): the raw log data.

    Returns:
        list: list of json objects.
    """
    logger.info('Processing raw log data')
    formatted_log_data = []
    for line in raw_log_data.split('>>>'):
        line = line.strip()
        if line:
            parsed_line = json.loads(line)
            message = parsed_line.get('message', '')
            timestamp = parsed_line.get('@timestamp', '')
            timestamp = timestamp.replace('T', ' ').replace('Z', '')
            level = parsed_line.get('log', {}).get('level', '')
            formatted_log_data.append(f'{timestamp} [{level}] {message}')
    return formatted_log_data


# Read data from file
INPUT_FILENAME = str(input('Enter the absolute path of the log file: '))
with open(INPUT_FILENAME, 'r', encoding='utf-8') as file:
    logger.info('Reading data from file')
    data = file.read()

# Process the data
output = process_raw_log_data(data)
os.mkdir(os.getcwd() + '/outputs')
output_filename = os.getcwd() + '/outputs/new_agent_log.log'

with open(output_filename, 'w', encoding='utf-8') as file:
    for log_event in output:
        file.writelines(log_event + '\n')

logger.info('Successfully generated new_agent_log.log')
