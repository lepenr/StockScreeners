#!/usr/bin/python2.7
import csv
import urllib2

#get ticket from txt file
ticket_output = ''
with open('tickets.txt','r') as f:
    for line in f:
        for word in line.split():
          ticket_output = ticket_output  + word +'+'

#url of Yahoo HTTP service
url = 'http://finance.yahoo.com/d/quotes.csv?s=' + ticket_output + '&f=snbaopl1p2va2'
response = urllib2.urlopen(url)
#Get and clean data from CSC
cr = csv.reader(response)
fifteen = ''
ten = ''
five = ''
high_volume = ''
permanent_ticket = ''
for row in cr:
    symbol = row[0]
    name = row[1]
    bid = row[2]
    ask = row[3]
    open = row[4]
    previousClose = row[5]
    last = row[6]
    change = row[7].replace('%','')
    change = float(change.replace('N/A','0'))
    volume = float(row[8].replace('N/A','0'))
    volume = float(row[8].replace('N/A','0'))/1000000
    avgvolume = float(row[9].replace('N/A','0'))/1000000

    #change = float(change.replace('N/A',0))
    #define color of change red down green up
    if change > 0:
        color = '<a style=\"color:green;\">'
    else:
        color = '<a style=\"color:red;\">'
    #----
    #This secion creates output in HTML format, which can be send as and HTML
    if change > 15 or change < (-15):
            fifteen = " %s %s%%</a> (%s)%s PreviousClose:%s LastClose:%s Volume:%sM AVGvolume%sM<br> %s \r\n " % (color, str(change), symbol,name, previousClose, last,round(volume,2),round(avgvolume,2),fifteen)
            #fifteen = color +  str(change)  + '%</a> ('  +symbol + ')' + name + bid + ask  +"\r\n" + '<br>' + fifteen
    else:
        if change > 10 or change < -10:
            ten = " %s %s%%</a> (%s)%s PreviousClose:%s LastClose:%s<br> %s \r\n " % (color, str(change), symbol,name, previousClose, last, ten)
        else:
            if change > 5 or change < -5:
                five = " %s %s%%</a> (%s)%s PreviousClose:%s LastClose:%s<br> %s \r\n " % (color, str(change), symbol,name, previousClose, last, five)
    if volume > avgvolume and ((volume - avgvolume)*100/(avgvolume) > 100):
        high_volume =   "%s %s%%</a> (%s)%s PreviousClose:%s LastClose:%s Volume:%sM AVGvolume%sM Volume up %s%%<br> %s \r\n " % (color, str(change), symbol,name, previousClose, last,round(volume,2),round(avgvolume,2),round((volume - avgvolume)*100/(avgvolume),2),high_volume)
   # if symbol in word2:
    #                 permanent_ticket = " %s %s%%</a> (%s)%s Ask:%s PreviousClose:%s LastClose:%s<br> %s \r\n " % (color, str(change), symbol,name,ask, previousClose, last, permanent_ticket)
    #OUTPUT 
    output = "\r\n" + '<b>Over 15% change:</b>' + "\r\n"+ '<br>' + fifteen +  '<br>' +'<b>Over 10% change:</b>' + "\r\n" + '<br>' + ten + '<br>' +'<b>Over 5% change:</b>' + "\r\n" + '<br>' + five +  '<br>' +'<b>Volume chng oved 100%: :</b>' + "\r\n" + '<br>'+ high_volume# + '<br>' + permanent_ticket

print (output)

#Email section

import email.message
import smtplib

msg = email.message.Message()
msg['Subject'] = 'Morning stock news'
msg['From'] = 'Stock Screener'
msg['To'] = 'Email adress'
#Setup a email format to HTLM
msg.add_header('Content-Type','text/html')
msg.set_payload(output)

s = smtplib.SMTP('smtp.gmail.com:587')
s.starttls()
s.login('Login - gmail email',
        'password')
s.sendmail(msg['From'], [msg['To']], msg.as_string())
