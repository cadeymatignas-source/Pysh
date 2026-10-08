import sys
from os import name
from subprocess import run

from prompt_toolkit import prompt
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import PythonLexer
from termcolor import colored


def main():
	platform = name

	print(sys.version)

	while True:
		pyi = prompt("> ", lexer=PygmentsLexer(PythonLexer))

		if pyi.lower() in ("exit", "exit()"):
			break

		elif pyi.lower() in ("cls", "clear"):
			if platform == "nt":
				run("cls", shell=True)
			else:
				run("clear", shell=True)

		elif pyi.startswith(("pip ", "uv ")):
			run(
				pyi,
				shell=True,
				stdin=sys.stdin,
				stdout=sys.stdout,
				stderr=sys.stderr,
			)

		else:
			try:
				exec(pyi)

			except IndentationError:
				block = [pyi]

				while True:
					extra = prompt("-> ", lexer=PygmentsLexer(PythonLexer))

					if not extra:
						break

					block.append(extra)

				exec("\n".join(block))

			except Exception as e:
				print(colored(f"{type(e)} happened with message {e}", "red"))
