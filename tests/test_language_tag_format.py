"""
Test simplified language tag format specific to CHT.
"""
import unittest
from pyxform.survey import Survey
from pyxform.section import Section
from pyxform.question import Question


class LanguageTagFormatTest(unittest.TestCase):
    """Test simplified language tag format specific to CHT."""

    def test_simplified_language_tag_format(self):
        """Test that simplified language tag format is used."""
        # Create a survey
        survey = Survey(name="test_survey")

        # Create a section with a multilingual label
        section = Section(name="section", parent=survey)
        section.label = {"en": "English Label", "fr": "French Label"}
        survey.add_child(section)

        # Create a question with a multilingual label
        question = Question(name="question", parent=section, type="text")
        question.label = {"en": "English Question", "fr": "French Question"}
        section.add_child(question)

        # Get translations
        translations = []
        for element in [section, question]:
            for translation in element.get_translations("en"):
                translations.append(translation)

        # Verify that simplified language tag format is used
        paths = [t["path"] for t in translations]
        self.assertTrue(any("label" == path for path in paths))

        # Verify that the old format is not used
        self.assertFalse(any("/data/section:label" == path for path in paths))
