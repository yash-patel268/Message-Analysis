import re
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
import os
import json

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")
emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')

with open("email_domains.json", "r") as f:
    common_emails = json.load(f)
    
with open("phonenumber_area_codes.json", "r") as f:
    canada_phonenumbers = json.load(f)

os.system('cls')

print("Hello user, this is the message analysis program which will be used to find phisihing within emails and text messages.\n")
print("For this instance of this application which type of message will be analyzed, text message or emai?\n")

input_checker = 0
input_type = ""
user_email = ""
common_domain = False
user_text = ""
common_area_code = False
user_message_content = ""
message_emotion = ""

while input_checker == 0:
    print("Write 'text' or 'email'.")
    input_type = input("Enter the message type: ")
    
    if input_type == 'text' or input_type == 'email':
        print("The message type selected is: " + input_type + "\n")
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
            print("The email entered is: " + user_email + "\n")
            input_checker = 1
        else:
            print("Your input is not a proper email.\n")
        
        if input_checker == 1:
            input_checker = 0
            break
else:
    while input_checker == 0:
        print("Write the phone number of sender")
        user_text = input("Enter the phone number: ")
        pattern = r"\d{3}-\d{3}-\d{4}"  

        if re.match(pattern, user_text):
            print("The phone number entered is: " + user_text + "\n")
            input_checker = 1
        else:
            print("Invalid phone number\n")
            
        if input_checker == 1:
            input_checker = 0
            break
        
while input_checker == 0:
    print("Write or copy/paste the message content.")
    user_message_content = input("Enter message now: ")
    print("\nThe message entered is: " + user_message_content)
    
    print("Is the message correct enter 'y' or 'n' ")
    verified_message = input("Enter your decision: ")
    
    if verified_message == 'y':
        print("You have verified the message content.\n")
        input_checker = 1
    else:
        print("Write the message again.\n")
        
    if input_checker == 1:
            input_checker = 0
            break  

emotion_labels = emotion(user_message_content)
emotion_output = emotion_labels[0]
emotion_type = emotion_output.get('label')

happy_words = ["admiration", "amusement", "approval", "caring", "desire", "excitement", "gratitude", "joy", "love", "optimism", "pride", "relief"]
depression_words = ["grief", "remorse", "sadness"]
anger_words = ["anger", "annoyance", "dissapointment", "dissaproval", "digust"]
anxiety_words = ["embrassment", "fear", "nervousness"]

if emotion_type in happy_words:
    message_emotion = "happy"
elif emotion_type in depression_words:
    message_emotion = "depression"
elif emotion_type in anger_words:
    message_emotion = "anger"
elif emotion_type in anxiety_words:
    message_emotion = "anxiety"
else:
    message_emotion = "neutral"
    
print("Emotion detected is: " + message_emotion)

if input_type == 'email':
    for item in common_emails:
        if item in user_email:
            input_checker = 1
    
    if input_checker == 1:
        print("Entered email has common domain.")
        common_domain = True
    else: 
        print("Entered email doesn't have common domain.")
        common_domain = False
else:
    for item in canada_phonenumbers:
        if item in user_text[:3]:
            input_checker = 1
            
    if input_checker == 1:
        print("Entered phone number is part of the area codes in Canada.")
        common_domain = True
    else: 
        print("Entered phone number isn't part of the area codes in Canada.")
        common_domain = False