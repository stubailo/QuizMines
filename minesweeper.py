from flask import Flask, request, make_response
from random import randint
import json

WIDTH=10
HEIGHT=10
NUM_MINES=20

app = Flask(__name__)
gameMap = []
playerMap = []
ips = set()

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
			if (gameMap[x][y] != 1) :
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
	
@app.route('/', methods=['POST', 'GET'])
def mine_server():
	output = dict()
	new_ip = request.access_route[0]
	if new_ip in ips :
		print "existing ip"
		# need logic
	else:
		ips.add(new_ip)
	if request.args.has_key('x'):
		x = int(request.args.get('x'))
		y = int(request.args.get('y'))
		if inBound(x, y):
			if gameMap[x][y] == -1:
				output["question"] = "Who is the first hedgehog?"
			else :
				expand(x,y)
	output["state"] = playerMap
	rep = make_response(json.dumps(output))
	rep.headers['Access-Control-Allow-Origin'] = "*"
	return rep

if __name__ == '__main__' :
	create_game()
	app.debug = True
	app.run(host='0.0.0.0')
