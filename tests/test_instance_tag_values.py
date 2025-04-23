"""
Test instance tag values copying specific to CHT.
"""
import unittest
from pyxform.survey import Survey
from pyxform.section import Section
from pyxform.question import Question


class InstanceTagValuesTest(unittest.TestCase):
    """Test instance tag values copying specific to CHT."""

    def test_instance_tag_values_copying(self):
        """Test that instance tag values are properly copied."""
        # Create a survey
        survey = Survey(name="test_survey")

        # Create a section with a tag attribute
        section = Section(name="section", parent=survey)
        section.instance = {"tag": "custom_tag"}
        survey.add_child(section)

        # Create a question with a tag attribute
        question = Question(name="question", parent=section, type="text")
        question.instance = {"tag": "another_tag"}
        section.add_child(question)

        # Generate XML instance
        xml_instance = survey.xml_instance()

        # Convert to string for inspection
        xml_str = xml_instance.toxml()

        # Verify that the section has tag="custom_tag" attribute
        self.assertIn('tag="custom_tag"', xml_str)

        # Verify that the question has tag="another_tag" attribute
        self.assertIn('tag="another_tag"', xml_str)
