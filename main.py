import re
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline
import os
import json

# Initializing the EmoRoBERTa library, code provided by creator, allows us to create a pipeline to feed words to be analyzed
tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")
emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')

# Open email data set, read contents, lower case the strings, assign to common_emails array
with open("email_domains.json", "r") as f:
    common_emails = json.load(f)
common_emails = [word.lower() for word in common_emails]

# Open area code data set, read contents, assign to canada_phonenumbers array
with open("phonenumber_area_codes.json", "r") as f:
    canada_phonenumbers = json.load(f)
    
# Open phishing word data set, read contents, lower case strings, assign to common_phishing_words array
with open("phishing_words.json", "r") as f:
    common_phishing_words = json.load(f)
common_phishing_words = [word.lower() for word in common_phishing_words]
    
# Initializing overall emotions arrays which are based of results of EmoRoBERTa analysis
happy_words = ["admiration", "amusement", "approval", "caring", "desire", "excitement", "gratitude", "joy", "love", "optimism", "pride", "relief"]
depression_words = ["grief", "remorse", "sadness"]
anger_words = ["anger", "annoyance", "dissapointment", "dissaproval", "digust"]
anxiety_words = ["embrassment", "fear", "nervousness"]

os.system('cls')

print("Hello user, this is the message analysis program which will be used to find phisihing within emails and text messages.\n")
print("For this instance of this application which type of message will be analyzed, text message or email?\n")

# Initialize var to check user input, will be reused throughout code
input_checker = 0
# Initialize var to hold user message type
input_type = ""
# Initialize var to hold subject line if user chooses email
user_email_subject_line = ""
# Initialize var to hold number of phishing words found in subject line
subject_line_score = 0
# Initialize var to hold total number of words in subject line
subject_line_words = 0
# Initialize var to hold email  if user chooses email
user_email = ""
# Initialize var to decision on whether email entered if they did has common domain
common_domain = False
# Initialize var to hold phone number  if user chooses text
user_text = ""
# Initialize var to decision on whether phone number entered has common area code
common_area_code = False
# Initialize var to hold main message regardless of email or text
user_message_content = ""
# Initialize var to hold number of phishing words found in message content
message_content_score = 0
# Initialize var to hold total number of words in message content
message_content_words = 0
# Initialize var to hold emotion of subject line if they choose email
subject_line_emotion = ""
# Initialize var to hold emotion of main message
message_emotion = ""
# Initialize var to hold overall phishing score
total_phishing_score = 0

# Loop to get user input of what type of message they would like to analyze
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

# Loop to obtain proper email if the user chooses email as the focus of the application
if input_type == 'email':
    while input_checker == 0:
        print("Write the email of sender.")
        user_email = input("Enter the email: ")
        
        if "@" in user_email and "." in user_email:
            print("The email entered is: " + user_email + "\n")
            input_checker = 1
        else:
            print("Your input is not a proper email.\n")
        
        if input_checker == 1:
            input_checker = 0
            break
# Loop to obtain proper phone number if the user chooses text as the focus of the application
else:
    while input_checker == 0:
        print("Write the phone number of sender in XXX-XXX-XXXX format")
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
      
# Loop to get subject line that is entered and is confirmed by user if email is focus
if input_type == 'email':
    while input_checker == 0:
        print("Write the emails subject line from sender.")
        user_email_subject_line = input("Enter subject line of email: ")
        print("\nThe subject line entered is: " + user_email_subject_line)
        
        print("Is the subject line correct enter 'y' or 'n' ")
        verified_message = input("Enter your decision: ")
    
        if verified_message == 'y':
            print("You have verified the subject line content.\n")
            input_checker = 1
        else:
            print("Write the subject line again.\n")
            
        if input_checker == 1:
                input_checker = 0
                verified_message = ""
                break 

# Loop to get main messaged that is entered and is confirmed by user regardless of text or email is focus    
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
            verified_message = ""
            break  
        
# Determine whether email is within common email dataset, if not increment overall phishing score, if email was choosen as focus
if input_type == 'email':
    for item in common_emails:
        if item in user_email:
            input_checker = 1
    
    # Start of report for email
    if input_checker == 1:
        print("Entered email has common domain.")
        common_domain = True
    else: 
        print("Entered email doesn't have common domain.")
        common_domain = False
        total_phishing_score += 1
