import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

HISTORY_FILE = "history.json"
MIN_LENGTH, MAX_LENGTH = 6, 32

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_password(length, use_digits, use_letters, use_special):
    chars = ""
    if use_digits: chars += string.digits
    if use_letters: chars += string.ascii_letters
    if use_special: chars += string.punctuation
    if not chars:
        return None
    return ''.join(random.choices(chars, k=length))

def on_generate():
    length = int(scale_length.get())
    use_digits = var_digits.get()
    use_letters = var_letters.get()
    use_special = var_special.get()
    
    if length < MIN_LENGTH or length > MAX_LENGTH:
        messagebox.showerror("Ошибка", f"Длина должна быть от {MIN_LENGTH} до {MAX_LENGTH}")
        return
    
    password = generate_password(length, use_digits, use_letters, use_special)
    if not password:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
        return
    
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    
    history.append(password)
    save_history(history)
    update_history_table()

def update_history_table():
    for i in tree.get_children():
        tree.delete(i)
    for p in history:
        tree.insert("", tk.END, values=(p,))

root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x400")

tk.Label(root, text="Длина пароля:").grid(row=0, column=0, padx=10, pady=5)
scale_length = tk.Scale(root, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL)
scale_length.set(12)
scale_length.grid(row=0, column=1, padx=10, pady=5)

var_digits = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Цифры", variable=var_digits).grid(row=1, column=0, sticky="w", padx=10)
var_letters = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Буквы", variable=var_letters).grid(row=1, column=1, sticky="w", padx=10)
var_special = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Спецсимволы", variable=var_special).grid(row=1, column=2, sticky="w", padx=10)

tk.Button(root, text="Сгенерировать", command=on_generate).grid(row=2, column=0, columnspan=3, pady=15)

tk.Label(root, text="Пароль:").grid(row=3, column=0, padx=10, pady=5)
entry_password = tk.Entry(root, width=40)
entry_password.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

tree = ttk.Treeview(root, columns=("password",), show="headings")
tree.heading("password", text="История паролей")
tree.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

history = load_history()
update_history_table()

root.mainloop()
