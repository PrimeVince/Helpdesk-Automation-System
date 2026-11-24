import json
from datetime import datetime
from pathlib import Path
from helpdesk.database import get_connection
from helpdesk.logger import get_logger

logger = get_logger()


def generate_ticket_summary():
    with get_connection() as connection:

        total = connection.execute(
            "SELECT COUNT(*) FROM tickets"
        ).fetchone()[0]

        status_summary = connection.execute(
            """
            SELECT status, COUNT(*)
            FROM tickets
            GROUP BY status
            """
        ).fetchall()

        priority_summary = connection.execute(
            """
            SELECT priority, COUNT(*)
            FROM tickets
            GROUP BY priority
            """
        ).fetchall()

        category_summary = connection.execute(
            """
            SELECT category, COUNT(*)
            FROM tickets
            GROUP BY category
            """
        ).fetchall()

        unresolved = connection.execute(
            """
            SELECT COUNT(*)
            FROM tickets
            WHERE status IN ('Open', 'In Progress')
            """
        ).fetchone()[0]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_tickets": total,
        "unresolved_tickets": unresolved,
        "by_status": dict(status_summary),
        "by_priority": dict(priority_summary),
        "by_category": dict(category_summary)
    }

def export_ticket_summary(output_directory=None):
    try:
        summary = generate_ticket_summary()

        if output_directory is None:
            reports_directory = Path(__file__).parent.parent / "reports"
        else:
            reports_directory = Path(output_directory)

        reports_directory.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        report_path = (
            reports_directory / f"ticket_summary_{timestamp}.json"
        )

        with open(report_path, "w", encoding="utf-8") as report_file:
            json.dump(summary, report_file, indent=4)

        logger.info(
            "Ticket summary report generated: %s",
            report_path
        )

        return report_path

    except Exception:
        logger.exception("Failed to generate ticket summary report")
        raise