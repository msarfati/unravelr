import flask

frontend = flask.Blueprint(
    'frontend',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/frontend',
)


@frontend.route('/')
def index():
    return flask.render_template('index.html')
