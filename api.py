from flask import Flask, jsonify, request

app = Flask(__name__)

# Endpoint: /first
@app.route("/first", methods=["GET"])
def first():
    response = jsonify({"message": "Success"})
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response.headers["Authorization"] = "Bearer token123"
    return response

# Endpoint: /second
@app.route("/second", methods=["POST"])
def second():
    if request.headers.get("Authorization") != "Bearer token123":
        return jsonify({"error": "Unauthorized"}), 401

    expected_body = {"param1": "value1", "param2": "value2"}
    if request.json != expected_body:
        return jsonify({"error": "Invalid payload"}), 400

    response = jsonify({"message": "Failure"})
    response.status_code = 400
    response.headers["Content-Type"] = "application/json"
    response.headers["Authorization"] = "Bearer token123"
    return response

if __name__ == "__main__":
    app.run(debug=True)
