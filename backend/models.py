# Python file with all the model classes (like users, sentences etc...)
import json 
import pandas as pd

class User:
    def __init__(self, name):
        self.name = name

    def from_dict(self):
        pass 

    def to_dict(self):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


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
    
