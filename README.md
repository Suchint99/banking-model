🔹 What This Program Does
It simulates a bank management system with both user and admin modes.

User Features:
Sign Up (New Account)
Asks for email, name, DOB, address.
Generates an Account Number.
Sends an OTP to your email for verification.

After verification:
Saves details in accounts.txt.
Creates a personal transaction file (<email>.txt).
Generates a QR code image containing account details.
Sends a welcome email with QR code attached.

✅ Example Output on console:

********OTP HAS BEEN SENT ON YOUR EMAIL.*********
******OTP Verified.********
************************************************************
CONGRATULATIONS!! YOUR ACCOUNT HAS BEEN CREATED,
LOGIN CREDENTIALS HAS BEEN SENT ON YOUR EMAIL.
************************************************************


And it generates this QR:
Login
Enter Account Number + Password.
Access menu:
Deposit money
Withdraw money
Show balance
Send money to another account
Show mini statement (last 3 transactions)
Email full statement as PDF attachment
Change password
Logout

✅ Example Output for Mini Statement:

Date: 22/08/2025
Transaction Type: DEPOSIT
Amount: Rs. 2000
Particular: BY CASH
Balance: Rs. 5000
-----------------------


Reset Password
Sends OTP to registered email.
After verification, allows new password.
Sends confirmation mail.
Find Account Number
If you forgot account number, enter Name + Email + Password → it displays your account number.
Admin Features (Hidden Code 7410)
If you enter 7410 at main menu, admin panel opens:
Add User (without OTP, directly create).
Show All Accounts in a table (using Pandas).
Delete User by Email.
Get all accounts data as PDF and send it via email.

✅ Example Output for Admin “Show All Data”:

 S.No.   Name       Email Address       Account Number      Amount  Code
  1    RAM KUMAR    ram@gmail.com       1234567890          2000    pass123
  2    SHYAM VERMA  shyam@gmail.com     9876543210          3500    shyam@123

Example of Generated PDF (Account Statement)

When user requests full statement:

The Kartikesh MC Bank
---------------------------------
Account Statement
Name: RAM KUMAR        Updated on: 22/08/2025
Account Number: 1234567890   Email: ram@gmail.com

Date        Particulars        Amount      Status        Balance
22/08/2025  BY CASH            Rs. 2000    DEPOSIT       Rs. 5000
22/08/2025  ATM Withdrawal     Rs. 1000    WITHDRAWAL    Rs. 4000


✅ So in short:
This program is a banking system simulator that:
Manages users and accounts
Logs transactions
Sends OTPs & statements by email
Generates QR codes & PDF account statements
Provides an admin panel for managing all users