# Determine whether area code of phone number is within canada area code dataset, if not increment overall phishing score, if text was choosen as focus        
else:
    for item in canada_phonenumbers:
        if item in user_text[:3]:
            input_checker = 1
    
    # Start of report for text
    if input_checker == 1:
        print("Entered phone number is part of the area codes in Canada.")
        common_domain = True
    else: 
        print("Entered phone number isn't part of the area codes in Canada.")
        common_domain = False
        total_phishing_score += 1
        
# Determine whether phishing is present within subject line, done by determining emotion and number of phishing words,
# the phishing words is then compared to overall words and if its less than 30% of subject line its considered safe,
# else overall phishing score is increment
# emotion is dependent on whether if theres phishing words are present, else it would be a false reading,
# if neutral, anxiety, or anger increment since it suspicious phrase tend to lay within those emotions. 
if input_type == "email":
    for item in common_phishing_words:
        if item in user_email_subject_line.lower():
            subject_line_score += 1
    
    emotion_labels = emotion(user_email_subject_line)
    emotion_output = emotion_labels[0]
    emotion_type = emotion_output.get('label')
    
    if emotion_type in happy_words:
        subject_line_emotion = "happy"
    elif emotion_type in depression_words:
        subject_line_emotion = "depression"
    elif emotion_type in anger_words:
        subject_line_emotion = "anger"
        if subject_line_score != 0:
            total_phishing_score += 1
    elif emotion_type in anxiety_words:
        subject_line_emotion = "anxiety"
        if subject_line_score != 0:
            total_phishing_score += 1
    else:
        subject_line_emotion = "neutral"
        if subject_line_score != 0:
            total_phishing_score += 1
    
    # Inclusion of subject for report if email is chosen as focus 
    print("Emotion detected in subject line is: " + subject_line_emotion)
    
    print("Number of phishing words used in the subject line is: " + str(subject_line_score))
    
    subject_line_words = user_email_subject_line.split()
    subject_line_words = len(subject_line_words)
    
    print("Number of words in the subject line is: " + str(subject_line_words))
    
    if ((subject_line_score/subject_line_words) < 0.30):
        print("The overall subject line score is within a safe range to be considered not phishing.")
    else:
        print("Phishing attempt was detected in the subject line.")
        total_phishing_score += 1

# Determine whether phishing is present within main message, done by determining emotion and number of phishing words,
# the phishing words is then compared to overall words and if its less than 20% of main message and it has less than 5 phishing words
# its considered safe, else overall phishing score is increment
# emotion is dependent on whether if theres phishing words are present, else it would be a false reading,
# if neutral, anxiety, or anger increment since it suspicious phrase tend to lay within those emotions. 
for item in common_phishing_words:
    if item in user_message_content.lower():
        message_content_score += 1

emotion_labels = emotion(user_message_content)
emotion_output = emotion_labels[0]
emotion_type = emotion_output.get('label')

if emotion_type in happy_words:
    message_emotion = "happy"
elif emotion_type in depression_words:
    message_emotion = "depression"
elif emotion_type in anger_words:
    message_emotion = "anger"
    if message_content_score != 0:
        total_phishing_score += 1
elif emotion_type in anxiety_words:
    message_emotion = "anxiety"
    if message_content_score != 0:
        total_phishing_score += 1
else:
    message_emotion = "neutral"
    if message_content_score != 0:
        total_phishing_score += 1
    
# Rest of report is printed regardless of focus
print("Emotion detected in message content is: " + message_emotion)
    
print("Number of phishing words used in the message content is: " + str(message_content_score))

message_content_words = user_message_content.split()
message_content_words = len(message_content_words)
    
print("Number of words in the subject line is: " + str(message_content_words))

if ((message_content_score/message_content_words) < 0.20 and message_content_score < 5):
    print("The overall message content score is within a safe range to be considered not phishing")
else:
    total_phishing_score += 1
    print("Phishing attempt was detected in the message content.")
    
# Overall phishing score for email determined by 5 different aspects:
# email domain, number of phishing words in subject line, emotion in subject line,
# number of phishing words in main message, and emotion in main message.
if input_type == "email":
    total_phishing_score = round((total_phishing_score/5)*100, 2)
    print("The phishing score is: " + str(total_phishing_score) + "%")
# Overall phishing score for text determined by 3 different aspects:
# phone number area code,number of phishing words in main message, and emotion in main message.
else:
    total_phishing_score = round((total_phishing_score/3)*100, 2)
    print("The phishing score is: " + str(total_phishing_score) + "%")