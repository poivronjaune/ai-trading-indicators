# src/ind/__main__.py
from .cli import main

if __name__ == "__main__":
    # Click requires passing prog_name=None for proper CLI execution
    main(prog_name="indicators")
