import random
import time
from datetime import datetime
from email.message import EmailMessage
import qrcode   #pip install qrcode[pil]
import smtplib
import os.path
import pandas as pd     #pip install pandas
from collections import deque
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle# type: ignore
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer,Paragraph, Frame, PageTemplate
from reportlab.lib import colors# type: ignore
from reportlab.lib.units import inch# type: ignore
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import HRFlowable
#from admin import*
sender_name="The Kartikesh MC Bank" #Sender Name.
sender_email= "vlpabhinavpandey@gmail.com" #Sender Email.
sender_name_and_email=f"{sender_name} <{sender_email}>"
sender_email_password="golhdbozrfthpcyq" #Sender's Email Password.

class BankAccount:
    def __init__(self, name, account_number, email, balance, password):
        self.name = name
        self.account_number = account_number
        self.email = email
        self.balance = balance
        self.password = password

    def set_password(self, new_password):
        self.password = new_password
        print("Password set successfully!")

    def deposit(self, amount):
        self.balance += amount
        self.update_balance_in_file()  # Update balance in file
        # Define the file path of user's db
        file_path = f'C:/Users/Abhinav Pandey/Documents/PYTHON/Database/{self.email}.txt'
        # Append to the file
        with open(file_path, 'a') as file:
            date=datetime.now().strftime("%d/%m/%Y")
            file.write(f"{date},BY CASH,Rs. {amount},DEPOSIT,Rs. {self.balance}\n")
        print(f"Deposit of {amount} successfully made. Current balance: {self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.update_balance_in_file()  # Update balance in file
            # Define the file path of user's db
            file_path = f'C:/Users/Abhinav Pandey/Documents/PYTHON/Database/{self.email}.txt'
            # Append to the file
            with open(file_path, 'a') as file:
                date=datetime.now().strftime("%d/%m/%Y")
                file.write(f"{date},BY CASH,Rs. {amount},WITHDRAWAL,Rs. {self.balance}\n")
            print(f"Withdrawal of {amount} successfully made. Current balance: {self.balance}")
        else:
            print("\n\t\t\t\t\tXXXXXX     Insufficient funds.     XXXXXX\n")

    def send_money(self, recipient_account, amount):
        print(f"Recipient Name: {recipient_account.name}")
        cnf=input("Is recipient name is correct? (Y/N): ").upper()
        if cnf=="Y":
            if amount <= self.balance:
                self.balance -= amount  # Deduct amount from sender's balance
                recipient_account.balance += amount  # Add amount to recipient's balance
                self.update_balance_in_file()  # Update sender's balance in file
                # Define the file path of sender's db
                file_path = f'C:/Users/Abhinav Pandey/Documents/PYTHON/Database/{self.email}.txt'
                # Append to the file
                with open(file_path, 'a') as file:
                    date=datetime.now().strftime("%d/%m/%Y")
                    file.write(f"{date},TO {recipient_account.name}-{recipient_account.account_number},Rs. {amount},WITHDRAWAL,Rs. {self.balance}\n")
                
                recipient_account.update_balance_in_file()  # Update recipient's balance in file
                # Define the file path of recipient's db
                file_path = f'C:/Users/Abhinav Pandey/Documents/PYTHON/Database/{recipient_account.email}.txt'
                # Append to the file
                with open(file_path, 'a') as file:
                    date=datetime.now().strftime("%d/%m/%Y")
                    file.write(f"{date},FROM {self.name}-{self.account_number},Rs. {amount},DEPOSIT,Rs. {recipient_account.balance}\n")

                print(f"Amount {amount} successfully sent to {recipient_account.name}'s account.")
                print(f"Current balance: {self.balance}")
            else:
                print("\n\t\t\t\t\tXXXXXX     Insufficient funds.     XXXXXX\n")
        elif cnf=="N":
            print("\n\t\t\t\t\tXXXXXX   Transaction is cancelled.   XXXXXX\n")
        else:
            print("\n\t\t\t\t------------------       Invalid Input.      --------------------")
            print("\n\t\t\t\t\tXXXXXX   Transaction is cancelled.   XXXXXX\n\n")

    def display_balance(self):
        print(f"Account Balance: {self.balance}")

    def update_balance_in_file(self):
        # Read all lines from accounts.txt
        with open("accounts.txt", "r") as file:
            lines = file.readlines()

        # Find and update the line corresponding to this account
        for i, line in enumerate(lines):
            if self.account_number in line:
                parts = line.strip().split(",")
                parts[3] = str(self.balance)
                lines[i] = ",".join(parts) + "\n"

        # Write the updated lines back to accounts.txt
        with open("accounts.txt", "w") as file:
            file.writelines(lines)


def generate_otp():
    return random.randint(1000, 9999)

def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

def create_account(accounts):
    print('''
                                **************************************************
                                            S   I   G   N       U   P
                                **************************************************
                  ''')
    eml = input('ENTER YOUR EMAIL : ').lower()
    email=eml.lower()
    if "@" not in email:
        email=eml+"@gmail.com"

    # Check if an account with the provided email already exists
    for account in accounts:
        if account.email == email:
            print("An account with this email already exists.")
            return None

    name = input("Enter your name: ").upper()
    dob=input("Enter your D.O.B. (in dd/mm/yyyy format): ")
    address=input("Enter your Address: ").upper()
    account_number = generate_account_number()
    for account in accounts:
        if account.account_number == account_number:
            generate_account_number()
    otp = generate_otp()


    message = EmailMessage()
    message["Subject"] = "OTP for Bank Account"
    message["From"] =sender_name_and_email
    message["To"] =f"{name} <{email}>"
    message.set_content(f"""Dear {name},

Welcome to our Bank! We are thrilled to have you as a valued user.

To complete your account setup, please use the following One-Time Password (OTP): {otp}

If you did not request this OTP, please contact our customer support immediately.

Thank you for choosing our Bank.

Best regards,
The Bank Team
""")
    # Connect to Gmail SMTP server and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_email_password)
        server.send_message(message)

    print('\n\t\t\t\t********OTP HAS BEEN SENT ON YOUR EMAIL.*********\n')

    for _ in range(3):
        user_otp = input('ENTER OTP : ')
        if user_otp == str(otp):
            print('''
                          ******OTP Verified.********
''')
            password = input('CREATE A NEW PASSWORD : ')
            balance = 0  # Initial balance
            account = BankAccount(name, account_number, email, balance, password)
    ########      GENERATING & SENDING QR.##########
            content=f"Name: {name}\nAccount Number: {account_number}\nEmail: {email}\nD.O.B.: {dob}\nAddress: {address}"
            img=qrcode.make(content)
            destination = f'C:/Users/Abhinav Pandey/Documents/PYTHON/Database/{email}_QR.png'
            img.save(destination)
        # Save account details to file
            with open("accounts.txt", "a") as file:
                file.write(f"{name},{email},{account_number},{balance},{password}\n")
        # Create a Transaction file.
            # Define the directory and file name
            directory = 'C:/Users/Abhinav Pandey/Documents/PYTHON/Database'
            file_name = f"{email}.txt"
            # Ensure the directory exists
            os.makedirs(directory, exist_ok=True)
            # Create the full file path
            file_path = os.path.join(directory, file_name)
            # Write to the file
            with open(file_path, 'w') as file:
                file.write("")
            #Sending Account Number to the User.
            account_number_message = EmailMessage()
            account_number_message["Subject"] = "Your Account Number"
            account_number_message["From"] =sender_name_and_email
            account_number_message["To"] = f"{name} <{email}>"
            account_number_message.set_content(f"""Congratulations, {name} ! Your Bank account has been successfully created!

We are absolutely delighted to welcome you to our Bank family. Your new account is now active and ready for you to start using. Here are the details of your account:

Account Number: {account_number}

To make your banking experience as seamless and convenient as possible, we have attached a QR code to this email. Simply scan the QR code with your mobile device to quickly access your account information and perform transactions on the go. This QR code ensures that you can manage your finances with just a few taps, anytime and anywhere.

Thank you for choosing our Bank. We are honored to be your trusted financial partner and look forward to helping you achieve your financial goals.

Warmest regards,
The Bank Team
 """)
            # Attach the PNG image
            with open(f'C:/Users/Abhinav Pandey/Documents/PYTHON/Database/{email}_QR.png', 'rb') as img_file:
                img_data = img_file.read()
                account_number_message.add_attachment(img_data, maintype='image', subtype='png', filename='QR.png')

            # Connect to Gmail SMTP server and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, sender_email_password)
                server.send_message(account_number_message)
            accounts.append(account)



            print('''
                            ************************************************************
                                                CONGRATULATIONS!!
                                            YOUR ACCOUNT HAS BEEN CREATED,
                                    LOGIN CREDENTIALS HAS BEEN SENT ON YOUR EMAIL.
                            ************************************************************                                   
''')
            return account
        else:
            print("\t\t\t\tXXXXXXXX   WRONG OTP   XXXXXXXX")
    print("Maximum attempts reached. Account creation aborted.")
    return None


def load_accounts():
    accounts = []
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as file:
            for line in file:
                name, email, account_number, balance, password = line.strip().split(",")
                account = BankAccount(name, account_number, email, float(balance), password)
                accounts.append(account)
    return accounts

def login(accounts):
    account_number = input("Enter your account number: ")

    for _ in range(3):
        password = input("Enter your password: ")
        for account in accounts:
            if account.account_number == account_number and account.password == password:
                print("Login successful.")
                return account
        print("Invalid credentials. Please try again.")
    print("Maximum attempts reached. Login failed.")
    return None

def reset_password(accounts, email):
    for account in accounts:
        if account.email == email:
            otp = generate_otp()

            message = EmailMessage()
            message["Subject"] = "Confirmation Code for Password Reset"
            message["From"] =sender_name_and_email
            message["To"] = f"{account.name} <{email}>"
            message.set_content(f"""Dear User,

We received a request to reset the password for your Advanced Bank account. If you made this request, please use the confirmation code below to reset your password. If you did not request a password reset, please ignore this message.

Your confirmation code is: {otp}

To reset your password, please enter this code in the password reset section.
Thank you for banking with us.

Best regards,
The Bank Team
""")
        # Connect to Gmail SMTP server and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, sender_email_password)
                server.send_message(message)


            for _ in range(3):
                user_otp = input("ENTER CONFIRMATION CODE : ")
                if user_otp == str(otp):
                    print("\n\t\t\t\t*******VERIFIED.*******\n")
                    new_password = input("CREATE A NEW PASSWORD : ")
                    confirm_password = input("CONFIRM NEW PASSWORD : ")
                    if new_password == confirm_password:
                        account.set_password(new_password)

                        # Update password in the accounts.txt file
                        with open("accounts.txt", "r+") as file:
                            lines = file.readlines()
                            file.seek(0)
                            for i, line in enumerate(lines):
                                if account.account_number in line:
                                    parts = line.strip().split(",")
                                    parts[-1] = new_password
                                    lines[i] = ",".join(parts) + "\n"
                            file.truncate(0)
                            file.writelines(lines)

                        new_password_message = EmailMessage()
                        new_password_message["Subject"] = "New Password and Account Number"
                        new_password_message["From"] =sender_name_and_email
                        new_password_message["To"] = f"{account.name} <{email}>"
                        new_password_message.set_content(f"""Dear User,

We wanted to inform you that your password has been successfully reset for your Bank account. Below are your updated account details:

Account Number: {account.account_number}
New Password: {new_password}

For security purposes, please ensure that your new password is strong and unique to protect your account.

If you did not request this password reset, please contact our customer support team immediately to secure your account.

Thank you for banking with us. We are here to assist you with any questions or concerns.

Best regards,
The Bank Team
""")

                    # Connect to Gmail SMTP server and send the email
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                            server.login(sender_email, sender_email_password)
                            server.send_message(new_password_message)    
                        print("\t\t\t\t*******YOUR REQUEST HAS BEEN ACCEPETED********")
                        return True
                    else:
                        print("Passwords do not match. Please try again.")
                        continue
                else:
                    print("OTP verification failed.")
            print("Maximum attempts reached. Password reset aborted.")
            return False
    print("Email not found.")
    return False

def find_account_number(accounts):
    name = input("Enter your Full Name: ").upper()
    email = input("Enter your E-mail Address: ").lower()
    if '@' not in email:
        email=email+'@gmail.com'
    password = input("Enter your password: ")

    for account in accounts:
        if account.name == name and account.email == email and account.password == password:
            print(f"Your account number is: {account.account_number}")
            return
    print("Account not found. Please check your credentials.")

def add_page_number_and_footer(canvas, doc):
    canvas.saveState()
    footer_text = Paragraph('&#169; 2024 All rights reserved by ~ The Kartikesh MC Bank.', getSampleStyleSheet()['Normal'])
    w, h = footer_text.wrap(doc.width, doc.bottomMargin)
    footer_text.drawOn(canvas, doc.leftMargin, h)
    canvas.drawRightString(doc.width - 20, 20, f"Page {doc.page}")
    canvas.restoreState()

def create_transaction_pdf(data, user_name, account_number, email, printing_date):
    filename = 'Account_Statement.pdf'
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    heading_style = styles['Title']
    subheading_style = ParagraphStyle(name='CenteredSubHeading', parent=styles['Heading2'], alignment=1)
    user_detail_style = ParagraphStyle(name='UserDetail', parent=styles['Normal'], fontSize=12, alignment=0)

    # Add heading and subheading
    heading = Paragraph('<b><u>The Kartikesh MC Bank</u></b>', heading_style)
    subheading = Paragraph('<b>Account Statement</b>', subheading_style)
    elements.append(heading)
    elements.append(Spacer(1, 12))  # Add space between heading and subheading
    elements.append(subheading)
    elements.append(Spacer(1, 12))  # Add space between subheading and horizontal rule

    # Add horizontal rule
    hr = HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black, spaceBefore=1, spaceAfter=1)
    elements.append(hr)
    elements.append(Spacer(1, 12))  # Add space between horizontal rule and user details

    # Add user details in a table for better alignment
    user_details_data = [
        [Paragraph(f"Name: {user_name}", user_detail_style), Paragraph(f"Updated on: {printing_date}", user_detail_style)],
        [Paragraph(f"Account number: {account_number}", user_detail_style), Paragraph(f"Email: {email}", user_detail_style)]
    ]
    user_details_table = Table(user_details_data, colWidths=[3.5*inch, 3.5*inch])
    user_details_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),
        ('BOX', (0, 0), (-1, -1), 0, colors.white),
    ]))
    elements.append(user_details_table)
    elements.append(Spacer(1, 24))  # Add space between user details and table

    # Define table headers and content
    table_data = [["Date", "Particulars", "Amount", "Status", "Balance"]]
    for entry in data:
        table_data.append([
            entry['Date'],
            entry['Particulars'],
            entry['Amount'],
            entry['Status'],
            entry['Balance']
        ])

    # Create Table object
    table = Table(table_data, repeatRows=1, hAlign='CENTER')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    # Add table to elements
    elements.append(table)
    elements.append(Spacer(1, 24))  # Add space between table and footer

    # Build PDF document
    doc.build(elements, onFirstPage=add_page_number_and_footer, onLaterPages=add_page_number_and_footer)
    return filename


