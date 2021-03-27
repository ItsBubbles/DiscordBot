import requests
import json




def raceSchedule(raceNumber):
   
    schedule = requests.get("http://ergast.com/api/f1/2021.json")
    schedulejson = json.loads(schedule.text)["MRData"]["RaceTable"]["Races"][raceNumber]

    raceLocation = json.loads(schedule.text)["MRData"]["RaceTable"]["Races"][raceNumber]["Circuit"]["Location"]

    circuitName = json.loads(schedule.text)["MRData"]["RaceTable"]["Races"][1]["Circuit"]

    return(schedulejson["raceName"], raceLocation["country"], schedulejson["date"], circuitName["circuitName"], raceLocation["locality"])

print(raceSchedule(0))

schedule = requests.get("http://ergast.com/api/f1/2021.json")
schedulejson = json.loads(schedule.text)["MRData"]["RaceTable"]["Races"][1]["Circuit"]
print(schedulejson)








