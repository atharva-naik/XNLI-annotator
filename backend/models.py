# Python file with all the model classes (like users, sentences etc...)
import gc
import json 
import pandas as pd
from passlib.hash import pbkdf2_sha256
# from MySQLdb import escape_string as thwart
from wtforms import Form, BooleanField, TextField, PasswordField, validators


# class RegistrationForm(Form):
#     username = TextField('Username', [validators.Length(min=4, max=20)])
#     email = TextField('Email Address', [validators.Length(min=6, max=50)])
#     password = PasswordField('New Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords must match')
#     ])
#     confirm = PasswordField('Repeat Password')
#     accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.DataRequired()])
class User:
    def __init__(self, **kwargs):
        for field in ["password", "username", "email"]:
            assert field in kwargs 
        self.username = kwargs["username"]
        self.email = kwargs["email"]
        self.password = kwargs["password"]
        self.path = f"data/annotations/{self.username}.csv"
        self.annotations = self.fetch_annotations()

    def fetch_annotation(self, id):
        try:
            record = self.annotations[self.annotations["id"] == id]
        except KeyError:
            record = {}
        if len(record) == 0:
            return {"id":"",
                    "EP":"",
                    "CP":"",
                    "UP":"",
                    "NP":"",
                    "EH":"",
                    "CH":"",
                    "UH":"",
                    "NH":""}
        else:
            return record.to_dict("records")[0]

    def to_dict(self):
        return {"username":self.username, 
                "email":self.email, 
                "password":self.password}

    def authenticate(self, password):
        if pbkdf2_sha256.verify(password, self.password):
            return True
        else:
            return False

    def fetch_annotations(self):
        try:
            self.annotations = pd.read_csv(self.path) 
        except FileNotFoundError:
            self.annotations = pd.DataFrame()
        except pd.errors.EmptyDataError:
            self.annotations = pd.DataFrame()

        return self.annotations

    def add_annotation(self, row):
        self.annotations = self.annotations.append(row, ignore_index=True)

    def update_annotation(self, id, annotation):
        # print(annotation)
        try:
            for key in annotation:
                print(key)
                self.annotations.loc[self.annotations["id"]==int(id), key] = annotation[key]
        except KeyError:    
            self.add_annotation(annotation)

    def save(self):
        self.annotations.to_csv(self.path, index=False)

    def __eq__(self, other):
        if self.username == other.username and self.email == other.email and pbkdf2_sha256(other.password, self.password):
            return True
        else:
            return False

    def __str__(self):
        return f'''name:{self.username}
email:{self.email}'''

    def __repr__(self):
        return self.username


class UserTable:
    def __init__(self, path):
        self.path = path
        try:
            self.data = pd.read_csv(path)
            self.columns = self.data.columns
        except pd.errors.EmptyDataError:
            self.data = pd.DataFrame()
            self.columns = []
        self.N = len(self.data)

    def get_user(self, username):
        '''Assuming that usernames are unique'''
        new_df = self.data[self.data["username"] == username]
        if len(new_df) == 0:
            return {}
        else:
            return User(**new_df.to_dict("records")[0])

    def all_usernames(self):
        try:
            for user in self.data["username"]:
                yield str(user)
        except KeyError:
            return []

    def add_user(self, user):
        if isinstance(user, User):
            self.data = self.data.append(user.to_dict(), ignore_index=True)
        elif isinstance(user, dict):
            # print("new user=", user)
            self.data = self.data.append(user, ignore_index=True)
            # print("data=", self.data)
        else:
            raise(TypeError)

    def save(self):
        self.data.to_csv(self.path, index=False)
        # print(self.data)
    def __str__(self):
       return self.data.__repr__()

    def __repr__(self):
        return f"user data is stored at {self.path}. There are {self.N} users."


class Collection:
    def __init__(self, class_):
        self.class_ = class_
        self.dict = {}
        self.size = 0
        self.pk = 0

    def append(self, obj):
        self.dict[self.pk] = obj
        self.pk += 1
        self.size += 1

    def pop(self, pk):
        del self.dict[pk]
        self.size -= 1

    def to_csv(self, path):
        import pandas as pd

        temp_list = [obj.to_dict() for obj in self.dict]
        pd.DataFrame(temp_list).to_csv(path, index=False) 

    def from_csv(self, path):
        import pandas as pd

        for record in pd.read_csv(path).to_dict("records"):
            self.append(self.class_.from_dict(record))

    def __len__(self):
        return self.size

    def __str__(self):
        return "["+",".join([obj.__str__() for obj in dict.values()])+"]"

    def __repr__(self):
        return "["+"\n,".join([obj.__str__() for obj in dict.values()])+"]"


if __name__ == "__main":
    # test the User and Collection classes
    users = Collection(User)
    user1 = User("Lili Mou")
    users.append(user1)
    user2 = User("Atharva Naik")
    user3 = User("Zijun Wu")
    users.append(user2)
    users.append(user3)
    
    print(user1)
    print(users)
    
