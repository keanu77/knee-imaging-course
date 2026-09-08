"""Run the DOM-independent JavaScript search regression harness in make test."""
import subprocess
from pathlib import Path

subprocess.run(["node", str(Path(__file__).with_name("search_aliases.mjs"))], check=True)
