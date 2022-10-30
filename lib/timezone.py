import time

# Calculate time based on the current location 
def calcOffsetSeconds():
    year = time.localtime()[0]       #get current year
    HHMarch   = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) #Time of March change to EEST
    HHOctober = time.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to EET
    now=time.time()
    if now < HHMarch :               # we are before last sunday of march
        sec = 7200 # EET:  UTC+2H
    elif now < HHOctober :           # we are before last sunday of october
        sec = 10800 # EEST: UTC+3H
    else:                            # we are after last sunday of october
        sec = 7200 # EET:  UTC+2H
    return(sec)