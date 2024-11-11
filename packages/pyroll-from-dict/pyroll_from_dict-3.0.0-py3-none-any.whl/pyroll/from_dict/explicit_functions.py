import re

function_regex = re.compile(r"\s*func:\s*(?P<expr>.*)\s*")


def is_function(value):
    try:
        return bool(function_regex.match(value))
    except TypeError:
        return False


def parse_function(s: str, namespaces: dict[str, ...]):
    match = function_regex.match(s)
    expr = compile(match["expr"], "<string>", "eval")

    def func(self):
        return eval(expr, namespaces, dict(self=self))

    return func
