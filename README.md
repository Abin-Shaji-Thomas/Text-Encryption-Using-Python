# SecureText — text encryption demonstration

A Python/Tkinter GUI project demonstrating AES, DES, and RSA encryption/decryption. Source code is in `text_encryption.py`; the repository also includes screenshots, a demo video, and a project report.

## Run

Requires Python 3 and the cryptography packages imported by the source. Install the required packages in a virtual environment if they are not already available, then run:

```sh
python text_encryption.py
```

Consult the imports at the top of `text_encryption.py` to identify package requirements; no `requirements.txt` is included.

## Contents

- `text_encryption.py` — application source
- `Scrennshots/` — screenshots (directory spelling retained as stored)
- `Video/` — demonstration video
- `Task1_Report_Abin_Shaji_Thomas.pdf` — project report
- `LICENSE` — license

## Cryptography and key handling

This project is an educational demonstration, not a reviewed secure messaging or file-protection product. DES is obsolete and must not be used to protect real data. Do not enter real secrets or rely on generated/stored keys for production use. Review key storage, modes, padding, and error handling in the current source before experimenting.
