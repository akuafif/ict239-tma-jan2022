
import csv
from flask_login import UserMixin
from typing import Dict, Optional

users = {str : Dict}

class User(UserMixin):
    def __init__(self, name: str, email: str, password: str) -> None:
        self.email = email
        self.password = password
        self.name = name

    # defining overriding method for UserMixin
    # https://flask-login.readthedocs.io/en/latest/_modules/flask_login/mixins/#UserMixin
    @staticmethod
    def get(email: str) -> str:
        return users.get(email)

    def is_authenticated(self) -> bool:
        return True

    def is_active(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> Optional[str]:
        return self.email

    def __str__(self) -> str:
        return f"<email: {self.email}, name: {self.name}, password: {self.password}>"

    def __repr__(self) -> str:
        return self.__str__()

    def save(self) -> None:
        # save user details to csv file
        users[self.email] = self
        with open('assets/users.csv', 'a+', newline='') as file:
            spamwriter = csv.writer(file)
            spamwriter.writerow([self.email,self.password,self.name])

print('\nLoading users from "assets/users.csv"')
with open('assets/users.csv', mode ='r') as file:
    csvFile = csv.reader(file)
    next(csvFile) # skip header
    for lines in csvFile:
        users[lines[0]] = User(email=lines[0],
                            password=lines[1],
                            name=lines[2])
        print(users.get(lines[0]))