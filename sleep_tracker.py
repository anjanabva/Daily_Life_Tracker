import tkinter as tk
from tkinter import messagebox
from datetime import date
from db import get_connection

def open_sleep_tracker_page(user_id):
    win = tk.Toplevel()
    win.title("Sleep Tracker")
    win.geometry("700x600")
    win.configure(bg="#fff0f5")

    tk.Label(win, text="Sleep Tracker", font=("Helvetica", 20, "bold"), bg="#d8bfd8").pack(fill=tk.X, pady=10)

    frame = tk.Frame(win, bg="#fff0f5")
    frame.pack(pady=10)

    tk.Label(frame, text="Date (YYYY-MM-DD):", bg="#fff0f5").grid(row=0, column=0, sticky="e")
    date_entry = tk.Entry(frame)
    date_entry.grid(row=0, column=1)
    date_entry.insert(0, str(date.today()))

    tk.Label(frame, text="Sleep Hours:", bg="#fff0f5").grid(row=1, column=0, sticky="e")
    hours_entry = tk.Entry(frame)
    hours_entry.grid(row=1, column=1)

    tk.Label(frame, text="Sleep Quality:", bg="#fff0f5").grid(row=2, column=0, sticky="e")
    quality_var = tk.StringVar()
    quality_var.set("good")
    tk.OptionMenu(frame, quality_var, "poor", "average", "good", "excellent").grid(row=2, column=1, sticky="w")

    listbox_ids = []

    def show_records():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT sleep_id, date, sleep_hours, sleep_quality FROM sleep_tracker WHERE user_id=%s ORDER BY date DESC", (user_id,))
            rows = cur.fetchall()
            conn.close()

            listbox.delete(0, tk.END)
            listbox_ids.clear()
            for r in rows:
                sid, d, hrs, q = r
                listbox.insert(tk.END, f"{d} | {hrs} hrs | {q}")
                listbox_ids.append(sid)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_record():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO sleep_tracker (user_id, date, sleep_hours, sleep_quality) VALUES (%s, %s, %s, %s)",
                        (user_id, date_entry.get(), float(hours_entry.get()), quality_var.get()))
            conn.commit()
            conn.close()
            show_records()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_record():
        if not listbox.curselection(): return
        index = listbox.curselection()[0]
        sid = listbox_ids[index]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE sleep_tracker SET date=%s, sleep_hours=%s, sleep_quality=%s WHERE sleep_id=%s",
                        (date_entry.get(), float(hours_entry.get()), quality_var.get(), sid))
            conn.commit()
            conn.close()
            show_records()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_record():
        if not listbox.curselection(): return
        index = listbox.curselection()[0]
        sid = listbox_ids[index]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM sleep_tracker WHERE sleep_id=%s", (sid,))
            conn.commit()
            conn.close()
            show_records()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_select(event):
        if not listbox.curselection(): return
        index = listbox.curselection()[0]
        sid = listbox_ids[index]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT date, sleep_hours, sleep_quality FROM sleep_tracker WHERE sleep_id=%s", (sid,))
            d, hrs, q = cur.fetchone()
            conn.close()
            date_entry.delete(0, tk.END)
            date_entry.insert(0, str(d))
            hours_entry.delete(0, tk.END)
            hours_entry.insert(0, str(hrs))
            quality_var.set(q)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Add Record", bg="#dda0dd", command=add_record).pack(pady=5)
    tk.Button(win, text="Update Selected", bg="#dda0dd", command=update_record).pack(pady=5)

    list_frame = tk.Frame(win, bg="#fff0f5")
    list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    listbox = tk.Listbox(list_frame, font=("Courier", 11), bg="white")
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    listbox.bind("<<ListboxSelect>>", on_select)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    tk.Button(win, text="Delete Selected", bg="#dda0dd", command=delete_record).pack(pady=5)

    show_records()
