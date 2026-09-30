# Pysh (PYthon SHell)

## This is a terminal shell I made with python

It uses cmd under the hood to run terminal commands, but you can configure it to use a different shell.

It has:

- Cmd commands;
- A custom python REPL;
- And custom commands

## Every custom command

- help: explains every command
- prompt (text): changes the prompt to the text after it
- prompt: resets prompt
- reset prompt: also resets prompt
- Coolguy38 is sigma: it responds
- pwd: prints the current working directory
- os: prints the current OS
- cd: also prints the current working directory
- pyexe: runs pyinstaller --onefile for you. If it reaches an error it asks you if you want to download pyinstaller
- pypub: builds and publishes your library to pypi. If it reaches an error it asks you if you want to download twine and build
- pack get: use this like the package manager you chose. (like pack get install Git.git if using winget)

- pythoner: this is the custom python repl, now put into a seperate keyword

- view: pysh's equivalent to bat
