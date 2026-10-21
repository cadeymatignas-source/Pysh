lazy import os
lazy import re
lazy import shlex
lazy import subprocess
lazy import sys
lazy import time
lazy import tomllib
lazy from pathlib import Path

lazy from termcolor import colored

platform = os.name
system = sys.platform
config_path = Path.home() / ".pysh.toml"
config_py_path = Path.home() / ".pyshrc"


if not config_path.exists():
	print("Hello new user. Generating .pysh.toml")

	config_path.parent.mkdir(parents=True, exist_ok=True)

	if system == "win32":
		config_path.write_text(
			"""package_manager = "winget"
	User = "root"
	prompt_color = "magenta"
	use_uv = false
	use_uv-publish = false
	AUTOCD = true
	"""
		)

	elif system == "linux":
		config_path.write_text(
			"""package_manager = "sudo apt"
	User = "root"
	prompt_color = "magenta"
	use_uv = false
	use_uv-publish = false
	AUTOCD = true
	"""
		)
	elif system == "darwin":
		config_path.write_text(
			"""package_manager = "brew"
	User = "root"
	prompt_color = "magenta"
	use_uv = false
	use_uv-publish = false
	AUTOCD = true
	"""
		)

if not config_py_path.exists():
	print("Generating .pyshrc")

	config_py_path.parent.mkdir(parents=True, exist_ok=True)

	config_py_path.write_text("# Put code here, to run once before the main code.")

with config_path.open("rb") as f:
	config = tomllib.load(f)

exec(config_py_path.read_text())

variables = {"USER": config["User"], "SHELL": sys.executable, "HOME": Path.home(), "USERPROFILE": Path.home()}


def expand_vars(text):
	for name, value in variables.items():
		text = text.replace(f"${name}", str(value))
	return text


