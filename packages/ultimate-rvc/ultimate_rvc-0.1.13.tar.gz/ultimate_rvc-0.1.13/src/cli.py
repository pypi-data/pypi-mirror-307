"""
Main entry point for the cli application of the Ultimate RVC
project.
"""

import time

from cli.main import app

end = time.time()
if __name__ == "__main__":
    app()
