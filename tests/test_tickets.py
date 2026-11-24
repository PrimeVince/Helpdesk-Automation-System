import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from helpdesk.database import initialize_database

class TestTicketSystem(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()

        self.test_database = (
            Path(self.temp_directory.name) / "test_helpdesk.db"
        )

        self.database_patcher = patch(
            "helpdesk.database.DATABASE_PATH",
            self.test_database
        )

        self.database_patcher.start()
        initialize_database()

    def tearDown(self):
        self.database_patcher.stop()
        self.temp_directory.cleanup()

    def test_create_ticket(self):
        from helpdesk.tickets import create_ticket, get_ticket

        ticket_id = create_ticket(
            "Test User",
            "IT",
            "Cannot connect to network",
            "Network",
            "High"
        )

        ticket = get_ticket(ticket_id)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket[1], "Test User")
        self.assertEqual(ticket[2], "IT")
        self.assertEqual(ticket[3], "Cannot connect to network")
        self.assertEqual(ticket[5], "High")
        self.assertEqual(ticket[6], "Open")

    def test_create_ticket_rejects_empty_fields(self):
        from helpdesk.tickets import create_ticket

        with self.assertRaises(ValueError):
            create_ticket(
                "",
                "IT",
                "Cannot connect to network",
                "Network",
                "High"
            )

    def test_create_ticket_rejects_invalid_priority(self):
        from helpdesk.tickets import create_ticket

        with self.assertRaises(ValueError):
            create_ticket(
                "Test User",
                "IT",
                "Cannot connect to network",
                "Network",
                "Urgent"
            )

    def test_get_ticket(self):
        from helpdesk.tickets import create_ticket, get_ticket

        ticket_id = create_ticket(
            "Jane Doe",
            "Finance",
            "Printer not working",
            "Hardware",
            "Medium"
        )

        ticket = get_ticket(ticket_id)

        self.assertIsNotNone(ticket)
        self.assertEqual(ticket[0], ticket_id)
        self.assertEqual(ticket[1], "Jane Doe")

    def test_get_nonexistent_ticket(self):
        from helpdesk.tickets import get_ticket

        ticket = get_ticket(9999)

        self.assertIsNone(ticket)

    def test_update_ticket_status(self):
        from helpdesk.tickets import (
            create_ticket,
            get_ticket,
            update_ticket_status
        )

        ticket_id = create_ticket(
            "John Doe",
            "IT",
            "Network unavailable",
            "Network",
            "High"
        )

        result = update_ticket_status(ticket_id, "In Progress")

        ticket = get_ticket(ticket_id)

        self.assertTrue(result)
        self.assertEqual(ticket[6], "In Progress")

    def test_update_nonexistent_ticket(self):
        from helpdesk.tickets import update_ticket_status

        result = update_ticket_status(9999, "Resolved")

        self.assertFalse(result)

    def test_delete_ticket(self):
        from helpdesk.tickets import (
            create_ticket,
            get_ticket,
            delete_ticket
        )

        ticket_id = create_ticket(
            "Test User",
            "IT",
            "Temporary test issue",
            "Other",
            "Low"
        )

        result = delete_ticket(ticket_id)
        ticket = get_ticket(ticket_id)

        self.assertTrue(result)
        self.assertIsNone(ticket)

    def test_delete_nonexistent_ticket(self):
        from helpdesk.tickets import delete_ticket

        result = delete_ticket(9999)

        self.assertFalse(result)

    def test_filter_tickets_by_status(self):
        from helpdesk.tickets import create_ticket, filter_tickets

        create_ticket("Alice", "HR", "Issue A", "Software", "Low")
        ticket_id = create_ticket(
            "Bob", "IT", "Issue B", "Network", "High"
        )

        from helpdesk.tickets import update_ticket_status
        update_ticket_status(ticket_id, "In Progress")

        results = filter_tickets(status="In Progress")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Bob")

    def test_filter_tickets_by_priority(self):
        from helpdesk.tickets import create_ticket, filter_tickets

        create_ticket("Alice", "HR", "Issue A", "Software", "Low")
        create_ticket("Bob", "IT", "Issue B", "Network", "Critical")

        results = filter_tickets(priority="Critical")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Bob")
    def test_search_tickets_by_user(self):
        from helpdesk.tickets import create_ticket, search_tickets

        create_ticket(
            "Vincent",
            "IT",
            "Network unavailable",
            "Network",
            "High"
        )

        results = search_tickets("Vincent")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Vincent")

    def test_search_tickets_by_issue(self):
        from helpdesk.tickets import create_ticket, search_tickets

        create_ticket(
            "Jane",
            "Finance",
            "Printer not responding",
            "Hardware",
            "Medium"
        )

        results = search_tickets("Printer")

        self.assertEqual(len(results), 1)
        self.assertIn("Printer", results[0][3])
    def test_generate_ticket_summary(self):
        from helpdesk.tickets import create_ticket, update_ticket_status
        from helpdesk.reports import generate_ticket_summary

        ticket_one = create_ticket(
            "Alice", "HR", "Software issue", "Software", "High"
        )

        ticket_two = create_ticket(
            "Bob", "IT", "Network issue", "Network", "Critical"
        )

        update_ticket_status(ticket_two, "Resolved")

        summary = generate_ticket_summary()

        self.assertEqual(summary["total_tickets"], 2)
        self.assertEqual(summary["unresolved_tickets"], 1)
        self.assertEqual(summary["by_status"]["Open"], 1)
        self.assertEqual(summary["by_status"]["Resolved"], 1)
        self.assertEqual(summary["by_priority"]["High"], 1)
        self.assertEqual(summary["by_category"]["Network"], 1)

    def test_export_ticket_summary(self):
        import json
        from helpdesk.tickets import create_ticket
        from helpdesk.reports import export_ticket_summary

        create_ticket(
            "Test User",
            "IT",
            "Network issue",
            "Network",
            "High"
        )

        report_directory = Path(self.temp_directory.name) / "reports"

        report_path = export_ticket_summary(report_directory)

        self.assertTrue(report_path.exists())

        with open(report_path, "r", encoding="utf-8") as report_file:
            report_data = json.load(report_file)

        self.assertEqual(report_data["total_tickets"], 1)
        self.assertEqual(report_data["unresolved_tickets"], 1)
        self.assertEqual(report_data["by_priority"]["High"], 1)

    def test_create_ticket_rejects_none_username(self):
        from helpdesk.tickets import create_ticket

        with self.assertRaises(ValueError):
            create_ticket(
                None,
                "IT",
                "Network issue",
                "Network",
                "High"
            )

    def test_update_ticket_rejects_empty_status(self):
        from helpdesk.tickets import update_ticket_status

        with self.assertRaises(ValueError):
            update_ticket_status(1, "")

    def test_search_tickets_rejects_empty_search(self):
        from helpdesk.tickets import search_tickets

        with self.assertRaises(ValueError):
            search_tickets("   ")