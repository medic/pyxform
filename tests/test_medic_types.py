"""
Testing medic types
"""
import re
import textwrap
from typing import Dict, List

from pyxform.xls2xform import convert
from tests.pyxform_test_case import PyxformTestCase
from tests.xpath_helpers.questions import xpq

def markdown_to_workbook_dict(md: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Parses a Markdown XLSForm (### survey + pipe tables) into a workbook_dict
    that convert() understands.
    """
    workbook = {}
    for section in re.split(r'^###\s+', md, flags=re.MULTILINE)[1:]:
        lines = section.strip().splitlines()
        if not lines:
            continue
        sheet = lines[0].strip().lower()
        if sheet != "survey":
            continue
        headers = [h.strip() for h in lines[1].split("|") if h.strip()]
        rows = []
        for row in lines[2:]:
            if not row.strip() or set(row.strip()) <= {"|", "-"}:
                continue
            values = [v.strip() for v in row.split("|") if v.strip()]
            if len(values) != len(headers):
                raise ValueError(f"Row length mismatch: {row}")
            rows.append(dict(zip(headers, values)))
        workbook["survey"] = rows
    return workbook


class TestCustomTypes(PyxformTestCase):
    """
    End-to-end test that converts a mini-XLSForm with all custom types
    and asserts the right <bind> and <input> elements are generated.
    """

    def assertPyxformXform(self, *, md=None, errored=False, **kwargs):
        # Preprocess Markdown into workbook_dict
        if md is not None:
            md = textwrap.dedent(md)
            kwargs["workbook_dict"] = markdown_to_workbook_dict(md)
        super().assertPyxformXform(errored=errored, **kwargs)

    def test_all_custom_types(self):
        # Inline Markdown XLSForm definition
        xls = """
        ### survey
        | type               | name               | label::en          |
        | db:person          | person             | Person             |
        | db:clinic          | clinic             | Clinic             |
        | db:health_center   | health_center      | Health Center      |
        | db:district_hospital | district_hospital | District Hospital |
        | tel                | phone              | Phone Number       |
        """

        # Definition of (name, expected type) for each question
        custom_types = [
            ("person", "db:person"),
            ("clinic", "db:clinic"),
            ("health_center", "db:health_center"),
            ("district_hospital", "db:district_hospital"),
            ("phone", "tel"),
        ]

        # Build the XPath assertions for <bind> and <input>
        bind_asserts = [
            xpq.model_instance_bind(name, qtype) for name, qtype in custom_types
        ]
        input_asserts = [
            xpq.body_label_inline("input", name, label)
            for (name, _), label in zip(
                custom_types,
                ["Person", "Clinic", "Health Center", "District Hospital", "Phone Number"],
                strict=True
            )
        ]

        # Run conversion + assertions
        self.assertPyxformXform(
            md=xls,
            xml__xpath_match=bind_asserts + input_asserts
        )


