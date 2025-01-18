<h1 align="center">QR-Code-Generator</h1>

This scripting project generates **QR codes** for custom-designed **meal stubs**. The 2000 meal stubs are embedded in **PDF files**, making them ready for printing. 

Tools mainly used:

- Python
- ReportLab

Example output (Designed Jan 05, 2025. Design is subject to change.):

![Meal Stubs](https://github.com/iragca/QR-Code-Generator/blob/main/docs/img/meal_stubs.png?raw=true)

<h2>Project Structure</h2>

> data/duckdb-implementation.ipynb

DuckDB implementation of storing and generating of the generated IDs. Preceded by SQLite which is now unsupported and removed.

<h2>Streamlined Generation using CLI</h2>

The following instructions assumes that the current working directory is the root folder and have 'virtualenv' package installed.

<div style="font-weight: bold; margin-bottom: 5px;">If you don't have 'virtualenv' installed, you can install it using 'pip'.</div>

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
