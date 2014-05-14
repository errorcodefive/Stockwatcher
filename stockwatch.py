import ystockquote
import smtplib
import argparse
import pygame

from time import strftime
from time import sleep
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
#NUMBER OF RETRY ATTEMPTS UNTIL WE MOVE ON
num = 2
#TIME TO CHECK PREVIOUS STOCK PRICE (MINUTES)
timeChange = 1
#debug mode (no emails sent) true or false
debugMode = True

#for daily update
def changePercent(price, change):
    percent = change/price*10000.0
    #rounding to two decimal places
    percent = int(percent)
    percent = percent/100.0
    return percent

#CHECK DIFFERENCE BETWEEN OPENING AND CLOSE, SCREEN FOR THRESHOLD CHANGE
def aftChange (symList,threshold):
    attempts = 0
    output = ""
    outList = []
    preOut = []
    for symbol in symList:
        attempts = 0
        change = 0.0
        priceTimeZero = 0.0
        priceTimeDelta = 0.0
        while attempts < num:
            attempts+=1
            try:        
                outList = [symbol, "NAME", "PRICE", "CHANGE", "PCHANGE"]
                outList[1] = ystockquote.get_company_name(symbol).strip("'\"")
                #get 1st price
                priceTimeZero = ystockquote.get_previous_close(symbol).strip("'\"")
                #get price last day
                priceTimeDelta = ystockquote.get_today_open(symbol).strip("'\"")
                #change this so it rounds to 2 decimal places
                outList[2] = priceTimeDelta
                #determine change
                change = float(priceTimeDelta) - float(priceTimeZero)
                outList[3] = change
                #calculate percent change
                outList[4] = changePercent(float(priceTimeDelta),change)
                attempts = num+1
                
            except:
                pass
        if outList[4]<=float(threshold):
            preOut.append(outList)    
    #output in nice format
    for i in range(len(preOut)):
        
        temp = preOut[i][0].ljust(7)+preOut[i][1].ljust(20)+preOut[i][2].ljust(7)+str(preOut[i][3]).rjust(8)+str(preOut[i][4]).rjust(8)+"%\n"
        output +=str(temp)
                
    return output

#CHECK DIFFERENCE BETWEEN LAST PRICE LAST DAY AND NOW
def mornChange (symList,threshold):
    attempts = 0
    output = ""
    outList = []
    preOut = []
    for symbol in symList:
        attempts = 0
        change = 0.0
        priceTimeZero = 0.0
        priceTimeDelta =0.0
        while attempts < num:
            attempts+=1
            try:        
                outList = [symbol, "NAME", "PRICE", "CHANGE", "PCHANGE"]
                outList[1] = ystockquote.get_company_name(symbol).strip("'\"")
                #get 1st price
                priceTimeZero = ystockquote.get_previous_close(symbol).strip("'\"")
                #get price last day
                priceTimeDelta = ystockquote.get_last_trade_price(symbol).strip("'\"")
                #change this so it rounds to 2 decimal places
                outList[2] = priceTimeDelta
                #determine change
                change = float(priceTimeDelta) - float(priceTimeZero)
                outList[3] = change
                #calculate percent change
                outList[4] = changePercent(float(priceTimeDelta),change)
                attempts = num+1
                
            except:
                pass
        if outList[4]<=float(threshold):
            preOut.append(outList)    
    #output in nice format
    for i in range(len(preOut)):
        
        temp = preOut[i][0].ljust(7)+preOut[i][1].ljust(20)+preOut[i][2].ljust(7)+str(preOut[i][3]).rjust(8)+str(preOut[i][4]).rjust(8)+"%\n"
        output +=str(temp)
                
    return output

def symPriceToday(symList):
    output = ""
    outList = []
    popIn = []
    attempts = 0
    for symbol in symList:
        popIn = [symbol, "NAME", "PRICE", "CHANGE", "PCHANGE"]
               
        #Company Name
        attempts = 0
        while attempts<num:
            attempts+=1
            try:
                popIn[1] = ystockquote.get_company_name(symbol).strip("'\"")
                #popIn[1] = ystockquote.get_company_name(symbol)
                attempts = num+1
            except:
                pass
        #Trade Price
        attempts = 0
        while attempts<num:
            attempts+=1
            try:
                popIn[2] = ystockquote.get_last_trade_price(symbol).strip("'\"")
                attempts = num+1
            except:
                pass
        #Change
        attempts = 0
        while attempts<num:
            attempts+=1
            try:
                popIn[3] = float(str(ystockquote.get_change(symbol).strip("+'\"")))
                attempts = num+1
            except:
                pass
        #Percent Change
        '''
        attempts = 0
        while attempts<num:
            attempts +=1
            try:
                popInt[4] = ystockquote.get_change_percent_change(symbol).strip("'\"")
                attempts = num+1
            except:
                pass
        '''
        popIn[4] = changePercent(float(popIn[2]),float(popIn[3]))
        outList.append(popIn)
        
    #Output Formatting
    for i in range(len(outList)):
        temp = outList[i][0].ljust(7)\
               +outList[i][1].ljust(20)\
               +outList[i][2].ljust(7)\
               +str(outList[i][3]).rjust(7)\
               +str(outList[i][4]).rjust(6)+"%\n"
        output += str(temp)
    return output

