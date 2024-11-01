from flask import Flask, render_template, jsonify, request
import json, subprocess, webbrowser

app = Flask(__name__)

@app.route("/")
def dash():
    with open("schema.json", "r") as f:
        schema = json.load(f)
    return render_template("dashboard.html", schema=schema)

@app.route("/activate", methods=["POST"])
def activate():
    data = request.json
    item_id = data.get("id")
    with open("schema.json", "r") as f:
        schema = json.load(f)
    for item in schema["dashboard_items"]:
        if item["id"] == item_id:
            break
    action_type = item["action"]["type"]
    if action_type == "command": subprocess.Popen(item["action"]["data"]["command"], shell=True)
    elif action_type == "uri":
        if item["action"]["data"]["handler"] == "system": webbrowser.open(item["action"]["data"]["uri"])
        else: subprocess.Popen(f"{item['action']['data']['handler']} {item["action"]["data"]["uri"]}", shell=True)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
