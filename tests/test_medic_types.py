import re
import textwrap
from typing import Dict, List

from tests.pyxform_test_case import PyxformTestCase
from tests.xpath_helpers.questions import xpq


def markdown_to_workbook_dict(md: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Parse a Markdown-defined XLSForm (### survey + pipe tables)
    into the ss_structure dict expected by PyxformTestCase.
    """
    workbook = {}
    for section in re.split(r"^###\s+", md, flags=re.MULTILINE)[1:]:
        lines = section.strip().splitlines()
        if not lines:
            continue
        sheet = lines[0].strip().lower()
        if sheet != "survey":
            continue
        headers = [h.strip() for h in lines[1].split("|") if h.strip()]
        rows: List[Dict[str, str]] = []
        for row in lines[2:]:
            if not row.strip() or set(row.strip()) <= {"|", "-"}:
                continue
            values = [v.strip() for v in row.split("|") if v.strip()]
            if len(values) != len(headers):
                raise ValueError(f"Row length mismatch in survey: {row}")
            rows.append(dict(zip(headers, values)))
        workbook["survey"] = rows
    return workbook


class TestCustomTypes(PyxformTestCase):
    """
    Tests for all custom types added in PR #27
    (db:person, db:clinic, db:health_center, db:district_hospital, tel).
    """

    def assertPyxformXform(self, *, md: str = None, errored: bool = False, **kwargs):
        # If md is provided, convert it into ss_structure (workbook dict)
        if md is not None:
            md = textwrap.dedent(md)
            ss = markdown_to_workbook_dict(md)
            # clear md so base will ignore it
            md = None
            kwargs["ss_structure"] = ss
        super().assertPyxformXform(
            md=md, ss_structure=kwargs.get("ss_structure"), errored=errored, **kwargs
        )

    def test_all_custom_types(self):
        # Define a single survey sheet with all custom types
        xls = """
        ### survey
        | type                 | name               | label::en          |
        | db:person            | person             | Person             |
        | db:clinic            | clinic             | Clinic             |
        | db:health_center     | health_center      | Health Center      |
        | db:district_hospital | district_hospital  | District Hospital |
        | tel                  | phone              | Phone Number       |
        """

        # List of (question name, expected bind type)
        custom_types = [
            ("person", "db:person"),
            ("clinic", "db:clinic"),
            ("health_center", "db:health_center"),
            ("district_hospital", "db:district_hospital"),
            ("phone", "tel"),
        ]

        # Build XPath assertions for binds
        bind_xpaths = [
            xpq.model_instance_bind(name, qtype) for name, qtype in custom_types
        ]

        # Build XPath assertions for input controls (labels must match exactly)
        labels = [
            "Person",
            "Clinic",
            "Health Center",
            "District Hospital",
            "Phone Number",
        ]
        input_xpaths = [
            xpq.body_label_inline("input", name, label)
            for (name, _), label in zip(custom_types, labels, strict=True)
        ]

        # Run conversion and assert all binds and inputs appear exactly once
        self.assertPyxformXform(md=xls, xml__xpath_match=bind_xpaths + input_xpaths)
