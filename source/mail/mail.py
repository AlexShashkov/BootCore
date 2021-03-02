import requests
from core import mail_conf


class Mail:
    @staticmethod
    def send_confirmation(to: str, code: str) -> int:
        return requests.post(
            f"https://api.mailgun.net/v3/{mail_conf['api_host']}/messages",
            auth=("api", mail_conf['api_key']),
            data={"from": f"Slave <bootcore@bootcore.icyftl.ru>",
                  "to": f"Somebody <{to}>",
                  "subject": "Bootcore code",
                  "text": f"Ok then. Your code is {code}"}).status_code
