# Holiday-Gift-Exchange
A quick script to randomize a gift exchange and email all the gifters so that nobody knows who everybody has.

# Settings and config 

## gifters:
    a name:
    another name:Sample postactivate script
export ALERT_WITH_EMAIL = True
export GMAIL_ADDRESS = <YOUREMAIL>@gmail.com
export GMAIL_PASSWORD = <YOUR_GMAIL_PASSWORD>


If ALERT_WITH_EMAIL is 'True' there must be an email list in 
config.yml.  Additionally GMAIL_USERNAME and GMAIL_PASSWORD
must be set.

Functionality has only been tested with a gmail account.  Other
servers will surely work, but might require tweaking.

## Config
The configuration file (congif.yml) contains a set of key:value
pairs for which the key is the gifter's name and the value
is their email.  If not using the email functionality just leave
the values empty:

    gifters:
        a name:
        another name:

## Images
Images in the ../images directory will be added to the emails
as attachments.  This is a great place to add a personal touch.

# Customizations that you need to make to use it:

1. Modify the names list

2. Modify the email list, should be in the same order as the names list.

3. Add your username to the backup_output_file_path.

4. Add your email and pasword to the send_mail function.  Note: be careful, maybe just add your password, run, and then delete it without saving so that you don't have to store it in plain text.

5. Customize the subject and text strings for a customized email. (optional)

6. Add an image path to the 'im_path' field to attach and additional holiday greating. (optional) 

## Gift Ideas:

1. Everyone loves socks, especially the fun ones.

2. People who played outside as kids like bush knives.

3. People who played inside as kids like kitchen knives.

4. Kids of all ages are alarmingly fond of stickers.

5. Snakes make bad gifts, they go on living long after the thrill of having a snake is gone. 

6. Hipster girls like funky boots and working class beanies.

7. Hipster guys like Ben Davis shirts.

8. Babies look funny in little track suits.

etc.