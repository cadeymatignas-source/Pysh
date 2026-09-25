import os
import subprocess
import sys
import tomllib
from pathlib import Path
from time import sleep

from termcolor import colored

config_path = Path.home() / ".pysh" / "config.toml"

if not config_path.exists():
	print("Hello new user. Generating config.toml")

	config_path.parent.mkdir(parents=True, exist_ok=True)

	config_path.write_text("""package_manager = "winget"
User = "root"
shell = "cmd.exe"
arg = "/c"
""")

with config_path.open("rb") as f:
	config = tomllib.load(f)

print(colored(f"Welcome to the python terminal, {config['User']}!", "blue"))
change = False
while True:
	try:
		if not change:
			temp = colored(f"PT -> {os.getcwd()}> ", "magenta")
		prompt = temp
		cmd = input(prompt).strip()
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
			elif command.lower() == "python":
				print(sys.version)
				while True:
					pyi = input(">")
					if pyi.lower() == "exit" or pyi.lower() == "exit()":
						break
					elif pyi.lower() == "cls" or pyi.lower() == "clear":
						subprocess.run([config["shell"], config["arg"], "cls"], shell=True)
					else:
						try:
							exec(pyi)
						except IndentationError:
							blockly = [pyi]
							while True:
								extra = input("->")
								if extra == "":
									break
								blockly.append(extra)
							exec("\n".join(blockly))
						except Exception as e:
							print(f"{type(e)} happened with message {e}.")
			elif command.lower() == "cd" or command.lower() == "pwd":
				print(os.getcwd())

			elif command.lower().startswith("cd "):
				path = command[3:].strip().strip("'\"")

				try:
					os.chdir(path)

				except Exception as e:
					print(colored(f"{type(e)} happened with message {e}.", "red"))

			elif command.lower().startswith("prompt "):
				temp = command[7:].strip()
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
- pack get: use this like the package manager you chose. (like pack get install Git.git if using winget)"""
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
								shell=True,
								stdin=sys.stdin,
								stdout=sys.stdout,
								stderr=sys.stderr,
							)
						case "n":
							print("Ok")
			elif command.lower().startswith("pypub "):
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
					downl = input("Oh no! Something failed! Download build and twine? (y/N)")
					match downl.lower():
						case "y":
							subprocess.run(
								[config["shell"], config["arg"], "pip install build twine"],
								shell=True,
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

			else:
				try:
					subprocess.run([config["shell"], config["arg"], command], shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

				except Exception as e:
					print(colored(f"Error {e} with type {type(e)}", "red"))
	except KeyboardInterrupt:
		continue
