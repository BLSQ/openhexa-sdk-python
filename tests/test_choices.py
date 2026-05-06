"""Tests for ChoicesFromFile dynamic parameter choices."""

import tempfile
from unittest import TestCase

import pytest

from openhexa.sdk.pipelines.exceptions import InvalidParameterError
from openhexa.sdk.pipelines.parameter import ChoicesFromFile, Parameter, parameter
from openhexa.sdk.pipelines.runtime import get_pipeline

# ---------------------------------------------------------------------------
# ChoicesFromFile construction
# ---------------------------------------------------------------------------


class TestChoicesFromFileConstruction:
    def test_csv_auto_detected(self):
        fc = ChoicesFromFile("districts.csv")
        assert fc.format == "csv"
        assert fc.path == "districts.csv"
        assert fc.column is None

    def test_json_auto_detected(self):
        fc = ChoicesFromFile("data/regions.json", column="code")
        assert fc.format == "json"
        assert fc.column == "code"

    def test_yaml_auto_detected(self):
        assert ChoicesFromFile("list.yaml").format == "yaml"

    def test_yml_normalised_to_yaml(self):
        assert ChoicesFromFile("list.yml").format == "yaml"

    def test_unsupported_extension_raises(self):
        with pytest.raises(InvalidParameterError, match="Supported extensions"):
            ChoicesFromFile("districts.xlsx")

    def test_no_extension_raises(self):
        with pytest.raises(InvalidParameterError, match="Supported extensions"):
            ChoicesFromFile("districts")

    def test_empty_path_raises(self):
        with pytest.raises(InvalidParameterError):
            ChoicesFromFile("")

    def test_non_string_column_raises(self):
        with pytest.raises(InvalidParameterError):
            ChoicesFromFile("districts.csv", column=42)

    def test_to_dict(self):
        fc = ChoicesFromFile("data/districts.csv", column="code")
        assert fc.to_dict() == {"format": "csv", "path": "data/districts.csv", "column": "code"}

    def test_to_dict_no_column(self):
        fc = ChoicesFromFile("districts.csv")
        assert fc.to_dict() == {"format": "csv", "path": "districts.csv", "column": None}


# ---------------------------------------------------------------------------
# String shorthand — Parameter.__init__
# ---------------------------------------------------------------------------


class TestStringShorthand:
    # --- happy paths ---

    def test_string_shorthand_csv(self):
        p = Parameter(code="district", type=str, choices="districts.csv")
        assert isinstance(p.choices, ChoicesFromFile)
        assert p.choices.path == "districts.csv"
        assert p.choices.format == "csv"
        assert p.choices.column is None

    def test_string_shorthand_json(self):
        p = Parameter(code="district", type=str, choices="data/regions.json")
        assert isinstance(p.choices, ChoicesFromFile)
        assert p.choices.format == "json"

    def test_string_shorthand_yaml(self):
        p = Parameter(code="district", type=str, choices="list.yaml")
        assert isinstance(p.choices, ChoicesFromFile)
        assert p.choices.format == "yaml"

    def test_string_shorthand_yml(self):
        p = Parameter(code="district", type=str, choices="list.yml")
        assert isinstance(p.choices, ChoicesFromFile)
        assert p.choices.format == "yaml"

    def test_string_shorthand_leading_slash_stripped(self):
        p = Parameter(code="district", type=str, choices="/choices.csv")
        assert p.choices.path == "/choices.csv"  # ChoicesFromFile stores as-is; stripping is app-side

    def test_string_shorthand_serialises_same_as_explicit(self):
        shorthand = Parameter(code="district", type=str, choices="districts.csv").to_dict()
        explicit = Parameter(code="district", type=str, choices=ChoicesFromFile("districts.csv")).to_dict()
        assert shorthand == explicit

    # --- static list still works ---

    def test_static_list_unaffected(self):
        p = Parameter(code="country", type=str, choices=["UG", "KE"])
        assert p.choices == ["UG", "KE"]

    def test_explicit_choices_from_file_unaffected(self):
        p = Parameter(code="district", type=str, choices=ChoicesFromFile("districts.csv", column="code"))
        assert p.choices.column == "code"

    # --- invalid strings raise clearly ---

    def test_string_no_extension_raises(self):
        with pytest.raises(InvalidParameterError, match="Supported extensions"):
            Parameter(code="district", type=str, choices="nodot")

    def test_string_unsupported_extension_raises(self):
        with pytest.raises(InvalidParameterError, match="Supported extensions"):
            Parameter(code="district", type=str, choices="file.xlsx")

    def test_empty_string_raises(self):
        with pytest.raises(InvalidParameterError):
            Parameter(code="district", type=str, choices="")

    # --- column cannot be specified via shorthand ---

    def test_shorthand_has_no_column(self):
        p = Parameter(code="district", type=str, choices="districts.csv")
        assert p.choices.column is None

    def test_decorator_with_string_shorthand(self):
        @parameter(code="district", type=str, choices="districts.csv")
        def my_pipeline(district):
            pass

        params = my_pipeline.get_all_parameters()
        assert isinstance(params[0].choices, ChoicesFromFile)


# ---------------------------------------------------------------------------
# String shorthand — AST round-trip
# ---------------------------------------------------------------------------


