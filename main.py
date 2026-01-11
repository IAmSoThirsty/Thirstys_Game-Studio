import importlib
import pkgutil
import sys


def find_app_module():
    """Attempt to find and import a package or module named 'app' in the current directory."""
    for finder, name, ispkg in pkgutil.iter_modules(["."]):
        if name == "app":
            return importlib.import_module("app")
    # try as a top-level package (in case run from src layout)
    try:
        return importlib.import_module("app")
    except ModuleNotFoundError:
        return None

def main():
    app_module = find_app_module()
    if app_module is None:
        print("[INFO] No 'app' package or module found.\n"
              "To get started, create an 'app' directory or app.py file in the root of this project.\n"
              "The entry point will attempt to run app.main() if defined, otherwise amend main.py.")
        sys.exit(1)
    # Attempt to call an app.main() if it exists
    if hasattr(app_module, "main"):
        print("[INFO] Running app.main()...")
        app_module.main()
    else:
        print("[INFO] Found 'app', but no 'main()' entry point. Implement app.main() to launch your game or app.")

if __name__ == "__main__":
    main()
