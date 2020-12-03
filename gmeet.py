from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import time, os, json, re, pyautogui

# try:
#     driver = webdriver.Chrome("gmeetclass/chromedriver.exe")
# except:
#     print("Your browser needs to be updated.")
#     input(": ")
#     raise SystemExit
# Login Page: https://accounts.google.com/signin/v2/identifier?service=classroom&passive=1209600&continue=https%3A%2F%2Fclassroom.google.com%2Fu%2F0%2Fh&followup=https%3A%2F%2Fclassroom.google.com%2Fu%2F0%2Fh&flowName=GlifWebSignIn&flowEntry=ServiceLogin


def clr(): os.system("CLS")

def get_counts(counting, highest):
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

class Gmeetclass:
    def __init__(self, user_dict, driver=None, time_table=None):
        self.user_dict = user_dict
        self.driver = driver
        self.time_table = time_table

    def setup(self):
        try:
            self.driver = webdriver.Chrome("gmeetclass/chromedriver.exe")
            print("Driver Connected")
        except exceptions.WebDriverException:
            print("Could not find chromedriver.exe. Makesure it is in the gmeetclass folder")
            input(": ")
            raise SystemExit

        except Exception as err:
            print(err)
            input(": ")
            raise SystemExit

        clr()
    
    def login(self):
        print("Loading login page.")
        self.driver.get("https://accounts.google.com/signin/v2/identifier?service=classroom&passive=1209600&continue=https%3A%2F%2Fclassroom.google.com%2Fu%2F0%2Fh&followup=https%3A%2F%2Fclassroom.google.com%2Fu%2F0%2Fh&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        print("Login with your school account then come back to this program and press enter to proceed")
        input(": ")
        clr()

    def start(self):
        self.time_table = TimeTable().get_time_table(self.user_dict['user_table'])

    def session(self):
        period_dict = self.user_dict['user_periods']
        subject_dict = self.user_dict['user_subjects']
        periods = [k for k in period_dict.keys()]
        start_minutes = self.get_minutes(self.user_dict['start_time'])
        print(f"Waiting until {self.user_dict['start_time']} to begin {self.time_table['0']}.")
        cminutes = self.get_minutes(re.findall(r"[0-9][0-9]:[0-9][0-9]", time.ctime())[0])
        while cminutes < start_minutes:
            print(f"{int(cminutes) - int(start_minutes)} minutes remain before I begin.")
            time.sleep(40)
            cminutes = self.get_minutes(re.findall(r"[0-9][0-9]:[0-9][0-9]", time.ctime())[0])

        for period in periods:
            clr()
            ctime = re.findall(r"[0-9][0-9]:[0-9][0-9]", time.ctime())[0]
            cminutes = self.get_minutes(ctime)
            print(f"The current time is {ctime}")
            print(f"Preparing to join {self.time_table[period]} which will end at {period_dict[period]}")
            endtime = self.get_minutes(period_dict[period])
            if cminutes > endtime: print("This session is already over"); continue
            self.driver.get(subject_dict[self.time_table[period]])
            time.sleep(5)
            joined = self.attempt_join()
            print("Attempting to join")
            while not joined and cminutes < endtime:
                joined = self.attempt_join()
                cminutes = self.get_minutes(re.findall(r"[0-9][0-9]:[0-9][0-9]", time.ctime())[0])
                if not joined: 
                    print("Something went wrong... trying again")
                    self.driver.get(subject_dict[self.time_table[period]])
                    joined = self.attempt_join()
                    cminutes = self.get_minutes(re.findall(r"[0-9][0-9]:[0-9][0-9]", time.ctime())[0])
                    if cminutes < endtime: break
                    continue
                clr()
            if cminutes > endtime: print("Class is over"); continue
            print(f"Joined {self.time_table[period]}")

            
            chat = pyautogui.locateOnScreen("gmeetclass/images/chat.png", confidence=0.7)
            
            if chat: 
                pyautogui.moveTo(chat)
                captions = pyautogui.locateOnScreen("gmeetclass/images/captions.png", confidence=0.8)
                while not captions:
                    pyautogui.moveTo(chat)
                    captions = pyautogui.locateOnScreen("gmeetclass/images/captions.png", confidence=0.8)
                    if not captions: continue
                    captions.click()
                pyautogui.click(chat)
                pyautogui.typewrite(self.user_dict['join_message'])
                pyautogui.press("enter")

            while cminutes < endtime:
                time.sleep(10)
                self.screen_check(self.time_table[period])
                cminutes = self.get_minutes(re.findall(r"[0-9][0-9]:[0-9][0-9]", time.ctime())[0])

            print("Session Over")
            time.sleep(2)
            clr()
            continue

        print("Bye bye")
        self.driver.close()

    def attempt_join(self):
        refresh = pyautogui.locateOnScreen("gmeetclass/images/reload.png", confidence=0.8)
        if refresh: return False
        print("We're almost there")
        time.sleep(10)
        dismiss = pyautogui.locateOnScreen("gmeetclass/images/dismiss.png", confidence=0.7)
        if dismiss: pyautogui.click(dismiss)
        block = pyautogui.locateOnScreen("gmeetclass/images/block.png", confidence=0.8)
        if block: pyautogui.click(block)
        time.sleep(5)
        join = pyautogui.locateOnScreen("gmeetclass/images/join.png", confidence=0.8)
        if join: 
            pyautogui.click(join)
            return True
        else: 
            print("Could not find Join Button")
            return False

    def screen_check(self, current_class):
        if not os.path.exists("gmeetclass/screenshots"): os.mkdir("gmeetclass/screenshots")
        if not os.path.exists(f"gmeetclass/screenshots/{current_class}"):os.mkdir(f"gmeetclass/screenshots/{current_class}")
        screenshots = [screenshot for screenshot in os.listdir(f"gmeetclass/screenshots/{current_class}") if screenshot.endswith(".png") and screenshot.startswith(current_class)]
        if screenshots:
            highest = self.get_last(screenshots) + 1
        else:
            highest = 1
        self.driver.save_screenshot(f"screenshots/{current_class}/{current_class}{highest}.png")
        print("Screenshot taken") 

    def get_last(self, itera):
        numbers = []
        for img in itera:
            numbers.append(int(re.findall(r"([0-9]+)", img.split(".")[0])[-1]))
        return sorted(numbers)[-1]

    def get_minutes(self, value):
        time = value.split(":")
        hours, minutes = int(time[0]), int(time[1])
        return (hours * 60) + minutes


class TimeTable:
    def __init__(self, periods=None, subjects=None):
        self.period_dict = periods
        self.subject_dict = subjects
        self.dotw = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}

    def make_time_table(self, user_dict=None):
        periods = [k for k in self.period_dict.keys()]
        subjects = [k for k in self.subject_dict.keys()]
        if not user_dict: table_dict = {}
        else: table_dict = user_dict['user_table']
        for day in self.dotw.values():
            table_dict[day] = {}
            print(f"Your Subjects are {subjects}")
            for period in periods:
                print(f"What subject do you have at session/period {period} on a {day}?")
                sub = input(": ").capitalize()
                while not sub in subjects:
                    print(f"Strange... That subject in your subject lineup. Delete the userdata folder at {os.getcwd()}\\gmeetclass and then restart the program to make changes.")
                    sub = input(": ").capitalize()
                
                table_dict[day][period] = sub

            print(f"Time Table for {day} complete!")
            time.sleep(2)
            clr()

        if user_dict: return user_dict
        else: return table_dict

    def get_time_table(self, table_dict):
        day = time.ctime().split(" ")[0]
        print(f"Getting your time table for {self.dotw[day]}")
        print(table_dict[self.dotw[day]])
        print("Completed")
        time.sleep(2)
        return table_dict[self.dotw[day]]
        

