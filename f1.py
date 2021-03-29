import requests
import json




def raceSchedule(raceNumber):
   
    schedule = requests.get("http://ergast.com/api/f1/2021.json")
    schedulejson = json.loads(schedule.text)["MRData"]["RaceTable"]["Races"][raceNumber]

    raceLocation = json.loads(schedule.text)["MRData"]["RaceTable"]["Races"][raceNumber]["Circuit"]["Location"]

    circuitName = json.loads(schedule.text)["MRData"]["RaceTable"]["Races"][1]["Circuit"]

    return(schedulejson["raceName"], raceLocation["country"], schedulejson["date"], circuitName["circuitName"], raceLocation["locality"])

def constructorStandings(raceYear):
    userYear = requests.get(f"http://ergast.com/api/f1/{raceYear}/constructorStandings.json")
    teamNames1 = json.loads(userYear.text)
    
    addonepostion = 0
    finalpostion = 1

 
    teamNamesList =[]
    
    teamPointsList = []
    for i in range (10):

        teamNames = teamNames1["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"][addonepostion]["Constructor"]["name"]

        teampoints = teamNames1["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"][addonepostion]["points"]
        
        teamNamesList.append(str(finalpostion) + "  " + teamNames)
        
        teamPointsList.append(teampoints)
        
        finalpostion +=1
        addonepostion +=1
        
        
    return(teamNamesList, teamPointsList)




# userYear = requests.get(f"http://ergast.com/api/f1/{1999}/constructorStandings.json")
# teamNames1 = json.loads(userYear.text)
# teamNames = teamNames1["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"][1]["points"]

# print(constructorStandings(1999))








