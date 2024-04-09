"""Tests related to the parsing of the pipeline code."""

import tempfile
from dataclasses import asdict
from unittest import TestCase

from openhexa.sdk.pipelines.exceptions import InvalidParameterError, PipelineNotFound
from openhexa.sdk.pipelines.runtime import get_pipeline_metadata


class AstTest(TestCase):
    """Test the parsing of the pipeline code."""

    def test_pipeline_not_found(self):
        """The file does not contain a @pipeline decorator."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            with open(f"{tmpdirname}/pipeline.py", "w") as f:
                f.write("print('hello')")

            with self.assertRaises(PipelineNotFound):
                get_pipeline_metadata(tmpdirname)

    def test_pipeline_no_parameters(self):
        """The file contains a @pipeline decorator but no parameters."""
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
                        ]
                    )
                )
            pipeline = get_pipeline_metadata(tmpdirname)
            self.assertEqual(
                asdict(pipeline), {"code": "test", "name": "Test pipeline", "parameters": [], "timeout": None}
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
                            "@pipeline('test', 'Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                        ]
                    )
                )
            pipeline = get_pipeline_metadata(tmpdirname)
            self.assertEqual(
                asdict(pipeline), {"code": "test", "name": "Test pipeline", "parameters": [], "timeout": None}
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
                            "@pipeline('test', 'Test pipeline')",
                            "@parameter('test_param', name='Test Param', type=int, default=42 * 30, help='Param help')",
                            "def test_pipeline(test_param):",
                            "    pass",
                        ]
                    )
                )
            with self.assertRaises(ValueError):
                get_pipeline_metadata(tmpdirname)

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
                            "@pipeline('test', 'Test pipeline', timeout=timeout)",
                            "@parameter('test_param', name='Test Param', type=int, help='Param help')",
                            "def test_pipeline(test_param):",
                            "    pass",
                        ]
                    )
                )
            with self.assertRaises(ValueError):
                get_pipeline_metadata(tmpdirname)

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
                            "@pipeline('test', 'Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline_metadata(tmpdirname)
            self.assertEqual(
                asdict(pipeline),
                {
                    "code": "test",
                    "name": "Test pipeline",
                    "parameters": [
                        {
                            "choices": None,
                            "multiple": False,
                            "code": "test_param",
                            "type": "int",
                            "name": "Test Param",
                            "default": 42,
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
                            "@parameter('test_param', name='Test Param', type=int, default=42, help='Param help', multiple=True)",
                            "@pipeline('test', 'Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline_metadata(tmpdirname)
            self.assertEqual(
                asdict(pipeline),
                {
                    "code": "test",
                    "name": "Test pipeline",
                    "parameters": [
                        {
                            "choices": None,
                            "multiple": True,
                            "code": "test_param",
                            "type": "int",
                            "name": "Test Param",
                            "default": 42,
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
                            "@pipeline('test', 'Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline_metadata(tmpdirname)
            self.assertEqual(
                asdict(pipeline),
                {
                    "code": "test",
                    "name": "Test pipeline",
                    "parameters": [
                        {
                            "choices": None,
                            "multiple": False,
                            "code": "dataset",
                            "type": "dataset",
                            "name": "Dataset",
                            "default": None,
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
                            "@pipeline('test', 'Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline_metadata(tmpdirname)
            self.assertEqual(
                asdict(pipeline),
                {
                    "code": "test",
                    "name": "Test pipeline",
                    "parameters": [
                        {
                            "choices": ["a", "b"],
                            "multiple": False,
                            "code": "test_param",
                            "type": "str",
                            "name": "Test Param",
                            "default": None,
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
                            "@pipeline('test', 'Test pipeline', timeout=42)",
                            "def test_pipeline():",
                            "    pass",
                        ]
                    )
                )
            pipeline = get_pipeline_metadata(tmpdirname)
            self.assertEqual(
                asdict(pipeline), {"code": "test", "name": "Test pipeline", "parameters": [], "timeout": 42}
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
                            "@pipeline('test', 'Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline_metadata(tmpdirname)
            self.assertEqual(
                asdict(pipeline),
                {
                    "code": "test",
                    "name": "Test pipeline",
                    "parameters": [
                        {
                            "choices": None,
                            "multiple": False,
                            "code": "test_param",
                            "type": "bool",
                            "name": "Test Param",
                            "default": True,
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
                            "@pipeline('test', 'Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            pipeline = get_pipeline_metadata(tmpdirname)
            self.assertEqual(
                asdict(pipeline),
                {
                    "code": "test",
                    "name": "Test pipeline",
                    "parameters": [
                        {
                            "choices": None,
                            "multiple": False,
                            "code": "test_param",
                            "type": "int",
                            "name": "Test Param",
                            "default": 42,
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
                            "@pipeline('test', 'Test pipeline')",
                            "def test_pipeline():",
                            "    pass",
                            "",
                        ]
                    )
                )
            with self.assertRaises(InvalidParameterError):
                get_pipeline_metadata(tmpdirname)
