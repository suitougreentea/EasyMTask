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
import model

class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect(users.create_login_url('/web/basic'))

class MailHandler(InboundMailHandler):
  def receive(self, message):
    logging.info(message.sender)
    q = model.Address.gql("WHERE address = :1", message.sender)
    if q.count() > 0:
      bodies = message.bodies("text/plain")
      text = ""
      for content_type, body in bodies:
        text = body.decode()
        break
      subject = ""
      if hasattr(message, "subject"):
        subject = message.subject
      result = chandler.CommonHandler(False, message.to[:-26], subject.strip(), text.strip()).get_response() # Trim @easymtask.appspotmail.com
      if not result["noReply"]:
        mail.EmailMessage (
          sender = result["sender"] + "@easymtask.appspotmail.com",
          to = message.sender,
          subject = result["subject"],
          html = result["body"]
        ).send()

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
          result = chandler.CommonHandler(True, self.request.path[5:], self.request.get("s").strip(), self.request.get("b").strip()).get_response() # Trim "/web/"
          if result["noReply"]:
            self.response.write("NO REPLY")
          else:
            self.response.write(result["body"])
    else:
      self.response.write("This action is administrator only")

class AdminHandler(webapp2.RequestHandler):
  def get(self):
    if users.is_current_user_admin():
      self.response.write("""
        <form method="post">
          <p><input type="radio" name="method" value="add" checked>Add
          <input type="radio" name="method" value="remove">Remove</p>
          <p>Address: <input name="address" type="input" /></p>
          <p>Cron: <input type="checkbox" name="cron" value="true"></p>
          <p><input type="submit" value="Submit" /></p>
        </form>
      """)
    else:
      self.response.write("This action is administrator only")
  def post(self):
    if users.is_current_user_admin():
      method = self.request.get("method")
      address = self.request.get("address")
      cron = self.request.get("cron") == "true"
      if address == "":
        self.error(400)
        self.response.write("Bad Request")
      else:
        if method == "add":
          q = model.Address.gql("WHERE address = :1", address)
          if q.count() == 0:
            model.Address(address=address, cron=cron).put()
            self.response.write("Completed")
          else:
            self.response.write("Already registered")
        elif method == "remove":
          q = model.Address.gql("WHERE address = :1", address)
          for c in q:
            c.delete()
          self.response.write("Completed")
        else:
          self.error(400)
          self.response.write("Bad Request")
    else:
      self.response.write("This action is administrator only")

class CronListHandler(webapp2.RequestHandler):
  def get(self):
    q = model.Address.all()
    for i in q:
      if i.cron:
        # send empty message (will return task list)
        result = chandler.CommonHandler(False, "basic", "", "").get_response()
        if not result["noReply"]:
          mail.EmailMessage (
            sender = result["sender"] + "@easymtask.appspotmail.com",
            to = i.address,
            subject = result["subject"],
            html = result["body"]
          ).send()

app = webapp2.WSGIApplication([
    (MailHandler.mapping()),
    ('/', MainHandler),
    ('/web/.*', HTTPHandler),
    ('/admin', AdminHandler),
    ('/cron/list', CronListHandler)
], debug=True)
