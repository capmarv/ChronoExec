import subprocess

ALLOWED_COMMANDS = {
    "SYSTEM_INFO": "uname -a",
    "HOSTNAME": "hostname",
    "CURRENT_USER": "whoami",
    "UPTIME": "uptime",

    "PROCESS_LIST": "ps aux",
    "DISK_USAGE": "df -h",
    "CURRENT_DIRECTORY": "pwd",

    "LIST_FILES": "ls -la",

    "CURRENT_TIME": "date",
}

def execute_command(command_name):

    if command_name not in ALLOWED_COMMANDS:
        return "Command not allowed"

    command = ALLOWED_COMMANDS[command_name]

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return result.stderr

    return result.stdout
