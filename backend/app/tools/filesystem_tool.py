from pathlib import Path


def list_files(path="."):

    files = []

    for item in Path(path).iterdir():

        files.append(str(item))

    return files
