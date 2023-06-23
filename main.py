import json
import logging

def process_data(data):
    output = []
    for line in data.split(">>>"):
        line = line.strip()
        if line:
            parsed_line = json.loads(line)
            message = parsed_line.get("message", "")
            timestamp = parsed_line.get("@timestamp", "")
            timestamp = timestamp.replace("T", " ").replace("Z", "")
            level = parsed_line.get("log", {}).get("level", "")
            output.append(f"{timestamp} [{level}] {message}")

    return output

# Read data from file
# filename = "agent.log.0"
filename = str(input("Enter the absolute path of the log file: "))
with open(filename, "r") as file:
    data = file.read()

# Process the data
output = process_data(data)

with open("new_agent.log.0", "w") as file:
    for log_event in output:
        file.write(log_event + "\n")

logging.critical("Successfully generated new_agent.log.0")