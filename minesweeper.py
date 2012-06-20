from flask import Flask, request
from random import randint
import json

WIDTH=10
HEIGHT=10
NUM_MINES=20

app = Flask(__name__)
gameMap = []
ips = set()

def create_game():
	for i in range(0, WIDTH):
		row = []
		for j in range(0, HEIGHT):
			row.append(0)	
		gameMap.append(row)
	for i in range(0,NUM_MINES) :
		planted = False
		while(not planted):
			x = randint(0,9)
			y = randint(0,9)
			if (gameMap[x][y] != 1) :
				gameMap[x][y] = 1
				planted = True
	return map

def inBound(x, y):
	return (x >= 0 and x < WIDTH and y>= 0 and y < HEIGHT)

def compute_mine(x, y):
	mines = 0
	for i in range(x-1,x+2):
		for j in range (y-1, y+2):
			if inBound(i,j):
				mines = mines + gameMap[i][j]
	return mines
				
@app.route('/', methods=['POST', 'GET'])
def mine_server():
	resp = 0
	new_ip = request.access_route[0]
	if new_ip in ips :
		print "existing ip"
		# need logic
	else:
		ips.add(new_ip)
	x_cord = int(request.args.get('x'))
	y_cord = int(request.args.get('y'))
	if inBound(x_cord, y_cord):
 		if gameMap[x_cord][y_cord] == 1:
			print "hit a mine"	# hit a mine
			resp = -1
		else :	
			resp = compute_mine(x_cord, y_cord)
	response = ""
	if request.method == 'POST' :
		response = response + "POST</br>"
	elif request.method == 'GET' :
		response = response +  "GET</br>"
	for ip in request.access_route :
		response = response + ip + "</br>"
	for i in range(0, WIDTH):
		response = response + str(gameMap[i]) + "</br>"
	print response
	return json.dumps({"state" : gameMap, "response" : resp})

if __name__ == '__main__' :
	create_game()
	app.debug = True
	app.run(host='0.0.0.0')
