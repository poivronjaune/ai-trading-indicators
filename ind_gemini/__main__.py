# ind/__main__.py

"""
Allows the package to be executed as a script via `python -m ind`.

This will launch the interactive command-line interface for processing
financial data files.
"""

from .cli import main

if __name__ == "__main__":
    main()
    