
from helpdesk.database import initialize_database
from helpdesk.tickets import (
    create_ticket,
    get_all_tickets,
    get_ticket,
    update_ticket_status,
    delete_ticket,
    search_tickets,
    filter_tickets
)
from helpdesk.reports import export_ticket_summary
from helpdesk.logger import get_logger

logger = get_logger()


def display_menu():
    print("\n" + "=" * 40)
    print("       HELPDESK AUTOMATION SYSTEM")
    print("=" * 40)
    print("1. Create a ticket")
    print("2. View all tickets")
    print("3. View a ticket")
    print("4. Update ticket status")
    print("5. Delete a ticket")
    print("6. Search tickets")
    print("7. Filter tickets")
    print("8. Generate reports")
    print("0. Exit")
    print("=" * 40)


def create_ticket_menu():
    print("\n--- CREATE NEW TICKET ---")

    user_name = input("User name: ")
    department = input("Department: ")
    issue = input("Describe the issue: ")
    category = input("Category: ")
    priority = input("Priority: ")

    try:
        ticket_id = create_ticket(
            user_name, department, issue, category, priority
        )
        print(f"\nTicket created successfully! Ticket ID: {ticket_id}")
    except ValueError as error:
        print(f"\nTicket creation failed: {error}")


def view_all_tickets_menu():
    print("\n--- ALL SUPPORT TICKETS ---")

    tickets = get_all_tickets()

    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print("-" * 50)
        print(f"Ticket ID:  {ticket[0]}")
        print(f"User:       {ticket[1]}")
        print(f"Department: {ticket[2]}")
        print(f"Issue:      {ticket[3]}")
        print(f"Category:   {ticket[4]}")
        print(f"Priority:   {ticket[5]}")
        print(f"Status:     {ticket[6]}")
        print(f"Created:    {ticket[7]}")
        print(f"Updated:    {ticket[8]}")

    print("-" * 50)
    print(f"Total tickets: {len(tickets)}")


def view_ticket_menu():
    print("\n--- VIEW SINGLE TICKET ---")

    try:
        ticket_id = int(input("Enter ticket ID: "))
        ticket = get_ticket(ticket_id)

        if ticket is None:
            print(f"No ticket found with ID {ticket_id}.")
            return

        print("\n" + "-" * 50)
        print(f"Ticket ID:  {ticket[0]}")
        print(f"User:       {ticket[1]}")
        print(f"Department: {ticket[2]}")
        print(f"Issue:      {ticket[3]}")
        print(f"Category:   {ticket[4]}")
        print(f"Priority:   {ticket[5]}")
        print(f"Status:     {ticket[6]}")
        print(f"Created:    {ticket[7]}")
        print(f"Updated:    {ticket[8]}")
        print("-" * 50)

    except ValueError:
        print("Invalid input. Please enter a numeric ticket ID.")


def update_ticket_menu():
    print("\n--- UPDATE TICKET STATUS ---")

    try:
        ticket_id = int(input("Enter ticket ID: "))
        ticket = get_ticket(ticket_id)

        if ticket is None:
            print(f"No ticket found with ID {ticket_id}.")
            return

        print(f"\nCurrent status: {ticket[6]}")
        print("\nAvailable statuses:")
        print("1. Open")
        print("2. In Progress")
        print("3. Resolved")
        print("4. Closed")

        status_options = {
            "1": "Open",
            "2": "In Progress",
            "3": "Resolved",
            "4": "Closed"
        }

        choice = input("\nSelect new status: ").strip()

        if choice not in status_options:
            print("Invalid status selection.")
            return

        new_status = status_options[choice]
        success = update_ticket_status(ticket_id, new_status)

        if success:
            print(f"\nTicket {ticket_id} updated to: {new_status}")
        else:
            print("Ticket status could not be updated.")

    except ValueError:
        print("Invalid input. Please enter a numeric ticket ID.")


