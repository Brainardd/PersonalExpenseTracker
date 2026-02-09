import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import json
from datetime import datetime
import matplotlib.pyplot as plt
from tkcalendar import DateEntry
import os

# ---------- File Setup ----------
FILENAME = "expenses.json"
if os.path.exists(FILENAME):
    with open(FILENAME, "r") as file:
        expenses = json.load(file)
else:
    expenses = []

# Ensure old entries have a date
for e in expenses:
    if "date" not in e:
        e["date"] = datetime.now().strftime("%Y-%m-%d")

# ---------- Functions ----------
def save_expenses():
    with open(FILENAME, "w") as file:
        json.dump(expenses, file, indent=4)

def add_or_update_expense():
    amount = amount_var.get()
    category = category_var.get()
    date_str = date_var.get()

    if not amount or not category or not date_str:
        messagebox.showerror("Input Error", "All fields are required")
        return
    try:
        amount_val = float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number")
        return

    if selected_index[0] is not None:
        expenses[selected_index[0]] = {"amount": amount_val, "category": category, "date": date_str}
        selected_index[0] = None
    else:
        expenses.append({"amount": amount_val, "category": category, "date": date_str})

    save_expenses()
    update_table()
    clear_fields()

def delete_expense():
    selected = treeview.selection()
    if not selected:
        return
    idx = int(treeview.item(selected[0])["values"][0]) - 1
    expenses.pop(idx)
    save_expenses()
    update_table()

def clear_all_expenses():
    if messagebox.askyesno("Confirm Reset", "Are you sure you want to clear all expenses?"):
        expenses.clear()
        save_expenses()
        update_table()
        clear_fields()

def edit_expense():
    selected = treeview.selection()
    if not selected:
        return
    idx = int(treeview.item(selected[0])["values"][0]) - 1
    exp = expenses[idx]
    amount_var.set(str(exp["amount"]))
    category_var.set(exp["category"])
    date_var.set(exp.get("date", datetime.now().strftime("%Y-%m-%d")))
    selected_index[0] = idx

def clear_fields():
    amount_var.set("")
    category_var.set("")
    date_var.set(datetime.now().strftime("%Y-%m-%d"))

def update_table():
    treeview.delete(*treeview.get_children())
    for i, e in enumerate(expenses):
        date_str = e.get("date", datetime.now().strftime("%Y-%m-%d"))
        treeview.insert("", "end", values=(i+1, e["category"], f"₱{e['amount']:.2f}", date_str))
    update_total()

def update_total():
    total = sum(e["amount"] for e in expenses)
    total_var.set(f"Total Spent: ₱{total:.2f}")

def show_statistics():
    if not expenses:
        messagebox.showinfo("No Data", "No expenses to show statistics.")
        return
    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]

    plt.figure(figsize=(6,6))
    plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=140)
    plt.title("Expenses by Category")
    plt.show()

# ---------- UI Setup ----------
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue") 

root = ctk.CTk()
root.title("Expense Tracker")
root.geometry("850x650")
root.minsize(800, 550)

# ---------- Top Frame (Inputs) ----------
top_frame = ctk.CTkFrame(root, corner_radius=12, fg_color="#f0f0f0")
top_frame.pack(padx=20, pady=15, fill="x")

amount_var = ctk.StringVar()
category_var = ctk.StringVar()
date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
selected_index = [None]

# Amount
ctk.CTkLabel(top_frame, text="Amount (₱)", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", padx=5, pady=(5,0))
ctk.CTkLabel(top_frame, text="Enter the expense amount", font=ctk.CTkFont(size=10)).grid(row=1, column=0, sticky="w", padx=5)
amount_entry = ctk.CTkEntry(top_frame, textvariable=amount_var)
amount_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

# Category
ctk.CTkLabel(top_frame, text="Category", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=1, sticky="w", padx=5, pady=(5,0))
ctk.CTkLabel(top_frame, text="Select the category", font=ctk.CTkFont(size=10)).grid(row=1, column=1, sticky="w", padx=5)
category_combo = ctk.CTkComboBox(top_frame, values=["Food","Transport","Bills","Shopping","Entertainment","Other"], variable=category_var)
category_combo.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Date Picker
ctk.CTkLabel(top_frame, text="Date", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=2, sticky="w", padx=5, pady=(5,0))
ctk.CTkLabel(top_frame, text="Pick the date", font=ctk.CTkFont(size=10)).grid(row=1, column=2, sticky="w", padx=5)
date_entry = DateEntry(
    top_frame,
    textvariable=date_var,
    date_pattern="yyyy-mm-dd",
    background='white',
    foreground='black',
    borderwidth=2,
    font=('Segoe UI', 11),
    showweeknumbers=False
)
date_entry.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

# Add Update Button
add_btn = ctk.CTkButton(top_frame, text="Add / Update Expense", command=add_or_update_expense, fg_color="#4caf50", hover_color="#45a049")
add_btn.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

top_frame.columnconfigure((0,1,2), weight=1)

# ---------- Middle Frame (Table) ----------
middle_frame = ctk.CTkFrame(root, corner_radius=12, fg_color="#f9f9f9")
middle_frame.pack(padx=20, pady=10, fill="both", expand=True)

columns = ("#", "Category", "Amount", "Date")
treeview = ttk.Treeview(middle_frame, columns=columns, show="headings")
for col in columns:
    treeview.heading(col, text=col)
    if col == "Category":
        treeview.column(col, width=200)
    elif col == "Amount":
        treeview.column(col, width=120)
    else:
        treeview.column(col, width=100, anchor="center")

# Alternate row colors
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", font=("Segoe UI", 12), rowheight=30, background="#ffffff", fieldbackground="#ffffff")
style.map('Treeview', background=[('selected', '#4a90e2')], foreground=[('selected', 'white')])

treeview.pack(side="left", fill="both", expand=True, padx=(0,0), pady=0)

scrollbar = ctk.CTkScrollbar(middle_frame, command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# ---------- Bottom Frame (Controls) ----------
bottom_frame = ctk.CTkFrame(root, corner_radius=12, fg_color="#f0f0f0")
bottom_frame.pack(padx=20, pady=10, fill="x")

ctk.CTkButton(bottom_frame, text="Edit Selected", command=edit_expense, fg_color="#2196f3", hover_color="#1976d2").pack(side="left", padx=8, pady=5)
ctk.CTkButton(bottom_frame, text="Delete Selected", command=delete_expense, fg_color="#f44336", hover_color="#d32f2f").pack(side="left", padx=8, pady=5)
ctk.CTkButton(bottom_frame, text="Clear All", command=clear_all_expenses, fg_color="#ff9800", hover_color="#fb8c00").pack(side="left", padx=8, pady=5)
ctk.CTkButton(bottom_frame, text="Show Statistics", command=show_statistics, fg_color="#9c27b0", hover_color="#7b1fa2").pack(side="left", padx=8, pady=5)

# ---------- Total Spent ----------
total_var = ctk.StringVar()
total_label = ctk.CTkLabel(root, textvariable=total_var, font=ctk.CTkFont(size=18, weight="bold"))
total_label.pack(pady=10)

# ---------- Initialize Table ----------
update_table()
root.mainloop()
