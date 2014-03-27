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
import webapp2
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import logging
from google.appengine.ext import db
import chandler

class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect(users.create_login_url('/web/basic'))

class MailHandler(InboundMailHandler):
  def receive(self, mail):
    # WIP
    bodies = mail.bodies("text/plain")
    bodies[0].decode()

    result = chandler.CommonHandler(False, None, None, None).get_response()
    mail.send_mail(
      sender = result.sender,
      to="",
      subject = result.subject,
      body = result.body
    )

class HTTPHandler(webapp2.RequestHandler):
  def get(self):
    if users.is_current_user_admin():
      if self.request.path[5:] == "":
        self.redirect("/web/basic")
      else:
        self.response.write("""
          <form method="post">
            <p><input name="s" type="input" /></p>
            <p><textarea name="b" rows="10"></textarea></p>
            <p><input type="submit" value="Submit" /></p>
          </form>
        """)
    else:
      self.response.write("This action is administrator only")
  def post(self):
    if users.is_current_user_admin():
        if self.request.path[5:] == "":
          self.redirect("/web/basic")
        else:
          self.response.write(chandler.CommonHandler(True, self.request.path[5:], self.request.get("s"), self.request.get("b")).get_response()["body"]) # trim "/web/"
    else:
      self.response.write("This action is administrator only")

class AdminHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write("AdminHandler")

class Task(db.Model):
  title = db.StringProperty()
  description = db.TextProperty()
  added = db.DateTimeProperty(auto_now_add=True)
  limit = db.DateTimeProperty()
  active = db.BooleanProperty()

class Address(db.Model):
  address = db.EmailProperty()

app = webapp2.WSGIApplication([
    (MailHandler.mapping()),
    ('/', MainHandler),
    ('/web/.*', HTTPHandler),
    ('/admin', AdminHandler)
], debug=True)
