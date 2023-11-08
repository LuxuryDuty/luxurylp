import json
import os, sys
import platform


def get_token(text):
    try:
        sq = text[text.find('=') + 1: text.find('&')]
        return sq
    except:
        return text


def setup():
    os_name = platform.system()
    if os_name == "Linux":
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
        print("Установка на Linux.")
        os.system("sudo apt update")
        os.system("sudo apt install apt-transport-https ca-certificates curl software-properties-common")
        os.system("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
        os.system("sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"")
        os.system("sudo apt update")
        os.system("sudo apt install docker-ce")
        os.system("docker build -t luxurylp .")

        print("Конфиг записан")
        print("Что бы запустить пропишите docker run -it luxurylp")
        print("Что бы посмотреть процессы введите docker ps")
        print("Что бы остановить процесс введите docker stop <id>")
        print("Что бы запустить процесс вновь введите docker start <id>")
    elif os_name == "Windows":
        print("Установка на Windows.")

        os.system(f'{sys.executable} -m pip install --upgrade pip')
        os.system(f'{sys.executable} -m pip install -r requirements.txt')

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

