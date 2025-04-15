Daily Life Tracker 📊

This is a personal daily life tracker/organizer I built using "Python's Tkinter" for the GUI and "MySQL" for the backend database.  
The idea is simple — to help keep track of different aspects of life like diary entries, expenses, sleep, and entertainment, and to be able to look back and gain some useful insights from them.

---

🔧 What it can do

- Create and manage multiple users
- Add, update, delete entries in:
  - 📖 Diary
  - 💰 Expenses
  - 🎬 Entertainment
  - 😴 Sleep
- View and filter entries by mood, tags, date range, amount, etc.
- Visual insights like:
  - Mood trends
  - Sleep quality patterns
  - Expense breakdowns by category
  - Entertainment status and ratings
- Simple interface that can be extended with new modules (like water tracker, goals, etc.)

---

💡 Why I built this

I wanted a single place where I could log my personal stuff — how I feel, how much I sleep, what I spend on, what I’m watching or reading — and then reflect on it later through charts and summaries.  
It’s part of my DBMS course, so I also made sure to apply database design concepts properly.

---

🧱 Tech used

- **Python** – Tkinter for GUI
- **MySQL** – Database backend
- **Matplotlib** – Charts and insights
- Other libraries – `datetime`, `mysql.connector`, `tkinter.messagebox`

---

📂 Database (basic structure)

- `users` – user_id, username
- `diary_entries` – mood, tags, text, date
- `expenses` – amount, category, date
- `entertainment_tracker` – title, category, status, rating
- `sleep_tracker` – hours, quality, date
- Lookup tables like `tags`, `expense_categories` etc. to keep it organized

---

🔍 Role of the database

1. Stores all entries per user in a structured format
2. Helps run CRUD operations (add/edit/delete entries)
3. Makes it easy to filter/search based on mood, category, date, etc.
4. Supports SQL queries to generate reports like:
   - Monthly expenses by category
   - Most common moods
   - Average sleep quality, etc.

---

▶️ Running it

1. Clone the project
2. Set up MySQL and run the schema file to create tables
3. Install requirements  
   `pip install mysql-connector-python matplotlib`
4. Start the GUI using:  
   `python login_gui.py`

---

🧑‍💻 About me
 
Part of my Course: CS2008 Database systems
Team Name : CraftHouse
Number of members : 1
Name : Anjana B Va
Roll no. : CS23B1098
