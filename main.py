import os

from .util import send_mail, load_config, convert_pairs_to_names
from .gift_match import get_gifter_matches, has_bad_pairs

# Load environment and config.
send_email = os.environ['ALERT_WITH_EMAIL']
CONFIG = load_config()

# If you have a holiday card image or two you want to
# add the paths in im_path it will be attached to each
# email.
image_directory = os.path.join(os.path.dirname(__name__), 'data', 'images')
IMAGE_PATHS = [
    os.path.join(image_directory, fn) for fn in os.listdir(image_directory)
]

# Saves a backup list to your desktop incase something happens
# and an email fails you should also have a record in your sent
# mail, but NO PEAKING!!
backup_output_file_path = os.path.join(
    os.path.dirname(__name__), 'data', 'gift_exchange_backup.txt'
)

if __name__ == '__main__':
    number_of_gifters = len(CONFIG['gifters'])
    # Check that there aren't any pairs in the not allowed list
    # or recipricals and nobody has themselves.
    # if any of these conditions are met it is re-randomized
    pairs = get_gifter_matches(number_of_gifters)
    while has_bad_pairs(pairs, CONFIG):
        pairs = get_gifter_matches(number_of_gifters)

    pairs = convert_pairs_to_names(pairs, CONFIG)

    if send_email:
        for pair in pairs:
            giver_name = pair[0]
            give_to_name = pair[1]

            # Format body string
            email_body = CONFIG['email_body'].format(
                amt=CONFIG['spending_limit'], give=give_to_name
            )
            # Send email
            send_mail(
                [CONFIG['gifters'][giver_name]], CONFIG['subject'],
                email_body, im_attach=IMAGE_PATHS
            )

    # Save local master file in case someone forgets.
    with open(backup_output_file_path, 'w') as f:
        f.write('\n'.join(['{} gives to {}'.format(*pair) for pair in pairs]))
    # TODO: save personalized files as an alternate to emailing.