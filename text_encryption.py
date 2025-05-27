# text_encryption.py

import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64
import os

# ===== AES Setup =====
def generate_aes_key():
    key = Fernet.generate_key()
    with open("aes_key.key", "wb") as f:
        f.write(key)
    return key

def load_aes_key():
    if os.path.exists("aes_key.key"):
        with open("aes_key.key", "rb") as f:
            return f.read()
    return generate_aes_key()

def aes_encrypt(msg):
    key = load_aes_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(msg.encode())
    return encrypted.decode()

def aes_decrypt(token):
    key = load_aes_key()
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(token.encode())
        return decrypted.decode()
    except:
        return "Invalid AES input or key."

# ===== DES Setup =====
des_key = b'8bytekey'  # DES key must be 8 bytes

def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text

def des_encrypt(msg):
    cipher = DES.new(des_key, DES.MODE_ECB)
    padded = pad(msg)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(encrypted).decode()

def des_decrypt(token):
    cipher = DES.new(des_key, DES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(base64.b64decode(token))
        return decrypted.decode().rstrip()
    except:
        return "Invalid DES input or key."

# ===== RSA Setup =====
if not os.path.exists("rsa_private.pem") or not os.path.exists("rsa_public.pem"):
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open("rsa_private.pem", "wb") as f:
        f.write(private_key)
    with open("rsa_public.pem", "wb") as f:
        f.write(public_key)

def load_rsa_keys():
    with open("rsa_private.pem", "rb") as f:
        private = RSA.import_key(f.read())
    with open("rsa_public.pem", "rb") as f:
        public = RSA.import_key(f.read())
    return private, public

def rsa_encrypt(msg):
    _, public = load_rsa_keys()
    cipher = PKCS1_OAEP.new(public)
    encrypted = cipher.encrypt(msg.encode())
    return base64.b64encode(encrypted).decode()

def rsa_decrypt(token):
    private, _ = load_rsa_keys()
    try:
        cipher = PKCS1_OAEP.new(private)
        decrypted = cipher.decrypt(base64.b64decode(token))
        return decrypted.decode()
    except:
        return "Invalid RSA input or key."

# ===== GUI Section =====
app = tk.Tk()
app.title("SecureText - AES / DES / RSA Encryption Tool")
app.geometry("700x600")
app.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 11))
style.configure("TCombobox", font=("Helvetica", 11))

ttk.Label(app, text="SecureText - Text Encryption Tool", font=("Helvetica", 18, "bold")).pack(pady=20)

# Dropdown for Algorithm
algo_var = tk.StringVar()
ttk.Label(app, text="Select Encryption Algorithm:").pack()
algo_menu = ttk.Combobox(app, textvariable=algo_var, values=["AES", "DES", "RSA"], state="readonly")
algo_menu.current(0)
algo_menu.pack(pady=5)

# Text Input
ttk.Label(app, text="Enter Text:").pack()
input_text = tk.Text(app, height=6, width=80)
input_text.pack(pady=10)

# Output Box
ttk.Label(app, text="Output:").pack()
output_text = tk.Text(app, height=6, width=80, bg="#f0f0f0")
output_text.pack(pady=10)

# Function Bindings
def encrypt_text():
    method = algo_var.get()
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Input Missing", "Please enter some text.")
        return

    if method == "AES":
        result = aes_encrypt(text)
    elif method == "DES":
        result = des_encrypt(text)
    elif method == "RSA":
        result = rsa_encrypt(text)
    else:
        result = "Unknown method selected."

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

def decrypt_text():
    method = algo_var.get()
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Input Missing", "Please enter some encrypted text.")
        return

    if method == "AES":
        result = aes_decrypt(text)
    elif method == "DES":
        result = des_decrypt(text)
    elif method == "RSA":
        result = rsa_decrypt(text)
    else:
        result = "Unknown method selected."

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

# Buttons
btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Encrypt", command=encrypt_text).grid(row=0, column=0, padx=20)
ttk.Button(btn_frame, text="Decrypt", command=decrypt_text).grid(row=0, column=1, padx=20)

# Footer
ttk.Label(app, text="Made by Abin | Pinnacle Internship 2025", font=("Arial", 10)).pack(pady=20)

app.mainloop()
