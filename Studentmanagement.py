# ---------------------------------------------------------
# PROJECT NAME : Student Management System (Tkinter)
# CREATED BY   : Minali Kaveesha Arandara
# DESCRIPTION  :
#     This program is a complete Student Management System
#     built using Python Tkinter. It includes:
#       - User Login & Registration
#       - Add / Update / Delete Students
#       - Automatic Student ID Generation
#       - Search Students by Name
#       - Summary Calculation (Count, Average, High, Low)
#       - Data stored safely in JSON files
#
# FILES USED :
#     marks.json  -> stores student marks & details
#     users.json  -> stores login usernames & passwords
#
# HOW IT WORKS :
#     - When the program starts, the login window appears.
#     - After login, the main student dashboard opens.
#     - All changes (add, update, delete) automatically
#       refresh the summary and save to JSON.
#
# ---------------------------------------------------------




import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

MARKS_FILE = "marks.json"
USERS_FILE = "users.json"

marks = []
users = {}

# ---------------------------------------------------------
# FILE LOAD / SAVE
# ---------------------------------------------------------
def save_marks():
    with open(MARKS_FILE, "w", encoding="utf-8") as f:
        json.dump(marks, f, indent=4)

def load_marks():
    global marks
    if os.path.exists(MARKS_FILE):
        try:
            with open(MARKS_FILE, "r", encoding="utf-8") as f:
                marks = json.load(f)
        except:
            marks = []
    else:
        marks = []

def save_users():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def load_users():
    global users
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
        except:
            users = {}
    else:
        users = {}

def ensure_default_user():
    load_users()
    if "admin" not in users:
        users["admin"] = "1234"
        save_users()

# ---------------------------------------------------------
# ID GENERATOR
# ---------------------------------------------------------
def generate_student_id():
    if not marks:
        return "STD001"
    nums = []
    for m in marks:
        sid = m.get("ID", "")
        if sid.startswith("STD"):
            try:
                nums.append(int(sid[3:]))
            except:
                pass
    next_num = max(nums) + 1 if nums else 1
    return f"STD{next_num:03d}"

