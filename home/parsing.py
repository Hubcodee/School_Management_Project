import imaplib,email
import os
import traceback
import pyperclip
from imbox import Imbox
from bs4 import BeautifulSoup

host = "imap.gmail.com"
# username = "testmailtesting17@gmail.com"
# password = 'Testmail#12345'

# EMAIL = username
# PASSWORD = password
# SERVER = host
#
# # connect to the server and go to its inbox
# mail = imaplib.IMAP4_SSL(SERVER)
# mail.login(EMAIL, PASSWORD)
allmails=dict()

def fetch_mails(mail_type,emailid,password):
    mail=imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(emailid,password)
    mail.list()

    mail.select(mail_type)

    status, data = mail.search(None, 'ALL')

    mail_ids = []

    for block in data:
        mail_ids += block.split()
    # print(mail_ids)
    for i in mail_ids:
        temp=dict()
        status, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_subject = message['subject']

                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content = part.get_payload(decode=True)
                            mail_content=mail_content.decode()
                            temp['content_type']='text'
                        elif part.get_content_type()== 'text/html':
                            mail_content = part.get_payload(decode=True)
                            mail_content=mail_content.decode()
                            temp['content_type']='html'
                        else:
                            temp['content_type']='elseother'
                            mail_content="""
                            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
                            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
                            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
                            <div class='container'><b> This email contains attachments which could be harmful we recommed Downloading only if your trust the Sender!</b></div>
                            <form action='download' method='post'>
                            {% csrf_token %}
                            <input name='send_from' style='display:none' value={}>
                            <input name='email' style='display:none' value={}>
                            <input name='password' style='display:none' value={}>
                            <button type='submit' onclick='location.href("download")' class='btn btn-danger center'> Download Attachments</button>
                            </form>
                            """.format(mail_from,emailid,password)
                            
                else:
                    temp['content_type']='other'
                    mail_content = message.get_payload(decode=True)

                temp['from']=mail_from
                temp['subject']=mail_subject
                temp['content']=mail_content
                temp['id']="maid"+str(i)
                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                print(f'Content: {mail_content}')
                print(f'Type: {temp["content_type"]}')
                allmails[i]=temp

    return(allmails)


# pyperclip.copy(f"{allmails}")


# x=fetch_mails("inbox")
# print(x)
def downloadattachments(hst,usrname,passkey,fromuser):
    if os.path.exists("attachments"):
        pass
    else:
        os.mkdir("attachments")
    download_folder = os.getcwd()+"/attachments"

    if not os.path.isdir(download_folder):
        os.makedirs(download_folder, exist_ok=True)

    mail = Imbox(hst, username=usrname, password=passkey, ssl=True, ssl_context=None, starttls=False)
    # currently it will receive message from user called shivanshusurya192@gmail.com if you want to change to specific user pass its name

    messages = mail.messages(sent_from=fromuser) # defaults to inbox

    for (uid, message) in messages:
        # mail.mark_seen(uid) # optional, mark message as read

        for idx, attachment in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}/{att_fn}"
                print(download_path)
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())
            except:
                print(traceback.print_exc())

    mail.logout()

"""
Available Message filters: 
# Gets all messages from the inbox
messages = mail.messages()
# Unread messages
messages = mail.messages(unread=True)
# Flagged messages
messages = mail.messages(flagged=True)
# Un-flagged messages
messages = mail.messages(unflagged=True)
# Messages sent FROM
messages = mail.messages(sent_from='sender@example.org')
# Messages sent TO
messages = mail.messages(sent_to='receiver@example.org')
# Messages received before specific date
messages = mail.messages(date__lt=datetime.date(2018, 7, 31))
# Messages received after specific date
messages = mail.messages(date__gt=datetime.date(2018, 7, 30))
# Messages received on a specific date
messages = mail.messages(date__on=datetime.date(2018, 7, 30))
# Messages whose subjects contain a string
messages = mail.messages(subject='Christmas')
# Messages from a specific folder
messages = mail.messages(folder='Social')
"""
