import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date
from db import get_connection

bg_color = "#fff0f5"  # light pink
header_color = "#d8bfd8"  # thistle
btn_color = "#dda0dd"  # plum

def open_entertainment_page(user_id):
    win = tk.Toplevel()
    win.title("Entertainment Tracker")
    win.geometry("700x600")
    win.configure(bg=bg_color)

    tk.Label(win, text="Entertainment Tracker", font=("Helvetica", 20, "bold"), bg=header_color).pack(fill=tk.X, pady=10)

    form_frame = tk.Frame(win, bg=bg_color)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg=bg_color).grid(row=0, column=0, sticky="e")
    date_entry = tk.Entry(form_frame)
    date_entry.grid(row=0, column=1)
    date_entry.insert(0, str(date.today()))

    tk.Label(form_frame, text="Category:", bg=bg_color).grid(row=1, column=0, sticky="e")
    category_var = tk.StringVar()
    category_var.set("music")
    categories = ["music", "book", "movie/series"]
    tk.OptionMenu(form_frame, category_var, *categories).grid(row=1, column=1, sticky="w")

    tk.Label(form_frame, text="Title:", bg=bg_color).grid(row=2, column=0, sticky="e")
    title_entry = tk.Entry(form_frame)
    title_entry.grid(row=2, column=1)

    tk.Label(form_frame, text="Progress:", bg=bg_color).grid(row=3, column=0, sticky="e")
    progress_var = tk.StringVar()
    progress_var.set("not started")
    progress_options = ["not started", "in progress", "completed"]
    tk.OptionMenu(form_frame, progress_var, *progress_options).grid(row=3, column=1, sticky="w")

    def add_entry():
        d = date_entry.get()
        category = category_var.get()
        title = title_entry.get()
        progress = progress_var.get()
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO entertainment_tracker (user_id, date, category, title, progress)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, d, category, title, progress))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Entry added!")
            show_entries()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_entry():
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an entry to update.")
            return
        index = selected[0]
        entry_id = listbox_ids[index]
        d = date_entry.get()
        category = category_var.get()
        title = title_entry.get()
        progress = progress_var.get()
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE entertainment_tracker
                SET date = %s, category = %s, title = %s, progress = %s
                WHERE entry_id = %s
            """, (d, category, title, progress, entry_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Entry updated!")
            show_entries()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_entry():
        selected = listbox.curselection()
        if not selected:
            return
        index = selected[0]
        entry_id = listbox_ids[index]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM entertainment_tracker WHERE entry_id = %s", (entry_id,))
            conn.commit()
            conn.close()
            show_entries()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_entries():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT entry_id, date, category, title, progress FROM entertainment_tracker WHERE user_id = %s ORDER BY date DESC", (user_id,))
            rows = cur.fetchall()
            conn.close()

            listbox.delete(0, tk.END)
            listbox_ids.clear()
            for row in rows:
                entry_id, d, category, title, progress = row
                display_text = f"{d} | {category} | {progress} | {title}"
                listbox.insert(tk.END, display_text)
                listbox_ids.append(entry_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_select(event):
        selected = listbox.curselection()
        if not selected:
            return
        index = selected[0]
        entry_id = listbox_ids[index]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT date, category, title, progress FROM entertainment_tracker WHERE entry_id = %s", (entry_id,))
            row = cur.fetchone()
            conn.close()
            if row:
                d, category, title, progress = row
                date_entry.delete(0, tk.END)
                date_entry.insert(0, str(d))
                category_var.set(category)
                title_entry.delete(0, tk.END)
                title_entry.insert(0, title)
                progress_var.set(progress)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn_frame = tk.Frame(win, bg=bg_color)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Add Entry", bg=btn_color, command=add_entry).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Update Selected", bg=btn_color, command=update_entry).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Delete Selected", bg=btn_color, command=delete_entry).pack(side=tk.LEFT, padx=10)

    list_frame = tk.Frame(win, bg=bg_color)
    list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    listbox = tk.Listbox(list_frame, font=("Courier", 11), bg="#ffffff")
    listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    listbox.bind("<<ListboxSelect>>", on_select)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    listbox_ids = []

    show_entries()
