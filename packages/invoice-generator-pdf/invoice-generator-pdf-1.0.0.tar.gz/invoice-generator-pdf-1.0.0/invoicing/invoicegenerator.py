import os

import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdfs_path, company_logo, company_name, product_id, product_name, amount_purchased, price_per_unit, total_price):
    """
           Generates PDF invoices from Excel files containing invoice data.

           This function reads Excel files in a specified directory, extracts relevant invoice data,
           and creates a PDF file for each invoice with a standardized format, including a header,
           rows of itemized purchases, total amount, company name, and company logo. The generated
           PDF files are saved to a specified directory.

           Parameters:
           -----------
           invoices_path : str
               Path to the directory containing invoice Excel files (in .xlsx format).
               Each Excel file should have a filename format of "invoice_nr-date.xlsx" and a sheet named "Sheet 1".

           pdfs_path : str
               Path to the directory where generated PDF invoices will be saved.

           company_logo : str
               Path to the company logo image file, which will be added to each PDF.

           company_name : str
               The name of the company to be displayed on each PDF invoice.

           product_id : str
               The column name in the Excel file representing the unique product ID.

           product_name : str
               The column name in the Excel file representing the product name.

           amount_purchased : str
               The column name in the Excel file representing the quantity of the product purchased.

           price_per_unit : str
               The column name in the Excel file representing the price per unit of the product.

           total : str
               The column name in the Excel file representing the total price for each product (quantity * price per unit).

           Returns:
           --------
           None
               The function saves each invoice as a PDF in the specified directory and does not return a value.
           """

    # glob.glob will return all file paths that match a specific pattern
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:
        # excels have multiple sheets in one document so having the sheet name is mandatory
        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # P stands for portrait
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filename = Path(filepath).stem
        invoice_nr, invoice_date = filename.split("-")

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=50, h=8, txt=f"Invoice nr. {invoice_nr}", ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=50, h=8, txt=f"Date: {invoice_date}", ln=1)

        # Header
        columns = df.columns
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font(family="Times", style="B", size=10)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=70, h=8, txt=columns[1], border=1)
        pdf.cell(w=30, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        # Adding rows to the table
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        total_sum = df["total_price"].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

        # add total sum sentence
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=30, h=8, txt=f"The total Price is {total_sum}", ln=1)

        # Add company name and logo
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=30, h=8, txt=f"{company_name}")
        pdf.image(company_logo, w=10)

        # Output file
        if not os.path.exists(pdfs_path):
            os.makedirs((pdfs_path))
        pdf.output(f"{pdfs_path}/{filename}.pdf")
