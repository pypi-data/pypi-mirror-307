from llm_multiple_choice.choice_code import ChoiceCodeSet


def format_choice_codes(code_set: ChoiceCodeSet) -> str:
    """
    Format a set of choice codes as a comma-separated string.

    Args:
        code_set (ChoiceCodeSet): The set of choice codes to format.

    Returns:
        str: A comma-separated string of choice codes.
    """
    codes_sorted = sorted(code.code for code in code_set.codes)
    return ", ".join(str(code) for code in codes_sorted)
