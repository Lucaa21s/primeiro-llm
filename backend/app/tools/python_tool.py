import subprocess


def run_python(code):

    result = subprocess.run(
        ["python", "-c", code],
        capture_output=True,
        text=True,
    )

    return result.stdout
