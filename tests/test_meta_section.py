"""
Test meta section handling specific to CHT.
"""
import unittest
from pyxform.survey import Survey
from pyxform.section import Section


class MetaSectionTest(unittest.TestCase):
    """Test meta section handling specific to CHT."""

    def test_meta_section_hidden_tag(self):
        """Test that meta section has tag='hidden' attribute."""
        # Create a survey with a meta section
        survey = Survey(name="test_survey")
        
        # Create a meta section
        meta_section = Section(name="meta", parent=survey)
        survey.add_child(meta_section)
        
        # Generate XML instance
        xml_instance = meta_section.xml_instance()
        
        # Convert to string for inspection
        xml_str = xml_instance.toxml()
        
        # Verify that the meta section has tag="hidden" attribute
        self.assertIn('tag="hidden"', xml_str)
