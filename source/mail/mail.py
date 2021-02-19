from os import system


class Mail:
    @staticmethod
    def send_confirmation(to: str, code: str):
        system(f'echo "Your code is <h1>{code}</h1>" | mail -s "BootCore code" {to}')
