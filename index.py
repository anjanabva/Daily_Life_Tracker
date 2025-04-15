# index.py
import tkinter as tk
from functools import partial

import diary_entries_page
import expenses
import sleep_tracker
import entertainment
import all_entries_viewer
import insights

def open_real_module(name, user_id):
    if name == "Diary Entries":
        diary_entries_page.open_diary_entries_page(user_id)
    elif name == "Expenses":
        expenses.open_expenses_page(user_id)
    elif name == "Sleep Tracker":
        sleep_tracker.open_sleep_tracker_page(user_id)
    elif name == "Entertainment Tracker":
        entertainment.open_entertainment_page(user_id)
    elif name == "🌸All Entries Viewer🌸":
        all_entries_viewer.open_all_entries_viewer(user_id)
    elif name == "🌸INSIGHTS🌸":
        insights.open_insights_page(user_id)
    


def open_index_menu(user_id):
    root = tk.Tk()
    root.title("Daily Life Tracker - Menu")
    root.geometry("600x500")
    root.configure(bg="#fff0f5")  # light boho pinkish

    tk.Label(root, text="Choose a module", font=("Helvetica", 18, "bold"), bg="#fff0f5", fg="#800080").pack(pady=20)

    modules = [
        "Diary Entries",
        "Expenses",
        "Sleep Tracker",
        "Entertainment Tracker"
    ]

    for name in modules:
        btn = tk.Button(
            root, text=name,
            width=30, height=2,
            bg="#e6ccff", fg="#000000",
            font=("Helvetica", 15),
            command=partial(open_real_module, name, user_id)
        )
        btn.pack(pady=5)

    name = "🌸All Entries Viewer🌸"
    tk.Button(
        root, text=name,
        width=50, height=5,
        bg="#e6ccff", fg="#000000",
        font=("Helvetica", 25),
        command=partial(open_real_module, name, user_id)
    ).pack(pady=5)

    tk.Button(
        root, text="🌸INSIGHTS🌸",
        width=50, height=5,
        bg="#e6ccff", fg="#000000",
        font=("Helvetica", 25),
        command=partial(open_real_module, "🌸INSIGHTS🌸", user_id)
    ).pack(pady=5)

    root.mainloop()
