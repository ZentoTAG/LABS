# Lab_1 Тагиров Вадим ИВТ-25-1б
import cProfile
import random
import os

def format_set(elements):
    if not elements:
        return "{∅}"
    return "{" + ", ".join(map(str, elements)) + "}"
    
class Set:
    def __init__(self, name, elements):
        self.name = name
        self.elements = elements

    def union(self, other):
        result = self.elements.copy()
        for el in other.elements:
            if el not in result:
                result.append(el)
        return result

    def intersect(self, other):
        result = []
        for el in self.elements:
            if el in other.elements and el not in result:
                result.append(el)
        return result

    def diff(self, other):
        result = []
        for el in self.elements:
            if el not in other.elements and el not in result:
                result.append(el)
        return result

    def sym_diff(self, other):
        result = []
        for el in self.elements:
            if el not in other.elements and el not in result:
                result.append(el)
        for el in other.elements:
            if el not in self.elements and el not in result:
                result.append(el)
        return result

    def __str__(self):
        if len(self.elements) != 0:
            return f"{self.name} = {{{', '.join(map(str, self.elements))}}}"
        else:
            return f"{self.name} = {{∅}}"


class SetCollection:
    def __init__(self, universum):
        self.U = universum
        self.sets = []
        self.operators = (("+"))

    def add(self, myset):
        if self.find(myset.name) is not None:
            return False
        self.sets.append(myset)
        return True

    def find(self, name):
        for s in self.sets:
            if s.name == name:
                return s
        return None

    def complement(self, name):
        s = self.find(name)
        if s is None:
            return None
        result = [x for x in self.U if x not in s.elements]
        return Set(f"¬{name}", result)

    def in_universum(self, el):
        return el in self.U

    def get_set(self, name):
        return self.find(name)

    def del_set(self, name):
        s = self.find(name)
        if s is not None:
            self.sets.remove(s)
            return True
        return False

    def in_SetCollection(self, name):
        return self.find(name) is not None

 
