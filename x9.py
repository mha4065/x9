#!/usr/bin/env python3

from argparse import ArgumentParser,RawTextHelpFormatter
import sys
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

parser = ArgumentParser(add_help=False, formatter_class=RawTextHelpFormatter)
parser.add_argument('-u', '--url', nargs='?', type=str, default='', help="Single URL to edit")
parser.add_argument('-l', '--list', nargs='?', type=str, default='', help="List of URLs to edit")
parser.add_argument('-p', '--parameters', nargs='?', type=str, default='', help="Parameter wordlist to fuzz")
parser.add_argument('-c', '--chunk', type=int, default=15, help="Chunk to fuzz the parameters. [default: 15]")
parser.add_argument('-v', '--value', action='append', help='Value for parameters to fuzz')
parser.add_argument('-gs', '--generate_strategy', choices=['normal', 'ignore', 'combine', 'all'], default='all', help="""Select the mode strategy from the available choice:
    normal: Remove all parameters and put the wordlist
    combine: Pitchfork combine on the existing parameters
    ignore: Don't touch the URL and put the wordlist
    all: All in one method""")
parser.add_argument('-vs', '--value_strategy', choices=['replace', 'suffix'], default='replace', help="""Select the mode strategy from the available choices:
    replace: Replace the value with gathered value
    suffix: Append the value to the end of the parameters""")
parser.add_argument('-o', '--output', type=str, default='', help="Output results")
parser.add_argument('-s', '--silent', help="Silent mode", action="store_true")
parser.add_argument('-h', '--help', action='store_true', help='Display help message')

args = parser.parse_args()

class colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NOCOLOR = '\033[0m'

if args.help:
    parser.print_help()
    sys.exit()

if not args.value:
    print()
    print(colors.RED + "Please enter your desired value as parameter value to fuzz !!!" + colors.NOCOLOR)
    print()
    print()
    print()
    parser.print_help()
    sys.exit()


def banner(colors):
    print("            ___  ")
    print("     __  __/ _ \ ")
    print("     \ \/ / (_) |")
    print("      >  < \__, |")
    print("     /_/\_\  /_/ ")
    print("                 ")
    print(colors.CYAN + " Developed by MHA    " + colors.NOCOLOR)
    print(colors.YELLOW + "     mha4065.com" + colors.NOCOLOR)
    print()
    print()

if not args.silent:
    banner(colors)

class Ignore:
    def __init__(self, urls, payload, wordlist):
        self.urls = urls
        self.payload = payload
        self.parameters = wordlist

    def update_url_parameters(self, url, payload):
        url_parts = urlparse(url)

        query_params = parse_qs(url_parts.query)
        
        for param in self.parameters:
            if param in query_params:
                del query_params[param]
        
        for param in self.parameters:
            query_params[param] = [payload]
        
        encoded_params = urlencode(query_params, doseq=True)
        
        updated_url_parts = list(url_parts)
        updated_url_parts[4] = encoded_params
        
        return urlunparse(updated_url_parts)

    def ignore_mode(self):
        try:
            if self.parameters:
                for url in self.urls:
                    for payload in self.payload:
                        url = self.update_url_parameters(url, payload)
                        results.append(url)
            else:
                print()
                print(colors.RED + "Please enter your parameter list as a text file !!!" + colors.NOCOLOR)
                print()
                print()
                print()
                parser.print_help()
                sys.exit()
        except Exception as e:
            print(e)

class Normal:
    def __init__(self, urls, payload, wordlist=None):
        self.urls = urls
        self.payload = payload
        self.wordlist = wordlist

    def replace_parameters(self, url, payload):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        query_params_copy = query_params.copy()

        if self.wordlist:
            for param in query_params_copy.keys():
                del query_params[param]

            for param in self.wordlist:
                query_params[param] = payload
        else:
            for param in query_params:
                query_params[param] = payload

        new_query = urlencode(query_params, doseq=True)
        new_parsed_url = parsed_url._replace(query=new_query)
        new_url = urlunparse(new_parsed_url)

        return new_url
    
    def normal_mode(self):
        try:
            for url in self.urls:
                for payload in self.payload:
                    new_url = self.replace_parameters(url, payload)
                    results.append(new_url)
        except Exception as e:
            print(e)

class Combine:
    def __init__(self, urls, payload, wordlist=None):
        self.urls = urls
        self.payload = payload
        self.parameters = wordlist

    def update_url_parameters(self, url):
        url_parts = urlparse(url)
        query_params = parse_qs(url_parts.query)
        
        for param in self.parameters:
            if param in query_params:
                del query_params[param]
        
        for param in self.parameters:
            query_params[param] = self.payload
        
        encoded_params = urlencode(query_params, doseq=True)
        
        updated_url_parts = list(url_parts)
        updated_url_parts[4] = encoded_params
        
        return urlunparse(updated_url_parts)

    def suffix(self, url, param, payload):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query, keep_blank_values=True)
        
        for key, values in query_params.items():
            for i in range(len(values)):
                if values[i] == param:
                    values[i] = param + payload

        new_query_string = urlencode(query_params, doseq=True)

        new_url = urlunparse(parsed_url._replace(query=new_query_string))
        if self.parameters:
            new_url = self.update_url_parameters(new_url)
        return new_url

    def suffix_mode(self):
        try:
            for url in self.urls:
                for payload in self.payload:
                    new_urls = []
                    parsed_url = urlparse(url)
                    query_params = parse_qs(parsed_url.query, keep_blank_values=True)

                    for key in query_params.keys():
                        for value in query_params[key]:
                            new_url = self.suffix(url, value, payload)
                            new_urls.append(new_url)

                    for new_url in new_urls:
                        results.append(new_url)
        except Exception as e:
            print(e)

    def replace(self, url, param, payload):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query, keep_blank_values=True)
        
        for key, values in query_params.items():
            for i in range(len(values)):
                if values[i] == param:
                    values[i] = payload

        new_query_string = urlencode(query_params, doseq=True)

        new_url = urlunparse(parsed_url._replace(query=new_query_string))
        if self.parameters:
            new_url = self.update_url_parameters(new_url)
        return new_url

    def replace_mode(self):
        try:
            for url in self.urls:
                for payload in self.payload:
                    new_urls = []
                    parsed_url = urlparse(url)
                    query_params = parse_qs(parsed_url.query, keep_blank_values=True)

                    for key in query_params.keys():
                        for value in query_params[key]:
                            new_url = self.replace(url, value, payload)
                            new_urls.append(new_url)

                    for new_url in new_urls:
                        results.append(new_url)
        except Exception as e:
            print(e)

