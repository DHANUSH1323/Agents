import requests
from smolagents import Tool

DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"


class GaiaFileReaderTool(Tool):
    name = "read_task_file"
    description = (
        "Downloads and reads a file associated with a GAIA task by its task_id. "
        "Returns the text content of the file. Use this when the question references "
        "an attached file, spreadsheet, or document."
    )
    inputs = {
        "task_id": {
            "type": "string",
            "description": "The task_id of the question whose file you want to read.",
        }
    }
    output_type = "string"

    def _detect_type(self, response: requests.Response) -> str:
        content_type = response.headers.get("Content-Type", "")
        disposition = response.headers.get("Content-Disposition", "")

        # Check filename in Content-Disposition header
        if "filename=" in disposition:
            fname = disposition.split("filename=")[-1].strip("\"' ")
            ext = fname.rsplit(".", 1)[-1].lower() if "." in fname else ""
            ext_map = {
                "xlsx": "excel", "xls": "excel",
                "pdf": "pdf",
                "csv": "csv",
                "json": "json",
                "txt": "text", "md": "text", "py": "text",
            }
            if ext in ext_map:
                return ext_map[ext]

        if "spreadsheet" in content_type or "excel" in content_type:
            return "excel"
        if "pdf" in content_type:
            return "pdf"
        if "csv" in content_type:
            return "csv"
        if "text" in content_type or "json" in content_type:
            return "text"
        return "unknown"

    def forward(self, task_id: str) -> str:
        url = f"{DEFAULT_API_URL}/files/{task_id}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"Error downloading file: {e}"

        file_type = self._detect_type(response)

        # Text / CSV / JSON
        if file_type in ("text", "csv", "json"):
            return response.text[:10000]

        # Excel files
        if file_type == "excel":
            try:
                import pandas as pd
                import io

                df = pd.read_excel(io.BytesIO(response.content))
                return df.to_string()
            except Exception as e:
                return f"Error reading Excel file: {e}"

        # PDF files
        if file_type == "pdf":
            try:
                import io
                import PyPDF2

                reader = PyPDF2.PdfReader(io.BytesIO(response.content))
                text = ""
                for page in reader.pages[:20]:
                    text += page.extract_text() + "\n"
                return text[:10000]
            except Exception as e:
                return f"Error reading PDF: {e}"

        # Fallback: try as text, then try as Excel
        try:
            text = response.text
            if text and text[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#\"'{[":
                return text[:10000]
        except Exception:
            pass

        try:
            import pandas as pd
            import io

            df = pd.read_excel(io.BytesIO(response.content))
            return df.to_string()
        except Exception:
            return f"File downloaded but could not parse. Content-Type: {response.headers.get('Content-Type', '')}, Size: {len(response.content)} bytes"


class CalculatorTool(Tool):
    name = "calculator"
    description = (
        "Evaluates a mathematical expression and returns the result. "
        "Supports basic arithmetic, powers, roots, etc. "
        "Input should be a valid Python math expression as a string."
    )
    inputs = {
        "expression": {
            "type": "string",
            "description": "A mathematical expression to evaluate, e.g. '2 + 3 * 4' or 'round(15.7)'",
        }
    }
    output_type = "string"

    def forward(self, expression: str) -> str:
        import math

        allowed = {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "len": len, "int": int, "float": float,
            "pow": pow, "sorted": sorted,
        }
        allowed.update({k: getattr(math, k) for k in dir(math) if not k.startswith("_")})

        try:
            result = eval(expression, {"__builtins__": {}}, allowed)
            return str(result)
        except Exception as e:
            return f"Error evaluating expression: {e}"


class StringReverseTool(Tool):
    name = "reverse_string"
    description = "Reverses a given string. Useful for tasks that ask for reversed text."
    inputs = {
        "text": {
            "type": "string",
            "description": "The text to reverse.",
        }
    }
    output_type = "string"

    def forward(self, text: str) -> str:
        return text[::-1]
