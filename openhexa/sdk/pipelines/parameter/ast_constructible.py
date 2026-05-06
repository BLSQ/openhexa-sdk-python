"""Mixin for classes that can reconstruct themselves from an AST Call node."""

import ast
import inspect


class AstConstructible:
    """Mixin that enables reconstruction of a class instance from an AST Call node.

    Any class whose ``__init__`` takes only scalar (``ast.Constant``) arguments
    can inherit from this mixin to gain automatic ``from_ast_call`` support in
    the pipeline AST parser — no changes to the parser needed when new parameters
    are added to the class.
    """

    @classmethod
    def from_ast_call(cls, node: ast.Call) -> "AstConstructible":
        """Reconstruct an instance from an AST Call node.

        Maps positional args to ``__init__`` parameter names via
        ``inspect.signature``, then merges keyword args, and calls ``cls``.
        """
        param_names = list(inspect.signature(cls).parameters.keys())
        kwargs = {
            param_names[i]: arg.value
            for i, arg in enumerate(node.args)
            if isinstance(arg, ast.Constant) and i < len(param_names)
        }
        kwargs |= {kw.arg: kw.value.value for kw in node.keywords if isinstance(kw.value, ast.Constant)}
        return cls(**kwargs)
