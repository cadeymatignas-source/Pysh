import os
import subprocess
import sys
from time import sleep

print("Welcome to the python terminal!")
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
			elif command.lower() == "Coolguy38 is sigma":
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
					print(f"{type(e)} happened with message {e}.")

			elif command.lower().startswith("prompt "):
				temp = command[7:].strip()
				change = True
			elif command.lower() == "reset prompt":
				change = False

			elif command.lower() == "help":
				subprocess.run("help", shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
				yes = input("Would you like more? (y/N)")
				match yes.lower():
					case "y":
						print("Help: explains every command,\nCoolguy38 is sigma: responds, \nreset prompt: Resets the prompt")
					case "N":
						continue
			else:
				try:
					subprocess.run(command, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

				except Exception as e:
					print(f"Error {e} with type {type(e)}")
	except KeyboardInterrupt:
		continue
