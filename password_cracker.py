import hashlib
from itertools import product
import sqlite3
import subprocess
import time
from passlib.hash import bcrypt, argon2
import os
import gzip
import re
from flask import Flask, request, render_template
from flask_socketio import SocketIO
import argparse

# Flask and SocketIO Initialization
app = Flask(__name__)
socketio = SocketIO(app)

# Helper Functions
def hash_password(password, algorithm):
    if algorithm == "bcrypt":
        return bcrypt.hash(password)
    elif algorithm == "argon2":
        return argon2.hash(password)
    else:
        algo = hashlib.new(algorithm)
        algo.update(password.encode())
        return algo.hexdigest()

def verify_password(password, hash_target, algorithm):
    if algorithm == "bcrypt":
        return bcrypt.verify(password, hash_target)
    elif algorithm == "argon2":
        return argon2.verify(password, hash_target)
    return hash_password(password, algorithm) == hash_target

def dictionary_attack(hash_target, wordlist, algorithm):
    try:
        reader = gzip.open if wordlist.endswith(".gz") else open
        with reader(wordlist, "rt", encoding="utf-8", errors="ignore") as file:
            for word in file:
                word = word.strip()
                if verify_password(word, hash_target, algorithm):
                    return word
    except FileNotFoundError:
        print("[!] Wordlist file not found.")
    return None

def brute_force_attack(hash_target, chars, max_length, algorithm):
    for length in range(1, max_length + 1):
        for combination in product(chars, repeat=length):
            word = ''.join(combination)
            if verify_password(word, hash_target, algorithm):
                return word
    return None

def rule_based_attack(hash_target, wordlist, algorithm):
    transformations = [
        (r'a', '@'), (r's', r'$'), (r'o', '0'), (r'i', '1')
    ]
    try:
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as file:
            for word in file:
                word = word.strip()
                transformed_word = word
                for pattern, replacement in transformations:
                    transformed_word = re.sub(pattern, replacement, transformed_word)
                if verify_password(transformed_word, hash_target, algorithm):
                    return transformed_word
    except FileNotFoundError:
        print("[!] Wordlist file not found.")
    return None

def hybrid_attack(hash_target, wordlist, chars, max_suffix_length, algorithm):
    try:
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as file:
            for word in file:
                word = word.strip()
                for length in range(1, max_suffix_length + 1):
                    for suffix in product(chars, repeat=length):
                        attempt = word + ''.join(suffix)
                        if verify_password(attempt, hash_target, algorithm):
                            return attempt
    except FileNotFoundError:
        print("[!] Wordlist file not found.")
    return None

# Dual Mode Handling: CLI or Web
def cli_mode():
    parser = argparse.ArgumentParser(description="Password Cracker CLI")
    parser.add_argument("-a", "--algorithm", required=True, help="Hash algorithm (e.g., md5, sha1, sha256, bcrypt, argon2)")
    parser.add_argument("-ht", "--hash_target", required=True, help="Target hash to crack")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist file for dictionary, hybrid, or rule-based attack")
    parser.add_argument("-b", "--bruteforce", action="store_true", help="Enable brute force attack")
    parser.add_argument("-c", "--charset", default="abcdefghijklmnopqrstuvwxyz", help="Character set for brute force")
    parser.add_argument("-ml", "--max_length", type=int, help="Max length for brute force")
    parser.add_argument("--hybrid", action="store_true", help="Enable hybrid attack (dictionary + brute force suffix)")
    parser.add_argument("--rule-based", action="store_true", help="Enable rule-based attack with transformations")
    args = parser.parse_args()

    if not args.wordlist and not args.bruteforce:
        print("[!] Please specify a wordlist or enable brute force attack.")
        return

    start_time = time.time()
    result = None

    if args.rule_based and args.wordlist:
        print("[*] Starting rule-based attack...")
        result = rule_based_attack(args.hash_target, args.wordlist, args.algorithm)
    elif args.wordlist and args.hybrid:
        print("[*] Starting hybrid attack...")
        result = hybrid_attack(args.hash_target, args.wordlist, args.charset, args.max_length, args.algorithm)
    elif args.wordlist:
        print("[*] Starting dictionary attack...")
        result = dictionary_attack(args.hash_target, args.wordlist, args.algorithm)
    elif args.bruteforce:
        if not args.max_length:
            print("[!] max_length is required for brute force attack.")
            return
        print("[*] Starting brute force attack...")
        result = brute_force_attack(args.hash_target, args.charset, args.max_length, args.algorithm)

    time_taken = time.time() - start_time
    if result:
        print(f"[+] Password found: {result}")
    else:
        print("[-] Password not found.")
    print(f"[*] Time taken: {time_taken:.2f} seconds")

# Web Mode Handling
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/crack", methods=["POST"])
def crack():
    try:
        hash_target = request.form["hash"]
        algorithm = request.form["algorithm"]
        wordlist = request.files.get("wordlist")
        charset = request.form.get("charset", "abcdefghijklmnopqrstuvwxyz")
        max_length = request.form.get("max_length", 4, type=int)
        hybrid_attack_option = "hybrid_attack" in request.form

        if not hash_target or not algorithm:
            return "Missing required parameters", 400

        start_time = time.time()
        result = None

        if hybrid_attack_option and wordlist:
            wordlist.save("uploaded_wordlist.txt")
            result = hybrid_attack(hash_target, "uploaded_wordlist.txt", charset, max_length, algorithm)
        elif wordlist:
            wordlist.save("uploaded_wordlist.txt")
            result = dictionary_attack(hash_target, "uploaded_wordlist.txt", algorithm)
        else:
            result = brute_force_attack(hash_target, charset, max_length, algorithm)

        time_taken = time.time() - start_time
        return render_template("result.html", hash=hash_target, algorithm=algorithm,
                               result=result or "Not Found", time_taken=f"{time_taken:.2f}")

    except Exception as e:
        return f"Internal Server Error: {e}", 500

# Run in Dual Mode
if __name__ == "__main__":
    if len(os.sys.argv) > 1:  # If arguments are passed, use CLI mode
        cli_mode()
    else:  # Otherwise, start Flask web server
        socketio.run(app, debug=True)

