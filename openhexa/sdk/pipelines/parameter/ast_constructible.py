"""Mixin for classes that can reconstruct themselves from an AST Call node."""

import ast
import inspect


class AstConstructible:
    """Mixin that enables reconstruction of a class instance from an AST Call node.

    Any class whose ``__init__`` takes only scalar (``ast.Constant``) arguments
    can inherit from this mixin and get ``from_ast_call`` for free.  Adding or
    renaming ``__init__`` parameters does *not* require touching the parser.

    To make the AST parser recognise a new subclass by name, add one entry to
    ``_AST_CALLABLE_TYPES`` in ``runtime.py`` (and ensure the subclass module is
    imported there).  Auto-registration via ``__init_subclass__`` would not remove
    that requirement — the registry entry only exists after the module is imported,
    so an explicit import would still be needed.
    """

    @classmethod
    def from_ast_call(cls, node: ast.Call) -> "AstConstructible":
        """Reconstruct an instance from an AST Call node.

        Maps positional args to ``__init__`` parameter names via
        ``inspect.signature``, then merges keyword args, and calls ``cls``.
        """
        param_names = list(inspect.signature(cls).parameters.keys())
        kwargs = {}
        for i, arg in enumerate(node.args):
            if i >= len(param_names):
                break
            if not isinstance(arg, ast.Constant):
                raise ValueError(
                    f"{cls.__name__}() positional argument {i + 1} must be a literal value, not a dynamic expression."
                )
            kwargs[param_names[i]] = arg.value
        for kw in node.keywords:
            if not isinstance(kw.value, ast.Constant):
                raise ValueError(
                    f"{cls.__name__}() keyword argument '{kw.arg}' must be a literal value, not a dynamic expression."
                )
            kwargs[kw.arg] = kw.value.value
        return cls(**kwargs)
