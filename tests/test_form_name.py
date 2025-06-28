"""
Test setting form name to data.
"""

from tests.pyxform_test_case import PyxformTestCase


class TestFormName(PyxformTestCase):
    def test_default_to_data_when_no_name(self):
        """Should default to form_name of 'test_name', and form id of 'data'."""
        self.assertPyxformXform(
            md="""
            | survey   |           |      |           |
            |          | type      | name | label     |
            |          | text      | city | City Name |
            """,
            name="test_name",
            # Match the opening <test_name> tag (it now includes prefix & delimiter attrs)
            instance__contains=['<test_name '],
            model__contains=['<bind nodeset="/test_name/city" type="string"/>'],
            xml__contains=[
                '<input ref="/test_name/city">',
                "<label>City Name</label>",
                "</input>",
            ],
        )

    def test_default_to_data(self):
        """
        Test using data as the name of the form which will generate <data />.
        """
        self.assertPyxformXform(
            md="""
               | survey |      |      |           |
               |        | type | name | label     |
               |        | text | city | City Name |
               """,
            name="data",
            # Match the opening <data> tag (it now includes prefix & delimiter attrs)
            instance__contains=['<data '],
            model__contains=['<bind nodeset="/data/city" type="string"/>'],
            xml__contains=[
                '<input ref="/data/city">',
                "<label>City Name</label>",
                "</input>",
            ],
        )

    def test_default_form_name_to_superclass_definition(self):
        """
        Test no form_name and setting name field, should use name field.
        """

        self.assertPyxformXform(
            md="""
               | survey |      |      |           |
               |        | type | name | label     |
               |        | text | city | City Name |
               """,
            name="some-name",
            # instance__contains=['<some-name id="data">'],
            # Match the opening <some-name> tag (it now includes prefix & delimiter attrs)
            instance__contains=['<some-name '],
            model__contains=['<bind nodeset="/some-name/city" type="string"/>'],
            xml__contains=[
                '<input ref="/some-name/city">',
                "<label>City Name</label>",
                "</input>",
            ],
        )