print(colored(f"Welcome to the python terminal, {config['User']}!", "blue"))
change = False
while True:
	try:
		if not change:
			temp = colored(f"PT -> {Path.cwd()}> ", config["prompt_color"])
		prompter = temp
		cmd = input(prompter).strip()

		commands = [c.strip() for c in re.split(r"&&|;|&", cmd) if c.strip()]
		has_and = "&&" in commands
		success = True
		for command in commands:
			if command.lower() == "exit":
				print("Goodbye!")
				sys.exit()
			elif command.lower() == "coolguy38 is sigma":
				print("Yes, im sigma B)")
			elif command == "cd" or command == "pwd":
				print(Path.cwd())

			elif command.lower().startswith("cd "):
				path = command[3:].strip().strip("'\"")

				try:
					os.chdir(expand_vars(path))

				except Exception as e:
					print(colored(f"{type(e)} happened with message {e}.", "red"))
					success = False

			elif command.lower().startswith("prompt "):
				temp = command[7:] + " "
				change = True
			elif command.lower() == "reset prompt" or command.lower() == "prompt":
				change = False

			elif command.lower() == "help":
				print(
					"""- help: explains every command
- coolguy38 is sigma: responds
- reset prompt: Resets the prompt
- prompt: Also resets the prompt
- pwd: Prints the current working directory
- pyexe <text>: Runs pyinstaller --onefile for you. If it reaches an error it asks you if you want to download pyinstaller
- pypub <text>: Builds and publishes your library to pypi. If it reaches an error it asks you if you want to download twine and build
- pack get: use this like the package manager you chose. (like pack get install Git.git if using winget)
- os: prints your os
- view <path>: Its basically cat but with syntax highlighting
- prompt <text>: Changes the prompt to <text>
- echo <text>: Prints <text>
- ls/dir: Lists the current directory
- ls <path>/dir <path>: Lists the directory at <path>
- md/mkdir <dir>: Makes a directory called <dir>
- time: Prints the current time
- cls/clear: Clears the terminal
- cd <path>: Changes the current directory to <path>
- cat <file>: Prints the contents of <file>
- <file>.pysh: Runs the .pysh file"""
				)

			elif command.lower().startswith("pyexe "):
				pyn = command[6:].strip()
				pynn = subprocess.run([config["shell"], config["arg"], f"pyinstaller --onefile {pyn}"], capture_output=True)
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
					success = False
			elif command.lower().startswith("pypub "):
				if config["use_uv"]:
					pyb = command[6:].strip()
					if config["use_uv-publish"]:
						pybb = subprocess.run(
							[
								config["shell"],
								config["arg"],
								f"uv build && uv-publish && uv pip install --upgrade --system {pyb}",
							],
							capture_output=True,
						)
					else:
						pybb = subprocess.run(
							[
								config["shell"],
								config["arg"],
								f"uv build && uv publish && uv pip install --upgrade --system {pyb}",
							],
							capture_output=True,
						)
				else:
					pyb = command[6:].strip()
					pybb = subprocess.run(
						[
							config["shell"],
							config["arg"],
							f"python -m build && python -m twine check dist/* && python -m twine upload dist/* && pip install --upgrade {pyb}",
						],
						capture_output=True,
					)
				if pybb.returncode != 0:
					if config["use_uv"]:
						downl = input("Oh no! Something failed! Download uv and uv-publish? (y/N)")
						match downl.lower():
							case "y":
								subprocess.run([config["shell"], config["arg"], "pipx install uv && uv tool install uv-publish"], capture_output=True)
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
					success = False
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
					success = False
			elif command.lower() == "os":
				print(system)

			elif command.lower().startswith("view "):
				viewed = command[5:].strip()

				viewer = subprocess.run(f"pygmentize {expand_vars(viewed)}", capture_output=True, shell=True)
				if viewer.returncode != 0:
					print(colored("File not found: Are you in the correct directory? Or is the file nonexistent?", "red"))
					success = False
			elif command.lower().startswith("cat "):
				file = command[4:].strip()

				try:
					print(expand_vars(Path(file).read_text()))
				except FileNotFoundError:
					print(colored(f"File {file} not found", "red"))
					success = False
			elif command.lower().startswith("echo "):
				echoed = command[5:].strip()
				print(expand_vars(echoed))
			elif command.lower() in ["ls", "dir"]:
				path = "."
				try:
					for entry in os.listdir(path):
						print(entry)
				except FileNotFoundError:
					print(f"Directory {path} not found")
					success = False
				except PermissionError:
					print(f"Permission denied to access {path}. Make sure you have permissions to view this directory.")
					success = False
			elif command.lower().startswith("ls "):
				pather = command[3:].strip()
				path = expand_vars(pather.strip("'\""))
				try:
					for entry in os.listdir(path):
						print(entry)
				except FileNotFoundError:
					print(f"Directory {path} not found")
					success = False
				except PermissionError:
					print(f"Permission denied to access {path}. Make sure you have permissions to view this directory.")
					success = False
			elif command.lower() == "setup":
				print("Setting up the python terminal...")
				subprocess.run(
					[config["shell"], config["arg"], "pip install --upgrade pygments "], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
				)
			elif command.lower().endswith(".pysh") or command.lower().endswith(".py") and not command.lower().startswith("python"):
				try:
					exec(Path(command).read_text())
				except FileNotFoundError:
					print(colored(f"File {command} not found", "red"))
					success = False

			elif command.lower().startswith("md "):
				makedir = command[3:].strip().strip("'\"")
				try:
					Path(makedir).mkdir(exist_ok=True)
				except PermissionError:
					print(f"You can't make a directory in {Path.cwd()}")
					success = False
			elif command.lower().startswith("mkdir "):
				makedir = command[6:].strip().strip("'\"")
				try:
					Path(makedir).mkdir(exist_ok=True)
				except PermissionError:
					print(f"You can't make a directory in {Path.cwd()}")
					success = False
			elif command.lower() == "time":
				print(time.strftime("%I:%M %p"))
			elif command.lower() in ["cls", "clear"]:
				subprocess.run("cls" if platform == "nt" else "clear", stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=True)

			else:
				if config["AUTOCD"]:
					try:
						os.chdir(expand_vars(command))
					except Exception:
						args = shlex.split(command)
						subprocess.run(args, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
				else:
					args = shlex.split(command)
					subprocess.run(args, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
			if not success and has_and:
				break

	except KeyboardInterrupt:
		print("^C")
		continue
	except EOFError:
		print("^D")
		print("Goodbye!")
		sys.exit()
	except Exception as e:
		print(colored(f"Error {e} with type {type(e)}", "red"))
