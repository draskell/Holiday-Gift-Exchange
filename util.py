import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate

import yaml


def get_yaml(file_path):
    '''Loads a YAML file at file_path.
    '''
    with open(file_path, 'r') as f:
        return yaml.load(f)

class ConfigError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        raise Exception('Configuration Error: {}'.format(message))

def validate_configuration(config):
    '''Validates that configuration is usable.
    '''
    # Check for an unsolvable condition.
    if len(config['gifters']) - len(config['disallowed_pairs']) * 2 < 3:
        raise ConfigError(
            'There is no way to solve your configuration without '
            'reciprical gifters.  Add more gifters or remove some '
            'of the disallowed pairs.'
        )
    names_in_disallowed_pairs = set(
        [name for pair in config['disallowed_pairs'] for name in pair]
    )
    names_of_gifters = set(config['gifters'].keys())
    if not names_in_disallowed_pairs.issubset(names_of_gifters):
        raise ConfigError(
            'Some of the names in the disallowed pairs are not in the '
            'gifter list.'
        )
    return config

class ConfigLoader(object):
    '''Class for storing configuration.

    TODO: Replace current YAML configuration loading.
    '''
    def __init__(self, path):
        self.path = path
        self.config = get_yaml(os.path.join(
            os.path.dirname(__name__), 'config.yml'
        ))
        self.config = validate_configuration(self.config)
        self.gifters = self.config['gifters']
        self.email_body = self.config['email_body']
        self.spending_limit = self.config['spending_limit']
        self.email_text_addition = (
            "\n\nSpend ${amt} on {give}, and don't "
            "forget to get something for your mom!"
        )
        self.email_body = self.email_body + self.email_text_addition
        self.name_map = {
            i: name for i, name
            in enumerate(self.gifters.keys())
        }
    
    def participant_count(self):
        '''Returns the count of participants.
        '''
        return len(self.config['gifters'])

    def map_pairs(self, pairs):
        '''Converts integet pairs back to name pairs.
        '''
        return [
            (self.name_map[pair[0]], self.name_map[pair[1]])
            for pair in pairs
        ]
    
    def formatted_email_body(self, recipient):
        '''Returns a formatted email body.
        '''
        return self.email_body.format(
            amt=self.spending_limit, give=recipient
        )

def load_config():
    '''Loads configuration file and adds some nessesary
    parameters.  
    
    TODO: The configuration object might be best as a class.
    '''
    # Load configuration file.
    config = get_yaml(os.path.join(
        os.path.dirname(__name__), 'config.yml'
    ))
    # Add the formattable part of the 
    email_text_addition = (
        "\n\nSpend ${amt} on {give}, and don't "
        "forget to get something for your mom!"
    )
    config['email_body'] += email_text_addition 
    config['name_map'] = {
        i: name for i, name in enumerate(config['gifters'].keys())
    }
    return validate_configuration(config)

def convert_pairs_to_names(pairs, config):
    '''Takes a set of integer pairs and converts
    them to name pairs.
    '''
    return [
        (config['name_map'][pair[0]], config['name_map'][pair[1]])
        for pair in pairs
    ]

def send_mail(recipients,subject,body,im_attach=None):
    '''Sends emails to recipients with subject and 
    body.

    :recipients: list
        List of recipients
    :subject: str
        Subject of the emails.
    :body: str
        Body of the emails.
    :im_attach: list 
        List of image filepaths.
    '''  
    gmail_user = os.environ['GMAIL_ADDRESS']
    gmail_pwd = os.environ['GMAIL_PASSWORD']
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = ', '.join(recipients)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    body = MIMEText(body)
    msg.attach(body)
    for im in im_attach or []:
        img_data = open(im, 'rb').read()
        image = MIMEImage(img_data, name = os.path.basename(im))
        msg.attach(image)
    try:
        # Servers other than GMAIL may be possible with 
        # another port here such as 486.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(msg['From'], recipients, msg.as_string())
        server.close()
        return 'Email sent regarding {0}'.format(subject)
    except:
        return 'Email failed regarding {0}'.format(subject)