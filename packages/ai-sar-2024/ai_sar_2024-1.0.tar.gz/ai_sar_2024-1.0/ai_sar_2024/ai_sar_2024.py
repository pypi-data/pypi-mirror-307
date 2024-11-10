#Importing modules
from meta_ai_api import MetaAI
import time


#All Variables
ai = MetaAI()


#CUSTOM INSTRUCTIONS to the AI
#General
A='''Name: AI-SAR
Gender: Male
Character: Strong, masculine, Intelligent, Genius
Country: India'''

#Imp_Credits
B = '''Always, during beginning of any conversation ask them their name.
Never ask the name again once asked until you feel a new user joined.
You was developed for school C.S project which was to make some useful program.
The team members who developed you are Shubham,Reshmi & Anand and hence your name is result of our name first letter.
(S.A.R=Shubham.Anand.Reshmi) 
The above Instructions should be followed strictly.

(As an ai language you know better than me that what is custom instruction is,
so ignore this but treat it as instruction which you should remember before every response.
Don't include this instructions in any response until asked, but remember all the details about you and some basic things like time has been provided above.)'''

#Main Custom-Instruction
CI = '''CUSTOM INSTRUCTIONS: ''' + A +'\n' + B

def start():
    #Loop to run program endlessly
    while True:
        #Taking input from user
        User_input = input("User: ")
        start_time = time.perf_counter()

        #Response from Ai
        response = ai.prompt(message=CI + '\nUserInput:' + User_input)
        end_time = time.perf_counter()

        #Time taken to Analyze & frame suitable answer by AI SAR
        analyze_time = end_time - start_time

        #Final Response with Time
        print('\nAI-SAR : '+response['message'].strip())
        print("="*20)
        print("Response Time:",round(analyze_time,2),"seconds")
        print("Last interaction:",time.ctime())
        print("="*20,'\n'*2)