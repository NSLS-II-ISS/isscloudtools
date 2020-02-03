from email.mime.text import MIMEText
import base64


def create_html_message(sender, to, subject, message_text):
    message = MIMEText(message_text,'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    #return message
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def upload_draft(gmail_service, message_body, user_id="me"):
    message = {'message': message_body}
    draft = gmail_service.users().drafts().create(userId=user_id, body=message).execute()
    print( 'Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))
    return draft