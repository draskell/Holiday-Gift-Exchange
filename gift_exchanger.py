# -*- coding: utf-8 -*-
"""

This script takes names listed in the names section and randomizes the names to make an exchange

Pairs of people who should not give to each other can be written out in not_allowed_pairs

You will need to enter your email and your email password in the send mail function below.  Additionally you need to put your 
username in the 'backup_output_file_path' below.  I've only used it with gmail (sender), you may have issues with other mail servers, let me know!

Also, customize the subject and text of the message below.

You can add an image in the im_path list if you like.

"""

import numpy as np
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate

# if true emails will be required to be entered below
email = True

#if you have a holiday card image you want to add it will be attached to each email
im_path = []
spending_limit = 20

# saves a backup list to your desktop incase something happens and an email fails
# you should also have a record in your sent mail, but NO PEAKING!!
backup_output_file_path = r'C:\Users\<YOUR-USERNAME>\Desktop\gift_exchange_backup.txt'

#list all the people (or animals in this case) that will be in the exchange, don't forget yourself!
names = ['Rudolph',
         'Donner',
         'Blitzen',
         'Prancer',
         'Dancer',
         'Vixen',
         'Comet',
         'Cupid',
         'Dasher',
         'Santa',
         'Mrs. Claus']

if email:
    # emails in order of the names above.  Leave list empty if you just want to tell people who they got
    emails = ['rudolph1982@gmail.com',
              'donner_rules@deermail.com'] #just a couple examples, if you want to send emails there must be as many emails as names
    try:
        mail_dict = dict(zip(names,emails))
    except:
        email = False

# these pairs will not be allowed uni-directionally        
not_allowed_pairs = [('Santa','Mrs. Claus'),('Rudolph','Vixen')]

# function to test if any of the pairs are not allowed
def find_bad_pairs(names, not_allowed_pairs, pairs):
    num_sets = []    
    for pair in not_allowed_pairs:
        num_sets.append(set([names.index(pair[0]),names.index(pair[1])]))
    for pair in pairs:
        if set(pair) in num_sets:
            return True
    return False

# function to check that the pairs don't consist of 2 people giving back and forth
def find_recipricals(pairs):
    ascending_pairs = []
    for i, pair in enumerate(pairs):
        if pair[0] > pair[1]:
            ascending_pairs.append((pair[1],pair[0]))
        else:
            ascending_pairs.append(pair)
    if len(pairs) != len(set(ascending_pairs)):
        return True
    return False

def send_mail(recipients,subject,text,im_attach=None):
    """
    recipients is a list
    """    
    gmail_user = '<YOUREMAIL>@gmail.com'
    gmail_pwd = '<YOURPASSWORD>'
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = ', '.join(recipients)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    text = MIMEText(text)
    msg.attach(text)
    for im in im_attach or []:
        img_data = open(im, 'rb').read()
        image = MIMEImage(img_data, name = os.path.basename(im))
        msg.attach(image)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587) #or port 465
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(msg['From'], recipients, msg.as_string())
        server.close()
        return 'Email sent regarding {0}'.format(subject)
        #print 'email sent'
    except:
        return 'Email failed regarding {0}'.format(subject)

# randomization of the names
give = range(len(names))
np.random.shuffle(give)
get = range(len(names))
np.random.shuffle(get)
pairs = zip(give,get)
has_bad_pairs = find_bad_pairs(names, not_allowed_pairs, pairs)
has_reciprical_pairs = find_recipricals(pairs)

# while loop to check that there aren't any pairs in the not allowed list or recipricals and nobody has themselves
# if any of these conditions are met it is re-randomized
while (len([pair for pair in pairs if pair[0] == pair[1]]) > 0) or has_bad_pairs or has_reciprical_pairs:
    get = range(len(names))
    np.random.shuffle(get)
    pairs = zip(give,get)
    has_bad_pairs = find_bad_pairs(names, not_allowed_pairs, pairs)
    has_reciprical_pairs = find_recipricals(pairs)

# write a backup file of wo has who in case an email fails or Mrs. Claus accidentally deletes her server
give_list = {}
with open(backup_output_file_path, 'w') as f:
    for name in names:
        for pair in pairs:
            if names.index(name) == pair[0]:
                gives = pair[1]
                give_list[name] = pair[1]
            elif names.index(name) == pair[1]:
                gets = pair[0]
        f.write('{name} gives to {gives} and gets from {gets}\n\n'.format(name=name.upper(),gives=names[gives],gets=names[gets]))
    
# script to email each participant with the name of the person they need to buy a gift for
    
email_subject = "Hey Everybody the Holiday Gift Exchange Results Are In!"
email_text = """
Happy Holidays!

It's that time of year again and you get to get out and supress the existential dread of another year having flown past by engaging in commerce.  

Spend ${amt} on {give}, and don't forget to get something for your mom!
"""

if len(emails) == len(names) and email:
    for name, email in mail_dict.iteritems():
        send_mail([email], email_subject, email_text.format(amt=str(spending_limit),give=give_list[name]), im_path)    
else:
    print "There are too many or too few emails."
