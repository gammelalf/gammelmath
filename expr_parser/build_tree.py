from expr_parser.tree import BinOp as _BinOp
from expr_parser.tree import UnaryOp as _UnaryOp
from expr_parser.operators.base import Operator as _Operator


def _process_scope(lst):
    def consume_operator(i):
        op = lst[i]
        if i+1 == len(lst) or isinstance(lst[i+1], _Operator):
            raise SyntaxError(f"Operator '{op}' is missing its operand")
        right = lst[i+1]

        if i > 0 and not isinstance(lst[i-1], _Operator):
            left = lst[i-1]
        else:
            left = None

        if left is None:
            return lst[:i] + [_UnaryOp(op, right)] + lst[i+2:]
        else:
            return lst[:i-1] + [_BinOp(left, op, right)] + lst[i+2:]

    while len(lst) > 1:
        if isinstance(lst[0], _Operator):
            index = 0
        else:
            index = 1

        while index + 2 < len(lst) \
                and isinstance(lst[index+2], _Operator) \
                and lst[index].priority < lst[index+2].priority:
            index += 2

        lst = consume_operator(index)

    return lst[0]
