# coding: UTF-8
import logging
import model

class CommonHandler:
  def __init__(self, is_web, address, subject, body):
    self.is_web = is_web
    self.address = address
    self.subject = subject
    self.body = body

  def get_response(self):
    sender = self.address
    body = "Addr: " + self.address + "<br />Subj: " + self.subject + "<br />Body:<br />" + "<br />".join(self.body.splitlines())
    subject = "No Event Handler"
    noReply = False

    if self.address == "basic":
      if self.subject == "":
        if self.body == "":
          # List Task
          sender = "basic"
          body = "<font size=4>* Task List *</font><br />"

          query = model.Task.gql("WHERE active = TRUE")
          for d in query:
            body += u"""<div>%s<br /><font size=2><a href="%s">詳細</a> <a href="%s">完了</a></font></div>""" % (
              d.title, self.get_link("detail-%d" % d.key().id()), self.get_link("complete-%d" % d.key().id()))

          subject = "Task List"
        else:
          # Commands
          lines = self.body.splitlines()
          body = ""
          
          for d in lines:
            result = self.action(None, d.strip().split())
            body += result["message"]

          if body == "":
            noReply = True
    elif self.address.startswith("detail-"):
      # Details
      sender = self.address
      d = model.Task.get_by_id(int(self.address[7:]))
      body = d.title
      subject = "Details"
    elif self.address.startswith("complete-"):
      # Complete task
      noReply = True
      d = model.Task.get_by_id(int(self.address[9:]))
      d.active = False
      d.put()

    logging.info(subject)
    logging.info(body)
    if self.is_web:
      header = "<html><head><title>"+subject+"</title></head><body>"
      footer = "<p><a href="+ self.get_link(sender) +">Respond</a></p></body></html>"
    else:
      header = "<html><head></head><body>"
      footer = "</body></html>"
    return {"noReply": noReply, "sender": sender, "subject": subject, "body": header+body+footer}

  def action(self, lastKey, array): 
    logging.info(array)
    cmd = array[0]
    if cmd == u"追加":
      title = array[1]
      d = model.Task(title=title, active=True)
      d.put()
      return {"message": "", "lastKey": d.key()}
    elif cmd == u"詳細":
      return
    elif cmd == u"削除":
      if array[1] == u"完了":
        query = model.Task.gql("WHERE active=FALSE")
        for d in query:
          d.delete()
        return {"message": "", "lastKey": None}

  def get_link(self,link):
    if self.is_web:
      return link
    else:
      return "mailto:"+link+"@easymtask.appspotmail.com"
