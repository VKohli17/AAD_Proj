import json
import os

import matplotlib.pyplot as plt
import operator
import numpy as np
import pandas as pd
from datawrapper import Datawrapper

# dw = Datawrapper(access_token = "token_here")
# dw.account_info()

path_to_jsons = '/home/albus/Downloads/ipl_json'
json_files = [pos_json for pos_json in os.listdir(path_to_jsons) if pos_json.endswith('.json')]
json_files.sort(key=lambda x: int(x.split('.')[0])) # sorting the json files in ascending order of the number in the file name

def all_winners(): # print the winners of all matches

    for num, js in enumerate(json_files):
        with open(os.path.join(path_to_jsons, js)) as json_file:
            data = json.load(json_file)
            if 'winner' in data['info']['outcome']:         # if the match had a straight winner
                print(data['info']['outcome']['winner'])
            elif 'result' in data['info']['outcome']:
                # if the result is "no result" print no result, else print the eliminator
                if data['info']['outcome']['result'] == 'no result':
                    print('no result') 
                else:
                    print(data['info']['outcome']['eliminator'])    # eliminator = winner of super over

def bowler_wickets_year(): # find the total number of wickets taken by A certain bowler in a certain edition of the IPL

    wickets = 0
    # ask user for name of bowler
    bowler_name = input('Enter the name of the bowler: ')
    # ask user for year
    year = input('Enter the year: ')
    for num, js in enumerate(json_files):                                                
        with open(os.path.join(path_to_jsons, js)) as json_file:                        # open the json file
            data = json.load(json_file)                                                 # load the json file
            for i in data['info']['dates']:                                             # iterate through the list "dates" in the dictionary "info"
                if i.startswith(str(year)):                                             # I only want the matches played in that year
                    if bowler_name in data['info']['registry']['people']:               # if the bowler is playing
                        for i in data['innings']:                                       # iterate through the list "innings" in the dictionary "info"
                            for j in i['overs']:                                        # iterate through the list "overs" in the dictionary in the list "innings"
                                for k in j['deliveries']:                               
                                    if 'wickets' in k and k['bowler'] == bowler_name:
                                        for l in k['wickets']:
                                            if l['kind'] != 'run out':
                                                wickets += 1

    print(bowler_name + " took " + str(wickets) + " wickets in " + str(year) + ".")

def top_wicket_takers_year(): # find the top 10 wicket takers in a certain year and plot a bar graph showing their wickets

    # create a dictionary with name of bowler as key and number of wickets taken as value
    wickets_dict = {}
    # ask user for the year
    year = input('Enter the year: ')
    for num, js in enumerate(json_files):
        with open(os.path.join(path_to_jsons, js)) as json_file:
            data = json.load(json_file)
            for i in data['info']['dates']:
                if i.startswith(str(year)):
                    for i in data['innings']:
                        for j in i['overs']:
                            for k in j['deliveries']:
                                if 'wickets' in k:
                                    for l in k['wickets']:
                                        if l['kind'] != 'run out':
                                            # add the name of the bowler to the dictionary. If not there, initialise with 0 else add 1 to wickets taken
                                            if k['bowler'] in wickets_dict:
                                                wickets_dict[k['bowler']] += 1
                                            else:
                                                wickets_dict[k['bowler']] = 1

    # sort the dictionary in descending order of wickets taken
    wickets_dict = {k: v for k, v in sorted(wickets_dict.items(), key=lambda item: item[1], reverse=True)}
    # print the wickets dictionary sorted in descending order of number of wickets taken
    # print(sorted(wickets_dict.items(), key=lambda x: x[1], reverse=True))

    # use numpy to display a graph of the 10 bowlers with the highest wickets

    bowlers = list(wickets_dict.keys())
    wickets = list(wickets_dict.values())
    top_wicket_takers = plt.figure(figsize=(10,10))
    # show a graph with the top 10 bowlers
    plt.bar(bowlers[:10], wickets[:10], color='black')
    plt.xlabel('Bowlers')
    # plt.xticks(rotation=90)
    # if names overflow, display them in 2 lines
    plt.xticks(rotation=90, ha='right')
    plt.ylabel('Wickets Taken')
    plt.title('Top 10 Wicket Takers in IPL ' + str(year))
    plt.show()

