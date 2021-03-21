
INF = 999

def Dijkstra(v0,vertex_total,INF=999): 
	book = set()
	minv = v0   
	dis = dict((k,INF) for k in range(1,vertex_total+1))
	dis[v0] = 0 
	while len(book)<vertex_total:
		book.add(minv)                                  
		for w in range(1,vertex_total+1):                               # 以当前点的中心向外扩散
			if dis[minv] +Graph[minv][w] < dis[w]:         # 如果从当前点扩展到某一点的距离小与已知最短距离      
				dis[w] = dis[minv] + Graph[w]         # 对已知距离进行更新
		new =INF                                       # 从剩下的未确定点中选择最小距离点作为新的扩散点
		for v in dis.keys():
			if v in book: continue
			if dis[v] < new: 
				new = dis[v]
				minv = v
	return dis	

Graph = []
for i in range(cities):
	Graph.append([INF]*cities)
Product = [0]*cities
Price = [100000000]*cities
Order = [0]*cities

for i in range(roads):
	g_o, g_i = list(map(int,input().split()))
	g_o -= 1
	g_i -= 1
	Graph[g_o][g_i] = 1

for i in range(whs):
	w, pr, loc = list(map(int,input().split()))
	loc -= 1
	Product[loc] = w
	Price[loc] = pr

orders = int(input())
for i in range(orders):
	e, loc = list(map(int,input().split()))
	loc -= 1
	Order[loc] = e

distance = Dijkstra(order_place, warehouse)
