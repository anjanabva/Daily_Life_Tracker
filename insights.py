import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from db import get_connection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import defaultdict

bg_color = "#fffaf0"
header_color = "#ffe4e1"
btn_color = "#dda0dd"

def open_insights_page(user_id):
    win = tk.Toplevel()
    win.title("Insights Dashboard")
    win.geometry("1000x700")
    win.configure(bg=bg_color)

    tk.Label(win, text="🌸 INSIGHTS 🌸", font=("Helvetica", 24, "bold"), bg=header_color).pack(fill=tk.X, pady=10)

    control_frame = tk.Frame(win, bg=bg_color)
    control_frame.pack(pady=10)

    graph_frame = tk.Frame(win, bg=bg_color)
    graph_frame.pack(fill=tk.BOTH, expand=True)

    time_var = tk.StringVar()
    time_dropdown = ttk.Combobox(control_frame, textvariable=time_var, state="readonly", width=20)
    time_dropdown["values"] = ["Monthly", "Weekly"]
    time_dropdown.set("Monthly")
    time_dropdown.grid(row=0, column=0, padx=5)

    section_var = tk.StringVar()
    section_dropdown = ttk.Combobox(control_frame, textvariable=section_var, state="readonly", width=35)
    section_dropdown["values"] = [
        "Diary: Mood %",
        "Diary: Tag %",
        "Diary: Entry Count",
        "Diary: Top 3 Moods",
        "Diary: Top 3 Tags",
        "Expenses: Total/Category",
        "Expenses: Category Ranking",
        "Expenses: Total Spending",
        "Sleep: Daily Hours with Avg",
        "Sleep: Sleep Quality %",        
        "Entertainment: Progress %",
        "Entertainment: Category/Title Count"
    ]
    section_dropdown.set("Diary: Mood %")
    section_dropdown.grid(row=0, column=1, padx=5)

    def clear_graph():
        for widget in graph_frame.winfo_children():
            widget.destroy()

    def show_graph():
        clear_graph()
        mode = time_var.get()
        section = section_var.get()

        conn = get_connection()
        cur = conn.cursor()

        today = datetime.today().date()
        since = today.replace(day=1) if mode == "Monthly" else today - timedelta(days=7)

        fig, ax = plt.subplots(figsize=(8, 5))

        if section == "Diary: Mood %":
            cur.execute("""
                SELECT mood, COUNT(*) FROM diary_entries
                WHERE user_id = %s AND date >= %s
                GROUP BY mood
            """, (user_id, since))
            data = cur.fetchall()
            labels, values = zip(*data) if data else ([], [])
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
            ax.set_title("Mood Distribution")

        elif section == "Diary: Tag %":
            cur.execute("""
                SELECT tag, COUNT(*) FROM diary_entries
                WHERE user_id = %s AND date >= %s
                GROUP BY tag
            """, (user_id, since))
            data = cur.fetchall()
            labels, values = zip(*data) if data else ([], [])
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
            ax.set_title("Tag Distribution")

        elif section == "Diary: Entry Count":
            cur.execute("""
                SELECT date, COUNT(*) FROM diary_entries
                WHERE user_id = %s AND date >= %s
                GROUP BY date
                ORDER BY date
            """, (user_id, since))
            data = cur.fetchall()
            if data:
                dates, counts = zip(*data)
                ax.plot(dates, counts, marker='o')
                ax.set_title("Diary Entries Over Time")
                ax.set_ylabel("Number of Entries")

        elif section == "Diary: Top 3 Moods":
            cur.execute("""
                SELECT mood, COUNT(*) AS count FROM diary_entries
                WHERE user_id = %s AND date >= %s
                GROUP BY mood
                ORDER BY count DESC
                LIMIT 3
            """, (user_id, since))
            data = cur.fetchall()
            if data:
                labels, values = zip(*data)
                ax.bar(labels, values, color='plum')
                ax.set_title("Top 3 Most Used Moods")
                ax.set_ylabel("Count")

        elif section == "Diary: Top 3 Tags":
            cur.execute("""
                SELECT tag, COUNT(*) AS count FROM diary_entries
                WHERE user_id = %s AND date >= %s
                GROUP BY tag
                ORDER BY count DESC
                LIMIT 3
            """, (user_id, since))
            data = cur.fetchall()
            if data:
                labels, values = zip(*data)
                ax.bar(labels, values, color='violet')
                ax.set_title("Top 3 Most Used Tags")
                ax.set_ylabel("Count")

        elif section == "Expenses: Total/Category":
            cur.execute("""
                SELECT category, SUM(amount) FROM expenses
                WHERE user_id = %s AND date >= %s
                GROUP BY category
            """, (user_id, since))
            data = cur.fetchall()
            if data:
                labels, values = zip(*data)
                ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
                ax.set_title("Expenses by Category")

        elif section == "Expenses: Category Ranking":
            cur.execute("""
                SELECT category, SUM(amount) FROM expenses
                WHERE user_id = %s AND date >= %s
                GROUP BY category ORDER BY SUM(amount) DESC
            """, (user_id, since))
            data = cur.fetchall()
            if data:
                labels, values = zip(*data)
                ax.bar(labels, values, color='orchid')
                ax.set_title("Spending by Category")

        elif section == "Expenses: Total Spending":
            cur.execute("""
                SELECT date, SUM(amount) FROM expenses
                WHERE user_id = %s AND date >= %s
                GROUP BY date ORDER BY date
            """, (user_id, since))
            data = cur.fetchall()
            if data:
                dates, totals = zip(*data)
                ax.plot(dates, totals, marker='o', color='green')
                ax.set_title("Daily Spending Trend")
                ax.set_ylabel("Amount Spent")

        elif section == "Sleep: Daily Hours with Avg":
            cur.execute("""
                SELECT date, sleep_hours FROM sleep_tracker
                WHERE user_id = %s AND date >= %s
                ORDER BY date
            """, (user_id, since))
            data = cur.fetchall()
            if data:
                dates, hours = zip(*data)
                ax.plot(dates, hours, marker='o', color='skyblue', label='Sleep Hours')
                avg = sum(hours) / len(hours)
                ax.axhline(avg, color='red', linestyle='--', label=f'Avg: {avg:.1f}h')
                ax.set_title("Sleep Hours Per Day")
                ax.set_ylabel("Hours")
                ax.legend()

        elif section == "Sleep: Sleep Quality %":
            cur.execute("""
                SELECT sleep_quality, COUNT(*) FROM sleep_tracker
                WHERE user_id = %s AND date >= %s
                GROUP BY sleep_quality
            """, (user_id, since))
            data = cur.fetchall()
            if data:
                labels, values = zip(*data)
                ax.pie(values, labels=labels, autopct="%1.1f%%")
                ax.set_title("Sleep Quality Breakdown")

        elif section == "Entertainment: Progress %":
            cur.execute("""
                SELECT progress, COUNT(*) FROM entertainment_tracker
                WHERE user_id = %s AND date >= %s
                GROUP BY progress
            """, (user_id, since))
            data = cur.fetchall()
            if data:
                labels, values = zip(*data)
                ax.pie(values, labels=labels, autopct="%1.1f%%")
                ax.set_title("Entertainment Progress")

        elif section == "Entertainment: Category/Title Count":
            cur.execute("""
                SELECT category, COUNT(*) FROM entertainment_tracker
                WHERE user_id = %s AND date >= %s
                GROUP BY category
            """, (user_id, since))
            data = cur.fetchall()
            if data:
                labels, values = zip(*data)
                ax.bar(labels, values, color='salmon')
                ax.set_title("Entertainment Count by Category")

        conn.close()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    tk.Button(control_frame, text="Show Insights", bg=btn_color, command=show_graph).grid(row=0, column=2, padx=10)
    show_graph()
