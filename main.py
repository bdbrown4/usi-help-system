#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# [ START demo app ]
# import webapp2

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         self.response.write('Hello world!')

# app = webapp2.WSGIApplication([
#     ('/', MainHandler)
# ], debug=True)
# [ END demo app ]

# [START app]
import logging

from flask import Flask, render_template, request
from google.appengine.ext import ndb
from models import Item
import uuid

app = Flask(__name__)
app.config.from_object('config')

from views import *

print "I'm here!"

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/questiontree')
def questiontree():
    return render_template('questiontree.html')


# @app.route('/submittedContacts')
# def submitted_contacts():
#     messages = Contact.query() #get all messages from contact class
#     return render_template(
#         'submittedContacts.html',
#         messages=messages)

def hello():
    return 'Hello World!'

# [END app]
