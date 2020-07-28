import sys
import subprocess
from smtplib import SMTP
import hashlib
import random
import datetime 
import pyfiglet
AdminEmail="rsaha0907@gmail.com"
creds={
    "Admin" :   {
                    "privilege"             :   "admin",
                    "user_id"               :   "1",
                    "name"                  :   "Rishav",
                    "password"              :   'e61cc90177d9a4b07240270b8f6caaf9420075f9bd8de502a32236cbb5f32056',
                    "amount"                :   1000,
                    "account_id"            :   1,
                    "Email"                 :   AdminEmail,
                    "twoStepVerification"   :   "No",
                    "LoggedIn"              :   "No"
                }
}
currentUser=[]


def RegisterUser():
    print(" CREATING NEW USER")
    print("====================")
    key=str(input("Enter your pin : "))
    hashedKey=hashlib.sha256(key.encode())
    password=hashedKey.hexdigest()
    userName=str(input("Enter your username : "))
    if userName in creds:
        if userName=="Admin" or userName == "admin" or userName == " admin":
            print("Sorry your username is not valid")
            sys.exit() 
        print("Username already in use")
    else:
        clientEmail=str(input("Enter your email address : "))
        for key in creds.keys():
            if creds[key]['Email']==clientEmail:
                print("Email already in use")
                break
        else:
            emailVerification(clientEmail,userName,password)

count=0  
def emailVerification(clientEmail,userName,password):
    otp=random.randrange(10000,99999)
    server=SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(AdminEmail,"iamacoder0907")
    from_addr=AdminEmail
    to_addr=clientEmail
    subj="ATM email verifiaction system"
    time=datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    message_text=otp
    message=f"Your OTP is {message_text}"
    server.sendmail(from_addr,to_addr,message)
    OTP=int(input("Enter your OTP : "))
    if OTP==otp:
        userAdding(userName,password,clientEmail)
    else:
        count+=1
        print("Sorry your OTP is not matching")
        print("We are sending a new otp to your email")
        emailVerification(clientEmail,userName,password)
        if count>3:
            sys.exit()

def userAdding(userName,password,clientEmail):
    account_id=random.randrange(1000000000,9999999999)
    name=str(input("Enter your name : "))
    amount=int(input("How much money would you like to deposit in your bank account : "))
    subCreds={
        userName:{
                "privilege"             :   "user",
                "user_id"               :   "2",
                "name"                  :   name,
                "password"              :   password,
                "amount"                :   amount,
                "account_id"            :   account_id,
                "Email"            :   clientEmail,
                "twoStepVerification"   :   "No",
                "LoggedIn"              :   "No"
        }
    }

    creds.update(subCreds)
    twoStepVerificationEnable(userName,subCreds)

def twoStepVerificationEnable(userName,subCreds):
    print("Do you want to activate two step verification in your bank account?")
    print("No")
    print("Yes")
    choose=str(input())
    if choose=='Yes' or choose=='yes':
        for key,pair in subCreds[userName].items():
            if subCreds[userName]["twoStepVerification"]=='No':
                subCreds[userName]["twoStepVerification"]='Yes'
                creds.update(subCreds)
            else:
                print("Two step verification is already enabled")
            break
    else:
        print("Two Step Verification makes you more secure :)")

    
def userLogout():
    LoginUsername=currentUser[0]
    if LoginUsername in creds:
        creds[LoginUsername]['LoggedIn']='No'
        print("Logged out")
        currentUser.clear()
    else:
        print("Not Logged in")

def balanceEnquiry():
    if creds[currentUser[0]]['LoggedIn']=='Yes':
        balance=creds[currentUser[0]]['amount']
        print(f"Total balance Left : {balance}")
    else:
        print("You need to login first")

def Userlogin():
    LoginUsername=str(input("Enter your username : "))
    if LoginUsername in creds:
        print("Username present")
        if creds[LoginUsername]['LoggedIn']=='No':
            LoginKey=str(input("Enter your password"))
            hashedKey=hashlib.sha256(LoginKey.encode())
            LoginPassword=hashedKey.hexdigest()
            if creds[LoginUsername]['password']==LoginPassword:
                creds[LoginUsername]['LoggedIn']="Yes"
                print("You are Logged in")
                currentUser.append(LoginUsername)

        
        else:
            print("You are already Logged In")
    else:
        print("Sorry username did not matched")

def main():
    banner=pyfiglet.figlet_format('Bank')
    print(banner)
    print('1. Register New User')
    print('2. Log In')
    print('3. Log Out')
    print('4. Balance Enquiry')
    option=int(input("Enter your options :"))
    if option==1:
        subprocess.call('clear')
        print(banner)
        RegisterUser()
    elif option==2:
        subprocess.call('clear')
        print(banner)
        Userlogin()
    elif option==3:
        subprocess.call('clear')
        print(banner)
        userLogout()
    elif option==4:
        subprocess.call('clear')
        print(banner)
        balanceEnquiry()
    else:
        print("Bad option")
        sys.exit()
while True:
    main()