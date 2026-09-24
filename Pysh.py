import os
import subprocess
import sys
from time import sleep

from termcolor import colored

print(colored("Welcome to the python terminal!", "blue"))
change = False
while True:
	try:
		if not change:
			temp = f"PT -> {os.getcwd()}> "
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
						subprocess.run("cls", shell=True)
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
				path = command[3:].strip()

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
				subprocess.run("help", shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
				yes = input("Would you like more? (y/N)")
				match yes.lower():
					case "y":
						print(
							"""Help: explains every command
							Coolguy38 is sigma: responds
							reset prompt: Resets the prompt
							prompt: Also resets the prompt
							pwd: Prints the current working directory"""
						)
					case "n":
						continue
			elif command.lower().startswith("pyexe "):
				pyn = command[6:].strip()
				pynn = subprocess.run(f"pyinstaller --onefile {pyn}", shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
				if pynn.returncode != 0:
					down = input("Oh no! Pyinstaller failed. Download? (y/N)")
					match down.lower():
						case "y":
							subprocess.run("pip install pyinstaller", shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
						case "n":
							print("Ok")
			elif command.lower().startswith("pypub "):
				pyb = command[6:].strip()
				pybb = subprocess.run(
					f"python -m build && python -m twine check dist/* && python -m twine upload dist/* && pip install --upgrade {pyb}",
					shell=True,
					stdin=sys.stdin,
					stdout=sys.stdout,
					stderr=sys.stderr,
				)
				if pybb.returncode != 0:
					downl = input("Oh no! Something failed! Download build and twine? (y/N)")
					match downl.lower():
						case "y":
							subprocess.run("pip install build twine", shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
						case "n":
							print("Ok")

			else:
				try:
					subprocess.run(command, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

				except Exception as e:
					print(colored(f"Error {e} with type {type(e)}", "red"))
	except KeyboardInterrupt:
		continue
