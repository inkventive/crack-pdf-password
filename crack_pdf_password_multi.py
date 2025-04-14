import PyPDF2
import multiprocessing
import time
import os

pdf_path = 'Your_PDF_Name.pdf'
wordlist_path = 'Your_Password_Wordlist.txt'
output_path = 'found_password.txt'

# Shared flag to stop all processes once the password is found
found = multiprocessing.Value('b', False)
found_password = multiprocessing.Array('c', b' ' * 100)

def try_passwords(passwords_chunk, pdf_path, found, found_password):
    for password in passwords_chunk:
        if found.value:
            return
        password = password.strip()
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if reader.decrypt(password):
                    with found.get_lock():
                        found.value = True
                        found_password.value = password.encode()
                    return
        except:
            continue

def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

def crack_pdf_password(pdf_path, wordlist_path, output_path='found_password.txt'):
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        passwords = f.readlines()

    total = len(passwords)
    print(f"[+] Loaded {total} passwords from wordlist.")

    cpu_count = multiprocessing.cpu_count()
    print(f"[+] Using {cpu_count} CPU cores for processing.")

    start_time = time.time()

    chunks = chunkify(passwords, cpu_count)
    processes = []

    for chunk in chunks:
        p = multiprocessing.Process(target=try_passwords, args=(chunk, pdf_path, found, found_password))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    if found.value:
        pw = found_password.value.decode().strip()
        print(f"\n[✓] Password found: {pw}")
        with open(output_path, 'w') as f:
            f.write(pw)
    else:
        print("\n[-] Password not found in wordlist.")

    print(f"⏱ Finished in {time.time() - start_time:.2f} seconds.")

# Run it
if __name__ == '__main__':
    crack_pdf_password(pdf_path, wordlist_path, output_path)
