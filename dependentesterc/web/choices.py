def _choices_with_current(base_choices, value):
    choices = list(base_choices)
    if value in (None, ""):
        return tuple(choices)

    value = str(value).strip()
    valid_values = {str(choice_value) for choice_value, _ in choices if choice_value not in (None, "")}
    if value not in valid_values:
        choices.append((value, f"{value} - {value}"))
    return tuple(choices)