#EMAIL INIT
sender = "errorcodefive@gmail.com"
receiver = "chinkylee@gmail.com"
username = "errorcodefive"
password = "Cadmium24"
eSubj = "Stock List Update - " + strftime("%Y-%m-%d %H:%M:%S")
msg = MIMEMultipart()
msg['From']= sender
msg['To'] = receiver
msg['Subject'] = eSubj

#PORTFOLIO
symListCan = ["CGX.TO"]
symListJap = ["NTDOY"]
symListUSFin = ["AXP"]
symListUSAero = ["BA", "LMT", "NOC"]
symListUSEnter = ["CMCSA", "DIS", "EA", "LGF", "TWX", "VIAB"]
symListUSSciTech = ["CRL", "HON", "MMM", "NFLX", "TMO", "TSM", "WDC", "GLW"]
symListUSFood = ["HSY"]

#WATCHLIST
symListWatch = ["TMO", "DOW", "MMM", "FOXA", "IMX","RTN", "GD", "STX", "SNDK", "COF"]

        
#ARGPARSE
parser = argparse.ArgumentParser()

parser.add_argument("-p", "--portfolio", help = "send email of portfolio stocks", action = 'store_true')
parser.add_argument("-wl","--watchlist", type = float, help = "check for n% decrease in price of watchlist stocks")
parser.add_argument("-m", "--morning", type = float, help = "check for n% decrease in price of watch list stock from last day's price to now")
parser.add_argument("-gui","--gui", help = "GUI Stockwatch", action = "store_true")

args = parser.parse_args()

#IF PORTFOLIO ARGUMENT PASSED
if args.portfolio:

	eOutput = "Canadian\n" + symPriceToday (symListCan)\
				  +"\nJapanese\n" + symPriceToday(symListJap)\
				  +"\nUS Financial\n" + symPriceToday(symListUSFin)\
				  +"\nUS Aeronautics\n" + symPriceToday(symListUSAero)\
				  +"\nUS Entertainment\n" + symPriceToday(symListUSEnter)\
				  +"\nUS Sci & Tech\n" + symPriceToday(symListUSSciTech)\
				  +"\nUS Food\n" + symPriceToday(symListUSFood)
				  
	if debugMode == True:
		print ("Portfolio Mode")
		print eOutput

	elif debugMode == False:
		#SEND EMAIL
		body = eOutput
		msg.attach(MIMEText(body, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username,password)
		eText = msg.as_string()
		server.sendmail(sender,receiver,eText)
		
#READ PERCENT CHANGE FROM ARGUMENTS AND CHECK WATCHLIST FOR STOCK CHANGES
if args.watchlist:
	perChange = args.watchlist
	eOutput = "Watchlist Report:\n" + "1% change \n" + aftChange(symListWatch,perChange)
	if debugMode == True:
		print ("Watchlist Mode")
		print perChange
		print eOutput
	elif debugMode == False:
		
		#SEND EMAIL
		body = eOutput
		msg.attach(MIMEText(body, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username,password)
		eText = msg.as_string()
		server.sendmail(sender,receiver,eText)
		
#READ PERCENT CHANGE FROM ARGUMENTS AND CHECK WATCHLIST FOR STOCK CHANGES FROM PREVIOUS DAY    
if args.morning:
	perChange = args.morning
	eOutput = "Morning Report:\n" +"1% change\n" + mornChange(symListWatch,perChange)
	if debugMode == True:

		print ("Morning Mode")
		print perChange
		print eOutput
	elif debugMode == False:
		#SEND EMAIL
		body = eOutput
		msg.attach(MIMEText(body, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com',587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username,password)
		eText = msg.as_string()
		server.sendmail(sender,receiver,eText)

if args.gui:
    pygame.init()
    screen = pygame.display.set_mode((1600,900))
    
