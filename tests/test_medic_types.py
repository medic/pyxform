# tests/test_custom_types_simple.py

from tests.pyxform_test_case import PyxformTestCase
from tests.xpath_helpers.questions import xpq


class TestCustomTypesSimple(PyxformTestCase):
    """
    Markdown-only test for each of medic custom types.
    """

    def test_db_person_bind(self):
        self.assertPyxformXform(
            name="db_person",
            md="""
            | survey |               |           |
            |        | type          | name      | label::en |
            |        | db:person     | person    | Person    |
            """,
            # assert there’s exactly one <bind type="db:person" nodeset="/data/person">
            xml__xpath_match=[xpq.model_instance_bind("person", "db:person")],
        )

    def test_db_clinic_bind(self):
        self.assertPyxformXform(
            name="db_clinic",
            md="""
            | survey |              |           |
            |        | type         | name      | label::en |
            |        | db:clinic    | clinic    | Clinic    |
            """,
            xml__xpath_match=[xpq.model_instance_bind("clinic", "db:clinic")],
        )

    def test_tel_bind(self):
        self.assertPyxformXform(
            name="tel_phone",
            md="""
            | survey |       |            |
            |        | type  | name       | label::en    |
            |        | tel   | phone      | Phone Number |
            """,
            xml__xpath_match=[xpq.model_instance_bind("phone", "tel")],
        )
