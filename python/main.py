from flask import Flask, redirect, render_template, request, jsonify
import os
import platform
import psutil
import subprocess

app = Flask("ballsOS")


def find_woi_files(start_path="/"):
    woi_files = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith(".WOI"):
                woi_files.append(os.path.join(root, file))
    return woi_files

def get_mountable_drives():
    result = subprocess.run(['mount'], capture_output=True, text=True)
    mounts = result.stdout.splitlines()
    mount_points = []
    for mount in mounts:
        parts = mount.split(' ')
        if len(parts) > 2:
            mount_points.append(parts[2])
    return mount_points


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
        "name":  platform.node(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "machine": platform.machine()
    }
    
    
    
    
    return(info)

@app.route("/listWOIs")
def listWOIs():
    mount_points = get_mountable_drives()
    all_woi_files = []
    for mount_point in mount_points:
        all_woi_files.extend(find_woi_files(mount_point))
    
    return jsonify(all_woi_files)
    

@app.route("/installWOI")
def  installWOI():
    path = request.form.get("path")
    



if __name__ == '__main__':
    app.run("127.0.0.1", 8080, debug=True )