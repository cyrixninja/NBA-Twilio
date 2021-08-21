from datetime import time
import re
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.static import teams
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import os


app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'playerinfo' in incoming_msg:
        player1= incoming_msg.split()
        player2= (player1[1])
        player = players.find_players_by_full_name(player2)
        player_id = (player[0]['id'])
        player_info = commonplayerinfo.CommonPlayerInfo(player_id)
        stats_data=player_info.get_normalized_dict()

        #Common Info
        fullname=stats_data['CommonPlayerInfo'][0]['DISPLAY_FIRST_LAST']
        birthday=stats_data['CommonPlayerInfo'][0]['BIRTHDATE']
        school=stats_data['CommonPlayerInfo'][0]['SCHOOL']
        country=stats_data['CommonPlayerInfo'][0]['COUNTRY']
        lastaffiliation=str(stats_data['CommonPlayerInfo'][0]['LAST_AFFILIATION'])
        height=stats_data['CommonPlayerInfo'][0]['HEIGHT']
        weight=stats_data['CommonPlayerInfo'][0]['WEIGHT']
        seasonexp=str(stats_data['CommonPlayerInfo'][0]['SEASON_EXP'])
        jersey=stats_data['CommonPlayerInfo'][0]['JERSEY']
        positon=stats_data['CommonPlayerInfo'][0]['POSITION']
        teamcity=stats_data['CommonPlayerInfo'][0]['TEAM_CITY']
        fromyear=str(stats_data['CommonPlayerInfo'][0]['FROM_YEAR'])
        toyear=str(stats_data['CommonPlayerInfo'][0]['TO_YEAR'])
        draftyear=str(stats_data['CommonPlayerInfo'][0]['DRAFT_YEAR'])
        #Headline Stats
        timeframe=str(stats_data['PlayerHeadlineStats'][0]['TimeFrame'])
        playername=stats_data['PlayerHeadlineStats'][0]['PLAYER_NAME']
        pts=str(stats_data['PlayerHeadlineStats'][0]['PTS'])
        ast=str(stats_data['PlayerHeadlineStats'][0]['AST'])
        reb=str(stats_data['PlayerHeadlineStats'][0]['REB'])
        pie=str(stats_data['PlayerHeadlineStats'][0]['REB'])
        #Player Info
        playerinfo=("Player Name"+":"+" "+fullname+ "\n"
        "Birthday"+":"+" "+birthday+ "\n"
        "School"+":"+" "+school+ "\n"
        "Country"+":"+" "+country+ "\n"
        "Last Affiliation"+":"+" "+lastaffiliation+ "\n"
        "Height"+":"+" "+height+ "\n"
        "Weight"+":"+" "+weight+ "\n"
        "Season EXP"+":"+" "+seasonexp+ "\n"
        "Jersey"+":"+" "+jersey+ "\n"
        "Position"+":"+" "+positon+ "\n"
        "Team City"+":"+" "+teamcity+ "\n"
        "From Year"+":"+" "+fromyear+ "\n"
        "To Year"+":"+" "+toyear+ "\n"
        "Draft Year"+":"+" "+draftyear+ "\n"
        "Timeframe"+":"+" "+timeframe+ "\n"
        "PTS"+":"+" "+pts+ "\n"
        "AST"+":"+" "+ast+ "\n"
        "REB"+":"+" "+reb+ "\n"
        "PIE"+":"+" "+pie+ "\n"
        )
        msg.body(playerinfo)
        return str(resp)
    if 'team by year' in incoming_msg:
        #teams by year
        teambyyear1=incoming_msg.split()
        teambyyear2=int(teambyyear1[3])
        teamsbyyear=teams.find_teams_by_year_founded(teambyyear2)
        teams_name=[d['full_name'] for d in teamsbyyear]
        teamsbyyear_name=" ".join(str(x) for x in teams_name)
        TotalTeamsbyyear=str(len(teamsbyyear))
        teamsbyyear_data=("Teams are :"+" "+teamsbyyear_name+ "\n"
        "Total Teams :"+" "+TotalTeamsbyyear+ "\n"
        )
        msg.body(teamsbyyear_data)
        return str(resp)
    if 'allteams' in incoming_msg:
        #all teams
        allteams=teams.get_teams()
        allteams_name=[d['full_name'] for d in allteams]
        allteamsname=" ".join(str(x) for x in allteams_name)
        TotalTeamsNumber=str(len(allteams))
        TotalTeamsData=("Teams are :"+" "+allteamsname+ "\n"
        "Total Teams :"+" "+TotalTeamsNumber+ "\n"
        )
        msg.body(TotalTeamsData)
        return str(resp)
    if 'team by name' in incoming_msg:
        #teams by name
        teambyname1=incoming_msg.split()
        teambyname2=(teambyname1[3])
        # Find teams by full name
        teamsbyname=teams.find_teams_by_full_name(teambyname2)
        teamsbyname_fullname=(teamsbyname[0]['full_name'])
        teamsbyname_city=(teamsbyname[0]['city'])
        teamsbyname_state=(teamsbyname[0]['state'])
        teamsbyname_yearfounded=str(teamsbyname[0]['year_founded'])
        teamsbynameinfo=(
        "Team Name"+":"+" "+teamsbyname_fullname+ "\n"
        "City"+":"+" "+teamsbyname_city+ "\n"
        "State"+":"+" "+teamsbyname_state+ "\n"
        "Year Founded"+":"+" "+teamsbyname_yearfounded+ "\n" 
        )
        msg.body(teamsbynameinfo)
        return str(resp)

    if 'team by state' in incoming_msg:
        #teams by state
        teambystate1=incoming_msg.split()
        teambystate2=(teambystate1[3])
        # Find teams by state.
        teamsbystate=teams.find_teams_by_state(teambystate2)
        teamsbystate_fullname=(teamsbystate[0]['full_name'])
        teamsbystate_city=(teamsbystate[0]['city'])
        teamsbystate_state=(teamsbystate[0]['state'])
        teamsbystate_yearfounded=str(teamsbystate[0]['year_founded'])
        teamsbystateinfo=(
        "Team Name"+":"+" "+teamsbystate_fullname+ "\n"
        "City"+":"+" "+teamsbystate_city+ "\n"
        "State"+":"+" "+teamsbystate_state+ "\n"
        "Year Founded"+":"+" "+teamsbystate_yearfounded+ "\n"
        )
        msg.body(teamsbystateinfo)
        return str(resp)

    if 'team by city' in incoming_msg:
        #teams by city
        teambycity1=incoming_msg.split()
        teambycity2=(teambycity1[3])
        # Find teams by city.
        teamsbycity=teams.find_teams_by_city(teambycity2)
        teamsbycity_fullname=(teamsbycity[0]['full_name'])
        teamsbycity_city=(teamsbycity[0]['city'])
        teamsbycity_state=(teamsbycity[0]['state'])
        teamsbycity_yearfounded=str(teamsbycity[0]['year_founded'])
        teamsbycityinfo=(
        "Team Name"+":"+" "+teamsbycity_fullname+ "\n"
        "City"+":"+" "+teamsbycity_city+ "\n"
        "State"+":"+" "+teamsbycity_state+ "\n"
        "Year Founded"+":"+" "+teamsbycity_yearfounded+ "\n"
        )
        msg.body(teamsbycityinfo)
        return str(resp)

if __name__ == '__main__':
    app.run()