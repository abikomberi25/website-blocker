# 🌐 Website Blocker

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![Database](https://img.shields.io/badge/Database-SQLite-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **Note:** This application modifies the Windows hosts file and must be run as **Administrator**.

A desktop productivity application built with Python that helps users stay focused by blocking distracting websites. It features a Tkinter-based graphical interface, a scheduled **Focus Mode**, and SQLite-based activity logging to record every block and unblock action.

---

## 📑 Table of Contents

* [Overview](#overview)
* [Project Motivation](#-project-motivation)
* [Features](#features)
* [Technologies Used](#technologies-used)
* [How It Works](#how-it-works)
* [Architecture](#architecture)
* [Database Design](#database-design)
* [Project Structure](#project-structure)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Utility Script](#utility-script)
* [Challenges Faced](#-challenges-faced)
* [Learning Outcomes](#-learning-outcomes)
* [Known Limitations](#known-limitations)
* [Future Improvements](#future-improvements)
* [Version History](#version-history)
* [Author](#author)
* [License](#license)

---

## Overview

Staying focused while working or studying often means manually avoiding distracting websites, which is easy to forget. This application automates the process by modifying the Windows hosts file to redirect selected websites to the local machine (`127.0.0.1`), making them inaccessible either manually or during a scheduled focus session.

---

## 🎯 Project Motivation

Maintaining concentration during study or work sessions is difficult due to easy access to social media, entertainment, and shopping websites.

This project was developed as a lightweight desktop application to help users improve productivity by temporarily blocking distracting websites manually or automatically through a scheduled Focus Mode.

---

## Features

| Feature                   | Description                                                 |
| ------------------------- | ----------------------------------------------------------- |
| 🔒 Manual Block / Unblock | Block or unblock websites instantly                         |
| ⏳ Focus Mode              | Automatically block websites during scheduled hours         |
| 🔁 Background Monitoring  | Continuously checks focus schedule without freezing the GUI |
| 🗃 SQLite Logging         | Records every block and unblock event                       |
| 📋 Recent Logs Viewer     | Displays the latest 50 actions                              |
| 🔄 Automatic DNS Flush    | Flushes DNS after every hosts file modification             |

---

## Technologies Used

* Python 3
* Tkinter
* SQLite3
* Threading
* Subprocess
* Datetime
* Windows Hosts File

---

## How It Works

1. User enters one or more website domains.
2. Clicking **Manual Block** adds entries to the Windows hosts file.
3. Clicking **Manual Unblock** removes those entries.
4. DNS cache is flushed so changes take effect immediately.
5. Every action is stored in the SQLite database.
6. Focus Mode automatically performs blocking and unblocking according to the configured schedule.

---

## Architecture

```text
                 User
                   │
                   ▼
             Tkinter GUI
                   │
                   ▼
          Application Logic
             │            │
             │            └────────► SQLite Database
             │
             └────────► Windows Hosts File
                              │
                              ▼
                         Flush DNS
                              │
                              ▼
                      Website Blocked
```

---

## Database Design

**Database:** `block_log.db`

**Table:** `actions`

| Column    | Description                |
| --------- | -------------------------- |
| id        | Auto Increment Primary Key |
| timestamp | Date and Time              |
| action    | BLOCK / UNBLOCK            |
| website   | Website Domain             |

The database is automatically created when the application is run for the first time.

---

## Project Structure

```text
website-blocker/
│
├── main.py
├── view_logs.py
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
└── assets/
```

---

## Requirements

* Python 3.10 or later
* Windows Operating System
* Administrator Privileges

---

## Installation

### Prerequisites

- Windows Operating System
- Python 3.10 or later
- Administrator privileges

### Clone the repository

```bash
git clone https://github.com/abikomberi25/website-blocker.git
cd website-blocker
```

### Run the application

```bash
python main.py
```

> **Important:** Run the application as **Administrator** because it modifies the Windows hosts file.

## Usage

### Manual Blocking
* Enter one or more website domains separated by commas.
* Click **Manual Block** or **Manual Unblock**.

### Focus Mode
* Enter Start Time and End Time in **HH:MM** (24-hour) format.
* Click **Start Focus Mode**.
* Websites are automatically blocked during the selected period and unblocked when it ends.

### View Logs
Click **Show Recent Logs** to display the latest 50 logged actions with timestamps.

---

## Utility Script

```bash
python view_logs.py
```

Prints all SQLite records directly in the terminal — useful for debugging or verifying that actions are being logged correctly, without opening the full GUI.

---

## 🚧 Challenges Faced

* Modifying the protected Windows hosts file safely without corrupting existing entries.
* Handling Administrator permission errors gracefully.
* Ensuring DNS changes apply immediately after hosts file edits.
* Maintaining GUI responsiveness while background threads run Focus Mode checks.
* Preventing duplicate entries when blocking the same site multiple times.

---

## 📚 Learning Outcomes

Through this project I gained practical experience with:

* Python GUI Development using Tkinter
* SQLite Database Integration
* Multithreading
* File Handling
* Windows Networking and DNS Cache Management
* Git and GitHub Version Control

---

## Known Limitations

* Windows only — hosts file path and DNS flush command are Windows-specific.
* Requires Administrator privileges to run.
* Focus Mode schedule is not saved — resets when the application is closed.
* All application logic is currently in a single file (`main.py`).
* Modern browsers using DNS-over-HTTPS (DoH) may bypass hosts file blocking.

---

## Future Improvements

### Version 1.1
* Screenshots and visual documentation
* Improved GUI design
* Better input validation

### Version 1.2
* Modular architecture
* Website categories / presets
* Search logs
* Configuration file support

### Version 2.0
* Analytics dashboard
* Dark mode
* Password protection
* Cross-platform support (macOS / Linux)
* User profiles

---

## Version History

### v1.0
* Manual website blocking and unblocking
* Scheduled Focus Mode
* SQLite activity logging
* Background scheduler
* Windows support

---

## Author

**Abhirami P C**  
B.Tech Information Technology  
PSG College of Technology

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.