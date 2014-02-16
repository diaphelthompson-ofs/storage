#tools web app
from flask import Flask, request, Response, redirect, url_for, render_template
from freedom.login.create_login import create_login, user_login
import time
import json
from freedom.library.business import dat_item, dat_collection
import requests

#tools web app
from flask import Flask, request, redirect, url_for, render_template, flash

from flask.ext.login import LoginManager, login_user, \
    login_required, logout_user, current_user

from freedom.library.auth import LoginForm, User

from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)
app.debug = True

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        if request.form.get('button') == "create_account":
            exists = create_login(request.form)
            if exists == False:
                return render_template('existing_user.html')
            if exists == True:    
                return render_template('created_user.html')

        if request.form.get('button') == "login":
            user = user_login(request.form)
            if user:
                session['user_id'] = user['user_id']
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                return redirect(url_for('index'))
            else:
                return render_template('login.html')

    else:
        return render_template('login.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    #import pdb; pdb.set_trace()
    if request.method == 'POST':

        if request.form.get('button') == "upload":
            file_in_question = request.files['file']
            information = request
            item = dat_item.DatItem()
            item.upload_item(file_in_question,information, app)
            return redirect('index')

        if request.form.get('button') == "collection_upload":
            collection_label = request.form.get('collection_label')
            collection = dat_collection.DatCollection()
            user_id = session['user_id']
            collection.add_collection(collection_label, user_id)
            return redirect('index')
    
    items = dat_item.DatItems()
    collections = dat_collection.DatCollections()
    user_collections = collections.retrieve_by_user(session['user_id'])
    filenames = items.retrieve_items(session['user_id'])
    loose_items, files_by_collection = items.items_by_collection(filenames)
    return render_template('/index.html', session=session, files=files_by_collection, \
        collections=user_collections, files_json=json.dumps(files_by_collection), loose_items=loose_items)
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    return redirect('login')

@app.route('/trial')
def trail():
    return render_template('/trial.html')

@app.route('/trial_again')
def trial_again():
    return render_template('/trial2.html')

@app.route('/page1')
def page1():
    return render_template("/page1.html")

@app.route('/page2')
def page2():
    return render_template("/page2.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)



