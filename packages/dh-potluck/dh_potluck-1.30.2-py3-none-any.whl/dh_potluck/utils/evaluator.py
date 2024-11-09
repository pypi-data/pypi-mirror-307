import operator as op
from ast import Add, BinOp, Constant, Div, Mult, Sub, UnaryOp, USub, dump, parse
from re import sub

PERMITTED_OPERATORS = {Add: op.add, Sub: op.sub, Mult: op.mul, Div: op.truediv, USub: op.neg}


class MathExpressionEvaluator:
    @staticmethod
    def evaluate_formula(formula: str):
        """Evaluate a string formula using ast functions.

        Args:
        - formula (str): The formula to be parsed and evaluated using ast functions. This function
        should only include numbers and operators inside a string i.e. '6/2*(1/2)'.


        Returns:
        - float: The value of the evaluated formula.
        """

        def _preprocess_formula(formula: str):
            formula = formula.replace('x', '*')
            return sub(r'(\d)\s*\(', r'\1*(', formula)

        def _evaluate(node):
            if isinstance(node, Constant):
                return node.n
            elif isinstance(node, BinOp):
                try:
                    return PERMITTED_OPERATORS[type(node.op)](
                        _evaluate(node.left), _evaluate(node.right)
                    )
                except ZeroDivisionError or TypeError:
                    return None

            elif isinstance(node, UnaryOp):
                return PERMITTED_OPERATORS[type(node.op)](_evaluate(node.operand))
            raise TypeError(f'Unsupported operation: {dump(node)}')

        processed_formula = _preprocess_formula(formula)
        node = parse(processed_formula, mode='eval').body
        return _evaluate(node)
