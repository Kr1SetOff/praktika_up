--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.4 в Ср апр 29 11:04:46 2026
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: barbershops
CREATE TABLE IF NOT EXISTS barbershops (id_barbershop INTEGER PRIMARY KEY AUTOINCREMENT, adress TEXT NOT NULL, name TEXT NOT NULL);

-- Таблица: clients
CREATE TABLE IF NOT EXISTS clients (id_client INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL, phone TEXT NOT NULL, email TEXT, reg TEXT NOT NULL DEFAULT (CURRENT_DATE));

-- Таблица: schedules
CREATE TABLE IF NOT EXISTS schedules (id_schedule INTEGER PRIMARY KEY AUTOINCREMENT, sotrudnik_id INTEGER REFERENCES sotrudniki (id_sotrudnik) ON DELETE CASCADE NOT NULL, day_week INTEGER NOT NULL CHECK (day_week BETWEEN 1 AND 7), start_time TEXT NOT NULL, end_time TEXT NOT NULL, lunch TEXT);

-- Таблица: services
CREATE TABLE IF NOT EXISTS services (id_service INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price REAL NOT NULL CHECK (price >= 0));

-- Таблица: sotrudniki
CREATE TABLE IF NOT EXISTS sotrudniki (id_sotrudnik INTEGER PRIMARY KEY AUTOINCREMENT, barbershop_id INTEGER REFERENCES barbershops (id_barbershop) ON DELETE CASCADE NOT NULL, full_name TEXT NOT NULL, position TEXT, phone TEXT NOT NULL);

-- Таблица: zapisi
CREATE TABLE IF NOT EXISTS zapisi (id_zapisi INTEGER PRIMARY KEY AUTOINCREMENT, client_id INTEGER NOT NULL REFERENCES clients (id_client) ON DELETE CASCADE, sotrudnik_id INTEGER NOT NULL REFERENCES sotrudniki (id_sotrudnik) ON DELETE CASCADE, services_id INTEGER NOT NULL REFERENCES services (id_service) ON DELETE CASCADE, data_zaiavki TEXT NOT NULL, status TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP), prichina_otmeni TEXT);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
