import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from db import get_connection

def open_all_entries_viewer(user_id):
    win = tk.Toplevel()
    win.title("All Entries Viewer")
    win.geometry("950x650")
    win.configure(bg="white")

    MODULES = ["Diary Entries", "Expenses", "Entertainment Tracker", "Sleep Tracker"]

    HEADER_FONT = ("Helvetica", 20, "bold")
    LABEL_FONT = ("Helvetica", 10)

    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def create_filters(module):
        clear_frame(filter_frame)

        fields.clear()

        if module == "Diary Entries":
            add_combobox("Mood", ["", "fear", "happy", "sad", "anger", "contempt", "nostalgia", "other"])
            add_combobox("Tag", ["", "work", "personal", "travel", "other"])
            add_date_range()

        elif module == "Expenses":
            add_combobox("Category", ["", "food", "shopping", "grocery", "health", "other"])
            add_range("Amount")
            add_date_range()

        elif module == "Entertainment Tracker":
            add_combobox("Category", ["", "music", "book", "movie/series"])
            add_entry("Title Contains")
            add_combobox("Progress", ["", "not started", "in progress", "completed"])
            add_date_range()

        elif module == "Sleep Tracker":
            add_combobox("Sleep Quality", ["", "poor", "average", "good", "excellent"])
            add_range("Sleep Hours")
            add_date_range()

    def add_combobox(label, values):
        tk.Label(filter_frame, text=label + ":", font=LABEL_FONT).pack(anchor="w")
        var = tk.StringVar()
        cb = ttk.Combobox(filter_frame, textvariable=var, values=values, state="readonly")
        cb.pack(fill="x", pady=2)
        fields[label] = var

    def add_entry(label):
        tk.Label(filter_frame, text=label + ":", font=LABEL_FONT).pack(anchor="w")
        var = tk.StringVar()
        entry = ttk.Entry(filter_frame, textvariable=var)
        entry.pack(fill="x", pady=2)
        fields[label] = var

    def add_range(label):
        tk.Label(filter_frame, text=label + " Range:", font=LABEL_FONT).pack(anchor="w")
        var_min = tk.StringVar()
        var_max = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=var_min).pack(fill="x", pady=1)
        ttk.Entry(filter_frame, textvariable=var_max).pack(fill="x", pady=1)
        fields[label + " Min"] = var_min
        fields[label + " Max"] = var_max

    def add_date_range():
        add_range("Date")

    def show_results():
        module = module_var.get()
        conditions = []
        params = [user_id]

        if module == "Diary Entries":
            query = """
                SELECT date, mood, tag, content FROM diary_entries
                WHERE user_id = %s {conditions} ORDER BY date DESC
            """
            if fields["Mood"].get():
                conditions.append("AND mood = %s")
                params.append(fields["Mood"].get())
            if fields["Tag"].get():
                conditions.append("AND tag = %s")
                params.append(fields["Tag"].get())
            add_date_filter("Date", conditions, params)

        elif module == "Expenses":
            query = """
                SELECT date, category, amount, description FROM expenses
                WHERE user_id = %s {conditions} ORDER BY date DESC
            """
            if fields["Category"].get():
                conditions.append("AND category = %s")
                params.append(fields["Category"].get())
            add_range_filter("Amount", conditions, params)
            add_date_filter("Date", conditions, params)

        elif module == "Entertainment Tracker":
            query = """
                SELECT date, category, title, progress FROM entertainment_tracker
                WHERE user_id = %s {conditions} ORDER BY date DESC
            """
            if fields["Category"].get():
                conditions.append("AND category = %s")
                params.append(fields["Category"].get())
            if fields["Title Contains"].get():
                conditions.append("AND title LIKE %s")
                params.append('%' + fields["Title Contains"].get() + '%')
            if fields["Progress"].get():
                conditions.append("AND progress = %s")
                params.append(fields["Progress"].get())
            add_date_filter("Date", conditions, params)

        elif module == "Sleep Tracker":
            query = """
                SELECT date, sleep_hours, sleep_quality FROM sleep_tracker
                WHERE user_id = %s {conditions} ORDER BY date DESC
            """
            if fields["Sleep Quality"].get():
                conditions.append("AND sleep_quality = %s")
                params.append(fields["Sleep Quality"].get())
            add_range_filter("Sleep Hours", conditions, params)
            add_date_filter("Date", conditions, params)

        final_query = query.format(conditions=" ".join(conditions))

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(final_query, params)
            rows = cur.fetchall()
            conn.close()

            result_box.delete(0, tk.END)
            for row in rows:
                result_box.insert(tk.END, " | ".join([str(r) for r in row]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_range_filter(base, conditions, params):
        min_val = fields[base + " Min"].get()
        max_val = fields[base + " Max"].get()
        if min_val:
            conditions.append(f"AND {base.lower().replace(' ', '_')} >= %s")
            params.append(min_val)
        if max_val:
            conditions.append(f"AND {base.lower().replace(' ', '_')} <= %s")
            params.append(max_val)

    def add_date_filter(base, conditions, params):
        add_range_filter(base, conditions, params)

    # --- UI ---
    tk.Label(win, text="All Entries Viewer", font=HEADER_FONT, bg="lavender").pack(fill=tk.X, pady=10)

    top_frame = tk.Frame(win, bg="white")
    top_frame.pack(pady=5)

    tk.Label(top_frame, text="Select Module:", font=LABEL_FONT).pack(side="left", padx=5)
    module_var = tk.StringVar()
    module_cb = ttk.Combobox(top_frame, textvariable=module_var, values=MODULES, state="readonly", width=30)
    module_cb.pack(side="left")
    module_cb.set(MODULES[0])

    tk.Button(top_frame, text="Show Results", command=show_results, bg="thistle").pack(side="left", padx=10)

    filter_frame = tk.Frame(win, bg="white")
    filter_frame.pack(pady=10, fill=tk.X, padx=10)

    fields = {}

    result_box = tk.Listbox(win, font=("Courier", 11), bg="white")
    result_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    module_cb.bind("<<ComboboxSelected>>", lambda e: create_filters(module_var.get()))
    create_filters(MODULES[0])
    show_results()