class Subjects:
    def __init__(self):
        pass

    def set_subjects(self, user_dict=None):
        count = get_counts("subjects do you do", 15)
        if not user_dict: my_dict = {}
        else: my_dict = user_dict['user_subjects']
        print("Enter the name for a subject that you do?")
        for _ in range(count):
            subject_name = input(": ").capitalize()
            print("What is the lookup google meet link for this class?")
            print("I recommend getting the link from the header in your google classroom that looks like https://meet.google.com/lookup/some_code.")
            link = input(": ")
            while not re.match(r"https://meet.google.com/.+", link):
                print("Strange. That isn't what I'm looking for. Try again...")
                link = input(": ")

            my_dict[subject_name] = link
            print("Enter your next Subject name")

        clr()
        if user_dict: return user_dict
        else: return my_dict
    

class Period:
    def __init__(self):
        pass

    def set_periods(self, user_dict=None):
        count = get_counts("periods/sessions do you have in a day", 10)
        print("Note: Time must be given in 24 hour format, so 1:00pm is 13:00")
        print("Therefore time will be entered in the format of 'hours:minutes' (09:20) for example.")
        
        if not user_dict: my_dict = {}
        else: my_dict = user_dict['user_periods']
        for num in range(count):
            print(f"What time does period {num} end?")
            etime = input(": ")
            while not re.match(r"[0-9][0-9]:[0-9][0-9]", etime):
                print("That does not match the format of '00:00'")
                etime = input(": ")

            my_dict[str(num)] = etime

        print("Completed.")
        time.sleep(2)
        clr()
        if user_dict: return user_dict
        else: return my_dict

