from flask import Flask
from flask import request
from flask import Response
from flask import g
import sqlite3
import json
app = Flask(__name__)

# get id
def getID(id):
    with sqlite3.connect("S:\Coding\Digivault_Server\Digivault_Server\Digivault_Server.db") as conn:
        c = conn.cursor()
        c.execute("SELECT user FROM ids WHERE id=?", (str(id).lower(),))
        result = c.fetchone()
    return result[0] if result else None

# get permissions
def getPermissions(uuid):
    with sqlite3.connect("S:\Coding\Digivault_Server\Digivault_Server\Digivault_Server.db") as conn:
        c = conn.cursor()
        c.execute("SELECT permissions FROM user WHERE uuid=?", (uuid,))
        permissions = c.fetchone()
    return permissions[0].split(",") if permissions else None

@app.route("/checkID", methods=['POST'])
def CheckID():
    reqData = request.get_json()
    if not reqData:
        return "Data isn't valid json", 400
    id = getID(reqData["id"])
    if not id:
        return "No User mapped to this id", 404
    permissions = getPermissions(id)
    permissions = json.dumps(permissions)
    return Response(permissions, mimetype='application/json')
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)