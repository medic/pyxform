"""
Test empty label handling specific to CHT.
"""
import unittest
from pyxform.survey import Survey
from pyxform.section import Section
from pyxform.question import Question


class EmptyLabelTest(unittest.TestCase):
    """Test empty label handling specific to CHT."""

    def test_empty_label_handling(self):
        """Test that empty labels are properly handled."""
        # Create a survey
        survey = Survey(name="test_survey")

        # Create a section with an empty label
        section = Section(name="section", parent=survey)
        section.label = ""
        survey.add_child(section)

        # Create a question with an empty label
        question = Question(name="question", parent=section, type="text")
        question.label = ""
        section.add_child(question)

        # Verify that no PyXFormError is raised for empty labels
        try:
            # This would raise an error if empty labels weren't handled properly
            section.xml_label()
            question.xml_label()

            # Also verify that the section and question validate properly
            section.validate()
            question.validate()
        except Exception as e:
            self.fail(f"Validation raised an exception: {e}")
