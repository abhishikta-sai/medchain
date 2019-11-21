import pandas as pd
from random import randrange
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random


file = open("drugs.txt", 'r')
drugs = file.readlines()
drugs = [i.replace("\n","") for i in drugs]

manufacturers = ["Pro-Medical Solutions", "Med-Awesome Solutions", "Save-a-life Solutions"]


def random_state(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


d1 = datetime.strptime('1/1/2018 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('1/1/2020 1:30 PM', '%m/%d/%Y %I:%M %p')
rows = []


for i in range(100):
    manufacturing_date = random_state(d1, d2)
    expiry_date = manufacturing_date + relativedelta(years=4)
    drug = random.choice(drugs)
    manufacturer = random.choice(manufacturers)
    quantity = random.choice(range(100))
    rows.append([drug, quantity, manufacturer, manufacturing_date.date(), expiry_date.date()])

df = pd.DataFrame(rows)
df.columns = ["Name", "Quantity", "Manufacturer", "Manufacturing Date", "Expiry Date"]
df.to_csv("data.csv", index=False)
