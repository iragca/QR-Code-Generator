"""
This script generates QR codes from data retrieved from a SQLite database 
and creates PDF files containing meal stubs with the generated QR codes.

Modules:
    os: Provides a way of using operating 
        system dependent functionality.
    shutil: Offers a number of high-level operations on files and collections of files.
    sqlite3: Provides a SQL interface compliant with the DB-API 2.0 specification.
    typing: Provides runtime support for type hints.
    qrcode: A library to generate QR codes.
    pandas: A library providing high-performance, 
            easy-to-use data structures and data analysis tools.
    tqdm: A library for creating progress bars.
    reportlab: A library for generating PDFs.

Classes:
    MealStubPDF: A class to create a PDF with meal stub details, including QR code, ID, and border.

Functions:
    cm_to_points(centimeter) -> float: Convert a measurement from centimeters to points.
    inch_to_points(inch) -> float: Convert a measurement from inches to points.
    create_A4_batch(ids: List[str], pdf=MealStubPDF): 
        Create a batch of meal stubs in an A4-sized PDF.

Exceptions:
    Handles exceptions during QR code generation, PDF creation, 
    and data saving, printing error messages to the console.

Execution:
    The script retrieves data from a SQLite database, generates QR codes, 
    creates PDFs with meal stubs, and saves the data in Parquet and CSV formats.
"""


import os
import shutil
import sqlite3
from typing import List

import qrcode
import pandas as pd
from tqdm import tqdm
from utils.batch_processing import zip_batch

# ReportLab
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Retrieve the data from the database
db_path = "../data/database.sqlite"
print(f"Reading data from '{db_path}'")
conn = sqlite3.connect(db_path)
cur = conn.cursor()
data = pd.read_sql("SELECT * FROM keys", conn)

# Create a directory named 'qr_codes' if it doesn't exist
try:
    if os.path.exists('qr_codes'):
        shutil.rmtree('qr_codes')

    os.makedirs('qr_codes')

    for idx, x in tqdm(data.iterrows(), desc="Generating QR codes", total=len(data)):
        enc_key = x['encryption_key']
        enc_id = x['encrypted_id']
        unenc_id = x['unencrypted_id']
        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(enc_id)
        qr.make(fit=True)

        # Create and save the QR code image
        img = qr.make_image(fill='black', back_color='white')
        img.save(f"qr_codes/{unenc_id}.png")

except Exception as e:
    print(f"{type(e).__name__}: Error in generating QR codes. {e}")

class MealStubPDF(canvas.Canvas):
    """A class to create a PDF with meal stub details, including QR code, ID, and border.
    Methods
    -------
    draw_qr_code(x, y, image_path, width, height)
        Draws a QR code image at the specified location with the given dimensions.
    draw_id(text)
        Draws the ID text at the specified location.
    draw_border(x, y, width, height)
        Draws a border rectangle at the specified location with the given dimensions.
    """

    def draw_qr_code(self, x, y, image_path, width, height):
        self.drawImage(image_path, x, y, width, height)

    def draw_id(self, text):
        self.setFont("Helvetica", 9)
        self.drawString(x, y, text)

    def draw_border(self, x, y, width, height, dashed):

        if dashed:
            self.setDash(1, 10)
        self.rect(x, y, width, height)

    def draw_admit_line(self, start_x, start_y, end_x, end_y, dashed):
        if dashed:
            self.setDash(2, 3)

        self.line(start_x, start_y, end_x, end_y)

def cm_to_points(centimeter) -> float:
    """Convert a measurement from centimeters to points.

    Args:
        centimeter (float): The measurement in centimeters to be converted.

    Returns:
        float: The measurement converted to points.
    """
    return centimeter * 72 / 2.54

def inch_to_points(inch) -> float:
    """Convert a measurement from inches to points.

    Args:
        inch (float): The measurement in inches to be converted.

    Returns:
        float: The measurement converted to points.
    """

    return inch * 72

