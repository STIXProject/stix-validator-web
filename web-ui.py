from flask import Flask, request, Response, render_template
import sdv
import StringIO
import urllib2
import json

app = Flask(__name__, static_folder='public', static_url_path='')

@app.route('/validate', methods=['POST', 'GET'])
def validate_ws():
    post_data = request.get_data()
    url = request.args.get('url')

    if url:
        try:
            return wrap_json_results(urllib2.urlopen(url).read())
        except ValueError:
            return Response('{"result": "error", "message": "could not find xml"}\n', mimetype='application/json')
    elif len(post_data) > 0:
        return wrap_json_results(post_data)
    else:
        return Response('{"result": "error", "message": "could not find xml"}\n', mimetype='application/json')

@app.route('/', methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        url = request.form['url']
        xml = request.form['xml']

        if url and len(url) > 0:
            try:
                results = get_results(urllib2.urlopen(url).read())
            except ValueError:
                results = {"result": "error", "message": "could not open url"}
        elif xml and len(xml) > 0:
            try:
                results = get_results(xml)
            except sdv.errors.ValidationError:
                results = {"result": "error", "message": "not well-formed"}
        else:
            results = {"result": "error", "message": "could not find xml"}

        return render_template('index.html', results=results, url=url, xml=xml, json=json.dumps(results))

    else:
        return render_template('index.html', results=None)


def get_results(data):
    return {
        "xml": sdv.validate_xml(StringIO.StringIO(data)).as_dict(),
        "best_practices": sdv.validate_best_practices(StringIO.StringIO(data)).as_dict(),
        "result": "validated"
    }


def wrap_json_results(data):
    return Response(json.dumps(results.as_json()) + "\n", mimetype='application/json')

if __name__ == "__main__":
    app.run('localhost', 5000, True)
