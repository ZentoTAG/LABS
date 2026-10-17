import os

class Matrix:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.n = len(data)

    def is_reflexive(self):
        return all(self.data[i][i] == 1 for i in range(self.n))

    def is_antireflexive(self):
        return all(self.data[i][i] == 0 for i in range(self.n))

    def is_symmetric(self):
        return all(self.data[i][j] == self.data[j][i] 
                   for i in range(self.n) for j in range(self.n))

    def is_antisymmetric(self):
        return all(not (self.data[i][j] == 1 and self.data[j][i] == 1) 
                   for i in range(self.n) for j in range(self.n) if i != j)

    def is_transitive(self):
        return all(self.data[i][k] == 1 
                   for i in range(self.n) for j in range(self.n) for k in range(self.n) 
                   if self.data[i][j] == 1 and self.data[j][k] == 1)

    def is_connected(self):
        return all(self.data[i][j] == 1 or self.data[j][i] == 1 
                   for i in range(self.n) for j in range(self.n) if i != j)

    def get_type(self):
        if self.is_reflexive() and self.is_symmetric() and self.is_transitive():
            return "Эквивалентность"
            
        if self.is_antisymmetric() and self.is_transitive():
            if self.is_antireflexive():
                return "Строгий порядок"
            elif self.is_connected():
                return "Полный линейный порядок"
            else:
                return "Частичный порядок"
                
        return "Никакое из перечисленных"

    def __str__(self):
        matrix_str = "\n".join(" ".join(map(str, row)) for row in self.data)
        return f"{self.name}:\n{matrix_str}"


class App:
    def __init__(self):
        self.matrixes = {}

    def load_from_file(self, name_of_file):
        path = f"files/{name_of_file}.txt"
        try:
            with open(path, "r") as file:
                return [list(map(int, line.split())) for line in file]
        except FileNotFoundError:
            print(f"Файл {path} не найден!")
            return None

    def add_matrix(self):
        name = input("Введите имя файла (например, m1): ")
        data = self.load_from_file(name)
        if data:
            self.matrixes[name] = Matrix(name, data)
            print(f"Матрица {name} успешно загружена.")
        input("Нажмите Enter...")

    # --- НОВЫЙ МЕТОД ЗАГРУЗКИ ВСЕХ МАТРИЦ ---
    def load_all_matrices(self):
        if not os.path.exists("files"):
            print("Папка 'files' не найдена!")
            input("Нажмите Enter...")
            return

        files = [f for f in os.listdir("files") if f.endswith(".txt")]
        if not files:
            print("В папке 'files' нет текстовых файлов!")
        else:
            for file in files:
                name = file.replace(".txt", "")
                data = self.load_from_file(name)
                if data:
                    self.matrixes[name] = Matrix(name, data)
            print(f"Успешно загружено матриц: {len(files)}")
        input("Нажмите Enter...")

    def print_report(self, matrix):
        print(matrix)
        print(f"Рефлексивность:      {'Да' if matrix.is_reflexive() else 'Нет'}")
        print(f"Антирефлексивность:  {'Да' if matrix.is_antireflexive() else 'Нет'}")
        print(f"Симметричность:      {'Да' if matrix.is_symmetric() else 'Нет'}")
        print(f"Антисимметричность:  {'Да' if matrix.is_antisymmetric() else 'Нет'}")
        print(f"Транзитивность:      {'Да' if matrix.is_transitive() else 'Нет'}")
        print(f"Связность:           {'Да' if matrix.is_connected() else 'Нет'}")
        print(f"ТИП:                 {matrix.get_type()}\n")

    def analyze_one(self):
        name = input("Введите имя матрицы: ")
        if name in self.matrixes:
            self.print_report(self.matrixes[name])
        else:
            print("Матрица не найдена!")
        input("Нажмите Enter...")

    def analyze_all(self):
        if not self.matrixes:
            print("Сначала загрузите матрицы!")
        else:
            for matrix in self.matrixes.values():
                self.print_report(matrix)
                print("-" * 30)
        input("Нажмите Enter...")

    def manager(self):
        while True:
            self.clear()
            print("""
=== ЛАБОРАТОРНАЯ РАБОТА 2: СВОЙСТВА ОТНОШЕНИЙ ===
1 - Загрузить одну матрицу из файла
2 - Загрузить все матрицы из папки
3 - Анализ одной матрицы
4 - Анализ всех загруженных матриц
0 - Выход
""")
            choice = input("Действие: ")
            match choice:
                case "0": break
                case "1": self.add_matrix()
                case "2": self.load_all_matrices()
                case "3": self.analyze_one()
                case "4": self.analyze_all()
                case _:
                    print("Неверный ввод!")
                    input("Нажмите Enter...")

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")


app = App()
app.manager()
