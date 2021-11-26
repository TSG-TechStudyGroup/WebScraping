from bs4 import BeautifulSoup
from numpy import result_type
from selenium import webdriver
import time
import pandas as pd

# Without selenium
# import requests
# url = "https://www.moneycontrol.com/mutual-funds/tata-large-cap-fund-direct-plan/portfolio-holdings/MTA788"
# headers = ({
#                 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
#                 'Accept-Language': 'en-US,en;q=0.5'
#                 })

# result = requests.get(url=url, headers=headers)

#setup the selenium driver
driver = webdriver.Edge() #"D:\Python\WebScraping\edgedriver_win64\msedgedriver.exe"

#Open the Url
driver.get("https://www.moneycontrol.com/mutual-funds/tata-large-cap-fund-direct-plan/portfolio-holdings/MTA788")
time.sleep(5)

#load the page source to BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'lxml')

#close the browser
driver.quit()

#Extract the data from page
table = soup.find('table', id="equityCompleteHoldingTable")   
tableBody = table.find('tbody') 
rows = tableBody.find_all('tr')

fundName = soup.find('h1', class_="page_heading navdetails_heading").text

#get all the data rows
data_rows = [row for row in rows if (len(row.contents) > 1)]

columns=['Stock Name', 'Category', 'Value(Mn)', '% of holding', '1M Change']
result = pd.DataFrame(columns=columns)

for data_row in data_rows:

    #get the cells
    cells = data_row.find_all('td')

    #data
    stockName = cells[0].find('a').text.strip()
    category = cells[1].text.strip()
    value = cells[2].text.strip()
    percentageOfHolding = cells[3].text.strip()
    oneMonthChange = cells[4].text.strip()

    df = pd.DataFrame([[stockName, category,value,percentageOfHolding,oneMonthChange]],columns=columns)
    result = result.append(df,ignore_index=True)
    
# result.to_excel('MFHolding.xlsx', sheet_name=fundName)
result.to_csv('MFHoldings.csv')
print(result)