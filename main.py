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
    if use_digits:
