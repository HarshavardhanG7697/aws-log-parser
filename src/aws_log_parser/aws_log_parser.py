import json
import os

import click
import structlog

logger = structlog.get_logger()

MIGRATION_SERVICES = ["ce", "drs", "mgn"]
CE_LOG_DIR = "/var/lib/aws-replication-agent"
CE_LOG_FILE = "agent.log.0"


def log_dir_exists(service: str) -> bool:
    return service in MIGRATION_SERVICES and os.path.exists(CE_LOG_DIR)


def log_file_in_current_dir(service: str) -> bool:
    current_dir = os.getcwd()
    return service in MIGRATION_SERVICES and os.path.exists(
        os.path.join(current_dir, CE_LOG_FILE)
    )


def parse_logs(raw_log_line: str) -> str:
    log_line = raw_log_line.split(">>>")
    formatted_log_line = ""

    if log_line and log_line != ["\n"]:
        parsed_line = json.loads(log_line[0])
        message = parsed_line.get("message", "")
        timestamp = parsed_line.get("@timestamp", "").replace("T", " ").replace("Z", "")
        level = parsed_line.get("log", {}).get("level", "")
        exception_message = parsed_line.get("exception", {}).get("message", "")
        exception_trace = parsed_line.get("exception", {}).get("trace", "")

        formatted_log_line = f"{timestamp} [{level}] {message}\n"
        if exception_message:
            formatted_log_line += f"{timestamp} [EXCEPTION] {exception_message}\n"
        if exception_trace:
            formatted_log_line += f"{timestamp} [TRACE] {exception_trace}\n"

    return formatted_log_line


@click.command()
@click.argument("service")
def main(service: str = "ce") -> None:
    output: list = []
    log_file = ""

    if log_dir_exists(service):
        log_file = os.path.join(CE_LOG_DIR, CE_LOG_FILE)
    elif log_file_in_current_dir(service):
        log_file = os.path.join(os.getcwd(), CE_LOG_FILE)

    if log_file:
        logger.info(f"located {log_file}.")
        output = []
        with open(log_file, "r") as raw_log_data:
            logger.info("parsing raw log file")
            for log_line in raw_log_data:
                output.append(parse_logs(log_line))
        click.echo_via_pager(output)
    else:
        logger.critical("no raw logs found.")


if __name__ == "__main__":
    main()
