#!/usr/bin/env python3

import argparse
import sys
import os
import itertools

def print_banner():
    banner = """
    ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██╗    ██╗███████╗ █████╗ ██╗   ██╗███████╗██████╗ 
    ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██║    ██║██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
    ██║ █╗ ██║██║   ██║██████╔╝██║  ██║██║ █╗ ██║█████╗  ███████║██║   ██║█████╗  ██████╔╝
    ██║███╗██║██║   ██║██╔══██╗██║  ██║██║███╗██║██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
    ╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝╚███╔███╔╝███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
                                                                                          
    A custom wordlist generator for personalized dictionary attacks.
    """
    print(banner)

def get_profile():
    profile = {}
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
        profile['keywords'] = [k.strip() for k in keywords.split(',')]
    else:
        profile['keywords'] = []
        
    return profile

def generate_combinations(profile):
    words = []
    
    # Extract base words
    base_words = []
    for key in ['firstname', 'lastname', 'nickname', 'company', 'pet', 'partner']:
        if profile.get(key):
            val = profile[key]
            base_words.extend([val.lower(), val.upper(), val.capitalize()])
            
    if profile.get('keywords'):
        for kw in profile['keywords']:
            if kw:  # Ensure we don't process empty strings
                base_words.extend([kw.lower(), kw.upper(), kw.capitalize()])
            
    # Add DOB components if valid
    dob = profile.get('dob')
    dates = []
    if dob and len(dob) == 8:
        dd, mm, yyyy = dob[:2], dob[2:4], dob[4:]
        yy = yyyy[2:]
        dates.extend([dob, dd+mm, yyyy, yy, yyyy+mm+dd])
    elif dob:
        # If it's just some random number, add it anyway
        dates.append(dob)
        
    # Append basic numbers and special chars commonly used
    suffixes = ['123', '1234', '12345', '1', '12', '123456', '2023', '2024', '!', '@', '!!', '!@#']
    suffixes.extend(dates)
    
    # Generate direct combinations
    for w in base_words:
        words.append(w)
        for s in suffixes:
            words.append(w + s)
            words.append(w + s + '!')
            words.append(w + s + '@')
            
    # Combinations of two base words
    for i, w1 in enumerate(base_words):
        for j, w2 in enumerate(base_words):
            if i != j:
                words.append(w1 + w2)
                for s in suffixes:
                    words.append(w1 + w2 + s)
                    words.append(w1 + "_" + w2 + s)
                    
    # Remove duplicates by converting to a set, then back to list
    return list(set(words))

def main():
    parser = argparse.ArgumentParser(
        description="WordWeaver: A custom wordlist generator based on user profiling, similar to cupp.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python wordweaver.py           # Runs in interactive mode to build a profile
  python wordweaver.py -o list.txt # Save output to specific file
        """
    )
    parser.add_argument("-i", "--interactive", action="store_true", help="Launch interactive prompt for profiling target (default behavior)")
    parser.add_argument("-o", "--output", help="Specify output file name. Default: <firstname>_wordlist.txt")
    parser.add_argument("-q", "--quiet", action="store_true", help="Do not print the banner")
    
    args = parser.parse_args()

    # The manual via -h is automatically handled by argparse

    if not args.quiet:
        print_banner()

    try:
        profile = get_profile()
    except KeyboardInterrupt:
        print("\n\n[-] User aborted.")
        sys.exit(1)
    
    print("\n[*] Generating wordlist based on the provided profile...")
    wordlist = generate_combinations(profile)
    
    # Avoid creating an empty wordlist if user provided nothing
    if not wordlist:
        print("[-] No input provided. Exiting.")
        sys.exit(0)
        
    print(f"[*] Generated {len(wordlist)} potential passwords.")
    
    # Determine output file name
    if args.output:
        out_file = args.output
    else:
        name = profile.get('firstname') or profile.get('company') or 'target'
        out_file = f"{name.lower()}_wordlist.txt"
        
    # Save the output file in the current working directory
    out_path = os.path.join(os.getcwd(), out_file)
    
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            for word in sorted(wordlist):
                f.write(word + "\n")
        print(f"[+] Wordlist saved successfully to: {out_path}")
    except Exception as e:
        print(f"[-] Failed to write to {out_path}: {e}")

if __name__ == "__main__":
    main()