def dev_create_account(accounts):
    accounts = load_accounts()
    eml = input("ENTER USER'S EMAIL : ").lower()
    email=eml.lower()
    if email=="":
        print("Please Enter a valid Email.")
    elif "@" not in email:
        email=eml+"@gmail.com"

    # Check if an account with the provided email already exists
    for account in accounts:
        if account.email == email:
            print("An account with this email already exists.")
            return None

    name = input("ENTER NAME: ").upper()
    dob=input("ENTER D.O.B. (in dd/mm/yyyy format): ")
    address=input("Enter Address: ").upper()
    account_number = input("ENTER ACCOUNT NUMBER: ")
    for account in accounts:
        if account.account_number == account_number:
            print("\t\t\t************   Account Number already exists.   ************")
            return None
    password = input('CREATE A NEW PASSWORD : ')
    balance = 0  # Initial balance
    account = BankAccount(name, account_number, email, balance, password)
    accounts.append(account)
    # Save account details to file
    with open("accounts.txt", "a") as file:
        file.write(f"{name},{email},{account_number},{balance},{password}\n")  

    # Create a Transaction file.
    # Define the directory and file name
    directory = 'C:/Users/Abhinav Pandey/Documents/PYTHON/Database'
    file_name = f"{email}.txt"
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    # Create the full file path
    file_path = os.path.join(directory, file_name)
    # Write to the file
    with open(file_path, 'w') as file:
        file.write("")  
    ##      GENERATING & SAVING QR.##########
    content=f"Name: {name}\nAccount Number: {account_number}\nEmail: {email}\nD.O.B.: {dob}\nAddress: {address}"
    img=qrcode.make(content)
    destination = f'C:/Users/Abhinav Pandey/Documents/PYTHON/Database/{email}_QR.png'
    img.save(destination)
    notification=input(f"Do you want to send notification to the {name} on {email} (Y/N)? ").lower()
    if notification!="y":
        print("\n")
    else:
        print("Sending...")
        account_number_message = EmailMessage()
        account_number_message["Subject"] = "Your Account Number"
        account_number_message["From"] =sender_name_and_email
        account_number_message["To"] = f"{name} <{email}>"
        account_number_message.set_content(f"""Congratulations, {name} ! Your Bank account has been successfully created!

We are absolutely delighted to welcome you to our Bank family. Your new account is now active and ready for you to start using. Here are the details of your account:

Account Number: {account_number}

To make your banking experience as seamless and convenient as possible, we have attached a QR code to this email. Simply scan the QR code with your mobile device to quickly access your account information and perform transactions on the go. This QR code ensures that you can manage your finances with just a few taps, anytime and anywhere.

Thank you for choosing our Bank. We are honored to be your trusted financial partner and look forward to helping you achieve your financial goals.

Warmest regards,
The Bank Team
""")
        # Attach the PNG image
        with open(f'C:/Users/Abhinav Pandey/Documents/PYTHON/Database/{email}_QR.png', 'rb') as img_file:
            img_data = img_file.read()
            account_number_message.add_attachment(img_data, maintype='image', subtype='png', filename='QR.png')

        # Connect to Gmail SMTP server and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_email_password)
            server.send_message(account_number_message)
    print('''
                            ************************************************************
                                                CONGRATULATIONS!!
                                            THE ACCOUNT HAS BEEN CREATED.
                            ************************************************************                                   
''')    
    return account
