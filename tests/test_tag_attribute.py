from tests.pyxform_test_case import PyxformTestCase

"""
Test hidden meta tags functionality in pyxform.
Tests that meta elements get the tag="hidden" attribute for CHT  functionality.
"""


class TagRestrictionTest(PyxformTestCase):
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
                "<q1/>",
                '<meta tag="hidden">',
                '<instanceID/>',
            ],
        )

    def test_meta_tag_with_multiple_groups(self):
        """Test that meta tag='hidden' works with multiple metadata groups."""
        self.assertPyxformXform(
            name="test_multiple",
            md="""
            | survey |             |              |            |
            |        | type        | name         | label      |
            |        | begin group | nested_field | Nested     |
            |        | text        | meta         | Meta       |
            |        | end group   |              |            |
            |        | begin group | nested_group | Nested     |
            |        | begin group | meta         | Meta Group |
            |        | deviceid    | dev_id       | Device ID  |
            |        | end group   |              |            |
            |        | end group   |              |            |
            """,
            xml__contains=[
                'tag="hidden"',
                '<meta tag="hidden">',
                '<instanceID/>',
            ],
        )
