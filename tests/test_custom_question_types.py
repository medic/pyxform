"""
Test custom question types specific to CHT.
"""
import unittest
from pyxform.builder import create_survey_element_from_dict


class CustomQuestionTypesTest(unittest.TestCase):
    """Test custom question types specific to CHT."""

    def test_db_person_type(self):
        """Test that db:person type is properly handled."""
        element = create_survey_element_from_dict({
            "type": "db:person",
            "name": "person",
            "label": "Select a person"
        })
        self.assertEqual(element.bind.get("type"), "db:person")

    def test_db_clinic_type(self):
        """Test that db:clinic type is properly handled."""
        element = create_survey_element_from_dict({
            "type": "db:clinic",
            "name": "clinic",
            "label": "Select a clinic"
        })
        self.assertEqual(element.bind.get("type"), "db:clinic")

    def test_db_health_center_type(self):
        """Test that db:health_center type is properly handled."""
        element = create_survey_element_from_dict({
            "type": "db:health_center",
            "name": "health_center",
            "label": "Select a health center"
        })
        self.assertEqual(element.bind.get("type"), "db:health_center")

    def test_db_district_hospital_type(self):
        """Test that db:district_hospital type is properly handled."""
        element = create_survey_element_from_dict({
            "type": "db:district_hospital",
            "name": "district_hospital",
            "label": "Select a district hospital"
        })
        self.assertEqual(element.bind.get("type"), "db:district_hospital")

    def test_tel_type(self):
        """Test that tel type is properly handled."""
        element = create_survey_element_from_dict({
            "type": "tel",
            "name": "phone",
            "label": "Enter phone number"
        })
        self.assertEqual(element.bind.get("type"), "tel")
