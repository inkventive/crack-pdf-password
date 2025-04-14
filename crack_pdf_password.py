import PyPDF2
import time

def crack_pdf_password(pdf_path, wordlist_path, output_path='found_password.txt'):
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
        passwords = wordlist.readlines()

    total = len(passwords)
    print(f"[+] Loaded {total} passwords from wordlist.\n")

    for i, password in enumerate(passwords):
        password = password.strip()
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if reader.decrypt(password):
                    print(f"\n[✓] Password found: {password}")
                    with open(output_path, 'w') as f:
                        f.write(password)
                    return
        except Exception:
            continue

        print(f"Trying password {i+1}/{total}: {password}", end='\r')

    print("\n[-] Password not found in wordlist.")

# Example usage
crack_pdf_password('your_pdf_name.pdf', 'your_password_list.txt')
