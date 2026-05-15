import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import calendar

conn = sqlite3.connect('3.db')
cursor = conn.cursor()

selected_id = None
selected_barber_id = None
selected_date_value = None
selected_time_slot = None
selected_dop_ids = []


def close():
    reg_log.destroy()


def check_user(nikname, phone, email):
    cursor.execute("SELECT full_name FROM clients WHERE full_name = ?", (nikname,))
    if cursor.fetchone():
        return "nickname"

    cursor.execute("SELECT phone FROM clients WHERE phone = ?", (phone,))
    if cursor.fetchone():
        return "phone"

    cursor.execute("SELECT email FROM clients WHERE email = ?", (email,))
    if cursor.fetchone():
        return "email"

    return None


def register():
    nikname = entry_nikname.get()
    phone = entry_phone.get()
    email = entry_email.get()
    password = entry_password.get()

    if not all([nikname, phone, email, password]):
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return

    exists = check_user(nikname, phone, email)
    if exists == "nickname":
        messagebox.showerror("Ошибка", "Пользователь с таким ником уже существует!")
        return
    elif exists == "phone":
        messagebox.showerror("Ошибка", "Пользователь с таким номером телефона уже существует!")
        return
    elif exists == "email":
        messagebox.showerror("Ошибка", "Пользователь с таким email уже существует!")
        return

    try:
        cursor.execute("INSERT INTO clients(full_name, phone, email, password) VALUES (?, ?, ?, ?)",
                       (nikname, phone, email, password))
        conn.commit()
        messagebox.showinfo("Успех", f"Пользователь {nikname} успешно зарегистрирован!")
        reg_window.destroy()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при регистрации: {e}")


def open_reg():
    global reg_window, entry_nikname, entry_phone, entry_email, entry_password

    reg_window = tk.Toplevel()
    reg_window.title("Регистрация")
    reg_window.geometry("350x450")
    reg_window.resizable(width=0, height=0)

    tk.Label(reg_window, text="Никнейм:").pack(pady=10)
    entry_nikname = tk.Entry(reg_window, width=30)
    entry_nikname.pack(pady=5)

    tk.Label(reg_window, text="Телефон:").pack(pady=10)
    entry_phone = tk.Entry(reg_window, width=30)
    entry_phone.pack(pady=5)

    tk.Label(reg_window, text="Email:").pack(pady=10)
    entry_email = tk.Entry(reg_window, width=30)
    entry_email.pack(pady=5)

    tk.Label(reg_window, text="Пароль:").pack(pady=10)
    entry_password = tk.Entry(reg_window, show="*", width=30)
    entry_password.pack(pady=5)

    tk.Button(reg_window, text="Зарегистрироваться", command=register,
              bg="green", fg="white", width=25, height=2).pack(pady=20)


def login():
    login_or_email = entry_log.get()
    password = entry_password_log.get()

    if not all([login_or_email, password]):
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return

    cursor.execute("SELECT full_name, password FROM clients WHERE full_name = ? OR email = ?",
                   (login_or_email, login_or_email))
    user = cursor.fetchone()

    if login_or_email == "admin" and password == "admin":
        log_window.destroy()
        reg_log.destroy()
        open_admin(user[0])
    elif user and user[1] == password:
        log_window.destroy()
        reg_log.destroy()
        open_main(user[0])
    else:
        messagebox.showerror("Ошибка", "Неверный логин/email или пароль!")


def open_log():
    global log_window, entry_log, entry_password_log

    log_window = tk.Toplevel()
    log_window.title("Вход в систему")
    log_window.geometry("350x300")
    log_window.resizable(width=0, height=0)

    tk.Label(log_window, text="Логин или Email:").pack(pady=20)
    entry_log = tk.Entry(log_window, width=30)
    entry_log.pack(pady=5)

    tk.Label(log_window, text="Пароль:").pack(pady=20)
    entry_password_log = tk.Entry(log_window, show="*", width=30)
    entry_password_log.pack(pady=5)

    tk.Button(log_window, text="Войти", command=login,
              bg="blue", fg="white", width=25, height=2).pack(pady=30)

