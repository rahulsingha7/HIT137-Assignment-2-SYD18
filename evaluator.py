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


def tree_to_string(node):
    if isinstance(node, int):
        return str(node)

    if isinstance(node, tuple):
        if node[0] == "neg":
            return f"(neg {tree_to_string(node[1])})"
        return f"({node[0]} {tree_to_string(node[1])} {tree_to_string(node[2])})"

    return "ERROR"


def evaluate_tree(node):
    if isinstance(node, int):
        return float(node)

    if isinstance(node, tuple):
        if node[0] == "neg":
            return -evaluate_tree(node[1])

        left = evaluate_tree(node[1])
        right = evaluate_tree(node[2])

        if node[0] == "+":
            return left + right
        if node[0] == "-":
            return left - right
        if node[0] == "*":
            return left * right
        if node[0] == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right

    raise ValueError("Invalid tree")


def format_tokens(tokens):
    if tokens == "ERROR":
        return "ERROR"

    parts = []
    for token_type, token_value in tokens:
        if token_type == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{token_type}:{token_value}]")
    return " ".join(parts)


def format_result(value):
    if value == "ERROR":
        return "ERROR"

    if value.is_integer():
        return str(int(value))

    return f"{value:.4f}"


def evaluate_file(input_path: str) -> list[dict]:
    results = []

    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    output_lines = []

    for line in lines:
        expression = line.rstrip("\n")

        try:
            tokens = tokenize(expression)
            if tokens == "ERROR":
                raise ValueError("Tokenization error")

            tokens = insert_implicit_multiplication(tokens)
            tree = parse_expression(tokens)

            tree_str = tree_to_string(tree)
            token_str = format_tokens(tokens)

            try:
                result = evaluate_tree(tree)
                result_str = format_result(result)
                stored_result = result
            except Exception:
                result_str = "ERROR"
                stored_result = "ERROR"

            results.append({
                "input": expression,
                "tree": tree_str,
                "tokens": token_str,
                "result": stored_result
            })

        except Exception:
            tree_str = "ERROR"
            token_str = "ERROR"
            result_str = "ERROR"

            results.append({
                "input": expression,
                "tree": "ERROR",
                "tokens": "ERROR",
                "result": "ERROR"
            })

        output_lines.append(f"Input: {expression}")
        output_lines.append(f"Tree: {tree_str}")
        output_lines.append(f"Tokens: {token_str}")
        output_lines.append(f"Result: {result_str}")
        output_lines.append("")

    with open("output.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(output_lines).rstrip() + "\n")

    return results


if __name__ == "__main__":
    evaluate_file("sample_input.txt")