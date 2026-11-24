# Helpdesk Automation System

A Python-based command-line helpdesk application designed to manage IT support tickets, track issues, and generate service reports using SQLite.

## Features

- **Ticket Management:** Create, view, update, and delete support tickets.
- **Priority Management:** Assign Low, Medium, High, or Critical priorities.
- **Status Tracking:** Track tickets through Open, In Progress, Resolved, and Closed statuses.
- **Ticket Categorization:** Classify issues as Hardware, Software, Network, Account & Access, or Other.
- **Search and Filtering:** Find tickets using keywords and filter by status or priority.
- **Database Persistence:** Store ticket records in an SQLite database.
- **Automated Reporting:** Generate and export ticket summaries in JSON format.
- **Logging and Error Handling:** Record application activities and errors for troubleshooting.
- **Automated Testing:** Includes unit tests for core ticket management and reporting functionality.

## Technologies Used

- Python
- SQLite
- JSON
- Python Standard Library
- `unittest` for automated testing

## Project Structure

```text
Helpdesk-Automation-System/
│
├── helpdesk/
│   ├── __init__.py
│   ├── database.py
│   ├── logger.py
│   ├── reports.py
│   └── tickets.py
│
├── tests/
│   ├── __init__.py
│   └── test_tickets.py
│
├── data/
├── logs/
├── reports/
│
├── main.py
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10 or later
- Windows, Linux, or macOS

No external Python packages are required.

## Installation and Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/PrimeVince/Helpdesk-Automation-System.git
   ```

2. Navigate into the project directory:

   ```bash
   cd Helpdesk-Automation-System
   ```

3. Run the application:

   ```bash
   python main.py
   ```

4. Follow the command-line menu to manage helpdesk