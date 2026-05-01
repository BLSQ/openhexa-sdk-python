"""Tests for FileChoices dynamic parameter choices."""

import tempfile
from unittest import TestCase

import pytest

from openhexa.sdk.pipelines.exceptions import InvalidParameterError
from openhexa.sdk.pipelines.parameter import FileChoices, Parameter, parameter
from openhexa.sdk.pipelines.runtime import get_pipeline

# ---------------------------------------------------------------------------
# FileChoices construction
# ---------------------------------------------------------------------------


class TestFileChoicesConstruction:
    def test_csv_auto_detected(self):
        fc = FileChoices("districts.csv")
        assert fc.format == "csv"
        assert fc.path == "districts.csv"
        assert fc.column is None

    def test_json_auto_detected(self):
        fc = FileChoices("data/regions.json", column="code")
        assert fc.format == "json"
        assert fc.column == "code"

    def test_yaml_auto_detected(self):
        assert FileChoices("list.yaml").format == "yaml"

    def test_yml_normalised_to_yaml(self):
        assert FileChoices("list.yml").format == "yaml"

    def test_unsupported_extension_raises(self):
        with pytest.raises(InvalidParameterError, match="Supported extensions"):
            FileChoices("districts.xlsx")

    def test_no_extension_raises(self):
        with pytest.raises(InvalidParameterError, match="Supported extensions"):
            FileChoices("districts")

    def test_empty_path_raises(self):
        with pytest.raises(InvalidParameterError):
            FileChoices("")

    def test_non_string_column_raises(self):
        with pytest.raises(InvalidParameterError):
            FileChoices("districts.csv", column=42)

    def test_to_dict(self):
        fc = FileChoices("data/districts.csv", column="code")
        assert fc.to_dict() == {"format": "csv", "path": "data/districts.csv", "column": "code"}

    def test_to_dict_no_column(self):
        fc = FileChoices("districts.csv")
        assert fc.to_dict() == {"format": "csv", "path": "districts.csv", "column": None}


# ---------------------------------------------------------------------------
# Parameter integration
# ---------------------------------------------------------------------------


class TestParameterWithFileChoices:
    def test_accepts_file_choices(self):
        p = Parameter(code="district", type=str, choices=FileChoices("districts.csv"))
        assert isinstance(p.choices, FileChoices)

    def test_to_dict_emits_file_choices_key(self):
        p = Parameter(code="district", type=str, choices=FileChoices("districts.csv", column="code"))
        d = p.to_dict()
        assert d["choices"] is None
        assert d["file_choices"] == {"format": "csv", "path": "districts.csv", "column": "code"}

    def test_to_dict_no_file_choices_key_for_static_choices(self):
        p = Parameter(code="country", type=str, choices=["UG", "KE"])
        d = p.to_dict()
        assert d["choices"] == ["UG", "KE"]
        assert "file_choices" not in d

    def test_rejects_file_choices_on_bool_type(self):
        with pytest.raises(InvalidParameterError, match="don't accept choices"):
            Parameter(code="flag", type=bool, choices=FileChoices("flags.csv"))

    def test_validate_single_skips_choices_check(self):
        p = Parameter(code="district", type=str, choices=FileChoices("districts.csv"))
        # Any string value passes — the platform validates against the resolved list
        assert p.validate("any_value") == "any_value"

    def test_validate_multiple_skips_choices_check(self):
        p = Parameter(code="district", type=str, choices=FileChoices("districts.csv"), multiple=True)
        assert p.validate(["A", "B", "C"]) == ["A", "B", "C"]

    def test_default_not_validated_against_file_choices(self):
        # Should not raise even though default isn't in any resolved list
        p = Parameter(code="district", type=str, choices=FileChoices("districts.csv"), default="UNKNOWN")
        assert p.default == "UNKNOWN"

    def test_decorator_with_file_choices(self):
        @parameter(code="district", type=str, choices=FileChoices("districts.csv"))
        def my_pipeline(district):
            pass

        params = my_pipeline.get_all_parameters()
        assert len(params) == 1
        assert isinstance(params[0].choices, FileChoices)


# ---------------------------------------------------------------------------
# AST round-trip
# ---------------------------------------------------------------------------


class TestAstFileChoices(TestCase):
    def _write_pipeline(self, tmpdir, param_line):
        with open(f"{tmpdir}/pipeline.py", "w") as f:
            f.write(
                "\n".join(
                    [
                        "from openhexa.sdk.pipelines import pipeline, parameter",
                        "from openhexa.sdk.pipelines.parameter import FileChoices",
                        "",
                        param_line,
                        "@pipeline(name='Test pipeline')",
                        "def test_pipeline(district):",
                        "    pass",
                    ]
                )
            )

    def test_file_choices_csv_positional_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices=FileChoices('districts.csv'))",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["choices"] is None
            assert param_dict["file_choices"] == {"format": "csv", "path": "districts.csv", "column": None}

    def test_file_choices_csv_with_column(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices=FileChoices('data/districts.csv', column='code'))",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["file_choices"] == {"format": "csv", "path": "data/districts.csv", "column": "code"}

    def test_file_choices_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices=FileChoices('regions.json', column='id'))",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["file_choices"]["format"] == "json"

    def test_file_choices_yaml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices=FileChoices('list.yml'))",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["file_choices"]["format"] == "yaml"

    def test_unsupported_call_in_choices_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(f"{tmpdir}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "",
                            "@parameter('district', type=str, choices=dict(a=1))",
                            "@pipeline(name='Test pipeline')",
                            "def test_pipeline(district):",
                            "    pass",
                        ]
                    )
                )
            with self.assertRaises(ValueError, msg="Unsupported call"):
                get_pipeline(tmpdir)
