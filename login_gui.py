import tkinter as tk
from tkinter import messagebox
from db import get_connection
import index

#colors for an aesthetic view
BG_COLOR = "#fef6e4"
BTN_BG = "#d81159"
BTN_FG = "white"
FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 14, "bold")

def login():
    username = entry_username.get().strip()
    if not username:
        messagebox.showerror("Error", "Username cannot be empty")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (username,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        messagebox.showinfo("Success", f"Welcome back, {username}!")
        root.destroy()
        index.open_index_menu(user_id)
    else:
        messagebox.showerror("Login Failed", "User not found. Please register.")

    cursor.close()
    conn.close()

def register():
    username = entry_username.get().strip()
    if not username:
        messagebox.showerror("Error", "Username cannot be empty")
        return

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (user_name) VALUES (%s)", (username,))
        conn.commit()
        messagebox.showinfo("Registered", "New user registered successfully!")
    except:
        conn.rollback()
        messagebox.showerror("Error", "Registration failed")
    finally:
        cursor.close()
        conn.close()

# GUI window appearance
root = tk.Tk()
root.title("Daily Life Tracker")
root.geometry("400x250")
root.config(bg=BG_COLOR)
root.resizable(False, False)

tk.Label(root, text="✨ Welcome to Daily Life Tracker ✨", font=TITLE_FONT, bg=BG_COLOR, fg="#2d2d2d").pack(pady=20)

tk.Label(root, text="Enter your username:", font=FONT, bg=BG_COLOR).pack()
entry_username = tk.Entry(root, width=30, font=FONT)
entry_username.pack(pady=5)

tk.Button(root, text="Login", width=20, bg=BTN_BG, fg=BTN_FG, font=FONT, relief="flat", command=login).pack(pady=8)
tk.Button(root, text="Register", width=20, bg="#9b1c77", fg="white", font=FONT, relief="flat", command=register).pack(pady=2)

root.mainloop()
