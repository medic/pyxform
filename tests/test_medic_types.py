import re
import textwrap

from tests.pyxform_test_case import PyxformTestCase
from tests.xpath_helpers.questions import xpq


def markdown_to_workbook_dict(md: str) -> dict[str, list[dict[str, str]]]:
    sheet_sections = re.split(r"^###\s+", md, flags=re.MULTILINE)[1:]
    survey_data = []

    for section in sheet_sections:
        lines = section.strip().splitlines()
        if not lines:
            continue
        sheet_name = lines[0].strip().lower()
        table_lines = lines[1:]

        if sheet_name != "survey":
            continue  # only keep survey section

        headers = [h.strip() for h in table_lines[0].split("|") if h.strip()]

        for line in table_lines[1:]:
            if not line.strip() or set(line.strip()) <= {"|", "-"}:
                continue
            values = [v.strip() for v in line.split("|") if v.strip()]
            if len(values) != len(headers):
                raise ValueError(f"Row length mismatch in {sheet_name}: {line}")
            survey_data.append(dict(zip(headers, values, strict=False)))

    return {"survey": survey_data}


class CustomTypesTest(PyxformTestCase):

    def assertPyxformXform(self, *, md=None, errored=False, **kwargs):
        if md:
            md = textwrap.dedent(md)
            workbook_dict = markdown_to_workbook_dict(md)
            kwargs["workbook_dict"] = workbook_dict
        super().assertPyxformXform(errored=errored, **kwargs)

    def test_all_db_types_with_helpers(self):
        xls = """
        ### survey
        | type             | name               | label::en          |
        | db:person        | person             | Person             |
        | db:clinic        | clinic             | Clinic             |
        | db:health_center | health_center      | Health Center      |
        | db:district_hospital | district_hospital | District Hospital |
        """

        db_types = [
            ("person", "db:person"),
            ("clinic", "db:clinic"),
            ("health_center", "db:health_center"),
            ("district_hospital", "db:district_hospital"),
        ]

        bind_xpaths = [xpq.model_instance_bind(name, dtype) for name, dtype in db_types]
        input_xpaths = [
            xpq.body_label_inline("input", name, label)
            for (name, dtype), label in zip(
                db_types,
                ["Person", "Clinic", "Health Center", "District Hospital"],
                strict=True,
            )
        ]

        self.assertPyxformXform(md=xls, xml__xpath_match=bind_xpaths + input_xpaths)

    def test_tel_type_with_helpers(self):
        xls = """
        ### survey
        | type | name  | label::en |
        | tel  | phone | Phone     |
        """

        xp_bind = xpq.model_instance_bind("phone", "tel")
        xp_input = xpq.body_label_inline("input", "phone", "Phone")

        self.assertPyxformXform(
            md=xls,
            xml__xpath_match=[xp_input],
            xml__xpath_count=[(xp_bind, 1)],
        )
