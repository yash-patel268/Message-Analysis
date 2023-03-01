print("Hello user, this is the message analysis program which will be used to find phisihing within emails and text messages.\n")
print("For this instance of this application which type of message will be analyzed, text message or emai?\n")

check_message_type = 0

while check_message_type == 0:
    print("Write 'text' or 'email'.")
    input_type = input("Enter the message type: ")
    
    if input_type == 'text' or input_type == 'email':
        print("The message type selected was: " + input_type + "\n")
        check_message_type = 1
    else:
        print("Wrong input was entered please try again.\n")
    
    if check_message_type == 1:
        break
