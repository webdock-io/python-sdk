import os
import unittest
from dotenv import load_dotenv
from typing import TYPE_CHECKING
from webdock import Webdock

load_dotenv()


class TestEvents(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.client = Webdock(os.getenv("TOKEN"))

    def test_1_list_events_default(self):
        """Test 1: List events with default parameters"""
        events = self.client.events.list()
        self.assertIsInstance(events.get("body"), list, "Events list should be of type list")
        if events.get("body"):
            event = events.get("body")[0]
            self.assertIn("id", event, "Event should have id field")
            self.assertIn("eventType", event, "Event should have eventType field")
            self.assertIn("status", event, "Event should have status field")

    def test_2_list_events_with_pagination(self):
        """Test 2: List events with pagination parameters"""
        events = self.client.events.list(page=1, limit=5)
        self.assertIsInstance(events.get("body"), list, "Events list should be of type list")
        self.assertLessEqual(len(events.get("body")), 5, "Should return at most 5 events")

    def test_3_list_events_with_type_filter(self):
        """Test 3: List events with type filter"""
        events = self.client.events.list(type="provision")
        self.assertIsInstance(events.get("body"), list, "Events list should be of type list")
        if events.get("body"):
            for event in events.get("body"):
                self.assertEqual(event.get("eventType"), "provision", "All events should be of type provision")

    def test_4_list_events_with_all_parameters(self):
        """Test 4: List events with all parameters"""
        events = self.client.events.list(page=1, limit=3, type="backup")
        self.assertIsInstance(events.get("body"), list, "Events list should be of type list")
        self.assertLessEqual(len(events.get("body")), 3, "Should return at most 3 events")
        if events.get("body"):
            for event in events.get("body"):
                self.assertEqual(event.get("eventType"), "backup", "All events should be of type backup")

    def test_5_events_data_structure(self):
        """Test 5: Events data structure validation"""
        events = self.client.events.list()
        self.assertIsInstance(events.get("body"), list, "Events list should be of type list")
        
        if events.get("body"):
            event = events.get("body")[0]
            # Check required fields exist
            self.assertIn("id", event, "Event should have id field")
            self.assertIn("startTime", event, "Event should have startTime field")
            self.assertIn("callbackId", event, "Event should have callbackId field")
            self.assertIn("serverSlug", event, "Event should have serverSlug field")
            self.assertIn("eventType", event, "Event should have eventType field")
            self.assertIn("action", event, "Event should have action field")
            self.assertIn("actionData", event, "Event should have actionData field")
            self.assertIn("message", event, "Event should have message field")
            self.assertIn("status", event, "Event should have status field")

    def test_6_events_data_types(self):
        """Test 6: Events data types validation"""
        events = self.client.events.list()
        self.assertIsInstance(events.get("body"), list, "Events list should be of type list")
        
        if events.get("body"):
            event = events.get("body")[0]
            # Check data types
            self.assertIsInstance(event.get("id"), int, "id should be an integer")
            self.assertIsInstance(event.get("startTime"), str, "startTime should be a string")
            self.assertIsInstance(event.get("callbackId"), str, "callbackId should be a string")
            self.assertIsInstance(event.get("serverSlug"), str, "serverSlug should be a string")
            self.assertIsInstance(event.get("eventType"), str, "eventType should be a string")
            self.assertIsInstance(event.get("action"), str, "action should be a string")
            self.assertIsInstance(event.get("actionData"), str, "actionData should be a string")
            self.assertIsInstance(event.get("message"), str, "message should be a string")
            self.assertIsInstance(event.get("status"), str, "status should be a string")

    def test_7_events_status_values(self):
        """Test 7: Events status values validation"""
        events = self.client.events.list()
        self.assertIsInstance(events.get("body"), list, "Events list should be of type list")
        
        valid_statuses = ["waiting", "working", "finished", "error"]
        for event in events.get("body"):
            self.assertIn(event.get("status"), valid_statuses, 
                         f"Event status should be one of {valid_statuses}")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestEvents.test_1_list_events_default)
    suite.addTest(TestEvents.test_2_list_events_with_pagination)
    suite.addTest(TestEvents.test_3_list_events_with_type_filter)
    suite.addTest(TestEvents.test_4_list_events_with_all_parameters)
    suite.addTest(TestEvents.test_5_events_data_structure)
    suite.addTest(TestEvents.test_6_events_data_types)
    suite.addTest(TestEvents.test_7_events_status_values)

    runner = unittest.TextTestRunner(verbosity=2, stream=True)
    runner.run(suite)
