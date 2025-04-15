import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date
from db import get_connection

bg_color = "#fff0f5"  # light pink
header_color = "#d8bfd8"  # thistle
btn_color = "#dda0dd"  # plum


def open_diary_entries_page(user_id):
    win = tk.Toplevel()
    win.title("Diary Entries")
    win.geometry("700x600")
    win.configure(bg=bg_color)

    tk.Label(win, text="Diary Entry Manager", font=("Helvetica", 20, "bold"), bg=header_color).pack(fill=tk.X, pady=10)

    form_frame = tk.Frame(win, bg=bg_color)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Date (YYYY-MM-DD):", bg=bg_color).grid(row=0, column=0, sticky="e")
    date_entry = tk.Entry(form_frame)
    date_entry.grid(row=0, column=1)
    date_entry.insert(0, str(date.today()))

    tk.Label(form_frame, text="Content:", bg=bg_color).grid(row=1, column=0, sticky="e")
    content_entry = tk.Text(form_frame, height=5, width=30)
    content_entry.grid(row=1, column=1)

    tk.Label(form_frame, text="Mood:", bg=bg_color).grid(row=2, column=0, sticky="e")
    mood_var = tk.StringVar(form_frame)
    mood_var.set("happy")
    mood_options = ["fear", "happy", "sad", "anger", "contempt", "nostalgia", "other"]
    tk.OptionMenu(form_frame, mood_var, *mood_options).grid(row=2, column=1, sticky="w")

    tk.Label(form_frame, text="Tag:", bg=bg_color).grid(row=3, column=0, sticky="e")
    tag_var = tk.StringVar(form_frame)
    tag_var.set("personal")
    tag_options = ["work", "personal", "travel", "other"]
    tk.OptionMenu(form_frame, tag_var, *tag_options).grid(row=3, column=1, sticky="w")

    def add_entry():
        d = date_entry.get()
        content = content_entry.get("1.0", tk.END).strip()
        mood = mood_var.get()
        tag = tag_var.get()
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO diary_entries (user_id, date, content, mood, tag)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, d, content, mood, tag))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Diary entry added!")
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
        content = content_entry.get("1.0", tk.END).strip()
        mood = mood_var.get()
        tag = tag_var.get()
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE diary_entries
                SET date = %s, content = %s, mood = %s, tag = %s
                WHERE entry_id = %s
            """, (d, content, mood, tag, entry_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Diary entry updated!")
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
            cur.execute("DELETE FROM diary_entries WHERE entry_id = %s", (entry_id,))
            conn.commit()
            conn.close()
            show_entries()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_entries():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT entry_id, date, content, mood, tag FROM diary_entries WHERE user_id = %s ORDER BY date DESC", (user_id,))
            rows = cur.fetchall()
            conn.close()

            listbox.delete(0, tk.END)
            listbox_ids.clear()
            for row in rows:
                entry_id, d, content, mood, tag = row
                content_preview = content.strip().replace("\n", " ")[:40] + ("..." if len(content.strip()) > 40 else "")
                display_text = f"{d} | {mood} | {tag} | {content_preview}"
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
            cur.execute("SELECT date, content, mood, tag FROM diary_entries WHERE entry_id = %s", (entry_id,))
            row = cur.fetchone()
            conn.close()
            if row:
                d, content, mood, tag = row
                date_entry.delete(0, tk.END)
                date_entry.insert(0, str(d))
                content_entry.delete("1.0", tk.END)
                content_entry.insert(tk.END, content)
                mood_var.set(mood)
                tag_var.set(tag)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Add Entry", bg=btn_color, command=add_entry).pack(pady=5)
    tk.Button(win, text="Update Selected", bg=btn_color, command=update_entry).pack(pady=5)

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

    tk.Button(win, text="Delete Selected", bg=btn_color, command=delete_entry).pack(pady=5)

    show_entries()