class Setup:
    def __init__(self, period_dict=None, subject_dict=None, table_dict=None, join_message=None, start_time=None):
        self.period_dict = period_dict
        self.subject_dict = subject_dict
        self.table_dict = table_dict
        self.join_message = join_message
        self.start_time = start_time


    def setup(self): 
        os.mkdir("gmeetclass")
        if os.path.exists("chromedriver.exe"): os.rename("chromedriver.exe", "./gmeetclass/chromedriver.exe")


    def set_msg(self, user_dict=None):
        print("What message should I send when Joining a google meet?")
        join_message = input(": ")
        if user_dict: user_dict['join_message'] = join_message; return user_dict
        return join_message

    def set_start_time(self, user_dict=None):
        print("What time does your first period/session begin?")
        etime = input(": ")
        while not re.match(r"[0-9][0-9]:[0-9][0-9]", etime):
            print("That does not match the format of '00:00'")
            etime = input(": ")

        if not user_dict: user_dict = {}
        user_dict['start_time'] = etime; return user_dict


    def userdata(self):
        if not os.path.exists("./gmeetclass/userdata"): os.mkdir("./gmeetclass/userdata")
        user_dict = {"user_periods": self.period_dict, "user_subjects": self.subject_dict, "user_table": self.table_dict, "join_message": self.join_message, "start_time": self.start_time}
        with open("gmeetclass/userdata/userdata.json", "w") as f:
            json.dump(user_dict, f, indent=4)

if not os.path.exists("./gmeetclass"): print("Please download the gmeetclass folder."); input(": "); raise SystemExit
if not os.path.exists("chromedriver.exe"): print("Please download the chromedriver.exe file."); input(": "); raise SystemExit

if not os.path.exists("./gmeetclass/userdata"): 
    period_dict = Period().set_periods()
    subject_dict = Subjects().set_subjects()
    table_dict = TimeTable(period_dict, subject_dict).make_time_table()
    join_message = Setup().set_msg()
    start_time = Setup().set_start_time()
    Setup(period_dict, subject_dict, table_dict, join_message, start_time).userdata()

with open("./gmeetclass/userdata/userdata.json") as f:
    try:
        user_dict = json.load(f)
    except json.JSONDecodeError:
        print("Something went wrong with your data... Please Relaunch the program")
        os.remove("./gmeetclass/userdata/userdata.json")
        os.rmdir("./gmeetclass/userdata")
        time.sleep(3)
        raise SystemExit
    except FileNotFoundError:
        print("Something went wrong with your data... Please Relaunch the program")
        os.remove("./gmeetclass/userdata/userdata.json")
        time.sleep(3)
        raise SystemExit

clr()
def showdict(dicti):
    for k, v in dicti.items():
        print(f"{k}: {v}")
    print()

def showinfo():
    print("Subjects:")
    showdict(user_dict['user_subjects'])
    print("Periods / Sessions:")
    showdict(user_dict['user_periods'])
    print("Time Table:")
    for k in user_dict['user_table'].keys():
        print(f"{k}:")
        showdict(user_dict['user_table'][k])
    print("Join Message:")
    print(user_dict['join_message'])
    print()
    print("Start Time:")
    print(user_dict['start_time'])
    print()

showinfo()

print("Is there anything here you wish to change? (y/n)")
change = input(": ")
if change.lower().startswith("y"):
    def changing(my_dict):
        while True:
            print("What would you like to change? Type 'nvm' to exit.")
            print("Options to change: 'user_subjects', 'user_periods', 'user_table', 'join_message', 'start_time'")
            change = input(": ")
            if change.lower() == "nvm": return my_dict
            elif change.lower() == "user_subjects": Subjects().set_subjects(my_dict)
            elif change.lower() == "user_periods": Period().set_periods(my_dict)
            elif change.lower() == "user_table": TimeTable(my_dict['user_periods'], my_dict['user_subjects']).make_time_table(my_dict)
            elif change.lower() == "join_message": Setup().set_msg(my_dict)
            elif change.lower() == "start_time": Setup().set_start_time(my_dict)
            else: print("I do not recognise that value.")
            clr()
            showinfo()
    user_dict = changing(user_dict)
    with open("gmeetclass/userdata/userdata.json", "w") as f:
        json.dump(user_dict, f, indent=4)
    print("Updated Successfully")

    
else: print("Moving on smartly")

clr()

session = Gmeetclass(user_dict)
session.setup()
session.login()
session.start()
session.session()