#!/usr/bin/python3
import os
import sys
import time
import urllib.request
import csv
import ssl
import socket


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


while True:
    output = open("./output.txt","r") 
    from pathlib import Path
    from collections import deque

    fn = Path('./output.txt')
    with fn.open('r') as f:
        last = deque(f,1)

    indexme = int(last[0])
    #print(indexme,flush=True)
    output.close()

    output = open("./output.txt","a+") 

    with open('./data.csv', "rt", encoding='ascii') as f:
        reader = csv.reader(f)
        row = next((item for item in reader if item[0] == str(indexme)), None)

        #print(row,flush=True)
        
        domain = row[1]
        domain1=urllib.parse.quote_plus(domain)

        #This is a sample API of a website, replace it with your specific rest API, here we are placing the domain value in the API: {0}
        url="http://yourwebsite.com/index.php/en/website/calculate?CalculationForm[domain]={0}&redirect=%2Fen%2Fcost%2F__DOMAIN__&instant=0" .format(domain1)
        
        #print(url,flush=True)
    
        from urllib.error import HTTPError, URLError
        try:
            #Call rest API
            response = urllib.request.urlopen(url, context=ctx, timeout=10).read().decode('utf-8')
        except HTTPError as error:
            logging.error('Data not retrieved because %s\nURL: %s', error, url)
            pass
        except URLError as error:
            if isinstance(error.reason, socket.timeout):
                logging.error('socket timed out - URL %s', url)
            else:
                logging.error('some other error happened')
            pass
        except socket.timeout:
            pass
        
        #Increase counter value to siwtch next row in CSV file
        indexme=indexme+1
        print(indexme,flush=True)

        #Write last index value to output file
        output.writelines(str(indexme))
        output.write("\n")
        output.seek(0)  
        output.close()

        #Wait for 10 seconds for next submit
        time.sleep(10)
