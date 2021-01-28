# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 10:37:38 2019

@author: kmpoo
"""
import csv
import requests
from time import sleep



TRIP = 0

def getGitHubapi(url,PW_CSV,LOG_CSV, header = None):
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
        repo_req = requests.get(url, auth=(PW_list[0][0], PW_list[0][1]), headers = header)
        TRIP = 1
    elif TRIP == 1:
        repo_req = requests.get(url, auth=(PW_list[1][0], PW_list[1][1]), headers = header)
        TRIP = 2
    else:
        repo_req = requests.get(url, auth=(PW_list[2][0], PW_list[2][1]), headers = header)        
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
        if repo_req.status_code:
            with open(LOG_CSV, 'at', encoding = 'utf-8', newline ="") as loglist:
                log_handle = csv.writer(loglist)
                log_handle.writerow(["Error accessing url",url,repo_req.status_code,repo_json['message']])
            return None   
        else:
            print("Error code = UNKNOWN ",". Error message = UNKNOWN")
            with open(LOG_CSV, 'at', encoding = 'utf-8', newline ="") as loglist:
                log_handle = csv.writer(loglist)
                log_handle.writerow(["Error accessing url","UNKNOWN","UNKNOWN"])
            return None

def ghpaginate(req):   
    """This function checks the response packet header to see if there is a link for the "next" page. Returns the link if next page exists else None """
    link = req.headers.get('link',None)
#    print("LINK+++",link)
    rel = ""
    if link:
        if 'rel="next"' in link: 
            """ if there exists a next page, do this """
            url_p = link.split('>; rel="next"')[0]
            url = url_p.split('<')[-1]
            return url
        else:
            return None
    else:
        return None 
    
def ghparse_row(repo_json, *items, prespace = 0):
    """ Create row"""
    repo_row = list()
    if prespace > 0:
        for i in range(int(prespace)):
            repo_row.append("")
    for item in items:  
        if "*" in item: 
            hitem = item.split("*")
        else: hitem = [item]
        
        if repo_json[hitem[0]] is not None:
            x = repo_json[hitem[0]]
            for i in hitem[1:]:            
                if x is not None:            
                    x = x[i] 
                else: 
                    repo_row.append("Not Found") 
                    break
            if x is str:
                repo_row.append(x.replace('\n',' ').replace('\r',' '))
            else:
                repo_row.append(x)
        else:
            repo_row.append("Not Found")
    return repo_row

def gettoken(token_file):
    """" Get the GH token from a text file"""
    with open(token_file, 'rb') as f:
        token = f.read().replace('\n', '')
    return token

if __name__ == '__main__':
  main()
  