def dev_delete_row_by_email(file_path, email):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with the specified email
    email_found = False
    for line in lines:
        if email in line:
            name = line.split(",") #B'coz The name is the first word in the line...
            print(f"Name: {name[0]}")
            email_found = True
            break

    if not email_found:
        print(f"No account found with email {email}.")
        return

    # Ask for confirmation
    confirmation = input(f"Do you want to delete the account for {name[0]}? (Y/N): ").strip().lower()
    if confirmation != 'y':
        print("\t\t\t\t************     Operation cancelled.    **************")
        return
    else:
        print("\t\t\t************    Account has been deleted sucessfully.    **************")
    # Filter out the line with the specified email
    lines = [line for line in lines if email not in line]

    # Write the remaining lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)
# Function to parse the data
def dev_parse_data(data):
    parsed_data = []
    for index, item in enumerate(data, start=1):
        values = item.strip().split(',')
        # Insert serial number at the beginning
        parsed_data.append([str(index)] + values)
    return parsed_data

def dev_create_pdf(filename, data):
    document = SimpleDocTemplate(filename, pagesize=letter)

    # Define the styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'title_style',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=18,
        alignment=1,  # Center alignment
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'subtitle_style',
        parent=styles['Title'],
        fontSize=14,
        alignment=1,  # Center alignment
        spaceAfter=12
    )

    copyright_style = ParagraphStyle(
        'copyright_style',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1,  # Center alignment
        spaceBefore=20
    )

    # Elements for the PDF
    elements = []

    # Title and Subtitle
    title = Paragraph('<u><b>The Bank Team</b></u>', title_style)
    subtitle = Paragraph('<u>Data of User\'s</u>', subtitle_style)

    elements.append(title)
    elements.append(subtitle)

    # Headers
    headers = ["S.No.", "Name", "Email Address", "Account Number", "Amount", "Code"]

    # Parse the data
    parsed_data = dev_parse_data(data)

    # Add headers to data
    table_data = [headers] + parsed_data

    # Creating the table
    table = Table(table_data, colWidths=[0.5*inch, 2*inch, 2*inch, 1.5*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Define the frames for the document layout
    frame_main = Frame(
        document.leftMargin, document.bottomMargin + 50,  # Leave space for footer
        document.width, document.height - 100,
        id='main_frame'
    )

    frame_footer = Frame(
        document.leftMargin, document.bottomMargin,
        document.width, 50,
        id='footer_frame'
    )

    # Define the PageTemplate
    def footer(canvas, doc):
        canvas.saveState()
        footer_text = Paragraph('&#169; 2024 All rights reserved by ~ The Bank Team.', copyright_style)
        w, h = footer_text.wrap(doc.width, doc.bottomMargin)
        footer_text.drawOn(canvas, doc.leftMargin, h)
        canvas.restoreState()

    page_template = PageTemplate(
        id='main_template',
        frames=[frame_main, frame_footer],
        onPage=footer
    )

    document.addPageTemplates([page_template])

    # Build the PDF
    document.build(elements)

def dev_send_email_with_attachment(pdf_filename,subject,to,content):
    # Create the email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_name_and_email
    msg['To'] = to
    msg.set_content(content)

    # Read the PDF file and attach it
    with open(pdf_filename, 'rb') as f:
        pdf_data = f.read()

    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=pdf_filename)

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_email_password)
        server.send_message(msg)
