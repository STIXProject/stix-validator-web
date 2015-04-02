from flask import Flask, request, Response
import sdv
import StringIO
import urllib2

app = Flask(__name__)

@app.route('/validate', methods=['POST', 'GET'])
def validate_ws():
    post_data = request.get_data()
    url = request.args.get('url')

    if url:
        print url
        proxies = {'http': 'http://gatekeeper.mitre.org:80', 'https': 'http://gatekeeper.mitre.org:80'}
        return get_results(urllib2.urlopen(url).read())
    elif len(post_data) > 0:
        return get_results(post_data)
    else:
        return Response('{"result": "error", "message": "could not find xml"}\n', mimetype='application/json')


def get_results(data):
    results = sdv.validate_xml(StringIO.StringIO(data))
    return Response(results.as_json() + "\n", mimetype='application/json')

if __name__ == "__main__":
    app.run('localhost', 5000, True)
