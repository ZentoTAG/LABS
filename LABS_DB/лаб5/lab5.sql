-- ==========================================
-- Лабораторная работа №5: Триггеры
-- (Основные таблицы созданы в ЛР №4)
-- ==========================================

USE Тагиров;

-- 1. Создание дополнительной таблицы LOG
CREATE TABLE IF NOT EXISTS LOG (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_time DATETIME,
    event_type VARCHAR(50),
    record_id INT,
    message VARCHAR(255)
);

--1. Триггер на добавление
DELIMITER //
CREATE TRIGGER trg_insert_employee
AFTER INSERT ON Table_Тагиров
FOR EACH ROW
BEGIN
    INSERT INTO LOG (event_time, event_type, record_id, message)
    VALUES (NOW(), 'INSERT', NEW.id, CONCAT('Добавлен сотрудник: ', NEW.ФИО));
END; //
DELIMITER ;

--3. Триггер на изменение
DELIMITER //
CREATE TRIGGER trg_update_employee
AFTER UPDATE ON Table_Тагиров
FOR EACH ROW
BEGIN
    INSERT INTO LOG (event_time, event_type, record_id, message)
    VALUES (NOW(), 'UPDATE', NEW.id, CONCAT('Обновлен сотрудник: ', NEW.ФИО));
END; //
DELIMITER ;

--4 Триггер на удаление
DELIMITER //
CREATE TRIGGER trg_delete_employee
AFTER DELETE ON Table_Тагиров
FOR EACH ROW
BEGIN
    INSERT INTO LOG (event_time, event_type, record_id, message)
    VALUES (NOW(), 'DELETE', OLD.id, CONCAT('Удален сотрудник: ', OLD.ФИО));
END; //
DELIMITER ;
