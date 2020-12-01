from selenium import webdriver
import pyautogui, time, os, json, re, time

# try:
#     driver = webdriver.Chrome("gmeetclass/chromedriver.exe")
# except:
#     print("Your browser needs to be updated.")
#     input(": ")
#     raise SystemExit

def clr(): os.system("CLS")

class Gmeetclass:
    def __init__(self):
        pass

class TimeTable:
    def __init__(self, periods, subjects):
        self.period_dict = periods
        self.subject_dict = subjects
        self.dotw = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}

    def make_time_table(self):
        periods = [int(k) for k in self.period_dict.keys()]
        subjects = [for k in self.subject_dict.keys()]
        table_dict = {}
        for day in self.dotw.values():
            table_dict[day] = {}
            print("Your Subjects are {subjects}")
            for period in periods:
                print(f"What subject do you have at session/period {period} on a {day}?")
                sub = input(": ").capitalize()
                while not sub in subjects:
                    print(f"Strange... That subject in your subject lineup. Delete the userdata folder at {os.cwd()}\\gmeetclass and then restart the program to make changes.")
                    sub = input(": ").capitalize()
                
                table_dict[day][period] = sub

            print(f"Time Table for {day} complete!")
            time.sleep(2)
            clr()

        return table_dict

class Subjects:
    def __init__(self, count):
        self.count = count

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

        clr()
        return my_dict
    

class Period:
    def __init__(self, count):
        self.count = count

    def timings(self):
        print("Note: Time must be given in 24 hour format, so 1:00pm is 13:00")
        print("Therefore time will be entered in the format of 'hours:minutes' (09:20) for example.")
        my_dict = {}
        for num in range(self.count):
            print(f"What time does period {num} end?")
            etime = input(": ")
            while not re.match(r"[0-9][0-9]:[0-9][0-9]", etime):
                print("That does not match the format of '00:00'")
                etime = input(": ")

            my_dict[str(num)] = etime

        print("Completed.")
        time.sleep(2)
        clr()
        return my_dict

class Setup:
    def __init__(self):
        pass

    def setup(self): os.mkdir("gmeetclass")
        

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

    def userdata(self):
        period_count = self.get_counts("periods/sessions do you have in a day", 10)
        sub_count = self.get_counts("subjects do you do", 15)
        period_dict = Period(period_count).timings()
        subject_dict = Subjects(sub_count).get_subjects()
        table_dict = TimeTable(period_dict, subject_dict).make_time_table()
        os.rename("chromedriver.exe", "./gmeetclass/chromedriver.exe")
        os.mkdir("./gmeetclass/userdata")
        user_dict = {"user_periods": period_dict, "user_subjects": subject_dict, "user_table": table_dict}
        with open("gmeetclass/userdata/userdata.json", "w") as f:
            json.dump(user_dict, f, indent=4)

if not os.path.exists("./gmeetclass"): Setup().setup()
if not os.path.exists("./gmeetclass/userdata"): Setup().userdata()
with open("userdata.json") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        print("Something went wrong with your data... Please Relaunch the program")
        os.rmdir("./gmeetclass/userdata")
        time.sleep(3)
        raise SystemExit