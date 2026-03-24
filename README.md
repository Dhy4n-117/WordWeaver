# WordWeaver
 
WordWeaver is a custom wordlist generator designed for personalized dictionary attacks. It builds highly targeted wordlists based on user profiling. By taking inputs such as names, birthdates, pets, and specific keywords, WordWeaver intelligently combines them with common suffixes, dates, and special characters to generate a comprehensive list of potential passwords.

## Features
- **Zero Dependencies**: Runs natively on any Python 3 environment. No `pip install` required.
- **Interactive Profiling**: Prompt-based interactive mode to quickly build a target profile.
- **Advanced Mutations Engine**:
  - **Leet Speak** (`--leet`): Automatically generates common leetspeak substitutions (e.g., `a -> 4`, `e -> 3`, `s -> $`).
  - **Case Permutation** (`--case-permute`): Exhaustively tests all casing scenarios for short keywords (`HacK`, `hACk`).
  - **Dynamic Year Sweeps** (`--years`): Easily iterate target suffixes across a range of years up to the current date.
  - **Special Characters** (`-s`): Define your own special character groupings to append/prepend (default: `!@#$%`).
- **Smart Filtering**: Built-in `--min-length` and `--max-length` parameters to drop useless passwords and save storage space.
- **Profile Import/Export**: Save targeting data to JSON (`--export-profile`) to resume or expand on it later without retyping (`--import-profile`).
- **External Mashing**: Blend your generated profile with an existing wordlist using `--external-list`.
- **Customizable Output**: Easily specify your own output filename.

## Installation

Ensure you have Python 3 installed. No external dependencies or libraries are required.

```bash
git clone (https://github.com/Dhy4n-117/WordWeaver)
cd WordWeaver
```

## Usage

Run the script interactively:
```bash
python3 wordweaver.py
```
You will be prompted to enter target details. *Note: You can leave any field blank if unknown.*

### Command-Line Arguments

```text
usage: wordweaver.py [-h] [-i] [--import-profile FILE] [--export-profile FILE]
                     [--leet] [--case-permute] [--years START_YEAR] [-s CHARS]
                     [--external-list FILE] [--min-length MIN_LENGTH]
                     [--max-length MAX_LENGTH] [-o OUTPUT] [-q]

WordWeaver: A custom wordlist generator based on user profiling.

options:
  -h, --help            show this help message and exit

Running Modes:
  -i, --interactive     Launch interactive prompt (default behavior if no import)
  --import-profile FILE
                        Load target profile from JSON file
  --export-profile FILE
                        Save target profile to JSON file and exit

Modifiers & Permutations:
  --leet                Enable Leet Speak permutations (e.g. a->@, e->3)
  --case-permute        Enable strict case permutations for all base words
  --years START_YEAR    Generate a sweep of years from START_YEAR to current year
  -s CHARS, --specials CHARS
                        Special chars to append (default: !@#$%)
  --external-list FILE  Append external wordlist items as base tokens

Filtering & Output:
  --min-length MIN_LENGTH
                        Minimum password length (default: 1)
  --max-length MAX_LENGTH
                        Maximum password length (default: 64)
  -o OUTPUT, --output OUTPUT
                        Specify output file name. Default: <target>_wordlist.txt
  -q, --quiet           Do not print the banner
```

### Examples

**Default interactive mode:**
```bash
python3 wordweaver.py
```

**Generate a highly targeted list with advanced filters:**
```bash
python3 wordweaver.py --leet --min-length 8 --max-length 14 -o target_passwords.txt
```

**Save a profile to disk for later use:**
```bash
python3 wordweaver.py --export-profile target_data.json
```

**Regenerate a list using an existing profile but target specific years:**
```bash
python3 wordweaver.py --import-profile target_data.json --years 1990 --case-permute
```

## Disclaimer
This tool is intended for educational purposes and authorized security testing only. You may only use this against systems you own or have explicit permission to test.
