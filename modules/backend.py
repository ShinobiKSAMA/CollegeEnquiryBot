from flask import session
import aiml
import sntnce as s
import random
import re
from mappings import map_keys
import os

sent_check = s.Sent_Similarity()

userName = "Anonymous"
user_auth_id=0
GREETING = ['Hello! My name is P8-bot. I will try my best to provide you information related to our College!']

DEFAULT_RESPONSES = ["I did not get you! Pardon please!","I couldn't understand what you just said! Kindly rephrase"
					 " what you said :-)" ]

EMPTY_RESPONSES = ["Say something! I would love to help you!","Don't hesitate. I'll answer your queries to the best"
				   " of my knowledge!","Say my friend!"]

ONE_WORD_RESPONSES = ["Please elaborate your query for me to understand!", "I could not understand your context, please say more!",
					  "Sorry, I could not get you! Please say something more for me to understand!"]

UNAME_REQ = 0
PWD_REQ = 0

def conv_mapping(inp):
	new_inp = ''
	keys = map_keys.keys()
	arr = inp.split()
	for a in arr:
		if(a in keys):
			new_inp = new_inp + str(map_keys[a])
		else:
			new_inp = new_inp + a
	return new_inp

def printBot(msg, lst=None):
	print(botName+": "+msg)
	if(lst!=None):
		print(botName+": ",lst)
	
def match(line, word):
	pattern = '\\b'+word+'\\b'
	if re.search(pattern, line, re.I)!=None:
		return True
	return False

def matchingSentence(inp):
	f = open('database/questions.txt')
	match = "";
	max_score=0;
	for line in f.readlines():
		score = sent_check.symmetric_sentence_similarity(inp, line)
		if score > max_score:
			max_score = score
			match = line
	f.close()
	return match, max_score

def preprocess(inp):
	if(inp!=""):
		if inp[-1]=='.':
			inp = inp[:-1]
	# to remove . symbol between alphabets. Eg. E.G.C becomes EGC
	inp = re.sub('(?<=\\W)(?<=\\w)\\.(?=\\w)(?=\\W)','',inp) 
	# to remove - symbol between alphabet. Eg. E-G-C becomes EGC
	inp = re.sub('(?<=\\w)-(?=\\w)',' ',inp) 
	# to remove . symbol at word boundaries. Eg. .E.G.C. becomes E.G.C
	inp = re.sub('((?<=\\w)\\.(?=\\B))|((?<=\\B)\\.(?=\\w))','',inp)
	# to remove ' ' symbol in acronyms. Eg. E B C becomes EBC
	inp = re.sub('(?<=\\b\\w) (?=\\w\\b)','',inp)
	inp = inp.upper()

	return inp

def isKeyword(word):
	f = open('database/questions.txt','r')
	keywords = f.read().split()
#    print(keywords)
	if(word in keywords):
		return True
	else: 
		return False

def start(inp, k):

	global userName,UNAME_REQ,PWD_REQ
	print(session.get('sid'))
	# tasks: remove punctuation from input or make it get parsed, do something when no match is found; removed last period to end sentence
	p_inp = preprocess(inp)
	
	inp = p_inp
	response = k.respond(inp, session.get('sid'))
	if(response=='No match'):
		# to invalidate wrong one-word input
		if(len(inp.split(" "))==1):
			if(isKeyword(inp)==False):
				return(random.choice(ONE_WORD_RESPONSES))
				
		inp = matchingSentence(inp)
#        print(inp)
		response = k.respond(inp[0], session.get('sid'))
		confidence = inp[1]
		if(confidence < 0.5):
			log = open('database/invalidated_log.txt','a')
			log.write(p_inp+"\n")
			log.close()
			return(random.choice(DEFAULT_RESPONSES))
		else:
			response = re.sub('( )?(http:[%\-_/a-zA-z0-9\\.]*)','<a href="\\2">\\2</a>',response)
#            print(response)
			return(response)
	elif(response==""):
		return(random.choice(EMPTY_RESPONSES))
	else: 
		response = re.sub('( )?(http:[%\-_/a-zA-z0-9\\.]*)','<a href="\\2">\\2</a>',response)
		return (response)
	
	if(k.getPredicate('name', session.get('sid'))!=""):
		userName = k.getPredicate('name', session.get('sid'))
	else:
		k.setPredicate('name','Anonymous', session.get('sid'))
		userName = k.getPredicate('name', session.get('sid'))    