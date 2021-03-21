# C[12][7]
# P[12]
# Path[12][5]

def getCoins(CC,PP):
	if PP == 0 or today - PP >= 7:
		return CC[6]
	else:
		return CC[today - PP - 1]

days = int(input())
C = []
for i in range(12):
    C.append(list(map(int,input().split())))

Path = [[2,3,5,6,7,1],
[1,3,4,6,8,2],
[1,2,4,5,9,3],
[2,3,8,9,10,4],
[1,3,7,9,11,5],
[1,2,7,8,12,6],
[1,5,6,11,12,7],
[2,4,6,10,12,8],
[3,4,5,10,11,9],
[4,8,9,11,12,10],
[5,7,9,10,12,11],
[6,7,8,10,11,12]]

P = [0]*12

today = 0
sum_coins = 0

if days == 1:
	nodes = [1,2,3]
	coins = list(map(lambda node: getCoins(C[node - 1],P[node - 1]), nodes))
	print(max(coins))
else:
	# if days % 2 == 1:
	# 	days += 1
	today = 1
	nodes = [1,2,3]
	coins = list(map(lambda node: getCoins(C[node - 1],P[node - 1]), nodes))
	c_node = coins.index(max(coins))
	sum_coins += max(coins)
	P[c_node] = today
	nodes = Path[c_node]
	today += 2
	while today <= days:
		coins = list(map(lambda node: getCoins(C[node - 1],P[node - 1]), nodes))
		n_index = coins.index(max(coins))
		c_node = nodes[n_index] - 1
		sum_coins += max(coins)
		P[c_node] = today
		nodes = Path[c_node]
		today += 2
	print(sum_coins)
