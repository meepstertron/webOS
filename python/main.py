from flask import Flask, redirect, render_template, request, jsonify, url_for, Response
import os
import platform
import psutil
import subprocess
import json
from flask_cors import CORS
import requests
from urllib.parse import urlparse
import paramiko








app = Flask("ballsOS")
CORS(app)


def run_ssh_command(host, username, password, command):
    """Connects to a remote host via SSH and runs a command."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname=host, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode()
        error = stderr.read().decode()
        return result if result else error
    except Exception as e:
        return str(e)
    finally:
        ssh.close()


def find_woi_files_everywhere():
    woi_files = []
    
    # Search for .WOI files starting from root ('/')
    for root, dirs, files in os.walk('/'):
        try:
            for file in files:
                # Case-insensitive check for .WOI extension
                if file.lower().endswith('.woi'):
                    woi_files.append(os.path.join(root, file))
        except PermissionError:
            # Skip directories/files without permissions
            continue
    
    return woi_files


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bios")
def bios():
    return render_template("bios.html")


@app.route("/systeminfo")
def info():
    info = {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "network": psutil.net_connections(kind='inet'),
        "name": platform.node(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "machine": platform.machine(),
        "version": "1.1"
    }
    
    return jsonify(info)


@app.route("/start")
def boot():
    # Define the path to the JSON file
    json_path = "/webOS/start.json"
    
    # Check if the file exists
    if os.path.exists(json_path):
        with open(json_path) as json_file:
            data = json.load(json_file)

            # Check if 'source' is in the data and is a valid path
            source = data.get("source")
            if source and os.path.isfile(source):
                # Redirect the user to the specified HTML file
                return redirect(url_for('serve_file', filename=source))
            else:
                # Render error template if 'source' is invalid
                error_message = "Invalid source path."
                return render_template('error.html', error=error_message)
    else:
        # Render error template if the JSON file doesn't exist
        error_message = "The start.json file does not exist."
        return render_template('error.html', error=error_message)

@app.route('/files/<path:filename>')
def serve_file(filename):
    # Assuming the HTML files are in a folder named 'html'
    return app.send_static_file(filename)
    

@app.route("/listWOIs")
def listWOIs():
    all_woi_files = find_woi_files_everywhere()
    return jsonify(all_woi_files)


@app.route("/installWOI", methods=["POST"])
def installWOI():
    path = request.form.get("path")
    os.mkdir("/webOS")
    print(path)
    return
# TODO: implement WOI installation

@app.route("/shutdown")
def  shutdown():
    os.system("shutdown now -h")
    return(200)
    
@app.route("/restart")
def restart():
    os.system("reboot now -h")
    return(200)

@app.route('/run-command', methods=['POST'])
def run_command():
    data = request.json
    host = data.get('host')
    username = data.get('username')
    password = data.get('password')
    command = data.get('command')

    if not all([host, username, password, command]):
        return jsonify({"error": "Missing parameters"}), 400

    result = run_ssh_command(host, username, password, command)
    print(result)
    return jsonify({"output": result})





if __name__ == '__main__':
    app.run("127.0.0.1", 8080, debug=True)
