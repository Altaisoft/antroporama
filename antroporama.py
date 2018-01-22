from bottle import route, run, static_file, jinja2_view
import jinja2
import os.path
import data


@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=os.path.join(
        os.path.dirname(__file__), 'static'
    ))


@route('/media/<filepath:path>')
def serve_media(filepath):
    return static_file(filepath, root=os.path.join(
        os.path.dirname(__file__), 'media'
    ))


@route('/')
@jinja2_view('index.html', template_lookup=['templates'])
def index():
    return {
        'species': data.species,
        'human_from_clay': data.human_from_clay,
        'intro': data.intro,
    }


run(host='localhost', port=8000, debug=True)