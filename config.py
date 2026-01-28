ROOT_DIR = "~/factorio"
LOG_DIR = f"{ROOT_DIR}/logs"

SERVER_EXECUTABLE = f"{ROOT_DIR}/bin/x64/factorio"
MAP_NAME = ""
SERVER_CONFIGS = "-log -NoBattlEye -crossplay"

START_SERVER_SCRIPT = f"{ROOT_DIR}/bin/x64/factorio {SERVER_CONFIGS} --start-server {ROOT_DIR}/saves/{MAP_NAME}.zip"
UPDATE_SERVER_SCRIPT = f"{ROOT_DIR}/update_server.bat"
