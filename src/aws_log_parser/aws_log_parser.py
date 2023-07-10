import click
import json
import os
import structlog

logger = structlog.get_logger()

MIGRATION_SERVICES = ["ce", "drs", "mgn"]
CE_LOG_DIR = "/var/lib/aws-replication-agent"
CE_LOG_FILE = "agent.log.0"


def log_dir_exists(service) -> bool:
    return service in MIGRATION_SERVICES and os.path.exists(CE_LOG_DIR)


def log_file_in_current_dir(service) -> bool:
    current_dir = os.getcwd()
    return service in MIGRATION_SERVICES and os.path.exists(os.path.join(current_dir, CE_LOG_FILE))


def parse_logs(raw_log_file):
    parsed_logs = []
    logger.info("parsing log file.")
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
    log_file = ""

    if log_dir_exists(service):
        log_file = os.path.join(CE_LOG_DIR, CE_LOG_FILE)
    elif log_file_in_current_dir(service):
        log_file = os.path.join(os.getcwd(), CE_LOG_FILE)

    if log_file:
        logger.info(f"located {log_file}.")
        output = parse_logs(log_file)
    else:
        logger.critical("no raw logs found.")

    click.echo_via_pager(output)


if __name__ == '__main__':
    main()
