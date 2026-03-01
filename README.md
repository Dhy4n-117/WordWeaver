# WordWeaver

WordWeaver is a custom wordlist generator designed for personalized dictionary attacks. It builds highly targeted wordlists based on user profiling. By taking inputs such as names, birthdates, pets, and specific keywords, WordWeaver intelligently combines them with common suffixes, dates, and special characters to generate a comprehensive list of potential passwords.

## Features
- **Interactive Profiling**: Prompt-based interactive mode to quickly build a target profile.
- **Intelligent Combinations**: Automatically generates combinations with upper/lower/title case, appends relevant dates, and mixes base words with common suffixes.
- **Save to File**: Outputs directly to a `.txt` file locally, ready for use with tools like Hydra, Hashcat, or GoBuster.
- **Customizable Output**: Easily specify your own output filename.

## Installation

Ensure you have Python 3 installed. No external dependencies or libraries are required.

```bash
git clone(https://github.com/Dhy4n-117/WordWeaver)
cd WordWeaver
```

## Usage

Run the script interactively:
```bash
python3 wordweaver.py
```
You will be prompted to enter target details:
- First Name
- Last Name
- Nickname
- Birthdate (DDMMYYYY)
- Company/Target Name
- Pet's Name
- Partner's Name
- Specific keywords (comma separated)

*Note: You can leave any field blank if unknown.*

### Command-Line Arguments

```text
usage: wordweaver.py [-h] [-i] [-o OUTPUT] [-q]

options:
  -h, --help                    show this help message and exit
  -i, --interactive             Launch interactive prompt for profiling target (default behavior)
  -o OUTPUT, --output OUTPUT    Specify output file name. Default: <firstname>_wordlist.txt
  -q, --quiet                   Do not print the banner
```

### Examples

**Default interactive mode:**
```bash
python3 wordweaver.py
```

**Generate a wordlist and save to a specific file:**
```bash
python3 wordweaver.py -o target_passwords.txt
```

**Run quietly without the banner:**
```bash
python3 wordweaver.py -q
```

## Disclaimer
This tool is intended for educational purposes and authorized security testing only. You may only use this against systems you own or have explicit permission to test.
