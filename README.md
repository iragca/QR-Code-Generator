<h1 align="center">QR-Code-Generator</h1>

This scripting project generates **unique AES 256-bit encrypted QR codes** for custom-designed **meal stubs**. The meal stubs are embedded in **PDF files**, making them ready for printing. 
Tools mainly used:

- Python
- ReportLab

Example output (Designed Jan 05, 2025. Design is ubject to change.):

![Meal Stubs](https://github.com/iragca/QR-Code-Generator/blob/main/docs/img/meal_stubs.png?raw=true)

<h2>Project Structure</h2>

> src/testing.ipynb

- Contains the initial exploration of libraries needed.

- Generating the ids with their encryption keys. 

- The generated data are then put inside an sqlite database.

> src/pdf_testing.ipynb

- Implementation of generating 2002 meal stubs inside PDF files
- Encrypted IDs are encoded as QR codes (encryption keys remain hidden in the database to serve as authentication)
- QR codes attached to meal stubs along with their corresponding unencrypted ID.
- 26 meal stubs per PDF file. 13 per each column.

> src/batch_generate.py

- Combines the functionalities of all code to enable streamlined generation.
- Subsequent changes to the meal stub design must be manually written.

<h2>Streamlined Generation using CLI</h2>

The following instructions assumes that the current working directory is the root folder and have 'virtualenv' package install

<div style="font-weight: bold; margin-bottom: 5px;">Installing 'virtualenv' using 'pip'</div>

```bash
pip install virtualenv
```

<h3>Running the script</h3>

1. Create a virtual environment. If you haven't yet.

<div style="font-weight: bold; margin-bottom: 5px;">Linux</div>

```bash
virtualenv .venv
source .venv/bin/activate
```

<div style="font-weight: bold; margin-bottom: 5px;">Powershell</div>

```bash
virtualenv .venv
.venv/bin/activate
```

2. Install required dependencies.

```bash
pip install -r requirements.txt
```

3. Move your working directory to 'src'. 

<div style="font-weight: bold; margin-bottom: 5px;">Linux and Powershell</div>

```bash
cd src
```

4. Run the script.

<div style="font-weight: bold; margin-bottom: 5px;">Linux</div>

```bash
python batch_generate.py
```


<div style="font-weight: bold; margin-bottom: 5px;">Powershell</div>

```bash
python ./batch_generate.py
```