def worms_2021(): # Making worm plots for all the matches from 2021

    allworms = {}
    for num, js in enumerate(json_files):
        with open(os.path.join(path_to_jsons, js)) as json_file:
            data = json.load(json_file)
            match = {}
            for x in data['info']['dates']:
                if x.startswith('2021'):
                    # if the field stage exists in "event"
                    if 'stage' in data['info']['event']:
                        matchID = data['info']['event']['stage']
                    elif 'match_number' in data['info']['event']:
                        matchID = str(data['info']['event']['match_number'])
                    filename = 'worms/' + matchID + '.png'
                    team1worm = {}
                    team2worm = {}
                    total_runs = 0
                    for j in data['innings'][0]['overs']:
                        for k in j['deliveries']:
                            total_runs += k['runs']['total']
                        team1worm[j['over']+1] = total_runs
                        # # increment all the values in the keys of dictionary by 1 to make it start from 1 instead of 0
                        # for i in range(len(list(team1worm.keys()))):
                        #     list(team1worm.keys())[i] += 1
                    first_total = total_runs
                    total_runs = 0
                    for j in data['innings'][1]['overs']:
                        for k in j['deliveries']:
                            total_runs += k['runs']['total']
                        team2worm[j['over']+1] = total_runs
                        # for i in range(len(list(team2worm.keys()))):
                        #     list(team2worm.keys())[i] += 1
                    # add team1worm and team2worm to the match dictionary as attributes, use info > teams > 0 and teams > 1 as keys
                    match[data['info']['teams'][0]] = team1worm
                    match[data['info']['teams'][1]] = team2worm
                    # add match to the allworms dictionary as attribute, use matchID as key
                    allworms[matchID] = match

                    # Code to plot the worms

                    overs_team1 = list(team1worm.keys())
                    runs_team1 = list(team1worm.values())
                    overs_team2 = list(team2worm.keys())
                    runs_team2 = list(team2worm.values())
                    # did these above:
                    # for i in range(len(overs_team1)):
                    #     overs_team1[i] += 1
                    # for i in range(len(overs_team2)):
                    #     overs_team2[i] += 1
                    plt.figure(figsize=(20,20))
                    if data['info']['teams'][0] == 'Chennai Super Kings':
                        plt.plot(overs_team1, runs_team1, ':', color='goldenrod')
                    elif data['info']['teams'][0] == 'Kolkata Knight Riders':
                        plt.plot(overs_team1, runs_team1, ':', color='indigo')
                    elif data['info']['teams'][0] == 'Mumbai Indians':
                        plt.plot(overs_team1, runs_team1, ':', color='blue')
                    elif data['info']['teams'][0] == 'Rajasthan Royals':
                        plt.plot(overs_team1, runs_team1, ':', color='magenta')
                    elif data['info']['teams'][0] == 'Royal Challengers Bangalore':
                        plt.plot(overs_team1, runs_team1, ':', color='black')
                    elif data['info']['teams'][0] == 'Sunrisers Hyderabad':
                        plt.plot(overs_team1, runs_team1, ':', color='xkcd:orange')
                    elif data['info']['teams'][0] == 'Delhi Capitals':
                        plt.plot(overs_team1, runs_team1, ':', color='darkblue')
                    elif data['info']['teams'][0] == 'Punjab Kings':
                        plt.plot(overs_team1, runs_team1, ':', color='red')
                    if data['info']['teams'][1] == 'Chennai Super Kings':
                        plt.plot(overs_team2, runs_team2, color='goldenrod')
                    elif data['info']['teams'][1] == 'Kolkata Knight Riders':
                        plt.plot(overs_team2, runs_team2, color='indigo')
                    elif data['info']['teams'][1] == 'Mumbai Indians':
                        plt.plot(overs_team2, runs_team2, color='blue')
                    elif data['info']['teams'][1] == 'Rajasthan Royals':
                        plt.plot(overs_team2, runs_team2, color='magenta')
                    elif data['info']['teams'][1] == 'Royal Challengers Bangalore':
                        plt.plot(overs_team2, runs_team2, color='black')
                    elif data['info']['teams'][1] == 'Sunrisers Hyderabad':
                        plt.plot(overs_team2, runs_team2, color='xkcd:orange')
                    elif data['info']['teams'][1] == 'Delhi Capitals':
                        plt.plot(overs_team2, runs_team2, color='darkblue')
                    elif data['info']['teams'][1] == 'Punjab Kings':
                        plt.plot(overs_team2, runs_team2, color='red')
                    plt.xlabel('Overs')
                    plt.ylabel('Runs')
                    plt.title(data['info']['teams'][0] + ' vs ' + data['info']['teams'][1])
                    plt.xticks(np.arange(1, 21, 1), ha='right')
                    plt.yticks(np.arange(0, first_total + 20, 10))
                    plt.savefig(filename)
                    plt.clf()
                    plt.close()

    # Save the allworms dictionary to a json file
    with open('allworms.json', 'w') as f:
        json.dump(allworms, f, indent=4)

