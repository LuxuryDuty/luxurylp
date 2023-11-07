import json
import os


def get_token(text):
    try:
        sq = text[text.find('=') + 1: text.find('&')]
        return sq
    except:
        return text

def setup():
    try:
        os.mkdir('luxurylp')
    except:
        pass
    
    tokens = []
    while len(tokens) != 3:
        token = input("Введите токен VK не обрезая его >> ")

        tokens.append(get_token(token))

    with open(os.path.join('config.json'), 'w', encoding='utf-8') as file:
        db = {
            "tokens": tokens
        }
        file.write(json.dumps(db))

    with open(os.path.join('luxurylp', 'lp_dc_config.json'), 'w', encoding='utf-8') as file:
        file.write('{"app_secret": "public", "app_id": 0}')

    print("Конфиг записан")

if __name__ == '__main__':
    setup()