def delete_ticket_menu():
    print("\n--- DELETE TICKET ---")

    try:
        ticket_id = int(input("Enter ticket ID: "))
        ticket = get_ticket(ticket_id)

        if ticket is None:
            print(f"No ticket found with ID {ticket_id}.")
            return

        print(f"\nTicket ID: {ticket[0]}")
        print(f"User: {ticket[1]}")
        print(f"Issue: {ticket[3]}")
        print(f"Status: {ticket[6]}")

        confirmation = input(
            "\nAre you sure you want to delete this ticket? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print("Deletion cancelled.")
            return

        if delete_ticket(ticket_id):
            print(f"Ticket {ticket_id} deleted successfully.")
        else:
            print("Ticket could not be deleted.")

    except ValueError:
        print("Invalid input. Please enter a numeric ticket ID.")


def search_tickets_menu():
    print("\n--- SEARCH TICKETS ---")

    search_term = input(
        "Enter name, department, issue, or category: "
    ).strip()

    if not search_term:
        print("Search term cannot be empty.")
        return

    tickets = search_tickets(search_term)

    if not tickets:
        print("No matching tickets found.")
        return

    print(f"\nFound {len(tickets)} matching ticket(s).")

    for ticket in tickets:
        print("-" * 50)
        print(f"Ticket ID:  {ticket[0]}")
        print(f"User:       {ticket[1]}")
        print(f"Department: {ticket[2]}")
        print(f"Issue:      {ticket[3]}")
        print(f"Category:   {ticket[4]}")
        print(f"Priority:   {ticket[5]}")
        print(f"Status:     {ticket[6]}")

    print("-" * 50)


def filter_tickets_menu():
    print("\n--- FILTER TICKETS ---")

    print("\nFilter by status:")
    print("1. Open")
    print("2. In Progress")
    print("3. Resolved")
    print("4. Closed")
    print("5. Any status")

    status_options = {
        "1": "Open",
        "2": "In Progress",
        "3": "Resolved",
        "4": "Closed",
        "5": None
    }

    status_choice = input("Select status: ").strip()

    if status_choice not in status_options:
        print("Invalid status selection.")
        return

    status = status_options[status_choice]

    print("\nFilter by priority:")
    print("1. Low")
    print("2. Medium")
    print("3. High")
    print("4. Critical")
    print("5. Any priority")

    priority_options = {
        "1": "Low",
        "2": "Medium",
        "3": "High",
        "4": "Critical",
        "5": None
    }

    priority_choice = input("Select priority: ").strip()

    if priority_choice not in priority_options:
        print("Invalid priority selection.")
        return

    priority = priority_options[priority_choice]
    tickets = filter_tickets(status, priority)

    if not tickets:
        print("\nNo matching tickets found.")
        return

    print(f"\nFound {len(tickets)} matching ticket(s).")

    for ticket in tickets:
        print("-" * 50)
        print(f"Ticket ID:  {ticket[0]}")
        print(f"User:       {ticket[1]}")
        print(f"Issue:      {ticket[3]}")
        print(f"Priority:   {ticket[5]}")
        print(f"Status:     {ticket[6]}")

    print("-" * 50)


def generate_reports_menu():
    print("\n--- GENERATE HELPDESK REPORT ---")

    try:
        report_path = export_ticket_summary()
        print("\nReport generated successfully!")
        print(f"Saved to: {report_path}")
    except Exception as error:
        print(f"Report generation failed: {error}")


def main():
    initialize_database()

    while True:
        display_menu()
        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                create_ticket_menu()
            elif choice == "2":
                view_all_tickets_menu()
            elif choice == "3":
                view_ticket_menu()
            elif choice == "4":
                update_ticket_menu()
            elif choice == "5":
                delete_ticket_menu()
            elif choice == "6":
                search_tickets_menu()
            elif choice == "7":
                filter_tickets_menu()
            elif choice == "8":
                generate_reports_menu()
            elif choice == "0":
                print("Exiting Helpdesk Automation System.")
                break
            else:
                print("Invalid selection. Please choose a valid option.")

        except Exception:
            logger.exception(
                "Unexpected error while processing menu option: %s",
                choice
            )
            print(
                "\nAn unexpected error occurred. "
                "The error has been logged. Please try again."
            )


if __name__ == "__main__":
    main()
