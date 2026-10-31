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

    def print_truth_table(self):
        print(f"\n--- Таблица истинности для {self.name} ---")
        print(" | ".join(self.vars) + " | F")
        print("-" * (4 * self.vars_count + 5))
        
        for i in range(self.n):
            binary_str = bin(i)[2:].zfill(self.vars_count)
            
            # Разбиваем строку на отдельные символы и выводим
            row = list(binary_str)
            print(" | ".join(row) + f" | {self.vector[i]}")
            
    def get_sdnf(self):
        print("\n--- СДНФ ---")
        self.sdnf_terms = []
        
        for i in range(self.n):
            if self.vector[i] == '1':
                term = []
                binary_str = bin(i)[2:].zfill(self.vars_count)
                
                for j in range(self.vars_count):
                    bit = binary_str[j]
                    var_name = self.vars[j]
                    if bit == '1':
                        term.append(var_name)
                    else:
                        term.append("¬" + var_name)
                self.sdnf_terms.append(term)
        
        if not self.sdnf_terms:
            print("Функция равна 0 (пустая СДНФ)")
            return []
        
        print(" ∨ ".join(["".join(t) for t in self.sdnf_terms]))
        return self.sdnf_terms
        
    def find_implicants(self, terms):
        print("\n--- импликанты ---")
        if len(terms) <= 1:
            print("Склеивать нечего.")
            return terms

        implicants = []
        
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                t1 = terms[i]
                t2 = terms[j]
                diff = 0
                diff_idx = -1
                
                for k in range(len(t1)):
                    if t1[k] != t2[k]:
                        diff += 1
                        diff_idx = k
                
                if diff == 1:
                    if t1[diff_idx] == "¬" + t2[diff_idx] or "¬" + t1[diff_idx] == t2[diff_idx]:
                        new_term = t1.copy()
                        new_term[diff_idx] = '-'
                        if new_term not in implicants:
                            implicants.append(new_term)
        
        if not implicants:
            print("Нет склеивающихся термов.")
        else:
            print(" ∨ ".join(["".join(t) for t in implicants]))
        return implicants

    def print_implicant_matrix(self, sdnf_terms, implicants):
        print("\n--- Импликантная матрица ---")
        if not implicants:
            return

        header = f"{'':<8} | "
        for t in sdnf_terms:
            header += f"{''.join(t):<8} | "
        print(header)
        print("-" * len(header))

        for imp in implicants:
            row = f"{''.join(imp):<8} | "
            for t in sdnf_terms:
                is_covered = True
                for k in range(len(imp)):
                    if imp[k] != '-' and imp[k] != t[k]:
                        is_covered = False
                        break
                row += f"{'+' if is_covered else ' ':<8} | "
            print(row)

    def get_mdnf(self, implicants, sdnf_terms):
        print("\n--- МДНФ ---")
        if not implicants:
            print(" ∨ ".join(["".join(t) for t in sdnf_terms]))
            return
            
        essential = []
        for t in sdnf_terms:
            covered_by = []
            for imp in implicants:
                is_covered = True
                for k in range(len(imp)):
                    if imp[k] != '-' and imp[k] != t[k]:
                        is_covered = False
                        break
                if is_covered:
                    covered_by.append(imp)
            
            if len(covered_by) == 1:
                if covered_by[0] not in essential:
                    essential.append(covered_by[0])
                
        if not essential:
            essential = implicants
            
        print(" ∨ ".join(["".join(t) for t in essential]))


class App:
    def __init__(self):
        self.functions = {}

    def add_function(self):
        name = input("Имя функции:: ")
        vector_input = input("Вектор функции: ").strip()
        
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
        
        # Вывод вектора функции в начале
        print(f"\nВектор функции {func.name}: {func.vector}")
        
        func.print_truth_table()
        sdnf = func.get_sdnf()
        
        if sdnf:
            implicants = func.find_implicants(sdnf)
            func.print_implicant_matrix(sdnf, implicants)
            func.get_mdnf(implicants, sdnf)
            
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