def rpos_2021(): # Finding runs made per over for all matches from 2021
    
    all_rpos = {}
    for num, js in enumerate(json_files):
        with open(os.path.join(path_to_jsons, js)) as json_file:
            data = json.load(json_file)
            match = {}
            for x in data['info']['dates']:
                if x.startswith('2021'):
                    # if the field stage exists in "event"
                    if 'stage' in data['info']['event']:
                        matchID = data['info']['event']['stage']
                    elif 'match_number' in data['info']['event']:
                        matchID = str(data['info']['event']['match_number'])
                    filename = 'runs_per_over/' + matchID + '.png'
                    team1rpos = {}
                    team2rpos = {}
                    total_runs = 0
                    for j in data['innings'][0]['overs']:
                        runs_in_over = 0
                        for k in j['deliveries']:
                            runs_in_over += k['runs']['total']
                        team1rpos[j['over']+1] = runs_in_over
                    for j in data['innings'][1]['overs']:
                        runs_in_over = 0
                        for k in j['deliveries']:
                            runs_in_over += k['runs']['total']
                        team2rpos[j['over']+1] = runs_in_over
                    # add team1rpos and team2rpos to the match dictionary as attributes, use info > teams > 0 and teams > 1 as keys
                    match[data['info']['teams'][0]] = team1rpos
                    match[data['info']['teams'][1]] = team2rpos
                    # add match to the all_rpos dictionary as attribute, use matchID as key
                    all_rpos[matchID] = match

                    # code to plot the rpos

                    overs_team1 = list(team1rpos.keys())
                    runs_team1 = list(team1rpos.values())
                    overs_team2 = list(team2rpos.keys())
                    runs_team2 = list(team2rpos.values())
                    plt.figure(figsize=(20,20))
                    if data['info']['teams'][0] == 'Chennai Super Kings':
                        plt.plot(overs_team1, runs_team1, ':', color='goldenrod')
                    elif data['info']['teams'][0] == 'Kolkata Knight Riders':
                        plt.plot(overs_team1, runs_team1, ':', color='indigo')
                    elif data['info']['teams'][0] == 'Mumbai Indians':
                        plt.plot(overs_team1, runs_team1, ':', color='blue')
                    elif data['info']['teams'][0] == 'Rajasthan Royals':
                        plt.plot(overs_team1, runs_team1, ':', color='magenta')
                    elif data['info']['teams'][0] == 'Royal Challengers Bangalore':
                        plt.plot(overs_team1, runs_team1, ':', color='black')
                    elif data['info']['teams'][0] == 'Sunrisers Hyderabad':
                        plt.plot(overs_team1, runs_team1, ':', color='xkcd:orange')
                    elif data['info']['teams'][0] == 'Delhi Capitals':
                        plt.plot(overs_team1, runs_team1, ':', color='darkblue')
                    elif data['info']['teams'][0] == 'Punjab Kings':
                        plt.plot(overs_team1, runs_team1, ':', color='red')
                    if data['info']['teams'][1] == 'Chennai Super Kings':
                        plt.plot(overs_team2, runs_team2, color='goldenrod')
                    if data['info']['teams'][1] == 'Kolkata Knight Riders':
                        plt.plot(overs_team2, runs_team2, color='indigo')
                    if data['info']['teams'][1] == 'Mumbai Indians':
                        plt.plot(overs_team2, runs_team2, color='blue')
                    if data['info']['teams'][1] == 'Rajasthan Royals':
                        plt.plot(overs_team2, runs_team2, color='magenta')
                    if data['info']['teams'][1] == 'Royal Challengers Bangalore':
                        plt.plot(overs_team2, runs_team2, color='black')
                    if data['info']['teams'][1] == 'Sunrisers Hyderabad':
                        plt.plot(overs_team2, runs_team2, color='xkcd:orange')
                    if data['info']['teams'][1] == 'Delhi Capitals':
                        plt.plot(overs_team2, runs_team2, color='darkblue')
                    if data['info']['teams'][1] == 'Punjab Kings':
                        plt.plot(overs_team2, runs_team2, color='red')
                    plt.xlabel('Overs')
                    plt.ylabel('Runs')
                    plt.title(data['info']['teams'][0] + ' vs ' + data['info']['teams'][1])
                    plt.xticks(np.arange(1, 21, 1), ha='right')
                    plt.yticks(np.arange(0, 40, 10))
                    plt.savefig(filename)
                    plt.clf()
                    plt.close()

    # save the all_rpos dictionary to a json file
    with open('all_rpos.json', 'w') as f:
        json.dump(all_rpos, f, indent=4)

