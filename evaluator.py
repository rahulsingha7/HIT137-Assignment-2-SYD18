def tokenize(expression):
    tokens = []
    i = 0

    while i < len(expression):
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit():
            num = ch
            i += 1
            while i < len(expression) and expression[i].isdigit():
                num += expression[i]
                i += 1
            tokens.append(("NUM", num))
            continue

        if ch in "+-*/":
            tokens.append(("OP", ch))
            i += 1
            continue

        if ch == "(":
            tokens.append(("LPAREN", ch))
            i += 1
            continue

        if ch == ")":
            tokens.append(("RPAREN", ch))
            i += 1
            continue

        return "ERROR"

    tokens.append(("END", ""))
    return tokens


def insert_implicit_multiplication(tokens):
    if tokens == "ERROR":
        return "ERROR"

    result = []

    for i in range(len(tokens) - 1):
        current_token = tokens[i]
        next_token = tokens[i + 1]
        result.append(current_token)

        current_type, _ = current_token
        next_type, _ = next_token

        if (current_type in ("NUM", "RPAREN") and next_type == "LPAREN") or \
           (current_type == "RPAREN" and next_type == "NUM"):
            result.append(("OP", "*"))

    result.append(tokens[-1])
    return result


def parse_expression(tokens):
    position = 0

    def parse_expr():
        nonlocal position
        node = parse_term()

        while position < len(tokens) and (
            tokens[position] == ("OP", "+") or tokens[position] == ("OP", "-")
        ):
            op = tokens[position][1]
            position += 1
            right = parse_term()
            node = (op, node, right)

        return node

    def parse_term():
        nonlocal position
        node = parse_factor()

        while position < len(tokens) and (
            tokens[position] == ("OP", "*") or tokens[position] == ("OP", "/")
        ):
            op = tokens[position][1]
            position += 1
            right = parse_factor()
            node = (op, node, right)

        return node

    def parse_factor():
        nonlocal position

        if position >= len(tokens):
            raise ValueError("Unexpected end of input")

        token_type, token_value = tokens[position]

        if token_type == "OP" and token_value == "-":
            position += 1
            operand = parse_factor()
            return ("neg", operand)

        if token_type == "OP" and token_value == "+":
            raise ValueError("Unary plus is not allowed")

        if token_type == "NUM":
            position += 1
            return int(token_value)

        if token_type == "LPAREN":
            position += 1
            node = parse_expr()

            if position >= len(tokens) or tokens[position][0] != "RPAREN":
                raise ValueError("Missing closing parenthesis")

            position += 1
            return node

        raise ValueError("Invalid syntax")

    tree = parse_expr()

    if position >= len(tokens) or tokens[position][0] != "END":
        raise ValueError("Unexpected token after expression")

    return tree


def evaluate_file(input_path: str) -> list[dict]:
    return []


if __name__ == "__main__":
    tokens = tokenize("2 + 3 * 4")
    tokens = insert_implicit_multiplication(tokens)
    print(tokens)
    print(parse_expression(tokens))