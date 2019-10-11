import requests

from ._api_key import API_KEY


def send_simple_message(dst, subject, txt):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox6b9a603f2820431d882814909b076f40.mailgun.org/messages",
        auth=("api", API_KEY),
        data={"from": "Mailgun Sandbox <noreply@sandbox6b9a603f2820431d882814909b076f40.mailgun.org>",
              "to": dst,
              "subject": subject,
              "text": txt})
