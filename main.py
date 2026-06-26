import threading
import time
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import sqlite3
import subprocess


DB_FILE = "block_log.db"
print("Program Started")
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        action TEXT,
        website TEXT
    )
    """)
    conn.commit()
    conn.close()

def log_action(action, website):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO actions (timestamp, action, website) VALUES (?, ?, ?)",
                   (timestamp, action, website))
    conn.commit()
    conn.close()


def flush_dns():
    try:
        print("[DEBUG] Flushing DNS...")
        subprocess.run("ipconfig /flushdns", shell=True)
        print("✅ DNS cache flushed.")
    except Exception as e:
        print(f"❌ Failed to flush DNS: {e}")

window = Tk()
window.geometry("750x500")
window.resizable(False, False)
window.title("Website Blocker with Focus Mode and Logs")

heading = Label(
    window,
    text="Website Blocker",
    font=("Arial", 24, "bold")
)
heading.pack(pady=20)

label1 = Label(window, text='Enter Website(s) ', font='arial 13 bold')
label1.place(x=30, y=80)

enter_Website = Text(window, font='arial', height=2, width=50)
enter_Website.place(x=260, y=75)

label_start = Label(
    window,
    text="Focus Start Time (HH:MM)",
    font=("Arial",12)
)

label_start.place(x=30,y=150)

focus_start_entry = Entry(
    window,
    font=("Arial",12),
    width=12
)

focus_start_entry.place(x=240,y=150)


label_end = Label(
    window,
    text="Focus End Time (HH:MM)",
    font=("Arial",12)
)

label_end.place(x=390,y=150)

focus_end_entry = Entry(
    window,
    font=("Arial",12),
    width=12
)

focus_end_entry.place(x=590,y=150)

status_label = Label(window, text='', font='arial 12', fg='darkgreen')
status_label.place(x=120,y=380)
host_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect_ip = "127.0.0.1"

focus_mode_active = False
focus_times = {"start": None, "end": None}



def get_websites():
    raw = enter_Website.get(1.0, END).strip().split(",")
    sites = set()
    for site in raw:
        site = site.strip().lower()
        if site:
            sites.add(site)
            if not site.startswith("www."):
                sites.add("www." + site)
    return list(sites)

def parse_time(t_str):
    try:
        return datetime.strptime(t_str, "%H:%M").time()
    except ValueError:
        return None

def in_focus_period(now, start, end):
    if start < end:
        return start <= now <= end
    else:
        return now >= start or now <= end

def read_hosts():
    try:
        with open(host_path, 'r') as file:
            lines = file.readlines()
            print("[DEBUG] Hosts file read.")
            return lines
    except PermissionError:
        print("❌ Permission denied to read hosts file.")
        status_label.config(text="❌ Permission denied to read hosts file.")
        return []

def write_hosts(lines):
    try:
        with open(host_path, 'w') as file:
            file.writelines(lines)
        print("[DEBUG] Hosts file written.")
    except PermissionError:
        print("❌ Permission denied to write hosts file.")
        status_label.config(text="❌ Permission denied to write hosts file.")

def block_websites(websites):
    lines = read_hosts()
    if not lines:
        return

    block_entries = [f"{redirect_ip} {site}\n" for site in websites]
    new_entries = [entry for entry in block_entries if entry not in lines]

    if new_entries:
        lines.extend(new_entries)
        write_hosts(lines)
        flush_dns()
        for site in websites:
            log_action("BLOCK", site)
        print(f"[BLOCK] Blocked: {', '.join(websites)}")
    else:
        print(f"[BLOCK] Already blocked: {', '.join(websites)}")

def unblock_websites(websites):
    lines = read_hosts()
    if not lines:
        return

    entries_to_remove = [f"{redirect_ip} {site}" for site in websites]
    new_lines = [line for line in lines if not any(site in line for site in entries_to_remove)]

    if len(new_lines) != len(lines):
        write_hosts(new_lines)
        flush_dns()
        for site in websites:
            log_action("UNBLOCK", site)
        print(f"[UNBLOCK] Unblocked: {', '.join(websites)}")
    else:
        print(f"[UNBLOCK] Nothing to unblock for: {', '.join(websites)}")



def start_focus_mode():
    start = parse_time(focus_start_entry.get().strip())
    end = parse_time(focus_end_entry.get().strip())

    if start is None or end is None:
        status_label.config(text="❌ Invalid time format. Use HH:MM.")
        return

    focus_times["start"] = start
    focus_times["end"] = end

    status_label.config(text=f"⏳ Focus Mode: {start.strftime('%H:%M')} - {end.strftime('%H:%M')}")

    now = datetime.now().time()
    if in_focus_period(now, start, end):
        websites = get_websites()
        if websites:
            block_websites(websites)
            global focus_mode_active
            focus_mode_active = True
            status_label.config(text="🔒 Focus Mode ON: Websites blocked")

def focus_mode_loop():
    global focus_mode_active
    while True:
        websites = get_websites()
        if not websites:
            time.sleep(3)
            continue

        now = datetime.now().time()
        start = focus_times.get("start")
        end = focus_times.get("end")

        if start is None or end is None:
            time.sleep(3)
            continue

        if in_focus_period(now, start, end):
            if not focus_mode_active:
                block_websites(websites)
                focus_mode_active = True
                status_label.config(text="🔒 Focus Mode ON: Websites blocked")
        else:
            if focus_mode_active:
                unblock_websites(websites)
                focus_mode_active = False
                status_label.config(text="🔓 Focus Mode OFF: Websites unblocked")

        time.sleep(3)



def manual_block():
    websites = get_websites()
    if not websites:
        status_label.config(text="⚠️ Please enter websites.")
        return
    block_websites(websites)
    status_label.config(text=f"✅ Blocked: {', '.join(websites)}")

def manual_unblock():
    websites = get_websites()
    if not websites:
        status_label.config(text="⚠️ Please enter websites.")
        return
    unblock_websites(websites)
    status_label.config(text=f"✅ Unblocked: {', '.join(websites)}")

def show_logs():
    log_win = Toplevel(window)
    log_win.title("Recent Block/Unblock Logs")
    log_win.geometry("600x400")

    scrollbar = Scrollbar(log_win)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(log_win, width=80, height=20, yscrollcommand=scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, action, website FROM actions ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        listbox.insert(END, "No logs found.")
    else:
        for row in rows:
            ts, act, web = row
            listbox.insert(END, f"{ts} | {act} | {web}")

    scrollbar.config(command=listbox.yview)



block_button = Button(window, text='Manual Block', font='arial', pady=5, command=manual_block,
                      width=15, bg='royal blue1', activebackground='grey')
block_button.place(x=120,y=220)

unblock_button = Button(window, text='Manual Unblock', font='arial', pady=5, command=manual_unblock,
                        width=15, bg='royal blue1', activebackground='grey')
unblock_button.place(x=400,y=220)

start_button = Button(window, text='Start Focus Mode', font='arial', pady=5, command=start_focus_mode,
                      width=20, bg='orange', activebackground='grey')
start_button.place(x=235,y=290)

logs_button = Button(window, text='Show Recent Logs', font='arial', pady=5, command=show_logs,
                     width=20, bg='sea green', fg='white', activebackground='grey')
logs_button.place(x=235,y=440)
init_db()
focus_thread = threading.Thread(target=focus_mode_loop, daemon=True)
focus_thread.start()
print("Opening GUI...")
window.mainloop()