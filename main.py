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
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
import logging

class MainHandler(webapp2.RequestHandler):
    def get(self):

        message = mail.EmailMessage(sender="a@easymtask.appspotmail.com",
                                            subject="Your account has been approved")
        
        message.to = "test@example.com"

        message.html = """
        <html><head></head><body>
        Dear Albert:

        Your example.com account has been approved.  You can now visit
        http://www.example.com/ and sign in using your Google Account to
        access new features.

        Please let us know if you have any questions.

        The example.com Team
        </body></html>
        """

        message.send()
        #self.response.write('Hello world!')

class ReceiveMailHandler(InboundMailHandler):
  def receive(self, mail):
    bodies = mail.bodies("text/plain")
    for content_type, body in bodies:
        logging.info(body.decode())

app = webapp2.WSGIApplication([
    (ReceiveMailHandler.mapping()),
    ('/', MainHandler)
], debug=True)
