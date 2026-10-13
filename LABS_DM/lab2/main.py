from os import system, name as os_name

class Matrix:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def is_reflexive(self):
        for i in range(len(self.data)):
            if self.data[i][i] == 1:
                continue
            else:
                return False
        return True

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
        form_str = str()
        for i in self.data:
            form_str += "".join(self.data[i])
            form_str += "\n"
        return f"{self.name} = {form_str}"

class App():
    def __init__(self):
       self.matrixes = dict()

    def print_matrix(self, name):
        print(self.get_matrix(name))

    def get_matrix(self, name):
        return self.matrixes[name]

    def get_copy(self, string):
        return string[::]

    def load_from_file(self, name_of_file):
        with open(f"files/{name_of_file}.txt", "r") as file:
            lines = file.readlines()
            for i in range(len(lines)):
                if "\n" in self.get_copy(lines[i]):
                    lines[i] = self.get_copy(lines[i]).replace("\n", "", 1)
                lines[i] = list(map(int, lines[i].split()))
        return lines
        
    def print_info(self):
        print("""
              пенис: """)
    
    def calc_answer(self):
        name_of_file = input("введите имя файла: ")
        self.matrixes[name_of_file] = Matrix(name_of_file, self.load_from_file(name_of_file))
        if self.matrixes[name_of_file].is_reflexive():
            print("эта чухня рефлексивна")

        print(self.matrixes[name_of_file])

    def manager(self):
        while True:
            self.clear()
            self.print_info()
            choice = input("действие: ")
            match choice:
                case "0":
                    break
                case "1":
                    self.calc_answer()
                case _:
                    print("неверный ввод")
            input()

    def clear(self):
        system("cls" if os_name == "nt" else "clear")

app = App()
app.manager()

