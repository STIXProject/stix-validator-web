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
        results = validate_url(url)
    elif len(post_data) > 0:
        results = validate_xml(post_data)
    else:
        results = {"result": "error", "message": "could not find xml"}

    return Response(json.dumps(results),mimetype="application/json")

@app.route('/', methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        url = request.form['url']
        xml = request.form['xml']

        if url and len(url) > 0:
            results = validate_url(url)
        elif xml and len(xml) > 0:
            results = validate_xml(xml)
        else:
            results = {"result": "error", "message": "could not find xml"}

        return render_template('index.html', results=results, url=url, xml=xml, json=json.dumps(results))
    else:
        return render_template('index.html', results=None)


def validate_xml(data):
    try:
        return {
            "xml": sdv.validate_xml(StringIO.StringIO(data)).as_dict(),
            "best_practices": sdv.validate_best_practices(StringIO.StringIO(data)).as_dict(),
            "result": "validated"
        }
    except sdv.errors.ValidationError as e:
        return {"result": "error", "message": str(e)}

def validate_url(url):
    try:
        return validate_xml(urllib2.urlopen(url).read())
    except ValueError:
        return {"result": "error", "message": "could not open url"}

if __name__ == "__main__":
    app.run('localhost', 5000, True)
