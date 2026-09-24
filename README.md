# Pysh (PYthon SHell)

## This is a terminal shell I made with python

It uses cmd under the hood to run terminal commands, but you can configure it to use a different shell.

It has:

- Cmd commands;
- A custom python REPL;
- And custom commands

## Every custom command

- help: explains every command
- prompt (text): Changes the prompt to the text after it
- prompt: Resets prompt
- reset prompt: Also resets prompt
- Coolguy38 is sigma: It responds
- pwd: Prints the current working directory
- pyexe: Runs pyinstaller --onefile for you. If it reaches an error it asks you if you want to download pyinstaller
- pypub: Builds and publishes your library to pypi. If it reaches an error it asks you if you want to download twine and build
- pack get: use this like the package manager you chose. (like pack get install Git.git if using winget)
