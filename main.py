import re

print("Hello user, this is the message analysis program which will be used to find phisihing within emails and text messages.\n")
print("For this instance of this application which type of message will be analyzed, text message or emai?\n")

input_checker = 0
input_type = ""
user_email = ""
user_text = ""

while input_checker == 0:
    print("Write 'text' or 'email'.")
    input_type = input("Enter the message type: ")
    
    if input_type == 'text' or input_type == 'email':
        print("The message type selected was: " + input_type + "\n")
        input_checker = 1
    else:
        print("Wrong input was entered please try again.\n")
    
    if input_checker == 1:
        input_checker = 0
        break

if input_type == 'email':
    while input_checker == 0:
        print("Write the email of sender")
        user_email = input("Enter the email: ")
        
        if "@" in user_email and "." in user_email:
            print("The email entered was: " + user_email + "\n")
            input_checker = 1
        else:
            print("Your input is not a proper email.\n")
        
        if input_checker == 1:
            input_checker = 0
            break
        
if input_type == 'text':
    while input_checker == 0:
        print("Write the phone number of sender")
        user_text = input("Enter the phone number: ")
        pattern = r"\d{3}-\d{3}-\d{4}"  

        if re.match(pattern, user_text):
            print("The phone number entered was: " + user_text + "\n")
            input_checker = 1
        else:
            print("Invalid phone number\n")
            
        if input_checker == 1:
            input_checker = 0
            break
