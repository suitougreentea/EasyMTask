from google.appengine.ext import db

class Task(db.Model):
  title = db.StringProperty()
  description = db.TextProperty()
  added = db.DateTimeProperty(auto_now_add=True)
  limit = db.DateTimeProperty()
  active = db.BooleanProperty()

class Address(db.Model):
  address = db.EmailProperty()
