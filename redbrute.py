import requests, json

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
        for password in self.passwords_list:
            data = {self.username_field_name: self.username, self.password_field_name: password}
            response = requests.get(self.url)
            if response.status_code == 404:
                print("Placeholder")

bf = BruteForcer("https://facebook.com", "username", "password", "aaa", "passlist.txt")
print(bf.get_settings())
print(bf.get_language_dict())