def create_A4_batch(
        ids: List[str],
        pdf = MealStubPDF
        ):
    """ Creates a batch of meal stub PDFs in A4 paper size.

    Args:
        ids (List[str]): List of IDs to generate QR codes and meal stubs for.
        pdf (class, optional): PDF generation class. Defaults to MealStubPDF.

    Raises:
        Exception: If there is an error in creating the PDF.

    The function performs the following steps:
        1. Sets up the save directory and filename for the PDF.
        2. Registers the custom font "Night-Driver".
        3. Defines the page size as A4.
        4. Initializes the PDF with the specified filename and page size.
        5. Draws a middle border line on the PDF.
        6. Iterates over the list of IDs to generate QR codes and meal stubs on both the left and right sides of the page.
        7. Draws QR codes, borders, admit lines, brand names, and admit strings for each ID.
        8. Saves the PDF after all stubs are generated.
    """

    try:
        save_directory = "pdfs"
        filename = f"{ids[0]}-{ids[-1]}.pdf"
        full_path = os.path.join(save_directory, filename)
        os.makedirs(save_directory, exist_ok=True)

        font_filename = "nightdriver.ttf"
        font_path = os.path.join("static/fonts", font_filename)
        font_name = "Night-Driver"
        pdfmetrics.registerFont(TTFont(font_name, font_path))

        pagesize = (
            inch_to_points(8.3),
            inch_to_points(13.5) # legal paper size
            ) # A4 Paper size

        meal_stub = pdf(
            filename = full_path,
            pagesize = pagesize # A4 Paper size
            )

        meal_stub.line(
            inch_to_points(4.15),
            inch_to_points(0),
            inch_to_points(4.15),
            inch_to_points(14)
            ) # Middle Border

        box_width = inch_to_points(4.15 - 0.50)
        box_height = inch_to_points(1)

        ids_left = ids[0:13]
        ids_right = ids[13:26]

        for i in range(0, len(ids_left), 1):

            # <Left Side>
            image_directory = "qr_codes"
            image_file_left = f"{ids_left[i]}.png"
            image_path_left = os.path.join(image_directory, image_file_left)

            meal_stub.draw_qr_code(
                x = inch_to_points(0.25),
                y = inch_to_points(i + 0.25),
                image_path = image_path_left,
                width = cm_to_points(2.5),
                height = cm_to_points(2.5)
                )

            meal_stub.draw_border(
                x = inch_to_points(0.25), # Left margin
                y = inch_to_points(i + 0.25), # Bottom margin
                width = box_width,
                height = box_height,
                dashed = True
                )

            meal_stub.draw_admit_line(
                start_x=box_width - inch_to_points(0.25),
                start_y=inch_to_points(i + 0.25),
                end_x=box_width - inch_to_points(0.25),
                end_y=inch_to_points(i + 1.25),
                dashed=True
            )

            # Brand Name
            meal_stub.setFillColor(colors.black)
            meal_stub.setFont("Times-Bold", 12)
            meal_stub.drawString(
                x = inch_to_points(2.1),
                y = inch_to_points(i + 0.95),
                text = "MCES"
            )

            meal_stub.setFillColor(colors.red)
            meal_stub.setFont("Night-Driver", 15)
            meal_stub.drawString(
                x = inch_to_points(1.73),
                y = inch_to_points(i + 0.65),
                text = "BALIK-LANTAW"
            )

            meal_stub.setFillColor(colors.red)
            meal_stub.setFont("Night-Driver", 12)
            meal_stub.drawString(
                x = inch_to_points(2.15),
                y = inch_to_points(i + 0.4),
                text = "2026"
            )

            meal_stub.saveState()
            x = inch_to_points(3.7)
            y = inch_to_points(i + 0.25 + 0.15)
            meal_stub.translate(x, y)
            meal_stub.rotate(90)

            # Admit String
            meal_stub.setFillColor(colors.black)
            meal_stub.setFont("Helvetica", 9)
            meal_stub.drawString(
                x = inch_to_points(-0.055),
                y = inch_to_points(0),
                text = "1 MEAL STUB"
            )

            meal_stub.setFillColor(colors.black)
            meal_stub.drawString(
                x = inch_to_points(0.05),
                y = inch_to_points(2.4),
                text = ids_left[i]
            )

            meal_stub.restoreState()

            # <Right Side>
            image_file_right = f"{ids_right[i]}.png"
            image_path_right = os.path.join(image_directory, image_file_right)

            meal_stub.draw_qr_code(
                x = inch_to_points(4.15 + .25),
                y = inch_to_points(i + 0.25),
                image_path = image_path_right,
                width = cm_to_points(2.5),
                height = cm_to_points(2.5)
                )

            meal_stub.draw_border(
                x = inch_to_points(4.15 + 0.25), # Left margin
                y = inch_to_points(i + 0.25), # Bottom margin
                width = box_width,
                height = box_height,
                dashed = True
            )

            meal_stub.draw_admit_line(
                start_x=inch_to_points(8.3 - 0.75),
                start_y=inch_to_points(i + 0.25),
                end_x=inch_to_points(8.3 - 0.75),
                end_y=inch_to_points(i + 1.25),
                dashed=True
            )

            meal_stub.saveState()
            x = inch_to_points((8.3 / 2) + 3.7)
            y = inch_to_points(i + 0.25 + 0.15)
            meal_stub.translate(x, y)
            meal_stub.rotate(90)

            # Admit String
            meal_stub.setFillColor(colors.black)
            meal_stub.setFont("Helvetica", 9)
            meal_stub.drawString(
                x = inch_to_points(-0.055),
                y = inch_to_points(0),
                text = "1 MEAL STUB"
            )

            meal_stub.setFillColor(colors.black)
            meal_stub.drawString(
                x = inch_to_points(0.05),
                y = inch_to_points(2.4),
                text = ids_right[i]
            )
            meal_stub.restoreState()

            # Brand Name
            meal_stub.setFillColor(colors.black)
            meal_stub.setFont("Times-Bold", 12)
            meal_stub.drawString(
                x = inch_to_points((8.3 / 2) + 2.1),
                y = inch_to_points(i + 0.95),
                text = "MCES"
            )
            meal_stub.setFillColor(colors.red)
            meal_stub.setFont("Night-Driver", 15)
            meal_stub.drawString(
                x = inch_to_points((8.3 / 2) + 1.73),
                y = inch_to_points(i + 0.65),
                text = "BALIK-LANTAW"
            )
            meal_stub.setFillColor(colors.red)
            meal_stub.setFont("Night-Driver", 12)
            meal_stub.drawString(
                x = inch_to_points((8.3 / 2) + 2.15),
                y = inch_to_points(i + 0.4),
                text = "2026"
            )
    except Exception as e:
        print(f"{type(e).__name__}: Error in creating PDF. {e}")
    else:
        meal_stub.save()
try:
    if os.path.exists('pdfs'):
        shutil.rmtree('pdfs')

    os.makedirs('pdfs')

    N = 26
    # Loop through the DataFrame in chunks of n rows
    for i in tqdm(range(0, len(data), N), desc="Generating PDF files"):
        chunk = data[i:i+N]['unencrypted_id']
        ids = chunk.tolist()

        create_A4_batch(ids)
except Exception as e:
    print(f"{type(e).__name__}: Error in generating PDF files. {e}")

zip_batch(['qr_codes', 'pdfs', r'../data'])
print("Done.")