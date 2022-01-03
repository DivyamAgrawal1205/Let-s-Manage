import pandas as pd                      # to analyse data from veg_data.csv
import datetime                          # to use date and time for check whether each and every item
import speech_recognition as sr          # to use speech and text


def date_ify(n):                         # to convert date and month into analysable form for vegetables
    time1 = datetime.date.today()
    month = time1.month
    date_number = n
    if month == 2:
        date_number = date_number + 31
    if month == 3:
        date_number = date_number + 59
    if month == 4:
        date_number = date_number + 90
    if month == 5:
        date_number = date_number + 120
    if month == 6:
        date_number = date_number + 151
    if month == 7:
        date_number = date_number + 181
    if month == 8:
        date_number = date_number + 212
    if month == 9:
        date_number = date_number + 243
    if month == 10:
        date_number = date_number + 273
    if month == 11:
        date_number = date_number + 304
    if month == 12:
        date_number = date_number + 334

    return date_number


def date_ify2(m, month):                 # to convert date and month into analysable form for packaged goods
    date_number = m
    if month == 2:
        date_number = date_number + 31
    if month == 3:
        date_number = date_number + 59
    if month == 4:
        date_number = date_number + 90
    if month == 5:
        date_number = date_number + 120
    if month == 6:
        date_number = date_number + 151
    if month == 7:
        date_number = date_number + 181
    if month == 8:
        date_number = date_number + 212
    if month == 9:
        date_number = date_number + 243
    if month == 10:
        date_number = date_number + 273
    if month == 11:
        date_number = date_number + 304
    if month == 12:
        date_number = date_number + 334

    return date_number


item_list = {}                            # to store consumable goods
expiry_list = {}                          # to store goods that would not be consumable in after one day
Time = datetime.date.today()              # to store date and time
day = Time.day
now_date = date_ify(day)                  # converting date into analysable form
while 1:
    # asking user whether he/she want to enter packaged food or vegetables
    choice = int(input("Enter 1 if you want to enter packaged items and 2 if you want to enter vegetables\n"))
    if choice == 2:  # if he/she want to enter vegetables
        # setting up for speech recognition
        recogniser = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recogniser.listen(source)
            veg = recogniser.recognize_google(audio)
            veg = veg.lower()
        # telling user what we understood
        print("You entered", veg)
        # using pandas to convert vegetable data into analysable form.
        veg_d = pd.read_csv("veg_data.csv")
        # now we start calculating approx. date for vegetable freshness
        life = 0
        # if veg is in the dataset take its value from the dataset
        try:
            life = veg_d.loc[veg_d["vegetable"] == veg, "shelf life"].values[0]
        # but if not available, then prompt the user and starting the whole process again
        except IndexError:
            print("This veg is not in our database!")
            continue
        new_time = now_date + life           # adding life of vegetable in current date
        item_list.update({veg: new_time})    # adding the vegetable in item's list

    else:  # if he/she want to enter packaged materials
        # setting up for speech recognition
        recogniser = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recogniser.listen(source)
            item = recogniser.recognize_google(audio)
            item = item.lower()
        # telling user what we understood
        print("You entered", item)
        # prompting the user if we understood wrong, starting the whole process again
        Error = input("If we understood wrong, Enter 0, Else enter anything")
        if Error == '0':
            continue
        print("Enter", item, "expiry date's day")          # asking the user to enter the day of the expiry date
        n_day = int(input())
        print("Enter", item, "expiry date's month")        # asking the user to enter the month within the current year
        n_month = int(input())
        new_time = date_ify2(n_day, n_month)               # converting the expiry date into analysable data
        item_list.update({item: new_time})                 # adding the good in item's list

    # iterating over the item_list to find if any item is getting its expiry date near
    for vg in item_list:
        # if expiry date is a day near
        if now_date + 1 == item_list[vg] or now_date == item_list[vg]:
            expiry_list.update({vg: item_list[vg]})
            print(vg, "will get expired within a day or two. Please consume it!")
        # if expiry date has passed
        elif now_date > item_list[vg]:
            expiry_list.update({vg: item_list[vg]})
    # creating a dummy expiry list to prevent runtime errors
    expiry_list2 = {}
    for vg2 in expiry_list:
        expiry_list2.update({vg2: expiry_list[vg2]})
    # iterating over dummy expiry list and deleting everything in item list from expiry list
    # and deleting everything in expiry list that has been expired
    for vg2 in expiry_list2:
        try:
            # delete from expiry list if expiry date has passed
            if now_date > item_list[vg2]:
                del expiry_list[vg2]
                print(vg2, "is not considered to be consumable as it is expired")
            # delete the element from item_list
            del item_list[vg2]
        # if the element is not in item's list, continue
        except KeyError:
            continue
    # showing the user the item list
    print("NEW ITEM LIST :", item_list)
    # showing the user the expiry list
    print("NEW EXPIRY LIST :", expiry_list)
