from flask import Flask, render_template, request, redirect
from flask import flash, url_for, jsonify

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, Item, User

# Login Session
from flask import session as login_session
import random
import string

# create a flow object from the clientsecrets json file
from oauth2client.client import flow_from_clientsecrets
# run into an error trying to exchange a authorization code for an access token
from oauth2client.client import FlowExchangeError
import httplib2
# converts python object into json
import json
# converts the return value from a function into a real response object that
# can be send off to our client
from flask import make_response
import requests

app = Flask(__name__)
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a state token to prevent request forgery.
# Store it in the session for later validation.


@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    # one time code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['content-Type'] = 'application/json'
        return response
    # check if the access token is valid.
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # if there was error in access token info got
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # check if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    # store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'

    output += '<img src="'
    output += login_session['picture']
    output += '"style = "width: 300px; height: 300px; border-radius:150px;'
    output += ' -webkit-border-radius: 150px;-moz-border-radisu: 150px;"> '

    flash("you are now logged in as %s" % login_session['username'])
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # only disconnect a connected user
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Revoke current token
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    result = httplib2.Http().request(url, 'GET')[0]

    if result['status'] == '200':
        # reset the user's session:
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # The given token was invalid
        response = make_response(
            json.dumps('Failed to revoke token for given user'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON APIs to view Catalog Information
@app.route('/catalog/<catalog_name>.json')
def catalogMenuJSON(catalog_name):
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    items = session.query(Item).filter_by(
        catalog=catalog).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/catalog/<catalog_name>/<item_name>.json')
def ItemJSON(catalog_name, item_name):
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    ItemInfo = session.query(Item).filter_by(name=item_name).filter_by(catalog=catalog).one()
    return jsonify(Item=ItemInfo.serialize)


@app.route('/catalog.json')
def catalogsJSON():
    catalogs = session.query(Catalog).all()
    return jsonify(catalogs=[r.serialize for r in catalogs])


# Show all catalogs
@app.route('/')
def showCatalogs():
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    return render_template('catalogs.html',
                           catalogs=catalogs,
                           username=login_session.get('username'))


# Create a new catalog
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCatalog():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCatalog = Catalog(
            name=request.form['name'],
            user_id=login_session['user_id'])
        session.add(newCatalog)
        flash('New Catalog %s Successfully Created' % newCatalog.name)
        session.commit()
        return redirect(url_for('showCatalogs'))
    else:
        return render_template('newCatalog.html',
                               username=login_session.get('username'))


# Edit a catalog
@app.route('/catalog/<catalog_name>/edit/', methods=['GET', 'POST'])
def editCatalog(catalog_name):
    if 'username' not in login_session:
        return redirect('/login')

    editedCatalog = session.query(
        Catalog).filter_by(name=catalog_name).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCatalog.name = request.form['name']
            flash('Catalog Successfully Edited %s' % editedCatalog.name)
            return redirect(url_for('showCatalogs'))
    else:
        return render_template('editCatalog.html',
                               catalog=editedCatalog,
                               username=login_session.get('username'))


# Delete a catalog
@app.route('/catalog/<catalog_name>/delete/', methods=['GET', 'POST'])
def deleteCatalog(catalog_name):
    if 'username' not in login_session:
        return redirect('/login')

    catalogToDelete = session.query(
        Catalog).filter_by(name=catalog_name).one()
    if request.method == 'POST':
        items = session.query(Item).filter_by(catalog=catalogToDelete).all()
        for item in items:
            session.delete(item)
        session.delete(catalogToDelete)
        flash('%s Successfully Deleted' % catalogToDelete.name)
        session.commit()
        return redirect(url_for('showCatalogs',
                                catalog_name=catalog_name))
    else:
        return render_template('deleteCatalog.html',
                               catalog=catalogToDelete,
                               username=login_session.get('username'))


# Show a catalog
@app.route('/catalog/<catalog_name>/')
def showCatalog(catalog_name):
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    items = session.query(Item).filter_by(
        catalog=catalog).all()
    return render_template('catalog.html',
                           items=items,
                           catalog=catalog,
                           username=login_session.get('username'))


###########################  ITEMS  ############################################

# Create a new item
@app.route('/catalog/<catalog_name>/new/',
           methods=['GET', 'POST'])
def newItem(catalog_name):
    if 'username' not in login_session:
        return redirect('/login')

    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    if request.method == 'POST':
        print(request.form['name'])
        if (request.form['name']=='') or (request.form['description']==''):
            return render_template('newItem.html',
                                   catalog_name=catalog_name,
                                   username=login_session.get('username'),
                                   error_messages='Input can not be empty.')
        else:
            newItem = Item(
                name=request.form['name'],
                description=request.form['description'],
                catalog_id=catalog.id,
                user_id=catalog.user_id)
            session.add(newItem)
            session.commit()
            flash('New Menu %s Item Successfully Created' % (newItem.name))
            return redirect(url_for('showCatalog', catalog_name=catalog_name))
    else:
        return render_template('newItem.html',
                               catalog_name=catalog_name,
                               username=login_session.get('username'))


# Edit a item
@app.route('/catalog/<catalog_name>/<item_name>/edit',
           methods=['GET', 'POST'])
def editItem(catalog_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')

    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    editedItem = session.query(Item).filter_by(name=item_name).filter_by(catalog=catalog).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showCatalog', catalog_name=catalog_name))
    else:
        return render_template('editItem.html',
                               catalog_name=catalog_name,
                               item_name=item_name,
                               item=editedItem,
                               username=login_session.get('username'))


# Delete a item
@app.route('/catalog/<catalog_name>/<item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(catalog_name, item_name):
    if 'username' not in login_session:
        return redirect('/login')

    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    itemToDelete = session.query(Item).filter_by(name=item_name).filter_by(catalog=catalog).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showCatalog', catalog_name=catalog_name))
    else:
        return render_template('deleteItem.html',
                               item=itemToDelete,
                               catalog_name=catalog_name,
                               username=login_session.get('username'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
