from sys import platform

if platform == "emscripten":
    from .pyodide import fetch
else:
    from .non_pyodide import fetch


del platform

__all__ = ["fetch"]
