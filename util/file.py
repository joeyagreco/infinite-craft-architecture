def load_file_to_string(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    return content
