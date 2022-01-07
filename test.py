class Person:
    def __init__(self):
        self.the_dict = {"Person": self}
        self.name = None
        self.the_name = Name(self.the_dict)

    def change_name(self):
        self.the_name.change_name()
        # self.name = self.the_dict["Name"]
        print(self.name)


class Name:
    def __init__(self, adict):
        self.adict = adict

    def change_name(self):
        self.adict["Person"].name = "Omotoye"
        # print(name)


the_person = Person()
the_person.change_name()
