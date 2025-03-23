#Importing the Required Librabies
import io
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PIL import Image
import tempfile
import webbrowser
import os
import csv
import pandas as pd
import time
#Complete Event Details
event_name=["Ideathon 3.0","Mock CID 2.0","Code and Ladders 2.0","CodeRace"]
event_details=["Two Days:'28th Feb and 1st March 2025","One Day:28th Feb","One Day:28th Feb","One Day:28th Feb"]
event_price=[250,50,100,0]
event_teamsize=[[2,3,4],[3,4,5],[1,2,3],[1]]
#Creating user details
def generate_qr(data):
   
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img
def generate_invoice(user_name, invoice_number, amount, event_name, team_size, event_details, left_logo, right_logo):
    qr_data = f"Invoice No: {invoice_number}\nName: {user_name}\nAmount:{amount}\nEvent: {event_name}\nTeam Size: {team_size}"
    qr_img = generate_qr(qr_data)
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    header_y = height - 80 
    c.drawImage(left_logo, 40, header_y-20, width=100, height=80)
    c.drawImage(right_logo, width - 140, header_y-20, width=90, height=80)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, header_y+10, "RESONANCE-2025")
    c.setStrokeColor(colors.blueviolet)
    c.setLineWidth(2.5)
    c.line(50,height-105,width-50,height-105)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height-130, "INVOICE")
    c.setLineWidth(1.5)
    c.line(width/3,height-135,2*(width/3),height-135)
    box_x, box_y, box_width, box_height = 50, height - 300 ,width - 100, 150
    c.setStrokeColor(colors.blueviolet)
    c.setLineWidth(1)
    c.rect(box_x, box_y, box_width, box_height)
    text_x = box_x + 15  
    text_y = box_y + box_height - 25  
    line_spacing = 20 
    c.setFont("Helvetica-Bold", 12)
    c.drawString(text_x, text_y, f"Name of the Student: {user_name}")
    c.drawString(text_x, text_y - line_spacing, f"Invoice Number: {invoice_number}")
    c.drawString(text_x, text_y - 2 * line_spacing, f"Amount:{amount}/-")
    c.drawString(text_x, text_y - 3 * line_spacing, f"Event Name: {event_name}")
    c.drawString(text_x, text_y - 4 * line_spacing, f"Team Size: {team_size}")
    c.drawString(text_x, text_y - 5 * line_spacing, f"Event Details: {event_details}")
    c.drawCentredString(width/2,height-320,"Computer Society of India GRIET - Resonance 2025 Event Management")
    c.drawCentredString(width/2,height-340,"Designed by Umesh Chandran Yenugula")
    temp_qr = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    qr_img.save(temp_qr.name)
    c.drawImage(temp_qr.name,(box_x+350),(height-283), width=125, height=125)
    c.save()
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    with open(temp_pdf.name, "wb") as f:
        f.write(pdf_buffer.getvalue())
    webbrowser.open(temp_pdf.name)
def creater():
    Name=str(input("Enter the Name of the Student:"))
    for i in range(len(event_name)):
        print(i+1,event_name[i],sep=".")
    while(True):
        eventname=int(input("Enter the Corresponding Serial No of the Event:"))
        confirm=int(input(f"Event Name:{event_name[eventname-1]},1or 0:"))
        if confirm==1:
            break
    if eventname-1<3:
        teamsize=int(input(f"Enter the Size of team{event_teamsize[eventname-1]}:"))
    else:
        teamsize=1
    amount=event_price[eventname-1]*teamsize
    print("Collect ",amount)
    time.sleep(2)
    pay=int(input("Confirm Payment:(1 or 0):"))
    left_logo="C:/Users/admin/Desktop/Screenshot_2025-02-16_214001-removebg-preview (1).png"
    right_logo= "C:/Users/admin/Desktop/csi_img-removebg-preview (1).png"
    file_name = "participants.csv"
    header = ["Name", "Event", "amount","InvoiceNumber"]
    
    file_exists = os.path.isfile(file_name)
    if not file_exists:
        invoice="CSIGRIETR25-1"
    else:
        df=pd.read_csv("participants.csv",index_col=0)
        last_index=df.shape[0]+1
        invoice=f"CSIGRIETR25-{last_index}"
    data = [Name,event_name[eventname-1],amount,invoice]
    if (pay==1):
        with  open(file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(header)
            writer.writerow(data)
        print(f"Details Saved!Thank you {Name}")
        generate_invoice(Name,
                     invoice,
                     amount,
                     event_name[eventname-1],
                     teamsize,
                     event_details[eventname-1],
                     left_logo,
                     right_logo)
    else:
        print("Payment failed")
creater()
