import requests
import random
import pyperclip
import time
from colorama import Style, Fore

charset = 'ABCDEFGabcdefg1234567!@#$%'


def authenticate_user(username: str, project_id: int) -> bool:
    author = requests.get(f"https://api.scratch.mit.edu/projects/{project_id}").json()["author"]["username"]
    code = ""
    for _ in range(20):
        code += charset[random.randint(0, len(charset) - 1)]
    code = Style.BRIGHT + Fore.BLUE + code + Style.RESET_ALL
    print(
        f"Your auth code for {username} is {code} it has been automatically copied to your clipboard\nGo to https://scratch.mit.edu/projects/{project_id} and paste your code in the comments")
    pyperclip.copy(code)
    start = time.time()
    while True:
        comments = requests.get(f"https://api.scratch.mit.edu/users/{author}/projects/{project_id}/comments/").json()
        for number in range(len(comments)):
            if comments[number]['author']['username'].upper() == username.upper() and comments[number]['content'] == code:
                print("User authenticated")
                return True
        time.sleep(0.5)

        if time.time() - start > 120:
            print("Authentication timed out, please try again")
            return False
