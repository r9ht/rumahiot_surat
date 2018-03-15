import requests


class MailGun():

    # Send simple text message using MailGun API
    # Sender doesn't only consist of email address without the domain -> without @domain
    # using API Key instead of SMTP Login

    def send_simple_message(self, domain_name, api_key, sender, sender_name, recipient_list, subject, text):
        return requests.post(
            "https://api.mailgun.net/v3/{}/messages".format(domain_name),
            auth=("api", "{}".format(api_key)),
            data={"from": "{} <{}@{}>".format(sender_name, sender, domain_name),
                  "to": recipient_list,
                  "subject": subject,
                  "text": text})




