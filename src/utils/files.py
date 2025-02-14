def create_temporal_file(data: bytes, file_path: str) -> None:
    try:
        with open(file_path, "wb") as file:
            file.write(data)
    except Exception as e:
        raise RuntimeError(f"Failed to create temporal file {file_path}: {e}")
