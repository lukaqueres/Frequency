import requests
import json
import flask
from flask import Flask, render_template, Response, request, redirect, url_for
app = Flask(__name__)

@app.route('/get_user_data', methods=['GET', 'POST'])
def server():
    print('Get route')
    if request.method == 'POST':
        # Then get the data from the form
        tag = request.form['tag']

        # Get the username/password associated with this tag
        user, password = tag_lookup(tag)

        # Generate just a boring response
        return 'The credentials for %s are %s and %s' % (tag, user, password) 
        # Or you could have a custom template for displaying the info
        # return render_template('asset_information.html',
        #                        username=user, 
        #                        password=password)

    # Otherwise this was a normal GET request
    else:   
        return render_template('main.html')