class Calculator:
    def __init__(self):
        self.sets = SetCollection(list(range(-30, 31)))

    def print_info(self):
        print(
"""Это мой калькулятор множеств, введите цифру для выбора действия
0 - завершить пограмму
1 - создать и ввести множество
2 - удалить множество
3 - вывести множество
4 - ввод математической формулы
    """)

    def print_set(self, set_name):
        if self.sets.in_SetCollection(set_name):
            print(self.sets.get_set(set_name))
        else: 
            print("такого множества нет")
             
    def input_manual(self, name, count):
        temp = list()
        try:
            while count != 0:
                el = int(input("элемент: "))
                if self.sets.in_universum(el) and el not in temp:
                    temp.append(el)
                    count -= 1
                else:
                    print("Число вне универсума или уже есть")
            self.sets.add(Set(name, sorted(temp)))
            print(f"Множество {name} создано")
        except:
            raise ValueError

    def input_random(self, name, count):
        temp = list()
        U_copy = self.sets.U.copy()
        try:
            while count != 0:
                el = random.choice(self.sets.U)
                if self.sets.in_universum(el):
                    temp.append(el)
                    count -= 1 
            self.sets.add(Set(name, sorted(temp)))
            print(f"Множество {name} создано")
        except:
            print("где-то ошибка")
                
    def input_conditions(self, name, condition):
        temp = self.sets.U.copy()
        if "нечёт" in condition:
            temp = [x for x in temp if x % 2 != 0]
        elif "чёт" in condition:
            temp = [x for x in temp if x % 2 == 0]
        
        if "неотриц" in condition:
            temp = [x for x in temp if x >= 0]
        elif "отриц" in condition:
            temp = [x for x in temp if x < 0]
        
        if "кратн" in condition:
            n = int(input("кратно: "))
            temp = [x for x in temp if x % n == 0]
        
        if "диап" in condition:
            x, y = list(map(int, input("диап в виде x y: ").split()))
            temp = [el for el in temp if x <= el <= y]
        
        self.sets.add(Set(name, sorted(temp)))
        print(f"Множество {name} создано: {format_set(temp)}")   
        
    def input_set(self, choice):
        pass

    def in_universum(self, el):
        return el in self.sets.U

    def formula_parser(self, formula):
        formula = formula.replace(" ", "")

        save = False
        if "=" in formula:
            parts = formula.split("=", 1)
            left = parts[0]
            formula = parts[1]
            save = True

        result = self.evaluate(formula)
        if result is None:
            print("Ошибка в формуле")
            return

        for s in self.sets.sets[:]:
            if s.name.startswith("_temp_"):
                self.sets.sets.remove(s)

        if save:
            self.sets.del_set(left)
            self.sets.add(Set(left, sorted(result.elements)))
            print(f"{left} = {format_set(sorted(result.elements))}")
        else:
            print(f"{format_set(sorted(result.elements))}")

    def evaluate(self, formula):
        formula = formula.replace(" ", "")

        while "(" in formula:
            start = formula.rfind("(")
            end = formula.find(")", start)
            if end == -1:
                print("Незакрытая скобка")
                return None

            inner = formula[start + 1:end]
            inner_result = self.evaluate(inner)
            if inner_result is None:
                return None

            temp_name = f"_temp_{start}"
            self.sets.add(Set(temp_name, inner_result.elements))
            formula = formula[:start] + temp_name + formula[end + 1:]

        tokens = []
        i = 0
        while i < len(formula):
            if formula[i] in "+-*^!":
                tokens.append(formula[i])
                i += 1
            else:
                j = i
                while j < len(formula) and formula[j] not in "+-*^!":
                    j += 1
                tokens.append(formula[i:j])
                i = j

        if not tokens:
            print("Пустая формула")
            return None

        if tokens[0] == "!":
            name = tokens[1]
            result = self.sets.complement(name)
            if result is None:
                print(f"Множество {name} не найдено")
                return None
            print(f"!{name} = {format_set(result.elements)}")
            i = 2
        else:
            result = self.sets.get_set(tokens[0])
            if result is None:
                print(f"Множество {tokens[0]} не найдено")
                return None
            i = 1

        while i < len(tokens):
            op = tokens[i]
            name = tokens[i + 1]
            other = self.sets.get_set(name)
            if other is None:
                print(f"Множество {name} не найдено")
                return None

            old = result.elements.copy()

            if op == "+":
                result = Set("temp", result.union(other))
            elif op == "*":
                result = Set("temp", result.intersect(other))
            elif op == "-":
                result = Set("temp", result.diff(other))
            elif op == "^":
                result = Set("temp", result.sym_diff(other))

            print(f"{format_set(old)} {op} {format_set(other.elements)} = {format_set(result.elements)}")
            i += 2

        return result
        
    def manager(self):
        while True:
            self.clear()
            self.print_info()
            choice = input("действие: ")
            match choice:
                case "0":
                    break
                case "1":
                    self.create_set()
                case "2":
                    self.delete_set()
                case "3":
                    self.show_set()
                case "4":
                    self.formula()
                case _:
                    print("неверный ввод")
            input()

    def create_set(self):
        choice = input("1 - вручную, 2 - случайно, 3 - по условиям: ")
        name = input("имя множества: ")
        match choice:
            case "1":
                count = int(input("Кол-во элементов: "))
                self.input_manual(name, count)
            case "2":
                count = int(input("Кол-во элементов: "))
                self.input_random(name, count)
            case "3":
                print("""
доступны условия:
  нечёт/чёт
  отриц/неотриц
  кратн
  диап
""")
                condition = input("условие: ")
                self.input_conditions(name, condition)
                input()
            case _:
                print("неверный ввод")

    def delete_set(self):
        name = input("имя множества: ")
        if self.sets.del_set(name):
            print(f"Множество {name} удалено")
        else:
            print("Такого множества нет")

    def show_set(self):
        name = input("имя множества: ")
        s = self.sets.get_set(name)
        if s is not None:
            print(s)
        else:
            print("Такого множества нет")

    def formula(self):
        formula = input("формула: ")
        self.formula_parser(formula)

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")
                        
calc = Calculator()
cProfile.run("calc.manager()")

    

# manager()
# print(calc_answer("A+B")
