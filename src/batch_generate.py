import qrcode
import sqlite3
import pandas as pd
import polars as pl
import pandas as pd
import sqlite3
import os
from tqdm import tqdm

conn = sqlite3.connect("../data/database.sqlite")
cur = conn.cursor()

data = pd.read_sql("SELECT * FROM keys", conn)
data

import os

# Create a directory named 'qr_codes' if it doesn't exist
if not os.path.exists('qr_codes'):
    os.makedirs('qr_codes')

print("Generating QR codes...")
for idx, x in tqdm(data.iterrows()):
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

from reportlab.pdfgen import canvas

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

from typing import List
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

def create_A4_batch(
        ids: List[str], 
        pdf = MealStubPDF
        ):
    
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
        meal_stub.setFont("Times-Bold", 12)
        meal_stub.drawString(
            x = inch_to_points(2.1), 
            y = inch_to_points(i + 0.95), 
            text = "MCES"
        )
        meal_stub.setFont("Night-Driver", 15)
        meal_stub.drawString(
            x = inch_to_points(1.73), 
            y = inch_to_points(i + 0.65), 
            text = "BALIK-LANTAW"
        )
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
        meal_stub.setFont("Helvetica", 9)
        meal_stub.drawString(
            x = inch_to_points(-0.055), 
            y = inch_to_points(0), 
            text = "1 MEAL STUB"
        )
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
        meal_stub.setFont("Helvetica", 9)
        meal_stub.drawString(
            x = inch_to_points(-0.055), 
            y = inch_to_points(0), 
            text = "1 MEAL STUB"
        )

        meal_stub.drawString(
            x = inch_to_points(0.05), 
            y = inch_to_points(2.4), 
            text = ids_right[i]
        )
        meal_stub.restoreState()

        # Brand Name
        meal_stub.setFont("Times-Bold", 12)
        meal_stub.drawString(
            x = inch_to_points((8.3 / 2) + 2.1), 
            y = inch_to_points(i + 0.95), 
            text = "MCES"
        )
        meal_stub.setFont("Night-Driver", 15)
        meal_stub.drawString(
            x = inch_to_points((8.3 / 2) + 1.73), 
            y = inch_to_points(i + 0.65), 
            text = "BALIK-LANTAW"
        )
        meal_stub.setFont("Night-Driver", 12)
        meal_stub.drawString(
            x = inch_to_points((8.3 / 2) + 2.15), 
            y = inch_to_points(i + 0.4), 
            text = "2026"
        )

    meal_stub.save()

n = 26

print("Generating PDF files...")
# Loop through the DataFrame in chunks of n rows
for i in tqdm(range(0, len(data), n)):
    chunk = data[i:i+n]['unencrypted_id']
    ids = chunk.tolist()

    create_A4_batch(ids)

print("Saved data to '../data/'")
data.to_parquet(r"../data/data.parquet", index=False)
data.to_csv(r"../data/data.csv", index=False)
