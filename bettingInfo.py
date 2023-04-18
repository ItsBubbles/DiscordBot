from selenium import webdriver
from selenium.webdriver.common.by import By

def bettingOdds():
    url = "https://sports.yahoo.com/nhl/odds/"
    driver = webdriver.Chrome()
    driver.get(url)

    # tableData = driver.find_elements(By.XPATH, "//*[@id=Col1-1-LeagueOdds-Proxy]/div/div[5]/div[1]/div")
    tableData = driver.find_elements(By.CLASS_NAME, "PREGAME")
    teamList = []
    for game in tableData:
        text = game.text.splitlines()
        text.pop(7)
        text.pop(8)
        text.pop(11)
        text.pop(12)
        teamList.append(text)
    teamList.pop(-1)
    return teamList