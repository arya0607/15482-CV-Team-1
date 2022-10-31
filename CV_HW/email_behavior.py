from email.mime.image import MIMEImage
from behavior import *
from transitions import Machine
import base64
# import imaplib
import json
import smtplib
import urllib.parse
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import lxml.html
from datetime import date

import sys
import os
import os.path as op
import glob
sys.path.append(op.dirname(op.dirname(op.abspath(__file__)))+"/../lib/")


'''
The behavior should email once every day
'''

GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

GOOGLE_CLIENT_ID = '800602998301-8qfktit8jclgcpm9nui7ototk4osmjjm.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REFRESH_TOKEN = "1//0d12S8CyPZKbRCgYIARAAGA0SNwF-L9IrsBVuxrC_AHO8Mr0i6U4aiezzOIT87QkauyyUuVUbQ3ZxwZ3Ji4Uk2ZtxEWXQvsoUAI4"


class Email(Behavior):

    def __init__(self):
        super(Email, self).__init__("EmailBehavior")
        print("Initializing Email Behavior")
        self.initial = 'halt'
        # STUDENT CODE: Modify these lines to add all your FSM states
        self.states = [self.initial, 'init']

        self.fsm = Machine(self, states=self.states, initial=self.initial,
                           ignore_invalid_triggers=True)

        # Add FSM transitions and actions
        # BEGIN STUDENT CODE
        self.fsm.add_transition(
            trigger='enable', source='halt', dest='init')
        self.fsm.add_transition(
            trigger='doStep', source='init', dest='halt', after='email')
        self.fsm.add_transition(trigger='disable', source='*', dest='halt')
        # END STUDENT CODE

    def enable(self):
        # Use 'enable' trigger to transition the FSM out of the 'initial' state
        print("Enabling Email")
        self.trigger("enable")

    def disable(self):
        # Use 'diable' trigger to transition the FSM into the 'initial' state
        self.trigger("disable")

    def act(self):
        # Use 'doStep' trigger for all other transitions
        self.trigger('doStep')

    # Add all your before / after action functions here
    # BEGIN STUDENT CODE

    def command_to_url(self, command):
        return '%s/%s' % (GOOGLE_ACCOUNTS_BASE_URL, command)

    def call_refresh_token(self, client_id, client_secret, refresh_token):
        params = {}
        params['client_id'] = client_id
        params['client_secret'] = client_secret
        params['refresh_token'] = refresh_token
        params['grant_type'] = 'refresh_token'
        request_url = self.command_to_url('o/oauth2/token')
        response = urllib.request.urlopen(request_url, urllib.parse.urlencode(
            params).encode('UTF-8')).read().decode('UTF-8')
        return json.loads(response)

    def generate_oauth2_string(self, username, access_token, as_base64=False):
        auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
        if as_base64:
            auth_string = base64.b64encode(
                auth_string.encode('ascii')).decode('ascii')
        return auth_string

    def refresh_authorization(self, google_client_id, google_client_secret, refresh_token):
        response = self.call_refresh_token(
            google_client_id, google_client_secret, refresh_token)
        return response['access_token'], response['expires_in']

    def send_mail(self, fromaddr, toaddr, subject, message, recent_image):
        access_token, expires_in = self.refresh_authorization(
            GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)
        auth_string = self.generate_oauth2_string(
            fromaddr, access_token, as_base64=True)

        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg.preamble = 'This is a multi-part message in MIME format.'
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        part_text = MIMEText(lxml.html.fromstring(
            message).text_content().encode('utf-8'), 'plain', _charset='utf-8')
        part_html = MIMEText(message.encode('utf-8'), 'html', _charset='utf-8')
        msg_alternative.attach(part_text)
        msg_alternative.attach(part_html)

        print("recent_image: ", recent_image)
        if recent_image:
            with open(recent_image, 'rb') as f:
                img_data = f.read()

            # print("name: ", op.basename(recent_image))
            # print("img_data: ", img_data)
            image = MIMEImage(img_data, name=op.basename(recent_image))
            msg.attach(image)

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo(GOOGLE_CLIENT_ID)
        server.starttls()
        server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()

    def email(self):
        fromaddr = 'nmarquez@andrew.cmu.edu'
        toadds = ['nmarquez@andrew.cmu.edu', 'srkhuran@andrew.cmu.edu',
                  'aryas@andrew.cmu.edu', 'rylin@andrew.cmu.edu']
        # toadds = ['terrbot.1@gmail.com']
        todayDate = date.today()
        subject = 'TerraBot1 Update: ' + str(todayDate)
        message = '<b>STATUS OF TERRABOT1</b><br><br>' + str(self.sensordata)
        print("Sending email...")

        folder_path = r'agents/CV_HW/greenhouse_images/'
        file_type = r'\*jpg'
        files = os.listdir("./greenhouse_images/")
        print("files: ", files)
        if files:
            recent_image = "./greenhouse_images/" + max(files)
        else:
            recent_image = None

        for add in toadds:
            try:
                self.send_mail(fromaddr, add, subject, message, recent_image)
                print("Email sent!")
            except:
                print("Email token needs to be refreshed")
    # END STUDENT CODE
