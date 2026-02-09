# 💸 Personal Expense Tracker (Executable Version)

A simple desktop **Expense Tracker** built with Python and Tkinter, packaged as a **standalone Windows executable (.exe)**.

No Python installation required to run the app.

---
<img width="594" height="598" alt="image" src="https://github.com/user-attachments/assets/d593fe71-e9c2-43c4-ba00-57edc71b48ef" />

## ✨ Features

- Add expenses with an **amount** and **category**
- Automatically saves expenses locally
- Displays all recorded expenses in a list
- Lightweight and beginner-friendly

---

## 📦 Running the Application (.EXE)

After building the project with PyInstaller, you will get:

```
dist/expense_tracker.exe
```

This file is the full application.

### ▶️ How to Run

1. Create a new folder anywhere on your computer  
   Example:
   ```
   Documents/ExpenseTracker
   ```

2. Copy **expense_tracker.exe** into that folder

3. Double-click **expense_tracker.exe**

The Expense Tracker window will open and you can start adding expenses.

---

## 💾 How Data Storage Works

The app automatically creates a file named:

```
expenses.json
```

This file stores all your saved expenses.

📌 It is created in the **same folder as the executable file**.

Your folder will look like this after using the app:

```
ExpenseTracker/
│
├── expense_tracker.exe
└── expenses.json
```

⚠️ Do not delete `expenses.json` if you want to keep your expense history.

---

## 🔁 Moving to Another Computer

To keep your data:

1. Copy both files:
   - `expense_tracker.exe`
   - `expenses.json`

2. Paste them into a folder on another computer  
3. Run the `.exe` — your expenses will still be there

---

## 🚫 Windows Security Warning

You might see:

> “Windows protected your PC”

This happens because the app is not digitally signed.

Click:
**More info → Run anyway**

This is normal for apps created with PyInstaller.

---

## 🛠 Troubleshooting

**App doesn't save data**
- Make sure the app is in a folder where you have write permission (Documents, Desktop, etc.)
- Do not run the app directly from inside a ZIP file

**Lost your data?**
- If `expenses.json` is deleted, previous expenses cannot be recovered.

---

## 🧠 Built With

- Python
- Tkinter (GUI)
- JSON (data storage)
- PyInstaller (to create executable)

---

## 📜 License

This project is open-source and free to use for learning purposes.
