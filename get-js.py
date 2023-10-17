#!/usr/bin/python3
import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from re import sub
from sys import argv, exit, stderr

from colorama import Fore, Style
from requests import get

# import wget


class customParser(argparse.ArgumentParser):
    def error(self, message):
        # stderr.write('error: %s\n' % message)
        self.print_help()
        exit(2)


def get_file(url):
    url = url.strip()
    fname = sub(r"(https?:\/\/)(\s)*", "", url).replace("/", "-")
    # wget.download(url, './')
    print(f"{Fore.YELLOW}[*]{Fore.GREEN}Getting:{Fore.BLUE} {url}")
    r = get(url, allow_redirects=True, verify=False, timeout=5)

    # print("Dhoom")
    # print(f"./output/{fname}")
    with open(f"./output/{fname}", "wb") as f:
        f.write(r.content)


def main():
    parser = customParser(description="File downloader")
    parser.add_argument("-f", "--files", type=str, help="File containing URL files")
    parser.add_argument(
        "-t", "--threads", help="Number of threads (default 15)", type=int, default=15
    )
    # parser.add_argument("-o", "--out", type=str, help="Output directory")
    args = parser.parse_args()
    # parser.add_argument("-f", type=str, help="pass the file containing urls")
    # if len(argv) != 2:
    # 	print(f"[!]See Usage: {argv[0]} -h")
    # 	exit(-1)

    try:
        url_list = open(args.files).readlines()
        path = os.path.join("./", "output")
        os.mkdir(path)
        print(f"{Fore.YELLOW}[*]{Fore.GREEN}Downloading the files....{Style.RESET_ALL}")
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            for url in url_list:
                f = executor.submit(get_file, url)
                # print(f.result())

    except Exception as e:
        print(f"{Fore.RED}[!]Error....missing arguments{Style.RESET_ALL}")
        parser.print_help()
        pass


if __name__ == "__main__":
    main()
