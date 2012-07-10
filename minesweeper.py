from flask import Flask, request, make_response
from random import randint
import json
import thread
import time

WIDTH=10
HEIGHT=10
NUM_MINES=20
NUM_PPL=1

app = Flask(__name__)
bears = [(0, "Baby Hugs Bear"), (1, "Birthday Bear")]#, (2,"Cheer Bear")]#, (3,"Friend Bear")], (4,"Funshine Bear")]
questions = []
answer = ""
curQuestionIndex = -1
gameMap = []
playerMap = []
hitMine = False
response = {"state": playerMap}
ips = dict()
last_ping = dict()
mines_found = NUM_MINES
turn = 0

def checkAlive():
    while (True):
        time.sleep(5)
        for (key, value) in last_ping.items():
            if (time.time() - value) > 20 :
                (bear, index, msg) = ips.get(key)
		print 'removing: ', bear
		print 'at index: ', index
                bears.append((index, bear))         
                del ips[key]
                del last_ping[key]

def create_questions():
	global questions
	qs = open('questions.txt')
	for line in qs :
		split = line.split(';')
		questions.append((split[0].strip(), split[1].strip().split(',')))
 
def create_game():
    for i in range(0, WIDTH):
        row = []
        p_row=[]
        for j in range(0, HEIGHT):
            row.append(None)
            p_row.append(None)
        gameMap.append(row)
        playerMap.append(p_row)
    for i in range(0,NUM_MINES) :
        planted = False
        while(not planted):
            x = randint(0,9)
            y = randint(0,9)
            if (gameMap[x][y] != -1) :
                gameMap[x][y] = -1
                planted = True
    return map

def inBound(x, y):
    return (x >= 0 and x < WIDTH and y>= 0 and y < HEIGHT)

def compute_mine(x, y):
    if gameMap[x][y] == -1 :
        return -1
    mines = 0
    for i in range(x-1,x+2):
        for j in range (y-1, y+2):
            if inBound(i,j) and gameMap[i][j] == -1:
                mines = mines + 1
    return mines

def compute_state(x,y):
    if inBound(x,y):
        if playerMap[x][y] != None :
            return -2
        mines = compute_mine(x,y)
        if mines == -1 :
            return -1
        else:
            playerMap[x][y] = mines
            if mines == 0 :
                compute_state(x-1, y)
                compute_state(x, y-1)
                compute_state(x-1, y-1)
                compute_state(x+1, y)
                compute_state(x, y+1)
                compute_state(x+1, y+1)
                compute_state(x-1, y+1)
                compute_state(x+1, y-1)
            return mines

def expand(x,y):
    mines = compute_mine(x,y)
    if mines != 0 :
        playerMap[x][y] = mines
    for i in range(x-1,x+2):
        for j in range (y-1, y+2):
            if inBound(i,j) and compute_mine(i,j) == 0 :
                compute_state(i,j)  

def checkWin():
    global mines_found
    global hitMine
    if mines_found == 0 and hitMine == False:
        for i in range(0, WIDTH) :
            for j in range(0, HEIGHT):
                if playerMap[i][j] == None :
                    return False
        return True
    return False
    
def handle_move(bear) :
	global ips
	global turn
        turn = (turn + 1) % NUM_PPL
	for (key, (b, index, msgs))  in ips.items() :
		msgs.append(("System", (bear + " has just moved")))	
			
def mine_logic(bear, x, y) :
    global response
    global questions
    global mines_found
    global hitMine
    global count
    global curQuestionIndex
    global answer
    if inBound(x, y):
        if request.args.has_key('flag'):
            if playerMap[x][y] == None :
                handle_move(bear)
		playerMap[x][y] = -2
                if gameMap[x][y] == -1 :
                    mines_found -= 1
                else :
                    mines_found += 1
            elif playerMap[x][y] == -2:
                handle_move(bear)
                playerMap[x][y] = None
                if gameMap[x][y] == -1: 
                    mines_found += 1
                else :
                    mines_found -= 1
        elif playerMap[x][y] == None:
            handle_move(bear)
            if gameMap[x][y] == -1:
                hitMine = True
                playerMap[x][y] = -1
		curQuestionIndex = randint(0, len(questions)-1 )
                (qs, answer) = questions[curQuestionIndex]
		response["question"] = qs
                mines_found -= 1
            else :
                expand(x,y)

def handle_connected(new_bear, new_index, new_ip) :
    global response
    connected_list = []
    for (key, (bear, index, msg)) in ips.items() :
        connected_list.append((bear, index, key))
    response['connected'] = connected_list
    response['player'] = (new_bear, new_index, new_ip)
    
@app.route('/', methods=['POST', 'GET'])
def mine_server():
    global bears
    global hitMine
    global curQuestionIndex
    global questions
    global answer
    new_ip = request.access_route[0]
    if new_ip not in ips :
        if len(bears) == 0 :
            overload['extra']="true"
            over_rep = make_response(json.dumps(overload))
            over_rep.headers['Access-Control-Allow-Origin']= "*"
            return over_rep
        (index, nbear) = bears.pop(0)
        ips[new_ip] = (nbear, index, [])
    last_ping[new_ip] = time.time()
    (new_bear, new_index, msg) = ips.get(new_ip)
    if request.args.has_key('message') :
        new_msg = (new_bear, request.args.get('message'))
        for (bear, ind, m) in ips.values():
            m.append(new_msg)
    if request.args.has_key('x') and not hitMine :
        print 'turn is: ', turn
	print 'index is: ', new_index
	if new_index != turn :
            can_move = {}
            can_move['moved']="false"
            move_rep = make_response(json.dumps(can_move))
            move_rep.headers['Access-Control-Allow-Origin']="*"
            return move_rep
        else :
            x = int(request.args.get('x'))
            y = int(request.args.get('y'))
            mine_logic(new_bear, x,y)
    if hitMine :
        if request.args.has_key('answer'):
            for oneAnswer in answer :
	        if request.args.get('answer').strip().lower() == oneAnswer.strip().lower():
                    hitMine = False
	            del questions[curQuestionIndex]
                    del response['question']
        if request.args.has_key('switch') and len(questions) > 1:
            new_question_num = randint(0, len(questions)-1)
            while (new_question_num == curQuestionIndex) :
                new_question_num = randint(0, len(questions)-1)
            del response['question']
            (new_trivia, new_trivia_ans) = questions[new_question_num]
	    for (key, (b, index_2, n_msgs))  in ips.items() :
                n_msgs.append(("System", (new_bear + " has just changed the question")))	
            response['question'] = new_trivia
            answer = new_trivia_ans
    if checkWin():
        response['win'] = "shire"
    print (new_bear + " has msg list: ")
    print msg
    response['messages'] = msg
    ips[new_ip] = (new_bear, new_index, [])
    handle_connected(new_bear, new_index, new_ip)
    rep = make_response(json.dumps(response))
    rep.headers['Access-Control-Allow-Origin'] = "*"
    return rep

if __name__ == '__main__' :
    create_game()
    create_questions()
    thread.start_new_thread(checkAlive, ())
    app.debug = True
    app.run(host='0.0.0.0')
