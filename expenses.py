import tkinter as tk
from tkinter import messagebox
from datetime import date
from db import get_connection

def open_expenses_page(user_id):
    win = tk.Toplevel()
    win.title("Expenses Tracker")
    win.geometry("700x600")
    win.configure(bg="#fff0f5")

    tk.Label(win, text="Expense Manager", font=("Helvetica", 20, "bold"), bg="#d8bfd8").pack(fill=tk.X, pady=10)

    frame = tk.Frame(win, bg="#fff0f5")
    frame.pack(pady=10)

    tk.Label(frame, text="Date (YYYY-MM-DD):", bg="#fff0f5").grid(row=0, column=0, sticky="e")
    date_entry = tk.Entry(frame)
    date_entry.grid(row=0, column=1)
    date_entry.insert(0, str(date.today()))

    tk.Label(frame, text="Amount:", bg="#fff0f5").grid(row=1, column=0, sticky="e")
    amount_entry = tk.Entry(frame)
    amount_entry.grid(row=1, column=1)

    tk.Label(frame, text="Category:", bg="#fff0f5").grid(row=2, column=0, sticky="e")
    category_var = tk.StringVar()
    category_var.set("food")
    tk.OptionMenu(frame, category_var, "food", "shopping", "grocery", "health", "other").grid(row=2, column=1, sticky="w")

    tk.Label(frame, text="Description:", bg="#fff0f5").grid(row=3, column=0, sticky="e")
    desc_entry = tk.Entry(frame, width=40)
    desc_entry.grid(row=3, column=1)

    listbox_ids = []

    def show_expenses():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT expense_id, date, amount, category, description FROM expenses WHERE user_id = %s ORDER BY date DESC", (user_id,))
            rows = cur.fetchall()
            conn.close()

            listbox.delete(0, tk.END)
            listbox_ids.clear()
            for r in rows:
                eid, d, amt, cat, desc = r
                preview = desc[:30] + ("..." if len(desc) > 30 else "")
                listbox.insert(tk.END, f"{d} | ₹{amt} | {cat} | {preview}")
                listbox_ids.append(eid)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_expense():
        try:
            d = date_entry.get()
            amt = int(amount_entry.get())
            cat = category_var.get()
            desc = desc_entry.get()
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO expenses (user_id, date, amount, category, description) VALUES (%s, %s, %s, %s, %s)", (user_id, d, amt, cat, desc))
            conn.commit()
            conn.close()
            show_expenses()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_expense():
        selected = listbox.curselection()
        if not selected: return
        index = selected[0]
        eid = listbox_ids[index]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""UPDATE expenses SET date=%s, amount=%s, category=%s, description=%s WHERE expense_id=%s""",
                        (date_entry.get(), int(amount_entry.get()), category_var.get(), desc_entry.get(), eid))
            conn.commit()
            conn.close()
            show_expenses()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_expense():
        selected = listbox.curselection()
        if not selected: return
        index = selected[0]
        eid = listbox_ids[index]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM expenses WHERE expense_id=%s", (eid,))
            conn.commit()
            conn.close()
            show_expenses()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_select(event):
        if not listbox.curselection(): return
        index = listbox.curselection()[0]
        eid = listbox_ids[index]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT date, amount, category, description FROM expenses WHERE expense_id=%s", (eid,))
            d, amt, cat, desc = cur.fetchone()
            conn.close()
            date_entry.delete(0, tk.END)
            date_entry.insert(0, str(d))
            amount_entry.delete(0, tk.END)
            amount_entry.insert(0, str(amt))
            category_var.set(cat)
            desc_entry.delete(0, tk.END)
            desc_entry.insert(0, desc)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Add Expense", bg="#dda0dd", command=add_expense).pack(pady=5)
    tk.Button(win, text="Update Selected", bg="#dda0dd", command=update_expense).pack(pady=5)

    frame2 = tk.Frame(win, bg="#fff0f5")
    frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    listbox = tk.Listbox(frame2, font=("Courier", 11), bg="white")
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    listbox.bind("<<ListboxSelect>>", on_select)

    scrollbar = tk.Scrollbar(frame2)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    tk.Button(win, text="Delete Selected", bg="#dda0dd", command=delete_expense).pack(pady=5)

    show_expenses()
