import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datawrapper import Datawrapper

# dw = Datawrapper(access_token = "token_here")

# dw.account_info()

path_to_jsons = '/home/albus/Downloads/ipl_json'
json_files = [pos_json for pos_json in os.listdir(path_to_jsons) if pos_json.endswith('.json')]
json_files.sort(key=lambda x: int(x.split('.')[0])) # sorting the json files in ascending order of the number in the file name

# print the winners of all matches

# for num, js in enumerate(json_files):
#     with open(os.path.join(path_to_jsons, js)) as json_file:
#         data = json.load(json_file)
#         if 'winner' in data['info']['outcome']:         # if the match had a straight winner
#             print(data['info']['outcome']['winner'])
#         elif 'result' in data['info']['outcome']:
#             # if the result is "no result" print no result, else print the eliminator
#             if data['info']['outcome']['result'] == 'no result':
#                 print('no result') 
#             else:
#                 print(data['info']['outcome']['eliminator'])    # eliminator = winner of super over

# find the total number of wickets taken by Harshal Patel in IPL 2021

# harshal_wickets = 0
# for num, js in enumerate(json_files):                                                
#     with open(os.path.join(path_to_jsons, js)) as json_file:                        # open the json file
#         data = json.load(json_file)                                                 # load the json file
#         for i in data['info']['dates']:                                             # iterate through the list "dates" in the dictionary "info"
#             if i.startswith('2021'):                                                # I only want the matches played in 2021
#                 if 'HV Patel' in data['info']['registry']['people']:                # if Harshal Patel is playing
#                     for i in data['innings']:                                       # iterate through the list "innings" in the dictionary "info"
#                         for j in i['overs']:                                        # iterate through the list "overs" in the dictionary in the list "innings"
#                             for k in j['deliveries']:                               
#                                 if 'wickets' in k and k['bowler'] == 'HV Patel':
#                                     for l in k['wickets']:
#                                         if l['kind'] != 'run out':
#                                             harshal_wickets += 1

# print("Harshal Patel took " + str(harshal_wickets) + " wickets in 2021.")

# find the total number of wickets taken by B Kumar in IPL 2017

# b_kumar_wickets = 0
# for num, js in enumerate(json_files):
#     with open(os.path.join(path_to_jsons, js)) as json_file:
#         data = json.load(json_file)
#         for i in data['info']['dates']:
#             if i.startswith('2017'):
#                 if 'B Kumar' in data['info']['registry']['people']:
#                     for i in data['innings']:
#                         for j in i['overs']:
#                             for k in j['deliveries']:
#                                 if 'wickets' in k and k['bowler'] == 'B Kumar':
#                                     for l in k['wickets']:
#                                         if l['kind'] != 'run out':
#                                             b_kumar_wickets += 1

# print("B Kumar took " + str(b_kumar_wickets) + " wickets in 2017.")

# find the top 10 wicket takers in IPL 2021 and plot a bar graph showing their wickets

# # create a dictionary with name of bowler as key and number of wickets taken as value
# wickets_dict = {}
# for num, js in enumerate(json_files):
#     with open(os.path.join(path_to_jsons, js)) as json_file:
#         data = json.load(json_file)
#         for i in data['info']['dates']:
#             if i.startswith('2021'):
#                 for i in data['innings']:
#                     for j in i['overs']:
#                         for k in j['deliveries']:
#                             if 'wickets' in k:
#                                 for l in k['wickets']:
#                                     if l['kind'] != 'run out':
#                                         # add the name of the bowler to the dictionary. If not there, initialise with 0 else add 1 to wickets taken
#                                         if k['bowler'] in wickets_dict:
#                                             wickets_dict[k['bowler']] += 1
#                                         else:
#                                             wickets_dict[k['bowler']] = 1

# # sort the dictionary in descending order of wickets taken
# wickets_dict = {k: v for k, v in sorted(wickets_dict.items(), key=lambda item: item[1], reverse=True)}
# # print the wickets dictionary sorted in descending order of number of wickets taken
# # print(sorted(wickets_dict.items(), key=lambda x: x[1], reverse=True))

# # use numpy to display a graph of the 10 bowlers with the highest wickets

# bowlers = list(wickets_dict.keys())
# wickets = list(wickets_dict.values())
# top_wicket_takers = plt.figure(figsize=(10,10))
# # show a graph with the top 10 bowlers
# plt.bar(bowlers[:10], wickets[:10], color='black')
# plt.xlabel('Bowlers')
# # plt.xticks(rotation=90)
# # if names overflow, display them in 2 lines
# plt.xticks(rotation=90, ha='right')
# plt.ylabel('Wickets Taken')
# plt.title('Top 10 Wicket Takers in IPL 2021')
# plt.show()

# create a dictionary with the number of overs as key and number of runs as value
# runs_graph = {}
# for num, js in enumerate(json_files):
#     with open(os.path.join(path_to_jsons, js)) as json_file:
#         data = json.load(json_file)
#         for i in data['info']['dates']:
#             if i.startswith('2021-10-15'):
#                 for i in data['innings']:
#                     if i['team'] == "Chennai Super Kings":
#                         for j in i['overs']:
#                             # # enter the over number as key and the runs scored in that over as value
#                             # runs_graph[j['over']] = j['runs']['total']
#                             runs_in_over = 0
#                             for k in j['deliveries']:
#                                 runs_in_over += k['runs']['total'] # adding runs from the delivery to the total runs in the over
#                             runs_graph[j['over']] = runs_in_over

