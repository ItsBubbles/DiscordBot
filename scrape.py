import requests
import urllib.request
from bs4 import BeautifulSoup
import random
from random import randint


def discordjoke():   
    file1 = open("Jokes.txt", "w+")
    brokenbot = "Broken Bot Try again 5 seconds"
    try:
        url = 'https://old.reddit.com/r/dadjokes/new/'                       
        request = urllib.request.Request(url, headers={'User-Agent': 'Chrome/76.0.3809.132'})
        html = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(html,'html.parser')

        main_table = soup.find("div",attrs={'id':'siteTable'})
        links = main_table.find_all("a",class_="title")

        extracted_records = []
        for link in links: 
            new_url = link['href']
            new_url = "https://reddit.com"+new_url 
            extracted_records.append(new_url)
            file1.write("\n")
            file1.write(new_url)
            
            

        pageurl =(random.choice(extracted_records))
        request2 = urllib.request.Request(pageurl)
        html2 = urllib.request.urlopen(request2).read()
        soup2 = BeautifulSoup(html2, 'html.parser')

        post = soup2.find_all("h1", class_="_eYtD2XCVieq6emjKBH3m")[0].text.strip()
        response = soup2.find_all('p', class_="_1qeIAgB0cPwnLhDF9XSiJM")[0].text.strip()
        final= post + " ------------------------ " + response
        file1.close()
        return final
    except:
        file2 = open("Jokes.txt", "r")

        randomLine = file2.readlines(randint(2, 26))
        
        
        request3 = urllib.request.Request(randomLine)
        html3 = urllib.request.urlopen(request3).read()
        soup3 = BeautifulSoup(html3, 'html.parser')
        post2 = soup2.find_all("h1", class_="_eYtD2XCVieq6emjKBH3m")[0].text.strip()
        response2 = soup2.find_all('p', class_="_1qeIAgB0cPwnLhDF9XSiJM")[0].text.strip()
        final2 = post + " ------------------------ " + response2
        file2.close()
        return final2
    






    




















