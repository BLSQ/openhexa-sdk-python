"""Tests related to the parsing of the pipeline code."""

import io
import tempfile
from unittest import TestCase
from unittest.mock import patch

from openhexa.sdk.pipelines.exceptions import InvalidParameterError, PipelineNotFound
from openhexa.sdk.pipelines.parameter import DHIS2Widget, IASOWidget
from openhexa.sdk.pipelines.runtime import get_pipeline


class AstTest(TestCase):
    """Test the parsing of the pipeline code."""

    def test_pipeline_not_found(self):
        """The file does not contain a @pipeline decorator."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write("print('hello')")

            with self.assertRaises(PipelineNotFound):
                get_pipeline(tmpdirname)

    def test_pipeline_no_parameters(self):
        """The file contains a @pipeline decorator but no parameters."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline",
                            "",
                            "@pipeline(name='Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "name": "Test pipeline",
                    "function": None,
                    "tasks": [],
                    "parameters": [],
                    "timeout": None,
                },
            )

    def test_pipeline_with_args(self):
        """The file contains a @pipeline decorator with args."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline",
                            "",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "function": None,
                    "tasks": [],
                    "name": "Test pipeline",
                    "parameters": [],
                    "timeout": None,
                },
            )

    def test_pipeline_with_invalid_parameter_args(self):
        """The file contains a @parameter decorator with a BinOp as default value."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "",
                            "@pipeline('Test pipeline')",
                            "@parameter('test_param', name='Test Param', type=int, default=42 * 30, help='Param help')",
                            "def test_pipeline(test_param):",
                            "    pass",
                        ]
                    )
                )
            with self.assertRaises(ValueError):
                get_pipeline(tmpdirname)

    def test_pipeline_with_invalid_pipeline_args(self):
        """The file contains a @pipeline decorator with invalid value."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "",
                            "timeout = 60 * 60",
                            "@pipeline('Test pipeline', timeout=timeout)",
                            "@parameter('test_param', name='Test Param', type=int, help='Param help')",
                            "def test_pipeline(test_param):",
                            "    pass",
                        ]
                    )
                )
            with self.assertRaises(ValueError):
                get_pipeline(tmpdirname)

    def test_pipeline_with_int_param(self):
        """The file contains a @pipeline decorator and a @parameter decorator with an int."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "",
                            "@parameter('test_param', name='Test Param', type=int, default=42, help='Param help')",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "name": "Test pipeline",
                    "function": None,
                    "tasks": [],
                    "parameters": [
                        {
                            "choices": None,
                            "multiple": False,
                            "code": "test_param",
                            "type": "int",
                            "name": "Test Param",
                            "default": 42,
                            "widget": None,
                            "connection": None,
                            "help": "Param help",
                            "required": True,
                        }
                    ],
                    "timeout": None,
                },
            )

    def test_pipeline_with_multiple_param(self):
        """The file contains a @pipeline decorator and a @parameter decorator with multiple=True."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "",
                            "@parameter('test_param', name='Test Param', type=int, default=[42], help='Param help', multiple=True)",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "name": "Test pipeline",
                    "function": None,
                    "tasks": [],
                    "parameters": [
                        {
                            "choices": None,
                            "multiple": True,
                            "code": "test_param",
                            "type": "int",
                            "name": "Test Param",
                            "default": [42],
                            "widget": None,
                            "connection": None,
                            "help": "Param help",
                            "required": True,
                        }
                    ],
                    "timeout": None,
                },
            )

    def test_pipeline_with_dataset(self):
        """The file contains a @pipeline decorator and use a parameter with 'dataset' type."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "from openhexa.sdk.pipelines.parameter import Dataset",
                            "",
                            "@parameter('dataset', name='Dataset', type=Dataset, help='Dataset', required=False)",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "function": None,
                    "name": "Test pipeline",
                    "tasks": [],
                    "parameters": [
                        {
                            "choices": None,
                            "multiple": False,
                            "code": "dataset",
                            "type": "dataset",
                            "name": "Dataset",
                            "default": None,
                            "widget": None,
                            "connection": None,
                            "help": "Dataset",
                            "required": False,
                        }
                    ],
                    "timeout": None,
                },
            )

    def test_pipeline_with_choices(self):
        """The file contains a @pipeline decorator and a @parameter decorator with choices."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "",
                            "@parameter('test_param', name='Test Param', type=str, choices=['a', 'b'], help='Param help')",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "name": "Test pipeline",
                    "function": None,
                    "tasks": [],
                    "parameters": [
                        {
                            "choices": ["a", "b"],
                            "multiple": False,
                            "code": "test_param",
                            "type": "str",
                            "name": "Test Param",
                            "default": None,
                            "widget": None,
                            "connection": None,
                            "help": "Param help",
                            "required": True,
                        }
                    ],
                    "timeout": None,
                },
            )

    def test_pipeline_with_timeout(self):
        """The file contains a @pipeline decorator with a timeout."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline",
                            "",
                            "@pipeline('Test pipeline', timeout=42)",
                            "def test_pipeline():",
                            "    pass",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "name": "Test pipeline",
                    "parameters": [],
                    "timeout": 42,
                    "function": None,
                    "tasks": [],
                },
            )

    def test_pipeline_with_bool(self):
        """The file contains a @pipeline decorator and a @parameter decorator with a bool."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "",
                            "@parameter('test_param', name='Test Param', type=bool, default=True, help='Param help')",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "name": "Test pipeline",
                    "function": None,
                    "tasks": [],
                    "parameters": [
                        {
                            "choices": None,
                            "multiple": False,
                            "code": "test_param",
                            "type": "bool",
                            "name": "Test Param",
                            "default": True,
                            "widget": None,
                            "connection": None,
                            "help": "Param help",
                            "required": True,
                        }
                    ],
                    "timeout": None,
                },
            )

    def test_pipeline_with_multiple_parameters(self):
        """The file contains a @pipeline decorator and multiple @parameter decorators."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "",
                            "@parameter('test_param', name='Test Param', type=int, default=42, help='Param help')",
                            "@parameter('test_param2', name='Test Param 2', type=str, choices=['a', 'b'], help='Param help 2')",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "name": "Test pipeline",
                    "function": None,
                    "tasks": [],
                    "parameters": [
                        {
                            "choices": None,
                            "multiple": False,
                            "code": "test_param",
                            "type": "int",
                            "name": "Test Param",
                            "default": 42,
                            "widget": None,
                            "connection": None,
                            "help": "Param help",
                            "required": True,
                        },
                        {
                            "choices": ["a", "b"],
                            "multiple": False,
                            "code": "test_param2",
                            "type": "str",
                            "name": "Test Param 2",
                            "default": None,
                            "widget": None,
                            "connection": None,
                            "help": "Param help 2",
                            "required": True,
                        },
                    ],
                    "timeout": None,
                },
            )

    def test_pipeline_with_unsupported_parameter(self):
        """The file contains a @pipeline decorator and a @parameter decorator with an unsupported type."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "",
                            "@parameter('test_param', name='Test Param', type=object, default=42, help='Param help')",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            with self.assertRaises(InvalidParameterError):
                get_pipeline(tmpdirname)

    def test_pipeline_with_connection_parameter_for_dhis2(self):
        """The file contains a @pipeline decorator and a @parameter decorator with a connection type."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "from openhexa.sdk.pipelines.widgets import DHIS2Widget",
                            "",
                            "@parameter('dhis_con', name='DHIS2 Connection', type=DHIS2Connection, required=True)",
                            "@parameter('data_element_ids', name='Data Elements id', type=str, widget=DHIS2Widget.ORG_UNITS, connection='dhis_con', required=True)",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.maxDiff = None
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "name": "Test pipeline",
                    "function": None,
                    "tasks": [],
                    "parameters": [
                        {
                            "code": "dhis_con",
                            "type": "dhis2",
                            "name": "DHIS2 Connection",
                            "default": None,
                            "multiple": False,
                            "choices": None,
                            "widget": None,
                            "connection": None,
                            "help": None,
                            "required": True,
                        },
                        {
                            "code": "data_element_ids",
                            "type": "str",
                            "name": "Data Elements id",
                            "widget": DHIS2Widget.ORG_UNITS.value,
                            "connection": "dhis_con",
                            "default": None,
                            "multiple": False,
                            "choices": None,
                            "help": None,
                            "required": True,
                        },
                    ],
                    "timeout": None,
                },
            )

    def test_pipeline_with_connection_parameter_for_iaso(self):
        """The file contains a @pipeline decorator and a @parameter decorator with a connection type."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "from openhexa.sdk.pipelines.widgets import IASOWidget",
                            "",
                            "@parameter('iaso_con', name='IASO Connection', type=IASOConnection, required=True)",
                            "@parameter('org_units', name='OrgUnits', type=int, widget=IASOWidget.IASO_ORG_UNITS, connection='iaso_con', required=True)",
                            "@parameter('projects', name='Projects', type=int, widget=IASOWidget.IASO_PROJECTS, connection='iaso_con', required=True)",
                            "@parameter('forms', name='Forms', type=int, widget=IASOWidget.IASO_FORMS, connection='iaso_con', required=True)",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline(org_units, forms, projects):",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline(tmpdirname)
            self.maxDiff = None
            self.assertEqual(
                pipeline.to_dict(),
                {
                    "name": "Test pipeline",
                    "function": None,
                    "tasks": [],
                    "parameters": [
                        {
                            "code": "iaso_con",
                            "type": "iaso",
                            "name": "IASO Connection",
                            "default": None,
                            "multiple": False,
                            "choices": None,
                            "widget": None,
                            "connection": None,
                            "help": None,
                            "required": True,
                        },
                        {
                            "code": "org_units",
                            "type": "int",
                            "name": "OrgUnits",
                            "widget": IASOWidget.IASO_ORG_UNITS.value,
                            "connection": "iaso_con",
                            "default": None,
                            "multiple": False,
                            "choices": None,
                            "help": None,
                            "required": True,
                        },
                        {
                            "code": "projects",
                            "type": "int",
                            "name": "Projects",
                            "widget": IASOWidget.IASO_PROJECTS.value,
                            "connection": "iaso_con",
                            "default": None,
                            "multiple": False,
                            "choices": None,
                            "help": None,
                            "required": True,
                        },
                        {
                            "code": "forms",
                            "type": "int",
                            "name": "Forms",
                            "widget": IASOWidget.IASO_FORMS.value,
                            "connection": "iaso_con",
                            "default": None,
                            "multiple": False,
                            "choices": None,
                            "help": None,
                            "required": True,
                        },
                    ],
                    "timeout": None,
                },
            )

    def test_pipeline_wit_wrong_connection_parameter(self):
        """The file contains a @pipeline decorator and a @parameter decorator with a non-existing connection type."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "from openhexa.sdk.pipelines.parameter import DHIS2Widget",
                            "",
                            "@parameter('dhis_con', name='DHIS2 Connection', type=DHIS2Connection, required=True)",
                            "@pipeline('Test pipeline')",
                            "@parameter('data_element_ids', name='Data Elements id', type=str, widget=DHIS2Widget.ORG_UNITS, connection='sds_con', required=True)",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            with self.assertRaises(InvalidParameterError):
                get_pipeline(tmpdirname)

    def test_pipeline_with_dhis2_widget_without_connection(self):
        """The file contains a @pipeline decorator and a @parameter decorator with a widget parameter field."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline, parameter",
                            "from openhexa.sdk.pipelines.parameter import DHIS2Widget",
                            "",
                            "@parameter('test_field_for_widget', name='Widget Param', type=str, widget=DHIS2Widget.ORG_UNITS, help='Param help')",
                            "@pipeline('Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            with self.assertRaises(InvalidParameterError):
                get_pipeline(tmpdirname)

    def test_pipeline_with_deprecated_code_argument_with_name(self):
        """The file contains a @pipeline decorator with the deprecated 'code' argument."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline",
                            "",
                            "@pipeline(code='test', name='Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
                pipeline = get_pipeline(tmpdirname)
                self.assertEqual(pipeline.to_dict()["name"], "Test pipeline")
                self.assertIn(
                    "The 'code' argument is deprecated and should not be used as a keyword.", fake_stdout.getvalue()
                )

    def test_pipeline_with_deprecated_code_as_arg(self):
        """The file contains a @pipeline decorator with the deprecated 'code' argument."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "from openhexa.sdk.pipelines import pipeline",
                            "",
                            "@pipeline('test', name='Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
                pipeline = get_pipeline(tmpdirname)
                self.assertEqual(pipeline.to_dict()["name"], "Test pipeline")
                self.assertIn("Providing both 'code' and 'name' is deprecated.", fake_stdout.getvalue())
