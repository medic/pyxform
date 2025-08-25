from tests.pyxform_test_case import PyxformTestCase

"""
Ensures that fields marked with 'hidden' in the instance::tag column 
get the tag="hidden" attribute in the compiled XForm.
"""

class TagRestrictionTest(PyxformTestCase):
    """Test cases for tag attribute functionality."""

    def test_instance_tag_hidden_attribute(self):
        """Test that fields with instance::tag 'hidden' get tag='hidden' attribute."""
        self.assertPyxformXform(
            name="test_hidden_tags",
            md="""
            | survey |             |                     |                     |               |
            |        | type        | name                | label               | instance::tag |
            |        | text        | patient_name        | Patient Name        |               |
            |        | integer     | patient_age_years   | Age in Years        | hidden        |
            |        | integer     | patient_age_months  | Age in Months       | hidden        |
            |        | begin group | data                | Data Group          | hidden        |
            |        | text        | field1              | Field 1             |               |
            |        | end group   |                     |                     |               |
            """,
            xml__contains=[
                '<patient_age_years tag="hidden"/>',
                '<patient_age_months tag="hidden"/>',
                '<data tag="hidden">',
                '<patient_name/>',  # Should NOT have tag attribute
                '<field1/>',       
            ],
        )

    def test_nested_groups_with_hidden_tags(self):
        """Test hidden tags work with nested groups."""
        self.assertPyxformXform(
            name="test_nested_hidden",
            md="""
            | survey |             |              |                |               |
            |        | type        | name         | label          | instance::tag |
            |        | begin group | outer_group  | Outer Group    |               |
            |        | text        | field1       | Field 1        |               |
            |        | begin group | inner_group  | Inner Group    | hidden        |
            |        | text        | field2       | Field 2        |               |
            |        | end group   |              |                |               |
            |        | end group   |              |                |               |
            """,
            xml__contains=[
                '<inner_group tag="hidden">',
                '<outer_group>',  # Should NOT have tag attribute
            ],
        )
