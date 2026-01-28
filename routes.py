import json

from loggers import logger, MemoryHandler
from flask import Flask, Response, render_template, jsonify, request
from factions import server_state, start_server, stop_server, update_server, send_rcon, add_mod, remove_mod

from config import *


app = Flask(__name__,
            static_folder='./static',
            template_folder='./templates')


with server_state.lock:
    app.extensions["ark_state"] = server_state


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start-server')
def start_server_route():
    with server_state.lock:
        if start_server():
            return Response("Server ON", mimetype='text/plain')
        return Response("Server OFF", mimetype='text/plain')


@app.route('/stop-server')
def stop_server_route():
    with server_state.lock:
        if stop_server():
            return Response("Server OFF", mimetype='text/plain')
        return Response("Server ON", mimetype='text/plain')


@app.route('/update-server')
def update_server_route():
    with server_state.lock:
        if update_server():
            return Response("Server updated", mimetype='text/plain')
        return Response("Server ON", mimetype='text/plain')


@app.route('/list-players')
def list_players_route():
    with server_state.lock:
        return Response(server_state.response_text, mimetype='text/plain')


@app.post('/send-rcon-command')
def send_rcon_command():
    if not request.is_json or not request.json:
        return Response("Invalid JSON", status=400, mimetype='text/plain')

    command = request.json.get("command", "")
    if not command:
        return Response("No command provided", status=400, mimetype='text/plain')

    response = send_rcon(command)
    if response:
        return jsonify({"response": response})
    return Response("Failed to send RCON command", status=500, mimetype='text/plain')


@app.route("/get-logs")
def get_logs():
    for handler in logger.handlers:
        if isinstance(handler, MemoryHandler):
            return jsonify(handler.get_logs())
    return jsonify([])


def check_mod(mod_id):
    url = f"https://www.curseforge.com/projects/{mod_id}"
    try:
        # scraper = cloudscraper.create_scraper()
        # response = scraper.get(url, allow_redirects=False, timeout=10)
        # if response.status_code in (301, 302, 308):
        #     real_url = response.headers.get('Location', '')
        #     if 'ark-survival-ascended' in real_url.lower():
        #         return {"valid": True, "mod_name": real_url.split('/')[-1]}
        # return {"valid": False, "status_code": response.status_code}
        return {"valie": True, "status_code": 200}  # Placeholder implementation
    except Exception as e:
        return {"valid": False, "error": str(e)}


@app.route('/check-mod/<int:mod_id>')
def check_mod_route(mod_id):
    result = check_mod(mod_id)
    return jsonify(result)


@app.route('/list-mods')
def list_mods_route():
    with open("webfiles/webmanager/mods.json", "r") as f:
        mods = json.load(f)
    return jsonify(mods)


@app.post('/add-mod')
def add_mod_route():
    if not request.is_json or not request.json:
        return Response("Invalid JSON", status=400, mimetype='text/plain')
    mod_id = request.json.get("mod_id", "")
    mod_name = request.json.get("mod_name", "")
    if add_mod(mod_id, mod_name):
        return Response(f"Mod {mod_name} added", mimetype='text/plain')
    return Response(f"Mod {mod_name} added", mimetype='text/plain')


@app.post('/remove-mod')
def remove_mod_route():
    if not request.is_json or not request.json:
        return Response("Invalid JSON", status=400, mimetype='text/plain')
    mod_id = request.json.get("mod_id", "")
    if remove_mod(mod_id):
        return Response(f"Mod {mod_id} removed", mimetype='text/plain')
    return Response(f"Mod {mod_id} not found", status=404, mimetype='text/plain')