def diff_in_worms(): # use greedy approach to sort the matches by degree of similarity of first worm and second worm

    alldiffs = {}
    totaldiffs = {}
    totalabsdiffs = {}
    weighted_diffs = {}
    weighted_diffs_2 = {}
    weighted_diffs_3 = {}
    for num, js in enumerate(json_files):
        with open(os.path.join(path_to_jsons, js)) as json_file:
            data = json.load(json_file)
            match = {}
            for x in data['info']['dates']:
                if x.startswith('2021'):
                    # if the field stage exists in "event"
                    if 'stage' in data['info']['event']:
                        matchID = data['info']['event']['stage']
                    elif 'match_number' in data['info']['event']:
                        matchID = str(data['info']['event']['match_number'])
                    team1worm = {}
                    team2worm = {}
                    diff = {}
                    total_runs = 0
                    for j in data['innings'][0]['overs']:
                        for k in j['deliveries']:
                            total_runs += k['runs']['total']
                        team1worm[j['over']+1] = total_runs
                    total_runs = 0
                    for j in data['innings'][1]['overs']:
                        for k in j['deliveries']:
                            total_runs += k['runs']['total']
                        team2worm[j['over']+1] = total_runs
                    # each entry in diff is the difference of entries of team1worm and team2worm
                    totaldiff = 0
                    totalabsdiff = 0
                    weighted_diff = 0
                    weighted_diff_3 = 0
                    for key in team2worm:
                        diff[key] = team2worm[key] - team1worm[key]
                        totaldiff += diff[key]
                        totalabsdiff += abs(diff[key])
                        weighted_diff += abs(diff[key]*(key))
                        weighted_diff_3 += abs(diff[key]*(key**2))

                    # trying to normalize 
                    weighted_diff_2 = weighted_diff*20/len(team2worm)
                    weighted_diff_3 = weighted_diff_3*((20/len(team2worm))**2)

                    # add match to the alldiffs dictionary as attribute, use matchID as key
                    alldiffs[matchID] = diff
                    totaldiffs[matchID] = totaldiff
                    totalabsdiffs[matchID] = totalabsdiff
                    weighted_diffs[matchID] = weighted_diff
                    weighted_diffs_2[matchID] = weighted_diff_2
                    weighted_diffs_3[matchID] = weighted_diff_3

    # sort the totalabsdiffs dictionary
    sorted_totalabsdiffs = sorted(totalabsdiffs.items(), key=operator.itemgetter(1))

    # sort the weighted_diffs dictionary
    sorted_weighted_diffs = sorted(weighted_diffs.items(), key=operator.itemgetter(1))

    # sort the weighted_diffs_2 dictionary
    sorted_weighted_diffs_2 = sorted(weighted_diffs_2.items(), key=operator.itemgetter(1))

    # sort the weighted_diffs_3 dictionary
    sorted_weighted_diffs_3 = sorted(weighted_diffs_3.items(), key=operator.itemgetter(1))

    # save the alldiffs dictionary to a json file
    with open('alldiffs.json', 'w') as f:
        json.dump(alldiffs, f, indent=4)

    # save the totaldiffs dictionary to a json file
    with open('totaldiffs.json', 'w') as f:
        json.dump(totaldiffs, f, indent=4)

    # save the totalabsdiffs dictionary to a json file
    with open('totalabsdiffs.json', 'w') as f:
        json.dump(totalabsdiffs, f, indent=4)

    # save the sorted totalabsdiffs dictionary to a json file
    with open('sorted_totalabsdiffs.json', 'w') as f:
        json.dump(sorted_totalabsdiffs, f, indent=4)

    # save the sorted weighted_diffs dictionary to a json file
    with open('sorted_weighted_diffs.json', 'w') as f:
        json.dump(sorted_weighted_diffs, f, indent=4)

    # save the sorted weighted_diffs_2 dictionary to a json file
    with open('sorted_weighted_diffs_2.json', 'w') as f:
        json.dump(sorted_weighted_diffs_2, f, indent=4)

    # save the sorted weighted_diffs_3 dictionary to a json file
    with open('sorted_weighted_diffs_3.json', 'w') as f:
        json.dump(sorted_weighted_diffs_3, f, indent=4)

