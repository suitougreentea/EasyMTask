import logging

class CommonHandler:
  def __init__(self, is_web, address, subject, body):
    self.is_web = is_web
    self.address = address
    self.subject = subject
    self.body = body

  def get_response(self):
    sender = self.address
    body = "Addr: " + self.address + "<br />Subj: " + self.subject + "<br />Body: " + self.body
    subject = "No Event Handler"

    if self.address == "basic":
      if self.subject == "":
        if self.body == "":
          sender = "basic"
          body = "<font size=4>* Task List *</font>"
          subject = "Task List"
    logging.info(subject)
    logging.info(body)
    if self.is_web:
      header = "<html><head><title>"+subject+"</title></head><body>"
      footer = "<p><a href="+ self.get_link(sender) +">Respond</a></p></body></html>"
    else:
      header = "<html><head></head><body>"
      footer = "</body></html>"
    return {"sender": sender, "subject": subject, "body": header+body+footer}

  def get_link(self,link):
    if self.is_web:
      return link
    else:
      return link+"@easymtask.appspotmail.com"
