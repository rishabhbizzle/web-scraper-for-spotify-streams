from turtle import pd
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
from datetime import timedelta

#creating some important variables

num = 0 #--> for some edge case ahead
num2 = 0 #--> for some edge case ahead
today = date.today()
yesterday = today - timedelta(days = 1)
d = yesterday.strftime("%B %d, %Y")

streams = []

streams.append(d)

df = pd.DataFrame(pd.read_csv('str.csv'))


jb = 'https://chartmasters.org/spotify-streaming-numbers-tool/?artist_name=justin+bieber&artist_id=&displayView=Disco'

login_data = {
    'log':'bieberr',
    'pwd':'', # --> password will go here in the string
    'wp-submit':'Log In',
    'testcookie':'1' }

#login using request on chartmasters website

with requests.Session() as s:
    url = "https://chartmasters.org/wp-login.php"
    # r = s.get(url)
    s.post(url, data=login_data)
    r = s.get(jb)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table', class_ = 'resultsTab')

    # from table collecting the streams of all singles & songs
    for row in table.find_all('tr',class_=""):
        data = row.find_all('td',class_="numbers" )
        row_data = [td.text.strip() for td in data]
        # print(row_data)
        streams.append(row_data[0])

    #from table collection the streams of all albums
    for row2 in table.find_all('tr',class_="albumTotals"):
        data2 = row2.find_all('td',class_="numbers" )
        row2_data = [td.text.strip() for td in data2]
        # print(row2_data)
        if num <= 10:
            streams.append(row2_data[0])
            num = num+1

    #from table collection the streams of the artist career total
    for row3 in table.find_all('tr',class_="careerTotals"):
        data3 = row3.find_all('td',class_="numbers" )
        row3_data = [td.text.strip() for td in data3]
        if num2 == 1:
            streams.append(row3_data[0])
        num2 = num2+1
    

    df2 = pd.DataFrame(streams)

    df = df.join(df2) # adding the new streams dataframe to old one

    df.to_csv('str.csv',index = False)

    print("SUCESSFULLY DONE")
        
        
        



    