def worms_allyears():

    for num, js in enumerate(json_files):
        with open(os.path.join(path_to_jsons, js)) as json_file:
            data = json.load(json_file)
            innings = {}
            for x in data['info']['dates']:
                # if x doesn't start with 2008 or 2009 or 2010 or 2011
                if not x.startswith('2008') and not x.startswith('2009') and not x.startswith('2010') and not x.startswith('2011'):
                # if x.startswith('2011'):
                    # check the first 4 characters of the date and copy them into a string named year
                    year = x[:4]
                    if 'stage' in data['info']['event']:
                        matchID = year + '_' + data['info']['event']['stage']
                    elif 'match_number' in data['info']['event']:
                        matchID = year + '_' + str(data['info']['event']['match_number'])
                    team1worm = {}
                    team2worm = {}
                    total_runs = 0
                    for j in data['innings'][0]['overs']:
                        for k in j['deliveries']:
                            total_runs += k['runs']['total']
                        team1worm[j['over']+1] = total_runs
                    first_total = total_runs
                    total_runs = 0
                    overs_team1 = list(team1worm.keys())
                    runs_team1 = list(team1worm.values())
                    plt.figure(figsize=(20,20))
                    plt.plot(overs_team1, runs_team1, color = 'black')
                    plt.xlabel('Overs')
                    plt.ylabel('Runs')
                    plt.title(matchID + '_1' + '_' + data['info']['teams'][0])
                    plt.xticks(np.arange(1, 21, 1), ha='right')
                    plt.yticks(np.arange(0, first_total + 20, 10))
                    plt.savefig('allworms/' + matchID + '_1.png')
                    plt.clf()
                    plt.close()
                    if len(data['innings']) > 1:
                        for j in data['innings'][1]['overs']:
                            for k in j['deliveries']:
                                total_runs += k['runs']['total']
                            team2worm[j['over']+1] = total_runs
                        second_total = total_runs
                        innings[year + '_' + matchID + '_1'] = team1worm
                        innings[year + '_' + matchID + '_2'] = team2worm
                        overs_team2 = list(team2worm.keys())
                        runs_team2 = list(team2worm.values())                
                        plt.figure(figsize=(20,20))
                        plt.plot(overs_team2, runs_team2, color = 'black')
                        plt.xlabel('Overs')
                        plt.ylabel('Runs')
                        plt.title(matchID + '_2' + '_' + data['info']['teams'][1])
                        plt.xticks(np.arange(1, 21, 1), ha='right')
                        plt.yticks(np.arange(0, second_total + 20, 10))
                        plt.savefig('allworms/' + matchID + '_2.png')
                        plt.clf()
                        plt.close()

    # save the innings dictionary to a json file
    with open('innings.json', 'w') as f:
        json.dump(innings, f, indent=4)

def debugginglmao():
    for num, js in enumerate(json_files):
        with open(os.path.join(path_to_jsons, js)) as json_file:
            data = json.load(json_file)
            match = {}
            for x in data['info']['dates']:
                if x.startswith('2011-05-21'):
                    print(len(data['innings']))

# whichever function you wanna use, substitute the name of the function here:
worms_allyears()