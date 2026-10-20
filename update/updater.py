import urllib.request
from sys import platform

if platform == "linux":
	url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Pysh-Linux.zip"
	destination = "Pysh-Linux.zip"
elif platform == "darwin":
	url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Pysh-macOS.zip"
	destination = "Pysh-macOS.zip"
elif platform == "win32":
	url = "https://github.com/cadeymatignas-source/Pysh/releases/latest/download/Pysh-Windows.zip"
	destination = "Pysh-Windows.zip"
try:
	print("Downloading new version")
	urllib.request.urlretrieve(url, destination)
	print("Download complete!")
except Exception as e:
	print(f"An error occurred: {e}")
