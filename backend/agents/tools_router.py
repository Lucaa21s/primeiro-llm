from tools.filesystem_tool import list_files
from tools.pdf_tool import read_pdf
from tools.python_tool import run_python


TOOLS = {
    "list_files": list_files,
    "read_pdf": read_pdf,
    "run_python": run_python,
}



def execute_tool(tool_name, args):

    if tool_name not in TOOLS:
        return "Tool não encontrada"

    tool = TOOLS[tool_name]

    return tool(**args)