def open_admin(username):
    def basedate():
        admin_window.destroy()
        bd = tk.Tk()
        bd.title("Управление бд")
        bd.geometry("900x600")

        notebook = ttk.Notebook(bd)
        notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        frame1 = ttk.Frame(notebook)
        frame2 = ttk.Frame(notebook)
        frame3 = ttk.Frame(notebook)
        frame4 = ttk.Frame(notebook)
        frame5 = ttk.Frame(notebook)
        frame6 = ttk.Frame(notebook)
        frame7 = ttk.Frame(notebook)
        notebook.add(frame1, text="Барбершоп")
        notebook.add(frame2, text="Сотрудник")
        notebook.add(frame3, text="Услуги")
        notebook.add(frame4, text="Записи клиентов")
        notebook.add(frame5, text="Клиент")
        notebook.add(frame6, text="Доп_Услуги")
        notebook.add(frame7, text="Расписание")
        def show_table(frame, table_name):
            for widget in frame.winfo_children():
                widget.destroy()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            columns = []
            for col in columns_info:
                columns.append(col[1])
            tree = ttk.Treeview(frame, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
            btn_refresh = ttk.Button(btn_frame, text="Обновить",
                                     command=lambda: load_data(tree, table_name))
            btn_refresh.pack(side=tk.LEFT, padx=5)
            btn_add = ttk.Button(btn_frame, text="Добавить",
                                 command=lambda: add_new(tree, table_name, columns))
            btn_add.pack(side=tk.LEFT, padx=5)
            btn_edit = ttk.Button(btn_frame, text="Изменить",
                                  command=lambda: edit_selected(tree, table_name, columns))
            btn_edit.pack(side=tk.LEFT, padx=5)
            btn_delete = ttk.Button(btn_frame, text="Удалить",
                                    command=lambda: delete_selected(tree, table_name))
            btn_delete.pack(side=tk.LEFT, padx=5)
            load_data(tree, table_name)
        def load_data(tree, table_name):
            for row in tree.get_children():
                tree.delete(row)
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            for row in data:
                tree.insert('', tk.END, values=row)
        def add_new(tree, table_name, columns):
            window = tk.Toplevel(bd)
            window.title(f"Добавить запись")
            window.geometry("300x400")
            entries = []
            for i, col in enumerate(columns):
                ttk.Label(window, text=col).pack(pady=3)
                entry = ttk.Entry(window)
                entry.pack(pady=3)
                entries.append(entry)
            def save():
                values = []
                for entry in entries:
                    values.append(entry.get())
                if "" in values:
                    messagebox.showwarning("Ошибка", "Заполните все поля!")
                    return

                placeholders = ','.join(['?' for _ in columns])
                columns_names = ','.join(columns)

                try:
                    cursor.execute(f"INSERT INTO {table_name} ({columns_names}) VALUES ({placeholders})", values)
                    conn.commit()
                    load_data(tree, table_name)
                    window.destroy()
                    messagebox.showinfo("Готово", "Запись добавлена!")
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

            ttk.Button(window, text="Сохранить", command=save).pack(pady=20)

        def edit_selected(tree, table_name, columns):
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Ошибка", "Выберите строку для изменения!")
                return

            values = tree.item(selected[0])['values']
            window = tk.Toplevel(bd)
            window.title(f"Изменить запись")
            window.geometry("300x400")
            entries = []
            for i, col in enumerate(columns):
                ttk.Label(window, text=col).pack(pady=3)
                entry = ttk.Entry(window)
                entry.insert(0, values[i])
                entry.pack(pady=3)
                entries.append(entry)
            def save():
                new_values = []
                for entry in entries:
                    new_values.append(entry.get())
                updates = []
                for i in range(1, len(columns)):
                    updates.append(f"{columns[i]} = ?")

                update_str = ', '.join(updates)

                try:
                    cursor.execute(f"UPDATE {table_name} SET {update_str} WHERE {columns[0]} = ?",
                                   new_values[1:] + [new_values[0]])
                    conn.commit()
                    load_data(tree, table_name)
                    window.destroy()
                    messagebox.showinfo("Готово", "Запись изменена!")
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

            ttk.Button(window, text="Сохранить", command=save).pack(pady=20)
        def delete_selected(tree, table_name):
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Ошибка", "Выберите строку для удаления!")
                return
            if messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
                values = tree.item(selected[0])['values']
                id_value = values[0]
                id_column = tree['columns'][0]

                try:
                    cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = ?", (id_value,))
                    conn.commit()
                    load_data(tree, table_name)
                    messagebox.showinfo("Готово", "Запись удалена!")
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

        show_table(frame1, "barbershops")
        show_table(frame2, "sotrudniki")
        show_table(frame3, "services")
        show_table(frame4, "zapisi")
        show_table(frame5, "clients")
        show_table(frame6, "dop_services")
        show_table(frame7, "schedules")

        bd.mainloop()
    admin_window = tk.Tk()
    admin_window.title("Главное окно")
    admin_window.geometry("400x300")
    admin_window.resizable(width=0, height=0)

    tk.Label(text=f"Добро пожаловать, {username}!").pack(pady=50)

    tk.Button(text="Управление бд", command=basedate, bg="green", fg="white", width=20, height=2).pack(pady=15)
    tk.Button(text="Выйти", command=lambda: close_main(admin_window), bg="red", fg="white", width=20, height=2).pack(pady=15)

    admin_window.mainloop()

def open_main(username):
    def zapis():
        global selected_id

        zapis_win = tk.Toplevel()
        zapis_win.title("Услуги")
        zapis_win.geometry("400x300")
        zapis_win.resizable(width=0, height=0)

        cursor.execute("SELECT id_service, name, price FROM services")
        services = cursor.fetchall()

        tree = ttk.Treeview(zapis_win, columns=("Name", "Price"), show="headings", height=10)
        tree.heading("Name", text="Услуга")
        tree.heading("Price", text="Цена")
        tree.column("Name", width=200)
        tree.column("Price", width=80)

        items = {}
        for sid, name, price in services:
            item = tree.insert("", tk.END, values=(name, price))
            items[item] = sid

        def choose_time():
            global selected_date_value, selected_time_slot

            time_win = tk.Toplevel()
            time_win.title("Выбор времени")
            time_win.geometry("350x400")
            time_win.resizable(width=0, height=0)

            tk.Label(time_win, text="Выберите дату:").pack(pady=10)

            calendar_frame = tk.Frame(time_win)
            calendar_frame.pack(pady=5)


            current_date = datetime.now()
            current_year = current_date.year
            current_month = current_date.month

            selected_date = tk.StringVar()
            selected_date.set(current_date.strftime("%Y-%m-%d"))

            def update_calendar(year, month):
                for widget in calendar_frame.winfo_children():
                    widget.destroy()

                month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                               'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

                nav_frame = tk.Frame(calendar_frame)
                nav_frame.grid(row=0, column=0, columnspan=7, pady=5)

                tk.Button(nav_frame, text="◀", command=lambda: change_month(-1), width=3).pack(side=tk.LEFT, padx=2)
                tk.Label(nav_frame, text=f"{month_names[month - 1]} {year}", width=20).pack(side=tk.LEFT, padx=2)
                tk.Button(nav_frame, text="▶", command=lambda: change_month(1), width=3).pack(side=tk.LEFT, padx=2)

                days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
                for i, day in enumerate(days):
                    tk.Label(calendar_frame, text=day, font=('Arial', 9, 'bold'), width=4).grid(row=1, column=i, pady=2)

                cal = calendar.monthcalendar(year, month)

                for i, week in enumerate(cal):
                    for j, day in enumerate(week):
                        if day != 0:
                            date = datetime(year, month, day)
                            if date >= current_date.replace(hour=0, minute=0, second=0, microsecond=0):
                                btn = tk.Button(calendar_frame, text=str(day), width=4,
                                                command=lambda d=date: select_date(d))
                                btn.grid(row=i + 2, column=j, pady=1)
                            else:
                                tk.Label(calendar_frame, text=str(day), width=4, fg='gray').grid(row=i + 2, column=j,
                                                                                                 pady=1)

            def change_month(delta):
                nonlocal current_year, current_month
                current_month += delta
                if current_month > 12:
                    current_month = 1
                    current_year += 1
                elif current_month < 1:
                    current_month = 12
                    current_year -= 1
                update_calendar(current_year, current_month)

            def select_date(date):
                selected_date.set(date.strftime("%Y-%m-%d"))
                date_label.config(text=f"Выбрана дата: {date.strftime('%d.%m.%Y')}")

            date_label = tk.Label(time_win, text=f"Выбрана дата: {current_date.strftime('%d.%m.%Y')}", fg="blue")
            date_label.pack(pady=5)

            update_calendar(current_year, current_month)

            tk.Label(time_win, text="Выберите время:").pack(pady=10)
            times = ['09:00', '10:00', '11:00', '12:00', '14:00', '15:00', '16:00', '17:00']
            time_combo = ttk.Combobox(time_win, values=times, width=15)
            time_combo.pack()

            def confirm_time():
                global selected_date_value, selected_time_slot

                selected_date_value = selected_date.get()
                selected_time_slot = time_combo.get()

                if not selected_date_value or not selected_time_slot:
                    messagebox.showwarning("Ошибка", "Выберите дату и время!")
                    return

                time_win.destroy()
                barber()

            tk.Button(time_win, text="Подтвердить", command=confirm_time, bg="green", fg="white").pack(pady=20)

        def take():
            global selected_id
            sel = tree.selection()
            if sel:
                selected_id = items[sel[0]]
                zapis_win.destroy()
                choose_time()
            else:
                messagebox.showwarning("Ошибка", "Выберите услугу!")

        tree.pack(padx=10, pady=10)
        btn = tk.Button(zapis_win, text="Выбрать", command=take)
        btn.pack()

    def barber():
        global selected_barber_id

        barber_win = tk.Toplevel()
        barber_win.title("Барбер")
        barber_win.geometry("400x300")
        barber_win.resizable(width=0, height=0)

        cursor.execute(
            "SELECT id_sotrudnik, full_name, position, phone FROM sotrudniki WHERE position LIKE '%барбер%' OR position LIKE '%стилист%'")
        barbers = cursor.fetchall()

        if not barbers:
            label = tk.Label(barber_win, text="Нет доступных барберов")
            label.pack(pady=50)

            def continue_without():
                global selected_barber_id
                selected_barber_id = None
                barber_win.destroy()
                dopoln()

            btn1 = tk.Button(barber_win, text="Продолжить без выбора", command=continue_without)
            btn1.pack(pady=10)
        else:
            label = tk.Label(barber_win, text="Выберите барбера:")
            label.pack(pady=10)

            tree_barber = ttk.Treeview(barber_win, columns=("Name", "Position", "Phone"), show="headings", height=8)
            tree_barber.heading("Name", text="ФИО")
            tree_barber.heading("Position", text="Должность")
            tree_barber.heading("Phone", text="Телефон")
            tree_barber.column("Name", width=150)
            tree_barber.column("Position", width=120)
            tree_barber.column("Phone", width=100)
            tree_barber.pack(pady=10)

            barber_items = {}
            for bid1, name1, position1, phone1 in barbers:
                item = tree_barber.insert("", tk.END, values=(name1, position1, phone1))
                barber_items[item] = bid1

            def select_barber():
                global selected_barber_id
                sel = tree_barber.selection()
                if sel:
                    selected_barber_id = barber_items[sel[0]]
                    for bid1, name1, position1, phone1 in barbers:
                        if bid1 == selected_barber_id:
                            label_selected.config(text=f"Выбран: {name1}")
                            break
                    barber_win.destroy()
                    dopoln()
                else:
                    messagebox.showwarning("Предупреждение", "Выберите барбера!")

            btn_select = tk.Button(barber_win, text="Выбрать", command=select_barber)
            btn_select.pack(pady=5)

            label_selected = tk.Label(barber_win, text="")
            label_selected.pack()

    def dopoln():
        global selected_dop_ids

        dopoln_win = tk.Toplevel()
        dopoln_win.title("Дополнение")
        dopoln_win.geometry("400x300")
        dopoln_win.resizable(width=0, height=0)

        cursor.execute(
            "SELECT ID_dop_services, name, price FROM dop_services WHERE services_id = ?",
            (selected_id,)
        )
        dop_services = cursor.fetchall()

        if not dop_services:
            label = tk.Label(dopoln_win, text="Для этой услуги нет дополнительных услуг")
            label.pack(pady=50)

            def skip():
                dopoln_win.destroy()
                next_step()

            btn = tk.Button(dopoln_win, text="Продолжить", command=skip)
            btn.pack(pady=10)
        else:
            label = tk.Label(dopoln_win, text=f"Доп.услуги для выбранной услуги:")
            label.pack(pady=10)

            tree_dop = ttk.Treeview(dopoln_win, columns=("Name", "Price"), show="headings", height=5)
            tree_dop.heading("Name", text="Услуга")
            tree_dop.heading("Price", text="Цена")
            tree_dop.column("Name", width=200)
            tree_dop.column("Price", width=80)
            tree_dop.pack(pady=10)

            dop_items = {}
            for did, name, price in dop_services:
                item = tree_dop.insert("", tk.END, values=(name, price))
                dop_items[item] = did

            selected_dop_ids = []
            selected_dop_names = []

            def add_dop():
                sel = tree_dop.selection()
                if sel:
                    dop_id = dop_items[sel[0]]
                    if dop_id not in selected_dop_ids:
                        selected_dop_ids.append(dop_id)
                        for did, name, price in dop_services:
                            if did == dop_id:
                                selected_dop_names.append(name)
                                label_selected.config(text=f"Выбрано: {', '.join(selected_dop_names)}")
                                break

            def next_step_local():
                global selected_dop_ids
                selected_dop_ids = selected_dop_ids
                dopoln_win.destroy()
                next_step()

            btn_add = tk.Button(dopoln_win, text="Добавить доп.услугу", command=add_dop)
            btn_add.pack(pady=5)

            label_selected = tk.Label(dopoln_win, text="Выбрано: нет")
            label_selected.pack()

            btn_next = tk.Button(dopoln_win, text="Далее", command=next_step_local)
            btn_next.pack(pady=10)

    def next_step():
        pay_win = tk.Toplevel()
        pay_win.title("Оплата")
        pay_win.geometry("350x300")
        pay_win.resizable(width=0, height=0)

        tk.Label(pay_win, text="Выберите способ оплаты:", font=("Arial", 12)).pack(pady=20)

        payment_type = tk.StringVar(value="cash")

        tk.Radiobutton(pay_win, text="Наличные", variable=payment_type, value="cash").pack(pady=10)
        tk.Radiobutton(pay_win, text="Картой", variable=payment_type, value="card").pack(pady=10)

        frame_card = tk.Frame(pay_win)
        tk.Label(frame_card, text="Реквизиты карты:").pack()
        card_details_entry = tk.Entry(frame_card, width=30, show="*")
        card_details_entry.pack(pady=5)

        def on_payment_change(*args):
            if payment_type.get() == "card":
                frame_card.pack(pady=10)
            else:
                frame_card.pack_forget()

        payment_type.trace_add('write', on_payment_change)

        def save_to_db():
            global selected_id, selected_barber_id, selected_date_value, selected_time_slot, selected_dop_ids

            pay_type = "Наличными" if payment_type.get() == "cash" else "Картой"

            if payment_type.get() == "card":
                card_details = card_details_entry.get()
                if not card_details:
                    messagebox.showwarning("Ошибка", "Введите реквизиты карты!")
                    return

            # Получаем ID клиента по username
            cursor.execute("SELECT id_client FROM clients WHERE full_name = ?", (username,))
            client = cursor.fetchone()
            if not client:
                messagebox.showerror("Ошибка", "Клиент не найден!")
                return

            client_id = client[0]

            current_datetime = f"{selected_date_value} {selected_time_slot}"
            dop_id = selected_dop_ids[0] if selected_dop_ids else None

            try:
                cursor.execute("""
                    INSERT INTO zapisi 
                    (client_id, sotrudnik_id, services_id, id_dop, data_zapisi, type) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    client_id,
                    selected_barber_id,
                    selected_id,
                    dop_id,
                    current_datetime,
                    pay_type
                ))
                conn.commit()

                messagebox.showinfo("Успех", "Запись успешно создана!")
                pay_win.destroy()

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить запись: {e}")

        tk.Button(pay_win, text="Подтвердить", command=save_to_db, bg="green", fg="white").pack(pady=20)

    main_window = tk.Tk()
    main_window.title("Главное окно")
    main_window.geometry("400x300")
    main_window.resizable(width=0, height=0)

    tk.Label(main_window, text=f"Добро пожаловать, {username}!").pack(pady=50)

    tk.Button(main_window, text="Запись", command=zapis, bg="green", fg="white", width=20, height=2).pack(pady=15)
    tk.Button(main_window, text="Выйти", command=lambda: close_main(main_window), bg="red", fg="white", width=20,
              height=2).pack(pady=15)

    main_window.mainloop()


def close_main(main_window):
    main_window.destroy()


reg_log = tk.Tk()
reg_log.title("Вход и Регистрация")
reg_log.geometry("350x400")
reg_log.resizable(width=0, height=0)

tk.Button(reg_log, text="Зарегистрироваться", command=open_reg, bg="green", fg="white", width=25, height=3).pack(
    pady=35)
tk.Button(reg_log, text="Войти", command=open_log, bg="blue", fg="white", width=25, height=3).pack(pady=35)
tk.Button(reg_log, text="Выйти", command=close, bg="red", fg="white", width=25, height=3).pack(pady=35)

reg_log.mainloop()

conn.close()