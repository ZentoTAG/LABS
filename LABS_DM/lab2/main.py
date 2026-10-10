from os import system, name as os_name

class Matrix:
    def __init__(self):
        self.name = str()
        self.data = list()

    def is_reflexive(self):
        pass

    def is_antireflexive(self):
        pass

    def is_symmetric(self):
        pass

    def is_antisymmetric(self):
        pass

    def is_transitive(self):
        pass

    def is_connected(self):
        pass

    def get_type(self):
        type = str()

    def __str__(self):
        print(f"{name} = {data}")

class App():
    def __init__(self):
        pass

    def load_from_file(self, name_of_file):
        pass

    def manager(self):
        pass
    
    def clear(self):
        system("cls" if os_name == "nt" else "clear")

app = App()
app.manager()

