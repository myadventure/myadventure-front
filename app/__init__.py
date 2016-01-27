from flask import Flask, render_template
import os

from app.mod_index.controllers import mod_index
from app.mod_map.controllers import mod_map
from app.mod_facebook.controllers import mod_facebook
from app.mod_auth.controllers import mod_auth
from app.mod_recent.controllers import mod_recent
from app.mod_user.controllers import mod_user

app = Flask(__name__, static_folder=os.getcwd() + '/app/static', static_url_path='', template_folder=os.getcwd() + '/app/templates')

app.config.from_pyfile('config.py', silent=True)


@app.errorhandler(400)
def bad_request(e):
    """Return a custom 400 error."""
    return 'The browser (or proxy) sent a request that this server could not understand.', 400


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return render_template('404.html')


@app.errorhandler(500)
def internal_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('img/map.ico')

# Registering module blueprints
app.register_blueprint(mod_index)
app.register_blueprint(mod_map)
app.register_blueprint(mod_facebook)
app.register_blueprint(mod_recent)
app.register_blueprint(mod_user)
app.register_blueprint(mod_auth)
