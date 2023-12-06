def get_file_strings(input_file_name: str) -> list[str]:
    with open(input_file_name) as f:
        return f.read().splitlines()