from tests.pyxform_test_case import PyxformTestCase

"""
Test hidden meta tags functionality in pyxform.
Tests that meta elements get the tag="hidden" attribute for CHT SMS functionality.
"""


class MetaTagHiddenTest(PyxformTestCase):
    """Test cases for hidden meta tags."""

    def test_meta_tag_hidden_by_default(self):
        """Test that meta elements get tag='hidden' attribute by default."""
        self.assertPyxformXform(
            name="test_meta",
            md="""
            | survey |        |         |       |
            |        | type   | name    | label |
            |        | text   | q1      | Q1    |
            """,
            xml__contains=[
                '<meta tag="hidden">',
                "<instanceID/>",
                "</meta>",
            ],
        )

    def test_meta_tag_with_audit(self):
        """Test that meta tag='hidden' is present when audit field is used."""
        self.assertPyxformXform(
            name="test_audit",
            md="""
            | survey |        |         |       |
            |        | type   | name    | label |
            |        | audit  | audit   |       |
            """,
            xml__contains=[
                '<meta tag="hidden">',
                "<audit/>",
                "<instanceID/>",
                "</meta>",
            ],
        )

    def test_meta_tag_with_sms_attributes(self):
        """Test that meta tag='hidden' is present with CHT SMS prefix and delimiter."""
        self.assertPyxformXform(
            name="test_sms",
            md="""
            | survey |        |         |       |
            |        | type   | name    | label |
            |        | text   | q1      | Q1    |
            """,
            xml__contains=[
                '<meta tag="hidden">',
                'prefix="J1!data!"',  # Default survey name is "data"
                'delimiter="#"',
                "<instanceID/>",
                "</meta>",
            ],
        )

    def test_meta_tag_with_multiple_fields(self):
        """Test that meta tag='hidden' works with multiple metadata fields."""
        self.assertPyxformXform(
            name="test_multiple",
            md="""
            | survey |           |         |       |
            |        | type      | name    | label |
            |        | deviceid  | dev_id  | Device ID |
            |        | start     | start   | Start |
            |        | end       | end     | End   |
            """,
            xml__contains=[
                '<meta tag="hidden">',
                "<dev_id/>",
                "<start/>",
                "<end/>",
                "<instanceID/>",
                "</meta>",
            ],
        )

    def test_meta_tag_consistent_across_forms(self):
        """Test that all forms get the meta tag='hidden' attribute consistently."""
        # Test a simple form
        self.assertPyxformXform(
            name="simple_form",
            md="""
            | survey |        |         |       |
            |        | type   | name    | label |
            |        | text   | name    | Name  |
            """,
            xml__contains=[
                '<meta tag="hidden">',
                "<instanceID/>",
                "</meta>",
            ],
        )

        # Test a form with choices
        self.assertPyxformXform(
            name="choice_form",
            md="""
            | survey |             |         |       |
            |        | type        | name    | label |
            |        | select_one colors | color | Color |
            | choices |       |       |       |
            |         | list_name | name | label |
            |         | colors | red   | Red   |
            |         | colors | blue  | Blue  |
            """,
            xml__contains=[
                '<meta tag="hidden">',
                "<instanceID/>",
                "</meta>",
            ],
        )
