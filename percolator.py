import heapq
import random
class Vertex:
	# `index` is a unique integer identifier, `color` is an integer in [-1, 0, 1].
	# Silver vertices have color=0, and teal vertices have color=1.
	# Unmarked vertices have color=-1.
	def __init__(self, index, color=-1):
		self.index = index
		self.color = color
	
	#for testing's sake
	def __repr__(self):
		return str(self.index)

class Edge:
	# `a` and `b` are Vertex objects corresponding to the endpoints of this edge.
	def __init__(self, a, b):
		self.a = a
		self.b = b

	def __repr__(self):
		return str(self.a) + "-" + str(self.b)

class Graph:
	# `vertices` and `edges` are iterables of Vertex and Edge objects respectively
	# Internally, we store these as set()s on the graph class.
	def __init__(self, vertices, edges):
		self.V = set(vertices)
		self.E = set(edges)

	def __repr__(self):
		return "V: " + str(self.V) + " E: " + str(self.E)

class PercolationPlayer:	
	#returns a dictionary with vertices as keys, and a list of edges the vertices connect
	#to as the keys' value
	def getEdges(graph):
		eList = {vertex : set() for vertex in graph.V}
		for edge in graph.E:
			eList[edge.a].add(edge)
			eList[edge.b].add(edge)
		return eList

	def getNeighbors(graph):
		nList = {vertex : set() for vertex in graph.V}
		for edge in graph.E:
			nList[edge.a].add(edge.b)
			nList[edge.b].add(edge.a)
		return nList

	def DFS(graph, vertex, visited, eList, nList):
		frontier = [vertex]
		V = []
		while frontier:
			current = frontier.pop()
			V.append(current)
			for neighbor in nList[current]:	
				if neighbor not in visited and neighbor not in V:
					frontier.append(neighbor)
		visited += V
		E = [edge for vertex in V for edge in eList[vertex]]
		return Graph(V, E)

	# Method to retrieve connected components
	# in an undirected graph
	def getConnectedComponents(graph):
		nList = PercolationPlayer.getNeighbors(graph)
		eList = PercolationPlayer.getEdges(graph)
		visited = []
		cc = []
		for v in graph.V:
			if v not in visited:
				cc.append(PercolationPlayer.DFS(graph, v, visited, eList, nList))
		return cc
	
	# Returns minimum set of vertices to be connected to all edges in edges
	def getVertexCover(edges, eList):
		cover = set()
		while edges:
			e = next(iter(edges))
			cover.add(e.a)
			cover.add(e.b)
			edges -= (eList[e.a] | eList[e.b])
		return cover
	
	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
	# Should return a vertex `v` from graph.V where v.color == -1
	def ChooseVertexToColor(graph, player):
		eList = PercolationPlayer.getEdges(graph)
		vertexHeap = []
		nList = PercolationPlayer.getNeighbors(graph)
		count = 0
		vertexList = graph.V
		for vertex in vertexList:
			if vertex.color == -1:
				heur = 0
				for neighbor in nList[vertex]:
					heur -= 1
					if neighbor.color == player: heur -= 25
					if len(eList[neighbor]) == 1: heur -= 5
				heapq.heappush(vertexHeap, (heur, count, vertex))
				count += 1
		if vertexHeap: return heapq.heappop(vertexHeap)[2]
	
	# `graph` is an instance of a Graph, `player` is an integer (0 or 1).
	# Should return a vertex `v` from graph.V where v.color == player
	def ChooseVertexToRemove(graph, player):
		goodEdges = {edge for edge in graph.E if edge.a.color == player and edge.b.color == player}
		vertexHeap = []
		count = 0
		eList = PercolationPlayer.getEdges(graph)
		for vertex in graph.V:
			if vertex.color == player:
				edgesToKeep = eList[vertex] & goodEdges
				heur = 3 * len(edgesToKeep) - len(eList[vertex])
				heapq.heappush(vertexHeap, (heur, count, vertex))
				count += 1
		if vertexHeap: return heapq.heappop(vertexHeap)[2]
				

# Feel free to put any personal driver code here.
def main():
	v1 = Vertex(1, -1)
	v2 = Vertex(2, 1)
	v3 = Vertex(3, -1)
	v4 = Vertex(4, 0)
	v5 = Vertex(5, 0)
	G = Graph([v1, v2, v3, v4, v5], [Edge(v1, v2), Edge(v2, v3), Edge(v4, v5)])
	print(PercolationPlayer.getVertexCover(G, PercolationPlayer.getEdges(G), 0))

if __name__ == "__main__":
	main()