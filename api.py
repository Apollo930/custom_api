from flask import Flask, jsonify

app = Flask(__name__)

# Route for /first (GET request)
@app.route('/first', methods=['GET'])
def first():
    response = Response(response="{}", status=200, mimetype="application/json")
    response.headers['Authorization'] = 'Bearer token123'
    return response


# Route for /second (GET request, but responds with 400 + JSON body)
@app.route('/second', methods=['GET'])
def second():
    response = jsonify({
        'param1': 'value1',
        'param2': 'value2'
    })
    response.status_code = 400  # Return 400 Bad Request as required
    response.headers['Content-Type'] = 'application/json'
    response.headers['Authorization'] = 'Bearer token123'
    return response

if __name__ == '__main__':
    app.run(debug=True)
