#!/usr/bin/env python3

import argparse
import sys
import os
import itertools
import json
import time

# --- Configuration & Mappings ---

LEET_MAPPING = {
    'a': ['a', '@', '4'],
    'b': ['b', '8'],
    'c': ['c', '(', '<'],
    'e': ['e', '3'],
    'g': ['g', '9', '6'],
    'i': ['i', '1', '!'],
    'l': ['l', '1', '|'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7', '+'],
    'z': ['z', '2']
}

DEFAULT_SPECIALS = "!@#$%"

def print_banner():
    banner = """
    ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗    ██╗███████╗ █████╗ ██╗   ██╗███████╗██████╗ 
    ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║    ██║██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
    ██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║ █╗ ██║█████╗  ███████║██║   ██║█████╗  ██████╔╝           @Dhy4n-117
    ██║███╗██║██║   ██║██╔══██╗██║  ██║██║███╗██║██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
    ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝╚███╔███╔╝███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
                                                                                          
    A custom wordlist generator for personalized dictionary attacks. (Advanced Edition)
    """
    try:
        print(banner)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(banner.encode('utf-8'))

def get_profile(interactive=True, default_years=[]):
    profile = {
        'keywords': [],
        'years': default_years.copy()
    }
    
    if interactive:
        print("\n[+] Please enter the target's details (leave blank if unknown):")
        profile['firstname'] = input("> First Name: ").strip()
        profile['lastname'] = input("> Last Name: ").strip()
        profile['nickname'] = input("> Nickname: ").strip()
        profile['dob'] = input("> Birthdate (DDMMYYYY): ").strip()
        profile['company'] = input("> Company/Target Name: ").strip()
        profile['pet'] = input("> Pet's Name: ").strip()
        profile['partner'] = input("> Partner's Name: ").strip()
        
        keywords = input("> Any specific keywords? (comma separated): ").strip()
        if keywords:
            profile['keywords'] = [k.strip() for k in keywords.split(',') if k.strip()]
            
        custom_years = input("> Any specific years? (comma separated, e.g., 2015,2023): ").strip()
        if custom_years:
             for y in custom_years.split(','):
                 if y.strip().isdigit():
                     profile['years'].append(y.strip())
    
    return profile

def save_profile(profile, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=4)
        print(f"[+] Profile saved to: {filepath}")
    except Exception as e:
        print(f"[-] Error saving profile: {e}")

def load_profile(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            profile = json.load(f)
        print(f"[+] Profile loaded from: {filepath}")
        return profile
    except Exception as e:
        print(f"[-] Error loading profile: {e}")
        sys.exit(1)

# --- Combination Generation Helpers ---

def get_leetspeak_variations(word):
    """Generates leetspeak permutations for a given word."""
    options = []
    for char in word.lower():
        if char in LEET_MAPPING:
            options.append(LEET_MAPPING[char])
        else:
            options.append([char])
            
    # product takes an iterable of iterables and performs cartesian product
    variations = [''.join(combo) for combo in itertools.product(*options)]
    return variations

def get_case_variations(word):
    """Generates all case permutations for a word (e.g. hack -> Hack, hAck, HAck...)."""
    options = [[char.lower(), char.upper()] if char.isalpha() else [char] for char in word]
    return [''.join(combo) for combo in itertools.product(*options)]

def get_date_components(dob):
     """Extract parts of a Date of Birth (DDMMYYYY)"""
     dates = []
     if dob and len(dob) == 8 and dob.isdigit():
         dd, mm, yyyy = dob[:2], dob[2:4], dob[4:]
         yy = yyyy[2:]
         dates.extend([dob, dd+mm, mm+dd, yyyy, yy, yyyy+mm+dd, dd+"_"+mm+"_"+yyyy])
     elif dob:
         dates.append(dob)
     return dates


def generate_combinations(profile, args):
    words = set()
    
    print("\n[*] Initializing base dictionary...")
    # 1. Gather Base Tokens
    base_tokens = set()
    for key in ['firstname', 'lastname', 'nickname', 'company', 'pet', 'partner']:
        val = profile.get(key, "").strip()
        if val:
            base_tokens.add(val.lower())
            
    for kw in profile.get('keywords', []):
        if kw.strip():
            base_tokens.add(kw.strip().lower())
            
    if args.external_list and os.path.exists(args.external_list):
        try:
             with open(args.external_list, 'r', encoding='utf-8') as f:
                 for line in f:
                     base_tokens.add(line.strip().lower())
             print(f"[+] Loaded {len(base_tokens)} base words (including external list).")
        except Exception as e:
             print(f"[-] Error loading external list: {e}")

    # 2. Case and Leetspeak Permutations on Base Tokens
    expanded_base = set()
    
    # We use a simple progress tracker for the terminal
    total_tokens = len(base_tokens)
    print(f"[*] Processing {total_tokens} base tokens for permutations (Case/Leet)...")
    
    for i, token in enumerate(base_tokens, 1):
        if args.case_permute:
             case_vars = get_case_variations(token)
        else:
             case_vars = [token.lower(), token.capitalize(), token.upper()]
             
        for cv in case_vars:
            expanded_base.add(cv)
            if args.leet:
                 expanded_base.update(get_leetspeak_variations(cv))
                 
        sys.stdout.write(f"\r    Progress: {i}/{total_tokens}")
        sys.stdout.flush()
    print() # Newline after progress

    # 3. Gather Suffixes/Prefixes
    suffixes = set(['123', '1234', '12345', '1', '12', '123456', '01'])
    if profile.get('dob'):
         suffixes.update(get_date_components(profile['dob']))
         
    for year in profile.get('years', []):
         if year:
             suffixes.add(year)
             if len(year) == 4:
                 suffixes.add(year[2:]) # Add short year '99' for '1999'

    # Special characters
    special_chars = list(args.specials) if args.specials else []
    
    # 4. Generate Final Combinations
    total_expanded = len(expanded_base)
    print(f"[*] Generating combinations for {total_expanded} expanded base words...")
    
    start_time = time.time()
    
    def add_word(w):
         if args.min_length <= len(w) <= args.max_length:
             words.add(w)

    for i, w1 in enumerate(expanded_base, 1):
        add_word(w1)
        
        # Append and Prepend single suffixes
        for s in suffixes:
             add_word(w1 + s)
             add_word(s + w1)
             
             for sc in special_chars:
                 add_word(w1 + s + sc)
                 add_word(sc + w1 + s)
                 add_word(w1 + sc + s)
                 
        # Combinations of two base words (if enabled, usually huge)
        # To avoid exponential memory explosion, only combine original tokens (not leet) if combining words
        if len(base_tokens) <= 15: # Arbitrary limit to prevent lockup
             for w2 in base_tokens:
                  if w1.lower() != w2.lower(): # Avoid johnjohn
                       # Just combine exact strings
                       add_word(w1 + w2)
                       add_word(w1 + "_" + w2)
                       for s in suffixes:
                            add_word(w1 + w2 + s)
                            add_word(w1 + "_" + w2 + s)
                            
        # Progress reporting
        if i % max(1, total_expanded // 20) == 0 or i == total_expanded:
             elapsed = time.time() - start_time
             sys.stdout.write(f"\r    Combining: {i}/{total_expanded} [{elapsed:.1f}s] - Current Size: {len(words)}")
             sys.stdout.flush()
             
    print()
    return list(words)


def main():
    parser = argparse.ArgumentParser(
        description="WordWeaver: A custom wordlist generator based on user profiling. (Advanced Edition)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python wordweaver.py           # Runs in interactive mode to build a profile
  python wordweaver.py --leet --min-length 6 --max-length 14 -o custom_list.txt
  python wordweaver.py --export-profile target.json # Save profile for later
  python wordweaver.py --import-profile target.json # Generate from saved profile
        """
    )
    
    group_mode = parser.add_argument_group('Running Modes')
    group_mode.add_argument("-i", "--interactive", action="store_true", help="Launch interactive prompt (default behavior if no import)")
    group_mode.add_argument("--import-profile", metavar="FILE", help="Load target profile from JSON file")
    group_mode.add_argument("--export-profile", metavar="FILE", help="Save target profile to JSON file and exit")
    
    group_mod = parser.add_argument_group('Modifiers & Permutations')
    group_mod.add_argument("--leet", action="store_true", help="Enable Leet Speak permutations (e.g. a->@, e->3)")
    group_mod.add_argument("--case-permute", action="store_true", help="Enable strict case permutations for all base words")
    group_mod.add_argument("--years", metavar="START_YEAR", type=int, help="Generate a sweep of years from START_YEAR to current year")
    group_mod.add_argument("-s", "--specials", metavar="CHARS", default=DEFAULT_SPECIALS, help="Special chars to append (default: %(default)s)")
    group_mod.add_argument("--external-list", metavar="FILE", help="Append external wordlist items as base tokens")
    
    group_filter = parser.add_argument_group('Filtering & Output')
    group_filter.add_argument("--min-length", type=int, default=1, help="Minimum password length (default: 1)")
    group_filter.add_argument("--max-length", type=int, default=64, help="Maximum password length (default: 64)")
    group_filter.add_argument("-o", "--output", help="Specify output file name. Default: <target>_wordlist.txt")
    group_filter.add_argument("-q", "--quiet", action="store_true", help="Do not print the banner")
    
    args = parser.parse_args()

    if not args.quiet:
        print_banner()

    # Determine Active Profile
    profile = {}
    
    default_years = []
    if args.years:
         current_year = int(time.strftime("%Y"))
         if args.years <= current_year:
             default_years = [str(y) for y in range(args.years, current_year + 1)]
         else:
             print(f"[-] Invalid --years start year: {args.years}")
             sys.exit(1)

    if args.import_profile:
        profile = load_profile(args.import_profile)
        # Ensure year sweep is included even if loading profile
        if 'years' not in profile:
             profile['years'] = []
        profile['years'].extend(default_years)
    else:
        try:
            profile = get_profile(interactive=True, default_years=default_years)
        except KeyboardInterrupt:
            print("\n\n[-] User aborted.")
            sys.exit(1)
            
    if args.export_profile:
        save_profile(profile, args.export_profile)
        if not args.import_profile and not profile.get('firstname'):
            # If they just exported an empty profile, just exit
            sys.exit(0)
    
    # Generate Wordlist
    wordlist = generate_combinations(profile, args)
    
    if not wordlist:
        print("[-] Wordlist resulted in 0 combinations. Check filtering rules.")
        sys.exit(0)
        
    print(f"[*] Generated {len(wordlist)} potential passwords (filtered by length {args.min_length}-{args.max_length}).")
    
    # Write Output
    if args.output:
        out_file = args.output
    else:
        name = profile.get('firstname') or profile.get('company') or 'target'
        out_file = f"{name.lower()}_wordlist.txt"
        
    out_path = os.path.join(os.getcwd(), out_file)
    
    try:
        print(f"[*] Writing to {out_path}...")
        with open(out_path, 'w', encoding='utf-8') as f:
             # Sort primarily by length, then alphabetical
             for word in sorted(wordlist, key=lambda w: (len(w), w)):
                f.write(word + "\n")
        print(f"[+] Wordlist saved successfully!\n")
    except Exception as e:
        print(f"[-] Failed to write to {out_path}: {e}")

if __name__ == "__main__":
    main()
