from flask import Flask, redirect, render_template, request, jsonify
import os
import platform
import psutil
import subprocess

app = Flask("ballsOS")


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
        "machine": platform.machine()
    }
    
    return jsonify(info)


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



if __name__ == '__main__':
    app.run("127.0.0.1", 8080, debug=True)
