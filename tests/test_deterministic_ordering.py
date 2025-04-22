"""
Test deterministic ordering of XML attributes.
"""
from pyxform.utils import node
import unittest


class DeterministicOrderingTest(unittest.TestCase):
    """Test deterministic ordering of XML attributes."""

    def test_deterministic_ordering(self):
        """Test that attribute ordering is deterministic."""
        # Create a node with multiple attributes in different orders
        attributes1 = {
            "appearance": "field-list",
            "relevant": "${condition}",
            "constraint": "${constraint}"
        }

        attributes2 = {
            "constraint": "${constraint}",
            "appearance": "field-list",
            "relevant": "${condition}"
        }

        # Generate XML for both attribute sets
        node1 = node("group", **attributes1)
        node2 = node("group", **attributes2)

        # Convert to string for comparison
        xml1 = node1.toxml()
        xml2 = node2.toxml()

        # The XML should be identical regardless of the order of attributes in the dictionary
        self.assertEqual(xml1, xml2)

        # Check that attributes are in alphabetical order
        # For example, 'appearance' should come before 'constraint'
        self.assertLess(
            xml1.find('appearance="field-list"'),
            xml1.find('constraint="${constraint}"')
        )

        # And 'constraint' should come before 'relevant'
        self.assertLess(
            xml1.find('constraint="${constraint}"'),
            xml1.find('relevant="${condition}"')
        )
