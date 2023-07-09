import click
import json
import os
import structlog

logger = structlog.get_logger()

MIGRATION_SERVICES = ["ce", "drs", "mgn"]
CE_LOG_DIR = "/var/lib/aws-replication-agent"
CE_LOG_FILE = "/agent.log.0"


def log_dir_exists(service):
    if service in MIGRATION_SERVICES:
        return os.path.exists(CE_LOG_DIR)
    else:
        logger.debug(f"{CE_LOG_DIR} not exist")
        return False


def log_file_exists(service):
    if service in MIGRATION_SERVICES:
        logger.debug(f"{os.getcwd() + CE_LOG_FILE} exist")
        return os.path.exists(os.getcwd() + CE_LOG_FILE)
    else:
        logger.debug(f"{os.path.exists(os.getcwd() + CE_LOG_FILE)} not exist")
        return False


def parse_logs(raw_log_file):
    parsed_logs = []
    with open(raw_log_file, "r") as raw_log_data:
        for line in raw_log_data:
            line = line.split('>>>')
            if line and line != ['\n']:
                parsed_line = json.loads(line[0])
                message = parsed_line.get('message', '')
                timestamp = parsed_line.get('@timestamp', '').replace('T', ' ').replace('Z', '')
                level = parsed_line.get('log', {}).get('level', '')
                exception_message = parsed_line.get('exception', {}).get('message', '')
                exception_trace = parsed_line.get('exception', {}).get('trace', '')

                log_line = f'{timestamp} [{level}] {message}\n'
                if exception_message:
                    log_line += f'{timestamp} [EXCEPTION] {exception_message}\n'
                if exception_trace:
                    log_line += f'{timestamp} [TRACE] {exception_trace}\n'

                parsed_logs.append(log_line)
        return parsed_logs



@click.command()
@click.argument('service')
def main(service="ce"):
    output = []
    if log_dir_exists(service):
        logger.warn(log_dir_exists(service))
        log_file = CE_LOG_DIR + CE_LOG_FILE
        logger.info(f"located {log_file}.")
        output = parse_logs(log_file)
    elif log_file_exists(service):
        logger.warn(log_dir_exists(service))
        log_file = os.getcwd() + CE_LOG_FILE
        logger.info(f"located {log_file}.")
        output = parse_logs(log_file)
    else:
        logger.critical(f"no raw logs found.")

    click.echo_via_pager(output)


if __name__ == '__main__':
    main()
