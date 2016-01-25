"""
controllers.py

Facebook module controllers.
"""
from flask import Blueprint, url_for, request, current_app, session, Response, redirect
from flask_oauthlib import client

mod_facebook = Blueprint('facebook', __name__, url_prefix='/facebook')

oauth = client.OAuth(current_app)

facebook = None


@mod_facebook.before_app_first_request
def register_facebook():
    global facebook
    facebook = oauth.remote_app(
        'facebook',
        consumer_key=current_app.config['FACEBOOK_APP_ID'],
        consumer_secret=current_app.config['FACEBOOK_APP_SECRET'],
        request_token_params={'scope': 'email'},
        base_url='https://graph.facebook.com',
        request_token_url=None,
        access_token_url='/oauth/access_token',
        access_token_method='GET',
        authorize_url='https://www.facebook.com/dialog/oauth'
    )

    @facebook.tokengetter
    def get_facebook_oauth_token():
        return session.get('facebook_token')


@mod_facebook.route('/login')
def login():
    callback = url_for(
        'facebook.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return facebook.authorize(callback=callback)


@mod_facebook.route('/login/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, client.OAuthException):
        return 'Access denied: %s' % resp.message

    session['facebook_token'] = (resp['access_token'], '')
    try:
        me = facebook.get('/me?fields=id,name,email,link')
    except client.OAuthException:
        return 'Access denied: %s' % resp.message

    # client_id = request.args.get('client_id')
    # scope = request.args.get('scope')
    # redirect_uri = request.args.get('redirect_uri')
    # response_type = request.args.get('response_type')
    return redirect(request.args.get('next'))


@mod_facebook.route('/me')
def me():
    me = facebook.get('/me?fields=id,name,email,link')
    return Response('Logged in as id=%s name=%s email=%s redirect=%s' % (me.data.get('id'), me.data.get('name'), me.data.get('email'), request.args.get('next')))