# CSKWorm = {}
# for num, js in enumerate(json_files):
#     with open(os.path.join(path_to_jsons, js)) as json_file:
#         data = json.load(json_file)
#         for i in data['info']['dates']:
#             if i.startswith('2021-10-15'):
#                 for i in data['innings']:
#                     if i['team'] == "Chennai Super Kings":
#                         total_runs = 0
#                         for j in i['overs']:
#                             for k in j['deliveries']:
#                                 total_runs += k['runs']['total'] # adding runs from the delivery to the total runs in the over
#                             CSKWorm[j['over']] = total_runs

# first_total = total_runs

# KKRWorm = {}
# for num, js in enumerate(json_files):
#     with open(os.path.join(path_to_jsons, js)) as json_file:
#         data = json.load(json_file)
#         for i in data['info']['dates']:
#             if i.startswith('2021-10-15'):
#                 for i in data['innings']:
#                     if i['team'] == "Kolkata Knight Riders":
#                         total_runs = 0
#                         for j in i['overs']:
#                             for k in j['deliveries']:
#                                 total_runs += k['runs']['total'] # adding runs from the delivery to the total runs in the over
#                             KKRWorm[j['over']] = total_runs

# # use matplotlib to display a graph of the runs scored in each over

# overs_csk = list(CSKWorm.keys())
# runs_csk = list(CSKWorm.values())
# overs_kkr = list(KKRWorm.keys())
# runs_kkr = list(KKRWorm.values())
# # increment all the numbers in overs by 1 to make it start from 1 instead of 0
# for i in range(len(overs_csk)):
#     overs_csk[i] += 1
# for i in range(len(overs_kkr)):
#     overs_kkr[i] += 1
# runs_per_over = plt.figure(figsize=(20,20))
# plt.plot(overs_csk, runs_csk, ':', color='gold')
# plt.plot(overs_kkr, runs_kkr, color='indigo')
# # make the plot bolder 
# plt.xlabel('Overs')
# plt.ylabel('Runs')
# plt.title('Runs scored in each over in IPL 2021 final')
# # use scale of 1 to 20 for the x labels
# plt.xticks(np.arange(1, 21, 1), ha='right')
# # use increments of 10 for the y axis labels
# plt.yticks(np.arange(0, first_total + 20, 10))
# # plt.show()
# name = 'runs_per_over.png'
# plt.savefig(name)

# Making worm plots for all the matches from 2021
for num, js in enumerate(json_files):
    with open(os.path.join(path_to_jsons, js)) as json_file:
        data = json.load(json_file)
        for x in data['info']['dates']:
            if x.startswith('2021'):
                # if the field stage exists in "event"
                if 'stage' in data['info']['event']:
                    filename = 'worms/' + data['info']['event']['stage'] + '.png'
                elif 'match_number' in data['info']['event']:
                    filename = 'worms/' + str(data['info']['event']['match_number']) + '.png'
                team1worm = {}
                team2worm = {}
                total_runs = 0
                for j in data['innings'][0]['overs']:
                    for k in j['deliveries']:
                        total_runs += k['runs']['total']
                    team1worm[j['over']] = total_runs
                first_total = total_runs
                total_runs = 0
                for j in data['innings'][1]['overs']:
                    for k in j['deliveries']:
                        total_runs += k['runs']['total']
                    team2worm[j['over']] = total_runs
                overs_team1 = list(team1worm.keys())
                runs_team1 = list(team1worm.values())
                overs_team2 = list(team2worm.keys())
                runs_team2 = list(team2worm.values())
                for i in range(len(overs_team1)):
                    overs_team1[i] += 1
                for i in range(len(overs_team2)):
                    overs_team2[i] += 1
                plt.figure(figsize=(20,20))
                if data['info']['teams'][0] == 'Chennai Super Kings':
                    plt.plot(overs_team1, runs_team1, ':', color='gold')
                elif data['info']['teams'][0] == 'Kolkata Knight Riders':
                    plt.plot(overs_team1, runs_team1, ':', color='indigo')
                elif data['info']['teams'][0] == 'Mumbai Indians':
                    plt.plot(overs_team1, runs_team1, ':', color='blue')
                elif data['info']['teams'][0] == 'Rajasthan Royals':
                    plt.plot(overs_team1, runs_team1, ':', color='magenta')
                elif data['info']['teams'][0] == 'Royal Challengers Bangalore':
                    plt.plot(overs_team1, runs_team1, ':', color='black')
                elif data['info']['teams'][0] == 'Sunrisers Hyderabad':
                    plt.plot(overs_team1, runs_team1, ':', color='orange')
                elif data['info']['teams'][0] == 'Delhi Capitals':
                    plt.plot(overs_team1, runs_team1, ':', color='darkblue')
                elif data['info']['teams'][0] == 'Punjab Kings':
                    plt.plot(overs_team1, runs_team1, ':', color='red')
                if data['info']['teams'][1] == 'Chennai Super Kings':
                    plt.plot(overs_team2, runs_team2, color='gold')
                elif data['info']['teams'][1] == 'Kolkata Knight Riders':
                    plt.plot(overs_team2, runs_team2, color='indigo')
                elif data['info']['teams'][1] == 'Mumbai Indians':
                    plt.plot(overs_team2, runs_team2, color='blue')
                elif data['info']['teams'][1] == 'Rajasthan Royals':
                    plt.plot(overs_team2, runs_team2, color='magenta')
                elif data['info']['teams'][1] == 'Royal Challengers Bangalore':
                    plt.plot(overs_team2, runs_team2, color='black')
                elif data['info']['teams'][1] == 'Sunrisers Hyderabad':
                    plt.plot(overs_team2, runs_team2, color='orange')
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