def file_to_list(filename, num_lines):
    lines = []
    with open(filename, 'r') as file:
        for i in range(num_lines):
            line = file.readline().strip()
            if not line:
                break
            lines.append(line)
    return lines

results = []

def generators(url, values, parameters):
    if args.generate_strategy == "normal":
        normal = Normal(url, values, parameters)
        normal.normal_mode()
    elif args.generate_strategy == "ignore":
        ignore = Ignore(url, values, parameters)
        ignore.ignore_mode()
    elif args.generate_strategy == "combine":
        if args.value_strategy == "suffix":
            combine = Combine(url, values, parameters)
            combine.suffix_mode()
        else:
            combine = Combine(url, values, parameters)
            combine.replace_mode()
    else:
        normal = Normal(url, values, parameters)
        normal.normal_mode()
        ignore = Ignore(url, values, parameters)
        ignore.ignore_mode()
        if args.value_strategy == "suffix":
            combine = Combine(url, values, parameters)
            combine.suffix_mode()
        else:
            combine = Combine(url, values, parameters)
            combine.replace_mode()

if args.list != '':
    try:
        urls = [line.strip() for line in open(args.list)]
        urls = list(set(urls))
        complete_urls = []
        for url in urls:
            if not url.startswith("http://") and not url.startswith("https://"):
                complete_urls.append("https://{}".format(url))
            else:
                complete_urls.append(url)
        
        values = []
        for payload in args.value:
            values.append(payload)
                        
        if args.parameters != "":
            wordlists = file_to_list(args.parameters, args.chunk)
        else:
            wordlists = []

        generators(complete_urls, values, wordlists)

        if len(results) > 0:
            results = list(set(results))

            # Output
            if args.output == '':
                for res in results:
                    if res:
                        print(res)
            else:
                for res in results:
                    if res:
                        print(res)
                        with open(args.output, 'a') as f:
                            f.write(res+'\n')
    except Exception as e:
        print(e)
    
elif args.url != '':
    try:
        url = args.url
        complete_urls = []
        if not url.startswith("http://") and not url.startswith("https://"):
            complete_urls.append("https://{}".format(url))
        else:
            complete_urls.append(url)

        values = []
        for payload in args.value:
            values.append(payload)
                        
        if args.parameters != "":
            wordlists = file_to_list(args.parameters, args.chunk)
        else:
            wordlists = []

        generators(complete_urls, values, wordlists)

        if len(results) > 0:
            results = list(set(results))

            # Output
            if args.output == '':
                for res in results:
                    if res:
                        print(res)
            else:
                for res in results:
                    if res:
                        print(res)
                        with open(args.output, 'a') as f:
                            f.write(res+'\n')
    except Exception as e:
        print(e)
else:
    if not sys.stdin.isatty():
        input_urls = [line.strip() for line in sys.stdin.readlines()]
        if len(input_urls) == 1:
            try:
                complete_urls = []

                url = input_urls[0]
                if url:

                    if ',' in url:
                        url = url.split(',')[0]

                    if not url.startswith("http://") and not url.startswith("https://"):
                        complete_urls.append("https://{}".format(url))
                    else:
                        complete_urls.append(url)

                    values = []
                    for payload in args.value:
                        values.append(payload)
                    
                    if args.parameters != "":
                        wordlists = file_to_list(args.parameters, args.chunk)
                    else:
                        wordlists = []

                    generators(complete_urls, values, wordlists)

                    if len(results) > 0:
                        results = list(set(results))

                        # Output
                        if args.output == '':
                            for res in results:
                                if res:
                                    print(res)
                        else:
                            for res in results:
                                if res:
                                    print(res)
                                    with open(args.output, 'a') as f:
                                        f.write(res+'\n')
                else:
                    parser.print_help()
                    sys.exit()
            except Exception as e:
                print(e)
        else:
            input_urls = list(set(input_urls))
            complete_urls = []
            for url in input_urls:
                if not url.startswith("http://") and not url.startswith("https://"):
                    complete_urls.append("https://{}".format(url))
                else:
                    complete_urls.append(url)
            try:
                values = []
                for payload in args.value:
                    values.append(payload)
                    
                if args.parameters != "":
                    wordlists = file_to_list(args.parameters, args.chunk)
                else:
                    wordlists = []

                generators(complete_urls, values, wordlists)
                        
                if len(results) > 0:
                    results = list(set(results))

                    # Output
                    if args.output == '':
                        for res in results:
                            if res:
                                print(res)
                    else:
                        for res in results:
                            if res:
                                print(res)
                                with open(args.output, 'a') as f:
                                    f.write(res+'\n')
            except Exception as e:
                print(e)
    else:
        print()
        print(colors.RED + '[-] ' + colors.NOCOLOR + 'Provide an URL or a file')