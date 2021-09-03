#!/bin/python3

import requests
import threading
from queue import Queue
import os
import argparse
import time
import sys
from bs4 import BeautifulSoup as bs


os.chdir('/root/Desktop')

BLUE = '\33[94m'
END = '\033[0m'
BOLD = '\033[1m'
GREEN = '\033[32m'
YELLOW = '\33[93m'
MAGENTA = '\033[35m'
WHITE = '\033[37m'
RED = '\033[31m'
CYAN = '\033[0;36m'
UNDERLINE = '\033[4m'

print(BOLD+YELLOW+"""
  __ _           _           
 / _(_)         | |          
| |_ _ _ __   __| | ___ _ __ 
|  _| | '_ \ / _` |/ _ \ '__|
| | | | | | | (_| |  __/ |   
|_| |_|_| |_|\__,_|\___|_|   
		
		"""+BOLD,WHITE,UNDERLINE+"""by: Bhavesh Harmalkar"""+END)                 

startTime = time.time()

def addArg():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d","--domain",dest="domain",required="True",help="Specify Domain")
	parser.add_argument("-t","--thread",dest="threads",type=int,help=" Fast output [default: 650]")
	parser.add_argument("-f","--faster",dest="faster",help="Fast Bruteforcing",nargs='?',const='')
	parser.add_argument("-w","--words",dest="wordlist",help="Finding More Subdomians",nargs='?',const='')
	parser.add_argument("-o","--output",dest="output",required="True",help="Output File")
	options = parser.parse_args()
	if not options.domain:
		parser.error("Specify Domain to Scan ")
	return options
	
args = addArg()
domain = args.domain
threads = args.threads
faster = args.faster
output = args.output
wordlist = args.wordlist


queue = Queue()
subdomains = []

def write_file(filename,subdomains):
	with open(str(filename),"w+") as f:
		for subdomain in subdomains:
			f.write(str(subdomain)+"\n")


def subsDomain(subdomain):
	host = subdomain+"."+domain
	try:
		r = requests.get("http://"+host,timeout=3)
		if r.status_code == 200:
			subdomains.append(host)
	except :
		#print("Invalid Domain Name")
		sys.exit()
		
def fill_queue(words):
	for single in words:
		queue.put(single)

def worker():
	while not queue.empty():
		subdomain = queue.get()
		subsDomain(subdomain)
		
print(BOLD,BLUE+"\n [+] DOMAIN NAME \t\t  -> "+END,BOLD+GREEN+"",domain,END+"\n")
print(BOLD,BLUE+"[+] OUTPUT STORED IN\t\t  -> "+END,BOLD+GREEN+""+"/root/Desktop/"+output,END+"\n")

try:

	if wordlist == None:
		print(BOLD,BLUE+"[+] WORDLIST    \t\t  -> "+END,BOLD+GREEN+" DEFAULT"+END+"\n")
		word = open("/usr/share/finder/advance.txt","r")
		words = word.read().splitlines()
		word.close()
	else:	
		print(BOLD,BLUE+"[+] WORDLIST    \t\t  -> "+END,BOLD+GREEN,wordlist,END+"\n")
		word = open(wordlist,"r")
		words = word.read().splitlines()
		word.close()
except:
	print(BOLD,RED+"\n\t    Wordlist NotFound: "+END,wordlist)
	sys.exit()

fill_queue(words)

thread_list = []
if faster == "":
	print(BOLD,BLUE+"[+] FASTER MODE \t\t  -> "+END,BOLD+GREEN+" ON"+END+"\n")
	print(BOLD,BLUE+"[+] THREAD MODE \t\t  -> "+END,BOLD+GREEN+" ON"+END+"    [High:950]")
	for f in range(950):
		thread1 = threading.Thread(target=worker)
		thread_list.append(thread1)
else:
	if threads:
		if threads > 850:
			print(BOLD,BLUE+"[+] FASTER MODE \t\t  -> "+END,BOLD+GREEN+" OFF"+END+"\n")
			print(BOLD,BLUE+"[+] THREAD MODE \t\t  -> "+END,BOLD+GREEN+" ON"+END+"    [Max:850]")
			for f in range(850):
				thread1 = threading.Thread(target=worker)
				thread_list.append(thread1)
		if threads < 849:
			print(BOLD,BLUE+"[+] FASTER MODE \t\t  -> "+END,BOLD+GREEN+" OFF"+END+"\n ")
			print(BOLD,BLUE+"[+] THREAD MODE \t\t  -> "+END,BOLD+GREEN+" ON"+END+"    Threads Count: ",threads)
			for f in range(threads):
				thread1 = threading.Thread(target=worker)
				thread_list.append(thread1)
	else:
		print(BOLD,BLUE+"[+] FASTER MODE \t\t  -> "+END,BOLD+GREEN+" OFF"+END+"\n")	
		print(BOLD,BLUE+"[+] THREAD MODE \t\t  -> "+END,BOLD+GREEN+" ON"+END+"    [Default:650]")	
		for t in range(650):
			thread1 = threading.Thread(target=worker)
			thread_list.append(thread1)
	
		


print(BOLD,BLUE+"\n [+] POSSIBLE SUBDOMAINS TO TRY   ->"+END,BOLD,GREEN,str(len(words)),END)

for thread in thread_list:
	thread.start()

for thread in thread_list:
	thread.join()

count = 0	
if output:
	print()
	print("    "+"-"*82)
	print(BOLD,YELLOW+"\tSno\t  Server\t\t\t\t\tSubdomains"+END)
	print("    "+"-"*82)

	for subDo in subdomains:
		count+=1
		print("\t",count,end="")
		try:
			header = requests.get("http://"+subDo,timeout=3)
			print(BOLD,WHITE+"\t"+header.headers['Server'],END,end="")

		except:
			print(BOLD,RED+"\tunknown",END,end="")
			pass	
		print(BOLD,GREEN+"\t\t\t\t"+subDo,END,end="")
		print()
		
			
	write_file(output,subdomains)
'''else:
	print("           "+"-"*26)
	print(BOLD,YELLOW+"\t   Sno\t     Subdomains"+END)
	print("           "+"-"*26)
	#print("\n")
	for subDo in subdomains:
		count+=1
		print("\t   ",count,end="",)
		print(BOLD,GREEN+"\t"+subDo,END)'''
	
endTime = time.time()
total = endTime - startTime
print(BOLD,MAGENTA+"\n\t    Time Taken:"+END,BOLD,WHITE,total,END,BOLD,MAGENTA+"Sec",END)		

	
	