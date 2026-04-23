import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"
CATEGORIES = ["Еда", "Транспорт", "Жильё", "Развлечения", "Прочее"]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_expense():
    try:
        amount = float(entry_amount.get())
        category = combo_category.get()
        description = entry_desc.get()
        date = entry_date.get()
        datetime.strptime(date, "%Y-%m-%d")
    except Exception as e:
        messagebox.showerror("Ошибка", "Проверьте корректность данных!")
        return

    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date,
    }
    expenses.append(expense)
    save_data(expenses)
    update_table()
    clear_inputs()

def update_table(filter_category=None, date_from=None, date_to=None):
    for i in tree.get_children():
        tree.delete(i)
    for ex in expenses:
        cat_match = filter_category is None or ex["category"] == filter_category
        date_ok = True
        if date_from:
            date_ok = date_ok and ex["date"] >= date_from
        if date_to:
            date_ok = date_ok and ex["date"] <= date_to
        if cat_match and date_ok:
            tree.insert("", tk.END, values=(ex["date"], ex["category"], f"{ex['amount']:.2f} ₽", ex["description"]))

def filter_expenses():
    cat = combo_filter_cat.get() or None
    d_from = entry_date_from.get() or None
    d_to = entry_date_to.get() or None
    update_table(filter_category=cat, date_from=d_from, date_to=d_to)

def clear_filter():
    combo_filter_cat.set("")
    entry_date_from.delete(0, tk.END)
    entry_date_to.delete(0, tk.END)
    update_table()

def calc_sum():
    d_from = entry_date_from.get()
    d_to = entry_date_to.get()
    try:
        if d_from: datetime.strptime(d_from, "%Y-%m-%d")
        if d_to: datetime.strptime(d_to, "%Y-%m-%d")
    except:
        messagebox.showerror("Ошибка", "Некорректный формат даты!")
        return
    total = sum(
        ex["amount"] for ex in expenses
        if (not d_from or ex["date"] >= d_from) and (not d_to or ex["date"] <= d_to)
    )
    messagebox.showinfo("Итого", f"Сумма расходов: {total:.2f} ₽")

def clear_inputs():
    entry_amount.delete(0, tk.END)
    combo_category.set(CATEGORIES[0])
    entry_desc.delete(0, tk.END)
    entry_date.delete(0, tk.END)

# --- Инициализация ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x500")

expenses = load_data()

# --- Вкладка "Добавить расход" ---
frame_add = ttk.LabelFrame(root, text="Добавить расход")
frame_add.pack(fill=tk.X, padx=10, pady=5)

ttk.Label(frame_add, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
entry_amount = ttk.Entry(frame_add)
entry_amount.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_add, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
combo_category = ttk.Combobox(frame_add, values=CATEGORIES)
combo_category.current(0)
combo_category.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_add, text="Описание:").grid(row=2, column=0, padx=5, pady=5)
entry_desc = ttk.Entry(frame_add)
entry_desc.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_add, text="Дата (ГГГГ-ММ-ДД):").grid(row=3, column=0, padx=5, pady=5)
entry_date = ttk.Entry(frame_add)
entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
entry_date.grid(row=3, column=1, padx=5, pady=5)

ttk.Button(frame_add, text="Добавить", command=add_expense).grid(row=4, columnspan=2, pady=10)

# --- Вкладка "Фильтр" ---
frame_filter = ttk.LabelFrame(root, text="Фильтр")
frame_filter.pack(fill=tk.X, padx=10, pady=5)

ttk.Label(frame_filter, text="Категория:").grid(row=0, column=0, padx=5, pady=5)
combo_filter_cat = ttk.Combobox(frame_filter, values=[""] + CATEGORIES)
combo_filter_cat.current(0)
combo_filter_cat.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_filter, text="Дата с:").grid(row=1, column=0, padx=5, pady=5)
entry_date_from = ttk.Entry(frame_filter)
entry_date_from.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_filter, text="Дата по:").grid(row=2, column=0, padx=5, pady=5)
entry_date_to = ttk.Entry(frame_filter)
entry_date_to.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(frame_filter, text="Фильтровать", command=filter_expenses).grid(row=3, column=0, padx=5, pady=5)
ttk.Button(frame_filter, text="Очистить фильтр", command=clear_filter).grid(row=3, column=1, padx=5, pady=5)
ttk.Button(frame_filter, text="Сумма за период", command=calc_sum).grid(row=4, columnspan=2, pady=10)

# --- Таблица расходов ---
tree = ttk.Treeview(root,
                    columns=("date", "category", "amount", "desc"),
                    show="headings")
tree.heading("date", text="Дата")
tree.heading("category", text="Категория")
tree.heading("amount", text="Сумма")
tree.heading("desc", text="Описание")
tree.pack(fill="both", expand=True, padx=10, pady=10)

update_table()
root.mainloop()
