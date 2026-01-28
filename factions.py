import json
import time
import threading
import subprocess
from datetime import datetime, timezone

from mcrcon import MCRcon
from controller import FactorioController

from loggers import logger, update_log_file
from config import *


def Facon():
    return MCRcon("127.0.0.1", "sudojimi", port=34200)

CONFIG_FILE = "config.json"


class ServerState:
    def __init__(self):
        self.controller: FactorioController = FactorioController(CONFIG_FILE)
        self.on: bool = False
        self.player_list: list[str] | None = None
        self.response_text: str = "Server OFF"
        self.lock = threading.Lock()

server_state = ServerState()


def server_is_running() -> bool:
    """ Checks if the factorio server is currently running.

    Returns:
        bool: True if the server is running, False otherwise.
    """
    if server_state.controller.server is not None and \
       server_state.controller.server.poll() is None:
        server_state.on = True
    else:
        server_state.on = False
    return server_state.on


def start_server():
    """ Starts the factorio server using a subprocess.

    Returns:
        bool: If the server is running after the call.
        Already running before calling also returns True.
    """

    server_state.on = True
    if server_is_running():
        logger.info("Server is already running.")
        return True

    logger.info("Starting server...")
    try:
        server_state.controller.start_server()
        logger.info("Server started successfully.")
        return True
    except Exception as e:
        logger.error("Error starting server: %s", e)
        return False


def stop_server():
    """ Stops the ARK server if it is running.

    Returns:
        bool: If the server was stopped successfully.
        If the server was not running, returns True.
    """
    server_state.on = False
    if server_is_running() is False:
        logger.info("Server is not running.")
        return True

    logger.info("Stopping server...")
    try:
        server_state.controller.stop_server()
        logger.info("Server stopped successfully.")
    except Exception as e:
        logger.error("Error stopping server: %s", e)
        return False
    update_log_file()
    logger.info("Server stopped, log file archived.")
    return True


def update_server():
    """ Updates the ARK server by running the update script.

    Returns:
        bool: If the server was updated successfully.
        Server must be stopped before updating.
    """

    logger.info("Updating server...")
    if server_is_running():
        logger.info("Server is running, please shutdown to update.")
        return False
    
    # TODO
    # subprocess.run(UPDATE_SERVER_SCRIPT, shell=True, check=True)
    logger.info("Server updated.")
    return True


def get_players() -> list[str] | None:
    # User "/players online" to get number of players
    # format: Online players (<count>): \n
    # format:   <player1> (Online)\n
    # format:   <player2> (Online)\n ...
    try:
        server = server_state.controller.server
        if server is None or server.poll() is not None:
            return None
        with Facon() as facon:
            response = facon.command("/players online")
            if not response:
                return None
            lines = response.split("\n")
            player_count_line = lines[0].strip()
            if player_count_line == "Online players (0):":
                return []
            players = [player.split("(")[0].strip() for player in lines[1:]]
            return players
    except Exception as e:
        logger.error("RCON command ListPlayers failed: %s", e)
    return None


def send_rcon(command: str):
    """ Sends an RCON command to the ARK server.

    Args:
        command (str): The RCON command to send.

    Returns:
        str: The response from the server.
    """
    if not server_is_running():
        logger.error("Server is not running, cannot send RCON command.")
        return "Server not running"
    try:
        with Facon() as facon:
            response: str = facon.command(command)
            if response:
                return response.strip()
            else:
                logger.error("No response from RCON command.")
                return "No response"
    except Exception as e:
        logger.error("RCON command failed: %s", e)
        return "RCON command failed"


def add_mod(mod_id: str, mod_name: str = ""):
    """ Adds a mod ID to the mods.json file.

    Args:
        mod_id (str): The mod ID to add.

    Returns:
        bool: True if the mod was added successfully, False otherwise.
    """
    try:
        with open("webfiles/webmanager/mods.json", "r") as f:
            mods = json.load(f)
        if mod_id not in mods:
            mods[mod_id] = mod_name
            with open("webfiles/webmanager/mods.json", "w") as f:
                json.dump(mods, f, indent=4)
            logger.info("Mod %s (%s) added successfully.", mod_name, mod_id)
            return True
        else:
            logger.info("Mod %s (%s) is already in the list.", mod_name, mod_id)
            return False
    except Exception as e:
        logger.error("Error adding mod ID %s: %s", mod_id, e)
        return False


def remove_mod(mod_id: str):
    """ Removes a mod ID from the mods.json file.

    Args:
        mod_id (str): The mod ID to remove.

    Returns:
        bool: True if the mod was removed successfully, False if it was not found.
    """
    try:
        with open("webfiles/webmanager/mods.json", "r") as f:
            mods = json.load(f)
        if mod_id in mods:
            mods = {id: name for id, name in mods.items() if id != mod_id}
            with open("webfiles/webmanager/mods.json", "w") as f:
                json.dump(mods, f, indent=4)
            logger.info("Mod %s removed successfully.", mod_id)
            return True
        else:
            logger.info("Mod %s not found in the list.", mod_id)
            return False
    except Exception as e:
        logger.error("Error removing mod ID %s: %s", mod_id, e)
        return False
