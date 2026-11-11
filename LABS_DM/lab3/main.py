import os


class BoolFunction:
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector
        self.n = len(vector)
        self.vars_count = 0
        while 2 ** self.vars_count < self.n:
            self.vars_count += 1
        self.vars = [chr(97 + i) for i in range(self.vars_count)]

    # терм вида "10-" превращаем в строку "a¬c"
    def term_to_str(self, term):
        res = ""
        for i in range(len(term)):
            if term[i] == '1':
                res += self.vars[i]
            elif term[i] == '0':
                res += "¬" + self.vars[i]
        if res == "":
            res = "1"
        return res

    def print_truth_table(self):
        print(f"\n--- Таблица истинности для {self.name} ---")
        print(" | ".join(self.vars) + " | F")
        print("-" * (4 * self.vars_count + 5))

        for i in range(self.n):
            binary_str = bin(i)[2:].zfill(self.vars_count)
            row = list(binary_str)
            print(" | ".join(row) + f" | {self.vector[i]}")

    def get_sdnf(self):
        print("\n--- СДНФ ---")
        sdnf = []

        for i in range(self.n):
            if self.vector[i] == '1':
                sdnf.append(bin(i)[2:].zfill(self.vars_count))

        if not sdnf:
            print("Функция равна 0 (пустая СДНФ)")
            return []

        print(" ∨ ".join([self.term_to_str(t) for t in sdnf]))
        return sdnf

    # склеиваем два терма, если они отличаются ровно в одной позиции
    # возвращает новый терм
    def glue(self, t1, t2):
        diff = 0
        idx = -1
        for k in range(len(t1)):
            if t1[k] != t2[k]:
                if t1[k] == '-' or t2[k] == '-':
                    return None
                diff += 1
                idx = k
        if diff != 1:
            return None
        return t1[:idx] + '-' + t1[idx + 1:]

    def find_implicants(self, sdnf):
        print("\n--- Неполные склеивания ---")
        prime = []        # простые импликанты
        current = sdnf
        step = 1

        while len(current) > 0:
            used = [False] * len(current)
            new_terms = []

            for i in range(len(current)):
                for j in range(i + 1, len(current)):
                    g = self.glue(current[i], current[j])
                    if g is not None:
                        used[i] = True
                        used[j] = True
                        if g not in new_terms:
                            new_terms.append(g)

            for i in range(len(current)):
                if not used[i] and current[i] not in prime:
                    prime.append(current[i])

            print(f"\nШаг {step}:")
            if new_terms:
                print(" ∨ ".join([self.term_to_str(t) for t in new_terms]))
            else:
                print("Склеивать больше нечего.")

            current = new_terms
            step += 1

        print("\nСокращённая ДНФ:")
        print(" ∨ ".join([self.term_to_str(t) for t in prime]))
        return prime

    # покрывает ли импликанта терм СДНФ
    def is_covered(self, imp, term):
        for k in range(len(imp)):
            if imp[k] != '-' and imp[k] != term[k]:
                return False
        return True

    def print_implicant_matrix(self, sdnf, implicants):
        print("\n--- Импликантная матрица ---")

        header = f"{'':<10} | "
        for t in sdnf:
            header += f"{self.term_to_str(t):<10} | "
        print(header)
        print("-" * len(header))

        for imp in implicants:
            row = f"{self.term_to_str(imp):<10} | "
            for t in sdnf:
                if self.is_covered(imp, t):
                    row += f"{'+':<10} | "
                else:
                    row += f"{'':<10} | "
            print(row)

    def get_mdnf(self, sdnf, implicants):
        print("\n--- МДНФ ---")

        # терм СДНФ, который покрывает только одна импликанта
        core = []
        for t in sdnf:
            covered_by = []
            for imp in implicants:
                if self.is_covered(imp, t):
                    covered_by.append(imp)
            if len(covered_by) == 1 and covered_by[0] not in core:
                core.append(covered_by[0])

        # какие термы ядро не покрыло
        left_terms = []
        for t in sdnf:
            ok = False
            for c in core:
                if self.is_covered(c, t):
                    ok = True
            if not ok:
                left_terms.append(t)

        # остальные импликанты перебором, самый короткий набор
        others = [imp for imp in implicants if imp not in core]
        best = []
        best_len = 10 ** 9
        if left_terms:
            for mask in range(1, 2 ** len(others)):
                chosen = []
                for i in range(len(others)):
                    if mask & (1 << i):
                        chosen.append(others[i])
                if len(chosen) >= best_len:
                    continue
                all_ok = True
                for t in left_terms:
                    ok = False
                    for imp in chosen:
                        if self.is_covered(imp, t):
                            ok = True
                    if not ok:
                        all_ok = False
                        break
                if all_ok:
                    best = chosen
                    best_len = len(chosen)

        result = core + best
        print(" ∨ ".join([self.term_to_str(t) for t in result]))


class App:
    def __init__(self):
        self.functions = {}

    def add_function(self):
        name = input("Имя функции: ")
        vector_input = input("Вектор функции: ").replace(" ", "")

        if not all(c in '01' for c in vector_input):
            print("Ошибка: вектор должен состоять только из 0 и 1!")
            input("Нажмите Enter...")
            return

        if len(vector_input) not in [2, 4, 8, 16, 32]:
            print("Ошибка: длина вектора должна быть степенью двойки!")
            input("Нажмите Enter...")
            return

        self.functions[name] = BoolFunction(name, vector_input)
        print(f"Функция {name} успешно добавлена.")
        input("Нажмите Enter...")

    def analyze_function(self):
        if not self.functions:
            print("Сначала добавьте хотя бы одну функцию!")
            input("Нажмите Enter...")
            return

        name = input("Введите имя функции: ")
        if name not in self.functions:
            print("Функция не найдена!")
            input("Нажмите Enter...")
            return

        func = self.functions[name]

        # вектор выводим по 4 знака через пробел
        v = func.vector
        groups = [v[i:i + 4] for i in range(0, len(v), 4)]
        print(f"\nВектор функции {func.name}: {' '.join(groups)}")

        func.print_truth_table()
        sdnf = func.get_sdnf()

        if sdnf:
            implicants = func.find_implicants(sdnf)
            func.print_implicant_matrix(sdnf, implicants)
            func.get_mdnf(sdnf, implicants)

        input("\nНажмите Enter...")

    def manager(self):
        while True:
            self.clear()
            print("""
=== ЛАБОРАТОРНАЯ РАБОТА 3: МЕТОД КВАЙНА ===
1 - Добавить функцию
2 - Выполнить минимизацию
0 - Выход
""")
            choice = input("Действие: ")
            match choice:
                case "0": break
                case "1": self.add_function()
                case "2": self.analyze_function()
                case _:
                    print("Неверный ввод!")
                    input("Нажмите Enter...")

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")


app = App()
app.manager()
