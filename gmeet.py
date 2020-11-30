from selenium import webdriver
import pyautogui, time, os, json, re

# try:
#     driver = webdriver.Chrome("chromedriver.exe")
# except:
#     print("Your browser needs to be updated.")
#     input(": ")
#     raise SystemExit

def clr(): 
    os.system("CLS")

class Gmeetclass:
    def __init__(self,):
        pass

class Subjects:
    def __init__(self):
        pass

class TimeTable:
    def __init__(self):
        pass

class Periods:
    def __init__(self):
        pass

class Setup:
    def __init__(self):
        pass

    def setup(self):
        os.mkdir("gmeetclass")
        os.mkdir("gmeetclass/screenshots")
        os.mkdir("gmeetclass/userdata")

    def get_counts(self, counting, highest):
        print(f"How many {counting}?")
        amount = input(": ")
        while True:
            try:
                amount = int(amount)
                if amount < 1 or amount > highest:
                    print(f"Value must be more than 0 and less than {highest}... please?")
                    raise ValueError
                break
            except ValueError:
                print("Come now... Give me a proper, logical number.")
                amount = input(": ")
        
        clr()
        return amount

    def get_subjects(self, sub_count):
        my_dict = {}
        print("Enter the name for a subject that you do?")
        for _ in range(sub_count):
            subject_name = input(": ").capitalize()
            print("What is the lookup google meet link for this class?")
            print("I recommend getting the link from the header in your google classroom that looks like https://meet.google.com/lookup/some_code.")
            link = input(": ")
            while not re.match(r"https://meet.google.com/.+", link):
                print("Strange. That isn't what I'm looking for. Try again...")
                link = input(": ")

            my_dict[subject_name] = link
            print("Enter your next Subject name")

    def userdata(self):
        num_of_periods = self.get_counts("periods/sessions do you have in a day", 10)
        sub_count = self.get_counts("subjects do you do", 15)
        subject_dict = self.get_subjects(sub_count)
    
if not os.path.exists("./gmeetclass"): Setup.setup()
if not os.path.exists("./gmeetclass/userdata"): Setup.userdata()