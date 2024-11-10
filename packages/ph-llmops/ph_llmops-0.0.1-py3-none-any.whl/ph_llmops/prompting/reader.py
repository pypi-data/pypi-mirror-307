def read_from_file(file_path: str) -> str:
    with open(file_path) as f:
        res = f.read()
        return res
