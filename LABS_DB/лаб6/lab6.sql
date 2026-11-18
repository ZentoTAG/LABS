-- 1. Создание представления 1
CREATE OR REPLACE VIEW View_Employees_Contact AS
SELECT ФИО, Телефон, ЗП
FROM Table_Тагиров;
-- 2. Создание представления 2
CREATE OR REPLACE VIEW View_Employees_Address AS
SELECT ФИО, Адрес
FROM Table_Тагиров
ORDER BY Адрес ASC;
-- 3. Создание представления 3
CREATE OR REPLACE VIEW View_Employees_Experience AS
SELECT ФИО, Стаж
FROM Table_Тагиров
WHERE Стаж > 4;
