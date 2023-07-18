# x9

<p align="center">
  <a href="#requirements">Requirements</a> •
  <a href="#installation">Installation</a> •
  <a href="#tool-options">Tool options</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">license</a>
</p>

x9 is a fuzzing tool to identify potentially vulnerable parameters in web application which can be scaled up for mass hunting

## Requirements
- Python3

## Installation
  1. `git clone https://github.com/mha4065/x9.git`
  2. `pip3 install -r requirements.txt`
  3. `chmod +x x9.py`
  4. `./x9.py -h`
  
### Note
- You can also download the binary file of the tool from the releases and move it to `/usr/local/bin/` path
- `x9 -h`


### Tool Options
- `-u` or `--url` : Single URL to edit
- `-l` or `--list` : List of URLs to edit
- `-p` or `--parameters` : Parameter wordlist to fuzz
- `-c` or `--chunk` : Chunk to fuzz the parameters. (default: 15)
- `-v` or `--value` : Value for parameters to fuzz
- `-gs` or `--generate_strategy` : Select the mode strategy from the available choice (default all):
					normal: Remove all parameters and put the wordlist
					combine: Pitchfork combine on the existing parameters
					ignore: Don't touch the URL and put the wordlist
					all: All in one method
- `-vs` or `--value_strategy` : Select the mode strategy from the available choices:
					replace: Replace the value with gathered value
					suffix: Append the value to the end of the parameters
- `-o` or `--output` : Output results
- `-s` or `--silent` : Silent mode
- `-h` or `--help` : Display help message


## Usage

Single URL with all methods
```
./x9.py -u "https://domain.tld/?param1=value1&param2=value2" -v '"mhainjected"' -p parameters.txt -c 20
```

List of URLs with all methods
```
./x9.py -l urls.txt -v '"mhainjected"' -p parameters.txt -c 20
```

Multiple value as payload
```
./x9.py -l urls.txt -v '"mhainjected"' -v "'mhainjected'" -v '<b/mhainjected' -p parameters.txt -c 20
```

Normal generation strategy
```
./x9.py -u "https://domain.tld/?param1=value1&param2=value2" -v '"mhainjected"' -p parameters.txt -c 20 -gs normal
```

Combine generation strategy with suffix value strategy
```
./x9.py -u "https://domain.tld/?param1=value1&param2=value2" -v '"mhainjected"' -p parameters.txt -c 20 -gs combine -vs suffix
```

Combine generation strategy with replace value strategy
```
./x9.py -u "https://domain.tld/?param1=value1&param2=value2" -v '"mhainjected"' -p parameters.txt -c 20 -gs combine -vs replace
```

Ignore generation strategy
```
./x9.py -u "https://domain.tld/?param1=value1&param2=value2" -v '"mhainjected"' -p parameters.txt -c 20 -gs ignore
```

Run the tool in silent mode
```
./x9.py -u "https://domain.tld/?param1=value1&param2=value2" -v '"mhainjected"' -p parameters.txt -c 20 -s
```

Write output to a file
```
./x9.py -u "https://domain.tld/?param1=value1&param2=value2" -v '"mhainjected"' -p parameters.txt -c 20 -o output.txt
```

You can also pipe your URL(s) to tools
```
echo "https://domain.tld/?param1=value1&param2=value2" | x9 -v '"mhainjected"' -p parameters.txt -c 20
```
```
cat urls.txt | x9 -v '"mhainjected"' -p parameters.txt -c 20
```

## License
This project is licensed under the MIT license. See the LICENSE file for details.
