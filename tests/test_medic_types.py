import textwrap

from tests.pyxform_test_case import PyxformTestCase
from tests.xpath_helpers.questions import xpq


class CustomTypesTest(PyxformTestCase):

    def test_all_db_types_with_helpers(self):
        xls = textwrap.dedent("""
### survey
| type             | name               | label::en          |
| db:person        | person             | Person             |
| db:clinic        | clinic             | Clinic             |
| db:health_center | health_center      | Health Center      |
| db:district_hospital | district_hospital | District Hospital |
""")

        db_types = [
            ("person", "db:person"),
            ("clinic", "db:clinic"),
            ("health_center", "db:health_center"),
            ("district_hospital", "db:district_hospital"),
        ]

        bind_xpaths = [xpq.model_instance_bind(name, dtype) for name, dtype in db_types]
        input_xpaths = [xpq.body_label_inline("input", name, label)
                        for (name, dtype), label in zip(
                            db_types,
                            ["Person", "Clinic", "Health Center", "District Hospital"],
                            strict=True
                        )]

        self.assertPyxformXform(
            md=xls,
            xml__xpath_match=bind_xpaths + input_xpaths
        )

    def test_tel_type_with_helpers(self):
        xls = textwrap.dedent("""
### survey
| type | name  | label::en |
| tel  | phone | Phone     |
""")

        xp_bind = xpq.model_instance_bind("phone", "tel")
        xp_input = xpq.body_label_inline("input", "phone", "Phone")

        self.assertPyxformXform(
            md=xls,
            xml__xpath_match=[xp_input],
            xml__xpath_count=[(xp_bind, 1)],
        )
