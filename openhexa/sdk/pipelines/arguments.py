import typing


class ArgumentType:
    def __str__(self):
        raise NotImplementedError

    @property
    def expected_type(self) -> typing.Type:
        raise NotImplementedError

    def validate(self, value: typing.Any) -> typing.Any:
        if not isinstance(value, self.expected_type):
            raise ValueError(f"Invalid type")

        return value


class String(ArgumentType):
    def __str__(self):
        return "string"

    @property
    def expected_type(self) -> typing.Type:
        return str


class Boolean(ArgumentType):
    def __str__(self):
        return "boolean"

    @property
    def expected_type(self) -> typing.Type:
        return bool


class Integer(ArgumentType):
    def __str__(self):
        return "integer"

    @property
    def expected_type(self) -> typing.Type:
        return int