# ---------------------------------------------------------
# ADD STUDENT FORM
# ---------------------------------------------------------
def add_student_from_form(parent, tree):
    form = tk.Toplevel(parent)
    form.title("Add Student")
    form.geometry("360x300")

    tk.Label(form, text="Add Student", font=("Arial", 14, "bold")).pack(pady=8)
    frame = tk.Frame(form)
    frame.pack(padx=10, pady=4)

    tk.Label(frame, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(frame, width=30)
    name_entry.grid(row=0, column=1)

    tk.Label(frame, text="Grade:").grid(row=1, column=0)
    grade_entry = tk.Entry(frame, width=30)
    grade_entry.grid(row=1, column=1)

    tk.Label(frame, text="Subject:").grid(row=2, column=0)
    subject_entry = tk.Entry(frame, width=30)
    subject_entry.grid(row=2, column=1)

    tk.Label(frame, text="Mark (0-100):").grid(row=3, column=0)
    mark_entry = tk.Entry(frame, width=30)
    mark_entry.grid(row=3, column=1)

    def do_add():
        name = name_entry.get().strip()
        grade = grade_entry.get().strip()
        subject = subject_entry.get().strip()
        mark_str = mark_entry.get().strip()

        if not name or not grade or not subject:
            messagebox.showerror("Error", "All fields required")
            return

        try:
            mark = int(mark_str)
            if not (0 <= mark <= 100):
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid mark")
            return

        sid = generate_student_id()
        student = {
            "ID": sid,
            "name": name,
            "grade": grade,
            "subject": subject,
            "mark": mark
        }

        marks.append(student)
        save_marks()
        tree.insert("", "end", iid=sid, values=(sid, name, grade, subject, mark))
        refresh_summary(parent)
        messagebox.showinfo("Success", f"Student added: {sid}")
        form.destroy()

    tk.Button(form, text="Save", command=do_add).pack(pady=8)

# ---------------------------------------------------------
# TREE VIEW
# ---------------------------------------------------------
def view_all_in_tree(window):
    cols = ("ID", "name", "grade", "subject", "mark")
    tree = ttk.Treeview(window, columns=cols, show="headings")

    for c in cols:
        tree.heading(c, text=c.upper())

    tree.column("ID", width=80, anchor="center")

    vsb = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    for m in marks:
        tree.insert("", "end", iid=m["ID"],
                    values=(m["ID"], m["name"], m["grade"], m["subject"], m["mark"]))

    return tree

# ---------------------------------------------------------
# UPDATE POPUP
# ---------------------------------------------------------
def update_popup(tree, parent):
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Select", "Please select a student row first")
        return

    sid = sel[0]
    rec = next((r for r in marks if r["ID"] == sid), None)
    if not rec:
        return

    win = tk.Toplevel(parent)
    win.title("Update Student")
    win.geometry("350x270")

    frm = tk.Frame(win)
    frm.pack(padx=10, pady=10)

    tk.Label(frm, text="Name:").grid(row=0, column=0)
    name_e = tk.Entry(frm, width=25)
    name_e.grid(row=0, column=1)
    name_e.insert(0, rec["name"])

    tk.Label(frm, text="Grade:").grid(row=1, column=0)
    grade_e = tk.Entry(frm, width=25)
    grade_e.grid(row=1, column=1)
    grade_e.insert(0, rec["grade"])

    tk.Label(frm, text="Subject:").grid(row=2, column=0)
    subj_e = tk.Entry(frm, width=25)
    subj_e.grid(row=2, column=1)
    subj_e.insert(0, rec["subject"])

    tk.Label(frm, text="Mark:").grid(row=3, column=0)
    mark_e = tk.Entry(frm, width=25)
    mark_e.grid(row=3, column=1)
    mark_e.insert(0, rec["mark"])

    def do_update():
        rec["name"] = name_e.get().strip()
        rec["grade"] = grade_e.get().strip()
        rec["subject"] = subj_e.get().strip()
        rec["mark"] = int(mark_e.get().strip())

        save_marks()
        refresh_tree(tree, parent)
        messagebox.showinfo("Updated", "Student updated successfully!")
        win.destroy()

    tk.Button(win, text="Update", command=do_update).pack(pady=12)

# ---------------------------------------------------------
# DELETE POPUP
# ---------------------------------------------------------
def delete_popup(tree, parent):
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Select", "Please select a student")
        return

    sid = sel[0]
    rec = next((r for r in marks if r["ID"] == sid), None)

    if not rec:
        return

    if not messagebox.askyesno("Confirm Delete", f"Delete student {rec['name']}?"):
        return

    marks.remove(rec)
    save_marks()
    refresh_tree(tree, parent)
    messagebox.showinfo("Deleted", "Student deleted successfully!")

# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------
def search_by_name_prompt(parent, tree):
    name = simpledialog.askstring("Search", "Enter name:")
    if not name:
        return

    name = name.lower()

    matches = [m["ID"] for m in marks if name in m["name"].lower()]

    if not matches:
        messagebox.showinfo("Search", "No results found")
        return

    tree.selection_set(matches)
    tree.see(matches[0])

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------
def refresh_summary(parent):
    count = len(marks)
    avg = round(sum(m["mark"] for m in marks) / count, 2) if count else 0
    mx = max(m["mark"] for m in marks) if count else 0
    mn = min(m["mark"] for m in marks) if count else 0

    parent.summary_count.config(text=f"Count: {count}")
    parent.summary_avg.config(text=f"Avg: {avg}")
    parent.summary_max.config(text=f"High: {mx}")
    parent.summary_min.config(text=f"Low: {mn}")

# ---------------------------------------------------------
# REFRESH TREE
# ---------------------------------------------------------
def refresh_tree(tree, parent):
    for i in tree.get_children():
        tree.delete(i)

    for m in marks:
        tree.insert("", "end", iid=m["ID"],
                    values=(m["ID"], m["name"], m["grade"], m["subject"], m["mark"]))

    refresh_summary(parent)

def main_app():
    root = tk.Tk()
    root.title("Student Management System")
    root.geometry("900x560")

    top = tk.Frame(root)
    top.pack(fill="x", padx=8, pady=6)

    table = tk.Frame(root)
    table.pack(expand=True, fill="both")

    bottom = tk.Frame(root)
    bottom.pack(fill="x", padx=8, pady=6)

    tree = view_all_in_tree(table)

    # --- FIXED BUTTONS (with correct parent: bottom) ---
    tk.Button(top, text="Add", command=lambda: add_student_from_form(bottom, tree)).pack(side="left", padx=5)
    tk.Button(top, text="Search", command=lambda: search_by_name_prompt(bottom, tree)).pack(side="left", padx=5)
    tk.Button(top, text="Update", command=lambda: update_popup(tree, bottom)).pack(side="left", padx=5)
    tk.Button(top, text="Delete", command=lambda: delete_popup(tree, bottom)).pack(side="left", padx=5)
    tk.Button(top, text="Refresh", command=lambda: refresh_tree(tree, bottom)).pack(side="left", padx=5)

    # --- SUMMARY LABELS ---
    bottom.summary_count = tk.Label(bottom, text="Count: 0")
    bottom.summary_count.pack(side="left", padx=10)

    bottom.summary_avg = tk.Label(bottom, text="Avg: 0")
    bottom.summary_avg.pack(side="left", padx=10)

    bottom.summary_max = tk.Label(bottom, text="High: 0")
    bottom.summary_max.pack(side="left", padx=10)

    bottom.summary_min = tk.Label(bottom, text="Low: 0")
    bottom.summary_min.pack(side="left", padx=10)

    # --- IMPORTANT: use bottom, not root ---
    refresh_summary(bottom)

    root.mainloop()

# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------
def register_window(parent):
    win = tk.Toplevel(parent)
    win.title("Register")
    win.geometry("320x200")

    frm = tk.Frame(win)
    frm.pack(padx=10, pady=8)

    tk.Label(frm, text="Username:").grid(row=0, column=0)
    u_entry = tk.Entry(frm)
    u_entry.grid(row=0, column=1)

    tk.Label(frm, text="Password:").grid(row=1, column=0)
    p_entry = tk.Entry(frm, show="*")
    p_entry.grid(row=1, column=1)

    def do_register():
        u = u_entry.get().strip()
        p = p_entry.get().strip()
        load_users()

        if u in users:
            messagebox.showerror("Error", "User exists")
            return

        users[u] = p
        save_users()
        messagebox.showinfo("Success", "User created")
        win.destroy()

    tk.Button(win, text="Register", command=do_register).pack(pady=8)

def login_window():
    load_users()
    ensure_default_user()

    win = tk.Tk()
    win.title("Login")
    win.geometry("350x250")

    frm = tk.Frame(win)
    frm.pack(padx=10, pady=10)

    tk.Label(frm, text="Username:").grid(row=0, column=0)
    user_e = tk.Entry(frm)
    user_e.grid(row=0, column=1)

    tk.Label(frm, text="Password:").grid(row=1, column=0)
    pass_e = tk.Entry(frm, show="*")
    pass_e.grid(row=1, column=1)

    def do_login():
        u = user_e.get().strip()
        p = pass_e.get().strip()
        load_users()

        if u in users and users[u] == p:
            messagebox.showinfo("Success", "Logged in")
            win.destroy()
            main_app()
        else:
            messagebox.showerror("Error", "Invalid login")

    tk.Button(win, text="Login", command=do_login).pack(pady=6)
    tk.Button(win, text="Register", command=lambda: register_window(win)).pack(pady=4)
    tk.Button(win, text="Quit", command=win.destroy).pack(pady=6)

    win.mainloop()

# ---------------------------------------------------------
# START APP
# ---------------------------------------------------------
if __name__ == "__main__":
    load_marks()
    ensure_default_user()
    login_window()

