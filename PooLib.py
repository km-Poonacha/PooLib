# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 10:37:38 2019

@author: kmpoo
"""
import requests
from time import sleep

PW_CSV = 'C:/Users/USEREN/Dropbox/HEC/Python/PW/PW_GitHub.csv'
TRIP = 0

def getGitHubapi(url):
    """This function uses the requests.get function to make a GET request to the GitHub api
    TRIP flag is used to toggle GitHub accounts. The max rate for searches is 30 per hr per account"""
    global TRIP
    """ Get PW info """
    PW_list = []
    
    with open(PW_CSV, 'rt', encoding = 'utf-8') as PWlist:
        PW_handle = csv.reader(PWlist)
        del PW_list[:]
        for pw in PW_handle:
            PW_list.append(pw)
    if TRIP == 0:
        repo_req = requests.get(url, auth=(PW_list[0][0], PW_list[0][1]))
        print(repo_req.status_code)
        TRIP = 1
    elif TRIP == 1:
        repo_req = requests.get(url, auth=(PW_list[1][0], PW_list[1][1]))
        print(repo_req.status_code)
        TRIP = 2
    else:
        repo_req = requests.get(url, auth=(PW_list[2][0], PW_list[2][1]))
        print(repo_req.status_code)
        TRIP = 0
        
    if repo_req.status_code == 200: 
        print(repo_req.headers['X-RateLimit-Remaining'])
        if int(repo_req.headers['X-RateLimit-Remaining']) <= 3:
            """  Re-try if Github limit is reached """
            print("************************************************** GitHub limit close t obeing reached.. Waiting for 10 mins" )
            """ Provide a 10 mins delay if the limit is close to being reached  """
            sleep(600)
            
        """ Return the requested data  """
        return repo_req
    else:
        print("Error accessing url = ",url)
        repo_json = repo_req.json()
        print("Error code = ",repo_req.status_code,". Error message = ",repo_json['message'])
        return 0   


     
if __name__ == '__main__':
  main()
  