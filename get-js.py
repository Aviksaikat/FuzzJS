#!/usr/bin/python3
from re import sub
import argparse
from concurrent.futures import ThreadPoolExecutor
from requests import get
from sys import argv
import os 
from colorama import Fore, Style
#import wget

def get_file(url):
	url = url.strip()
	fname = sub(r"(https?:\/\/)(\s)*", '', url).replace('/','-')
	#wget.download(url, './')
	print(f"{Fore.YELLOW}[*]{Fore.GREEN}Getting:{Fore.BLUE} {url}")
	r = get(url, allow_redirects=True, verify=False, timeout=5)

	#print("Dhoom")
	with open(f"./{args.out}/{fname}", "wb") as f:
		f.write(r.content)

def main():
	parser = argparse.ArgumentParser(description="File downloader")
	parser.add_argument("-f", "--files", type=str, help="File containing URL files")
	parser.add_argument('-t', '--threads', help='Number of threads (default 15)', type=int, default=15)
	parser.add_argument("-o", "--out", type=str, help="Output directory")
	args = parser.parse_args()
	#parser.add_argument("-f", type=str, help="pass the file containing urls")
	# if len(argv) != 2:
	# 	print(f"[!]See Usage: {argv[0]} -h")
	# 	exit(-1)

	url_list = open(args.files).readlines()
	
	"""
	Syntax: os.mkdir(path, mode = 0o777, *, dir_fd = None)

	Parameter:
	path: A path-like object representing a file system path. A path-like object is either a string or bytes object representing a path.
	mode (optional): A Integer value representing mode of the directory to be created. If this parameter is omitted then default value Oo777 is used.
	dir_fd (optional): A file descriptor referring to a directory. The default value of this parameter is None.
	If the specified path is absolute then dir_fd is ignored.

	Note: The ‘*’ in parameter list indicates that all following parameters (Here in our case ‘dir_fd’) are keyword-only parameters and they can be provided using their name, not as positional parameter.

	Return Type: This method does not return any value.
	"""
	
	path = os.path.join("./", args.out)
	os.mkdir(path)
	#file.get_file(url)

	print(f"{Fore.YELLOW}[*]{Fore.GREEN}Downloading the files....")
	with ThreadPoolExecutor(max_workers=args.threads) as executor:
		for url in url_list:
			f = executor.submit(get_file, url)
			#print(f.result())

if __name__ == '__main__':
	main()

