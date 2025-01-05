<h1 align="center">QR-Code-Generator</h1>

QR Code Generator for meal stubs using 256-bit AES encryption (prototype)

> src/testing.ipynb

- Contains the initial exploration of libraries needed 

- Generating the ids with their encryption keys. 

- The generated data are then put inside an sqlite database.

> src/pdf_testing.ipynb

- Implementation of generating 2002 meal stubs inside PDF files
- Encrypted IDs are encoded as QR codes (encryption keys remain hidden in the database to serve as authentication)
- QR codes attached to meal stubs along with their corresponding unencrypted ID
- 26 meal stubs per PDF file. 13 per each column.

<h2>Streamlined Generation</h2>
Move your working directory to 'src'. Run the following command in the terminal.

```bash
python batch_generate.py
```
