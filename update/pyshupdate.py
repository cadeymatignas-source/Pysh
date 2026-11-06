import urllib.request
from sys import platform

version = input("""Choose:
[a] Pysh
[b] Installer
[c] Bundle""")
if version == "a":
	if platform == "linux":
		url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Pysh-Linux.zip"
		destination = "Pysh-Linux.zip"
	elif platform == "darwin":
		url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Pysh-macOS.zip"
		destination = "Pysh-macOS.zip"
	elif platform == "win32":
		url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Pysh-Windows.zip"
		destination = "Pysh-Windows.zip"
elif version == "b":
	if platform == "linux":
		url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Installer-Linux.zip"
		destination = "Installer-Linux.zip"
	elif platform == "darwin":
		url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Installer-macOS.zip"
		destination = "Installer-macOS.zip"
	elif platform == "win32":
		url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Installer-Windows.zip"
		destination = "Installer-Windows.zip"
elif version == "c":
	if platform == "linux":
		url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Pysh-Bundle-Linux.zip"
		destination = "Pysh-Bundle-Linux.zip"
	elif platform == "darwin":
		url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Pysh-Bundle-macOS.zip"
		destination = "Pysh-Bundle-macOS.zip"
	elif platform == "win32":
		url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Pysh-Bundle-Windows.zip"
		destination = "Pysh-Bundle-Windows.zip"
try:
	print("Downloading new version")
	urllib.request.urlretrieve(url, destination)
	print("Download complete!")
except Exception as e:
	print(f"An error occurred: {e}")
