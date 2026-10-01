lazy import subprocess
lazy import sys
lazy import tomllib
lazy from os import chdir, name
lazy from pathlib import Path
lazy from time import sleep

lazy from prompt_toolkit import prompt
lazy from prompt_toolkit.lexers import PygmentsLexer
lazy from pygments.lexers import PythonLexer
lazy from termcolor import colored

platform = name

config_path = Path.home() / ".pysh" / "config.toml"
config_py_path = Path.home() / ".pysh" / "config.py"

if not config_path.exists():
	print("Hello new user. Generating config.toml")

	config_path.parent.mkdir(parents=True, exist_ok=True)

	config_path.write_text(
		"""package_manager = "winget"
User = "root"
shell = "cmd.exe"
arg = "/c"
prompt_color = "magenta"
use_uv = false
use_uv-publish = false
"""
		if platform == "nt"
		else """package_manager = "sudo apt"
User = "root"
shell = "bash"
arg = "-c"
prompt_color = "magenta"
use_uv = false
use_uv-publish = false
"""
	)

if not config_py_path.exists():
	print("Generating config.py")

	config_py_path.parent.mkdir(parents=True, exist_ok=True)

	config_py_path.write_text("# Put code here, to run once before the main code.")

with config_path.open("rb") as f:
	config = tomllib.load(f)

exec(config_py_path.read_text())

print(colored(f"Welcome to the python terminal, {config['User']}!", "blue"))
change = False
while True:
	try:
		if not change:
			temp = colored(f"PT -> {Path.cwd()}> ", config["prompt_color"])
		prompter = temp
		cmd = input(prompter).strip()
		commands = [c.strip() for c in cmd.split("&&")]

		for command in commands:
			if command.lower() == "exit":
				print("Goodbye!")
				sleep(0.5)
				sys.exit()
			elif command.lower() == "coolguy38 is sigma":
				print("Yes, im sigma B)")
			elif command == "":
				print("Empty command")
			elif command.lower() == "pythoner":
				print(sys.version)
				while True:
					pyi = prompt(">", lexer=PygmentsLexer(PythonLexer))

					if pyi.lower() in ("exit", "exit()"):
						break
					elif pyi.lower() in ("cls", "clear"):
						if platform.lower() == "nt":
							subprocess.run([config["shell"], config["arg"], "cls"])
						else:
							subprocess.run([config["shell"], config["arg"], "clear"])
					elif pyi.startswith("pip ") or pyi.startswith("uv "):
						subprocess.run([config["shell"], config["arg"], pyi])
					else:
						try:
							exec(pyi)
						except IndentationError:
							blockly = [pyi]
							while True:
								extra = prompt("->", lexer=PygmentsLexer(PythonLexer))
								if extra == "":
									break
								blockly.append(extra)
							exec("\n".join(blockly))
						except Exception as e:
							print(f"{type(e)} happened with message {e}.")

			elif command == "cd" or command == "pwd":
				print(Path.cwd())

			elif command.lower().startswith("cd "):
				path = command[3:].strip().strip("'\"")

				try:
					chdir(path)

				except Exception as e:
					print(colored(f"{type(e)} happened with message {e}.", "red"))

			elif command.lower().startswith("prompt "):
				temp = command[7:]
				change = True
			elif command.lower() == "reset prompt" or command.lower() == "prompt":
				change = False

			elif command.lower() == "help":
				subprocess.run([config["shell"], config["arg"], "help"], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
				yes = input("Would you like more? (y/N)")
				match yes.lower():
					case "y":
						print(
							"""- help: explains every command
- coolguy38 is sigma: responds
- reset prompt: Resets the prompt
- prompt: Also resets the prompt
- pwd: Prints the current working directory
- pyexe: Runs pyinstaller --onefile for you. If it reaches an error it asks you if you want to download pyinstaller
- pypub: Builds and publishes your library to pypi. If it reaches an error it asks you if you want to download twine and build
- pack get: use this like the package manager you chose. (like pack get install Git.git if using winget)
- pythoner: this is the custom python REPL
- os: prints your os
- view: Its basically cat but with syntax highlighting"""
						)
					case "n":
						continue
			elif command.lower().startswith("pyexe "):
				pyn = command[6:].strip()
				pynn = subprocess.run(
					[config["shell"], config["arg"], f"pyinstaller --onefile {pyn}"], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
				)
				if pynn.returncode != 0:
					down = input("Oh no! Pyinstaller failed. Download? (y/N)")
					match down.lower():
						case "y":
							subprocess.run(
								[config["shell"], config["arg"], "pip install pyinstaller"],
								stdin=sys.stdin,
								stdout=sys.stdout,
								stderr=sys.stderr,
							)
						case "n":
							print("Ok")
			elif command.lower().startswith("pypub "):
				if config["use_uv"]:
					pyb = command[6:].strip()
					if config["use_uv-publish"]:
						pybb = subprocess.run(
							[
								config["shell"],
								config["arg"],
								f"uv build && uv-publish && uv pip install --upgrade {pyb}",
							],
							stdin=sys.stdin,
							stdout=sys.stdout,
							stderr=sys.stderr,
						)
					else:
						pybb = subprocess.run(
							[
								config["shell"],
								config["arg"],
								f"uv build && uv publish && uv pip install --upgrade {pyb}",
							],
							stdin=sys.stdin,
							stdout=sys.stdout,
							stderr=sys.stderr,
						)
				else:
					pyb = command[6:].strip()
					pybb = subprocess.run(
						[
							config["shell"],
							config["arg"],
							f"python -m build && python -m twine check dist/* && python -m twine upload dist/* && pip install --upgrade {pyb}",
						],
						stdin=sys.stdin,
						stdout=sys.stdout,
						stderr=sys.stderr,
					)
				if pybb.returncode != 0:
					if config["use_uv"]:
						downl = input("Oh no! Something failed! Download uv and uv-publish? (y/N)")
						match downl.lower():
							case "y":
								subprocess.run(
									[config["shell"], config["arg"], "pipx install uv && uv tool install uv-publish"],
									stdin=sys.stdin,
									stdout=sys.stdout,
									stderr=sys.stderr,
								)
							case "n":
								print("Ok")
					else:
						downl = input("Oh no! Something failed! Download build and twine? (y/N)")
						match downl.lower():
							case "y":
								subprocess.run(
									[config["shell"], config["arg"], "pipx install build twine"],
									stdin=sys.stdin,
									stdout=sys.stdout,
									stderr=sys.stderr,
								)
							case "n":
								print("Ok")
			elif command.lower().startswith("pack get "):
				getd = command[9:].strip()
				subprocess.run(
					[config["shell"], config["arg"], f"{config['package_manager']} {getd}"], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
				)
			elif command.lower() == "whoami":
				print(f"You are {config['User']}")

			elif command.lower().endswith(")"):
				try:
					exec(command)
				except NameError:
					print(colored(f"Command {command} doesnt exist", "red"))
			elif command.lower() == "os":
				print("Windows" if platform == "nt" else "POSIX - like MacOS or Linux")

			elif command.lower().startswith("view "):
				viewed = command[5:].strip()

				viewer = subprocess.run(
					[config["shell"], config["arg"], f"pygmentize {viewed}"], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
				)
				if viewer.returncode != 0:
					print(colored("File not found: Are you in the correct directory? Or is the file nonexistent?", "red"))
			else:
				try:
					subprocess.run([config["shell"], config["arg"], command], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

				except Exception as e:
					print(colored(f"Error {e} with type {type(e)}", "red"))
	except KeyboardInterrupt:
		continue