class TestAstStringShorthand(TestCase):
    def _write_pipeline(self, tmpdir, param_line):
        with open(f"{tmpdir}/pipeline.py", "w") as f:
            f.write(
                "\n".join(
                    [
                        "from openhexa.sdk.pipelines import pipeline, parameter",
                        "",
                        param_line,
                        "@pipeline(name='Test pipeline')",
                        "def test_pipeline(district):",
                        "    pass",
                    ]
                )
            )

    def test_ast_string_shorthand_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices='districts.csv')",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["choices"] is None
            assert param_dict["choices_from_file"] == {"format": "csv", "path": "districts.csv", "column": None}

    def test_ast_string_shorthand_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices='regions.json')",
            )
            p = get_pipeline(tmpdir)
            assert p.to_dict()["parameters"][0]["choices_from_file"]["format"] == "json"

    def test_ast_string_shorthand_yaml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices='list.yml')",
            )
            p = get_pipeline(tmpdir)
            assert p.to_dict()["parameters"][0]["choices_from_file"]["format"] == "yaml"

    def test_ast_string_shorthand_same_output_as_explicit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices='districts.csv')",
            )
            shorthand_dict = get_pipeline(tmpdir).to_dict()["parameters"][0]

        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices=ChoicesFromFile('districts.csv'))",
            )
            # need the import for the explicit form
            with open(f"{tmpdir}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "from openhexa.sdk.pipelines.parameter import ChoicesFromFile",
                            "",
                            "@parameter('district', type=str, choices=ChoicesFromFile('districts.csv'))",
                            "@pipeline(name='Test pipeline')",
                            "def test_pipeline(district):",
                            "    pass",
                        ]
                    )
                )
            explicit_dict = get_pipeline(tmpdir).to_dict()["parameters"][0]

        assert shorthand_dict == explicit_dict

    def test_ast_static_list_unaffected(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('country', type=str, choices=['UG', 'KE'])",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["choices"] == ["UG", "KE"]
            assert "choices_from_file" not in param_dict

    def test_ast_string_no_extension_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices='nodot')",
            )
            with self.assertRaises(InvalidParameterError):
                get_pipeline(tmpdir)

    def test_ast_string_unsupported_extension_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices='file.xlsx')",
            )
            with self.assertRaises(InvalidParameterError):
                get_pipeline(tmpdir)


# ---------------------------------------------------------------------------
# Parameter integration
# ---------------------------------------------------------------------------


class TestParameterWithChoicesFromFile:
    def test_accepts_file_choices(self):
        p = Parameter(code="district", type=str, choices=ChoicesFromFile("districts.csv"))
        assert isinstance(p.choices, ChoicesFromFile)

    def test_to_dict_emits_file_choices_key(self):
        p = Parameter(code="district", type=str, choices=ChoicesFromFile("districts.csv", column="code"))
        d = p.to_dict()
        assert d["choices"] is None
        assert d["choices_from_file"] == {"format": "csv", "path": "districts.csv", "column": "code"}

    def test_to_dict_no_file_choices_key_for_static_choices(self):
        p = Parameter(code="country", type=str, choices=["UG", "KE"])
        d = p.to_dict()
        assert d["choices"] == ["UG", "KE"]
        assert "choices_from_file" not in d

    def test_rejects_file_choices_on_bool_type(self):
        with pytest.raises(InvalidParameterError, match="don't accept choices"):
            Parameter(code="flag", type=bool, choices=ChoicesFromFile("flags.csv"))

    def test_validate_single_skips_choices_check(self):
        p = Parameter(code="district", type=str, choices=ChoicesFromFile("districts.csv"))
        # Any string value passes — the platform validates against the resolved list
        assert p.validate("any_value") == "any_value"

    def test_validate_multiple_skips_choices_check(self):
        p = Parameter(code="district", type=str, choices=ChoicesFromFile("districts.csv"), multiple=True)
        assert p.validate(["A", "B", "C"]) == ["A", "B", "C"]

    def test_default_not_validated_against_file_choices(self):
        # Should not raise even though default isn't in any resolved list
        p = Parameter(code="district", type=str, choices=ChoicesFromFile("districts.csv"), default="UNKNOWN")
        assert p.default == "UNKNOWN"

    def test_decorator_with_file_choices(self):
        @parameter(code="district", type=str, choices=ChoicesFromFile("districts.csv"))
        def my_pipeline(district):
            pass

        params = my_pipeline.get_all_parameters()
        assert len(params) == 1
        assert isinstance(params[0].choices, ChoicesFromFile)


# ---------------------------------------------------------------------------
# AST round-trip
# ---------------------------------------------------------------------------


class TestAstChoicesFromFile(TestCase):
    def _write_pipeline(self, tmpdir, param_line):
        with open(f"{tmpdir}/pipeline.py", "w") as f:
            f.write(
                "\n".join(
                    [
                        "from openhexa.sdk.pipelines import pipeline, parameter",
                        "from openhexa.sdk.pipelines.parameter import ChoicesFromFile",
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
                "@parameter('district', type=str, choices=ChoicesFromFile('districts.csv'))",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["choices"] is None
            assert param_dict["choices_from_file"] == {"format": "csv", "path": "districts.csv", "column": None}

    def test_file_choices_csv_with_column(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices=ChoicesFromFile('data/districts.csv', column='code'))",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["choices_from_file"] == {"format": "csv", "path": "data/districts.csv", "column": "code"}

    def test_file_choices_csv_with_column_positional(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices=ChoicesFromFile('data/districts.csv', 'code'))",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["choices_from_file"] == {"format": "csv", "path": "data/districts.csv", "column": "code"}

    def test_file_choices_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices=ChoicesFromFile('regions.json', column='id'))",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["choices_from_file"]["format"] == "json"

    def test_file_choices_yaml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self._write_pipeline(
                tmpdir,
                "@parameter('district', type=str, choices=ChoicesFromFile('list.yml'))",
            )
            p = get_pipeline(tmpdir)
            param_dict = p.to_dict()["parameters"][0]
            assert param_dict["choices_from_file"]["format"] == "yaml"

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
