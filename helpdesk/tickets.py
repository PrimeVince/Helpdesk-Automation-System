
from helpdesk.database import get_connection
from helpdesk.logger import get_logger

logger = get_logger()

def validate_text(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be completed.")

    return value.strip()

def create_ticket(user_name, department, issue, category, priority):
    user_name = validate_text(user_name, "User name")
    department = validate_text(department, "Department")
    issue = validate_text(issue, "Issue")
    category = validate_text(category, "Category")
    priority = validate_text(priority, "Priority")

    valid_priorities = ["Low", "Medium", "High", "Critical"]
    valid_categories = [
        "Hardware",
        "Software",
        "Network",
        "Account & Access",
        "Other"
    ]

    if category not in valid_categories:
        raise ValueError(
            f"Invalid category. Choose from: {', '.join(valid_categories)}"
        )

    if priority not in valid_priorities:
        raise ValueError(
            f"Invalid priority. Choose from: {', '.join(valid_priorities)}"
        )

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tickets (
                user_name, department, issue, category, priority
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_name, department, issue, category, priority)
        )

        ticket_id = cursor.lastrowid

    logger.info(
        "Ticket created: ID=%s, User=%s, Priority=%s",
        ticket_id,
        user_name,
        priority
    )

    return ticket_id



def get_ticket(ticket_id):
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT * FROM tickets WHERE ticket_id = ?",
            (ticket_id,)
        )

        return cursor.fetchone()


def get_all_tickets():
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT * FROM tickets ORDER BY created_at DESC"
        )

        return cursor.fetchall()


def update_ticket_status(ticket_id, new_status):
    new_status = validate_text(new_status, "Status")

    valid_statuses = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    if new_status not in valid_statuses:
        raise ValueError(
            f"Invalid status. Choose from: {', '.join(valid_statuses)}"
        )

    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE tickets
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE ticket_id = ?
            """,
            (new_status, ticket_id)
        )

        success = cursor.rowcount > 0

    if success:
        logger.info(
            "Ticket status updated: ID=%s, New Status=%s",
            ticket_id,
            new_status
        )

    return success


def delete_ticket(ticket_id):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM tickets WHERE ticket_id = ?",
            (ticket_id,)
        )

        success = cursor.rowcount > 0

        if success:
            logger.warning(
                "Ticket deleted: ID=%s",
                ticket_id
            )

        return success


def filter_tickets(status=None, priority=None):
    query = "SELECT * FROM tickets WHERE 1=1"
    parameters = []

    if status:
        query += " AND status = ?"
        parameters.append(status)

    if priority:
        query += " AND priority = ?"
        parameters.append(priority)

    query += " ORDER BY created_at DESC"

    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return cursor.fetchall()

def search_tickets(search_term):
    search_term = validate_text(search_term, "Search term")

    search_pattern = f"%{search_term}%"

    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT * FROM tickets
            WHERE user_name LIKE ?
               OR department LIKE ?
               OR issue LIKE ?
               OR category LIKE ?
            ORDER BY created_at DESC
            """,
            (
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern
            )
        )

        return cursor.fetchall()
