import sys
import time
import signal
import threading
from datetime import datetime, timezone, timedelta


from loggers import logger
from routes import app, server_state
from factions import stop_server, get_players
# from utils import *


def poll():
    print("Starting player polling thread...")
    while True:
        with server_state.lock:
            server_state.player_list = get_players()

            if server_state.player_list:
                logger.info("Players connected: [%s]", ", ".join(server_state.player_list))
                server_state.response_text = "[" + ", ".join(server_state.player_list) + "]"

            elif server_state.on:
                logger.info("# Server ON, no players connected.")
                server_state.response_text = "Server ON and empty."

            else:
                logger.info("# Server OFF.")
                server_state.response_text = "Server OFF"

        time.sleep(5)


def on_interrupt(sig, _):
    logger.info("Received signal %s, shutting down server...", sig)
    stop_server()
    sys.exit(0)

signal.signal(signal.SIGINT, on_interrupt)
signal.signal(signal.SIGTERM, on_interrupt)


def main():
    threading.Thread(target=poll, daemon=True).start()
    # if set host to 0.0.0.0, it will be accessible from all network interfaces
    # by all, i mean even those in the colledge wifi, like mobile phone
    app.run(host="192.168.193.47", port=57270, debug=False)


if __name__ == "__main__":
    main()