def dev_get_data_on_mail():
    with open ("accounts.txt", "r+") as file:
                                    data = file.readlines()
                                    # Create the PDF
                                    pdf_filename = "Bank_Data.pdf"
                                    print("Sending...")
                                    dev_create_pdf(pdf_filename,data)
                                    # Send the email with the attachment
                                    subject="User Data Report"
                                    to=sender_name_and_email
                                    content="Requested Data on  Admin Mail."
                                    dev_send_email_with_attachment(pdf_filename,subject,to,content)
                                    print("All data has been sent on Admin Email Account.")

def main():
    print("""
                                **************************************************************
                                **************  W   E   L   C   O   M   E   ******************
                                **************************************************************
          """)


    while True:
        accounts = load_accounts()
        print('''        
                    *******************     M  A   I   N       M   E   N   U       ********************           
''')
        print('''
                1.  S   I   G   N       U   P
                
                2.  L   O   G   I   N
                
                3.  R   E   S   E   T 

                4.  F I N D   A C C O U N T   N U M B E R      
                
                5.  E   X   I   T

''')

        choice = input("ENTER YOUR CHOICE : ")

        if choice == '1':
            user_account = create_account(accounts)
            if user_account:
                accounts.append(user_account)
        elif choice == '2':
            user_account = login(accounts)
            if user_account:
                print('''
                                        ********************************************
                                        *********    LOGIN SUCCESSFULLY    *********
                                        ********************************************
                ''')
                # Implement account management functionality here
                # Account Management Loop
                while True:
                    print("\n\t\t\t\t\t","*"*40)
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Display Balance")
                    print("4. Send Money")
                    print("5. Mini Account Statement")
                    print("6. Get Statement on Mail")
                    print("7. Change Password")
                    print("8. Logout\n")

                    account_choice = input("Enter your choice: ")

                    if account_choice == '1':
                        amount =input("Enter amount to deposit: ")
                        if amount.isdigit() and float(amount)>0:
                           amount=float(amount)
                           user_account.deposit(amount)
                        else:
                            print("\n\t\t\t\t\t########   Invalid Amount     ########")
                        
                    elif account_choice == '2':
                        amount =(input("Enter amount to withdraw: "))
                        if amount.isdigit() and float(amount)>0:
                            amount=float(amount)
                            user_account.withdraw(amount)
                        else:
                            print("\n\t\t\t\t\t########   Invalid Amount     ########")
                        
                    elif account_choice == '3':
                        user_account.display_balance()
                    elif account_choice == '4':
                        recipient_account_number = input("Enter recipient account number: ")
                        amount = input("Enter amount to send: ")
                        if amount.isdigit() and float(amount)>0:
                            amount=float(amount)
                            recipient_account = next((acc for acc in accounts if acc.account_number == recipient_account_number), None)
                            if recipient_account:
                                user_account.send_money(recipient_account, amount)
                            else:
                                print("Recipient account not found.")
                        else:
                            print("\n\t\t\t\t\t########   Invalid Amount     ########")
                        
                    elif account_choice == '5':    
                        # Define the file path
                        file_path = f'C:/Users/Abhinav Pandey/Documents/PYTHON/Database/{user_account.email}.txt'
                        # Read the entire file into a list
                        with open(file_path, 'r') as file:
                            last_lines = deque(file, maxlen=3)
                        # Process each line
                        for line in last_lines:
                            date, transaction_mode, amount, transaction_type, balance = line.strip().split(',')
                            print("\n")
                            print(f"Date: {date}")
                            print(f"Transaction Type: {transaction_type}")
                            print(f"Amount: {amount}")
                            print(f"Particular: {transaction_mode}")
                            print(f"Balance: {balance}")
                            print('-----------------------')
                        print("\n\t\t\t**********************     Press Enter to Continue!!    ************************")
                        input()
                    elif account_choice=='6':
                        print("Sending...")
                        # Define the file path
                        file_path = f'C:/Users/Abhinav Pandey/Documents/PYTHON/Database/{user_account.email}.txt'
                        # Read the entire file into a list
                        with open(file_path, 'r') as file:
                            data = file.readlines()
                        # Parse and format the data into rows with columns
                        formatted_data = []
                        for line in data:
                            parts = line.strip().split(',')
                            formatted_data.append({
                                'Date': parts[0],
                                'Particulars': parts[1],
                                'Amount': parts[2],
                                'Status': parts[3],
                                'Balance': parts[4]
                            })
                        # Create PDF with formatted data
                        date=datetime.now().strftime("%d/%m/%Y")
                        pdf_filename = create_transaction_pdf(formatted_data,user_account.name,user_account.account_number,user_account.email,date)
                        # Send the email with the attachment
                        subject="Account Statement"
                        to=f"{user_account.name} <{user_account.email}>"
                        content="""
Dear Valued Customer,

We hope this message finds you well.
Please find attached your latest bank account statement. This statement includes all transactions on your account. We encourage you to review it carefully and keep it for your records.

Thank you! 
Best regards,
The Bank Team
"""
                        dev_send_email_with_attachment(pdf_filename,subject,to,content)
                        print("Account Statement has been sent on your E-Mail.")
                    elif account_choice == '7':
                        new_password = input("Enter new password: ")
                        user_account.set_password(new_password)
                        with open("accounts.txt", "r+") as file:
                            lines = file.readlines()
                            file.seek(0)
                            for i, line in enumerate(lines):
                                if user_account.account_number in line:
                                    parts = line.strip().split(",")
                                    parts[-1] = new_password
                                    lines[i] = ",".join(parts) + "\n"
                            file.truncate(0)
                            file.writelines(lines)
                        print("Password changed successfully.")
                    elif account_choice == '8':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '5':
            print('''
              **************************************************************
                            THANKS FOR USING OUR SYSTEM
              **************************************************************
              ''')
            break
        elif choice=='3':
            eml = input("Enter your email address: ")  # Prompt for user's email
            if '@' not in eml:
                eml=eml+'@gmail.com'
            else:
                pass
            email=eml.lower()
            reset_password(accounts, email)  # Call reset_password function with accounts list and email

        elif choice=='4':
            find_account_number(accounts)
        elif choice == '7410':
            accounts=load_accounts()
            st="                    D   E   V   L   O   P   E   R       M   O   D   E       A   C   T   I   V   A   T   E   D"
            a=['']
            for i in range(32,123):
                a.append(chr(i))
            pr=""
            rm=""
            for i in range(0,len(st)):
                while(pr!=st[i]):
                    pr=random.choice(a)
                    time.sleep(0.001)
                    print(rm+pr)
                rm=rm+pr
            print('''
                                **************************************************************
                                            A    D   M   I   N       P   A   N   E   L
                                **************************************************************
              ''')
            dev_eml=input("Enter Devloper's Email: ").lower()
            if "@" not in dev_eml:
                dev_eml+="@gmail.com"
            if dev_eml==sender_email:
                dev_pass=input("Enter Execution Code: ")
                if dev_pass==dev_eml:
                    while True:
                        print('''
1. Add User.
2. Display All Data.
3. Delete User's Account.
4. Get All data on Email.
5. Back.                                                          
''')
                        dev_choice = input("Enter your choice: ")

                        if dev_choice=="1":
                            user_account = dev_create_account(accounts)
                            if user_account:
                                accounts.append(user_account)

                        elif dev_choice=="2":
                            with open ("accounts.txt", "r+") as file:
                                    data = file.readlines()
                                    # Process the data into a list of lists
                                    processed_data = [line.strip().split(',') for line in data]

                                    # Define the column names
                                    columns = ['Name', 'Email Address', 'Account Number', 'Amount', 'Code']

                                    # Create the DataFrame
                                    df = pd.DataFrame(processed_data, columns=columns)

                                    # Add an S.No column starting from 1
                                    df.insert(0, 'S.No.', range(1, len(df) + 1))

                                    # Display the DataFrame
                                    print(df.to_string(index=False))
                        elif dev_choice=="3":
                            # Get the email input from the user
                            user_email = input("Enter the email to delete the account: ").lower()
                            if user_email =="":
                                print("Please enter a valid Email...")
                            elif "@" not in user_email:
                                user_email+="@gmail.com"
                                # Path to the accounts file
                            file_path = 'accounts.txt'
                                # Delete the row with the specified email
                            dev_delete_row_by_email(file_path, user_email)
                        elif dev_choice=="4":
                            dev_get_data_on_mail()
                        elif dev_choice=="5":
                            break
                        else:
                            print("You have pressed wrong key!!")

                else:
                    print("\n\t\t\t\tXXXXXX     Wrong Password      XXXXXX\n")
            else:
                print("\n\t\t\t\tXXXXXXX     Wrong Email     XXXXXX\n")
        else:
            print("Invalid choice. Please try again.")
            continue

if __name__ == "__main__":
    main()
