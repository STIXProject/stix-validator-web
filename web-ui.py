from flask import Flask, request
import sdv
import StringIO

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate_ws():
    data = request.get_data()
    results = sdv.validate_xml(StringIO.StringIO(data))
    return Response(results.as_json(), mimetype='application/json')

if __name__ == "__main__":
    app.run('0.0.0.0', 5000, True)
