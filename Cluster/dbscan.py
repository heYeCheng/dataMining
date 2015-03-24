#coding=utf-8
from math import log

'''auth HeYecheng  fshyhyc@gmail.com
   2015 - 03 - 24
   本算法是 DBSCAN ，一种基于高密度连通区域的聚类算法

   给定一个对象集合D，对象之间的距离函数为distance(*，*)，邻域半径为Eps。
   Eps邻域：给定对象半径Eps内的邻域称为该对象的Eps邻域。我们用 N eps(p)  表示点p的Eps-半径内的点的集合，即
             N eps(p) = {q| q 在数据集D 中，distance(p,q)<= Eps}
   MinPts：给定邻域  N eps(p) 包含的点的最小数目，用以决定点p是簇的核心部分还是边界点或噪声。
   核心对象：如果对象的Eps邻域包含至少 MinPts 个的对象，则称该对象为核心对象。
   边界点：边界点不是核心点，但落在某个核心点的邻域内。
   噪音点：既不是核心点，也不是边界点的任何点。
   直接密度可达：如果p在q的Eps邻域内，而q是一个核心对象，则称对象p 从对象q出发时是直接密度可达的(directly density-reachable)。
   密度可达：从关于Eps 和 MinPts 直接密度可达的，则对象p是从对象q关于Eps和MinPts密度可达的(density-reachable)。
   密度相连：如果存在对象O∈D，使对象p和q都是从O关于Eps和MinPts密度可达的，那么对象p到q是关于Eps和MinPts密度相连的(density-connected)。


    DBSCAN(D, eps, MinPts)
	   C = 0
	   for each unvisited point P in dataset D
	      mark P as visited
	      NeighborPts = regionQuery(P, eps)
	      if sizeof(NeighborPts) < MinPts
	         mark P as NOISE
	      else
	         C = next cluster
	         expandCluster(P, NeighborPts, C, eps, MinPts)
	          
	expandCluster(P, NeighborPts, C, eps, MinPts)
	   add P to cluster C
	   for each point P' in NeighborPts 
	      if P' is not visited
	         mark P' as visited
	         NeighborPts' = regionQuery(P', eps)
	         if sizeof(NeighborPts') >= MinPts
	            NeighborPts = NeighborPts joined with NeighborPts'
	      if P' is not yet member of any cluster
	         add P' to cluster C
	          
	regionQuery(P, eps)
	   return all points within P's eps-neighborhood (including P)
'''
def mergeArr(arr1, arr2):
	# 用于进行两个数组的合并，并去掉重复值
	for x in arr2:
		if x not in arr1:
			arr1.append(x)

	return arr1

def ManhattanDis(p, py):
	# 计算曼哈顿距离
	dis = 0
	for i in xrange(0, len(p)):
		dis += abs(p[i] - py[i])

	return dis

def init_prepare(D, eps):
	# 用于首先计算每个点的邻域
	resArr = [0] * len(D)   
	for i in xrange(0, len(D)):
		resArr[i] = []
		for j in xrange(0, len(D)):
			if i == j:
				resArr[i].append(j)
			else:
				# 计算两个点之间的距离
				dis = ManhattanDis(D[i], D[j])
				if dis <= eps:
					resArr[i].append(j)

	return resArr


def regionQuery(P):
	# 返回某个点的邻域
	return epsArr[P]

def expandCluster(P, NeighborPts, C, cIndex, eps, MinPts):
	# 根据某些点进行不断扩展，合并邻域
	global cluArr
	C.append(P)
	cluArr[P] = cIndex

	for sgP in NeighborPts:
		if MarkArr[sgP] == 0:
			MarkArr[sgP] = 1   # mark P as visited
			subNeighborPts = regionQuery(sgP)
			if len(subNeighborPts) >= MinPts:
				NeighborPts = mergeArr(NeighborPts, subNeighborPts)

		if cluArr[sgP] == -1:
			C.append(sgP)


def DBSCAN(D, eps, MinPts):
	global MarkArr
	C = []
	cIndex = 0
	for x in xrange(0, len(D)):
		if MarkArr[x] == 0:
			# print x
			MarkArr[x] = 1   # mark P as visited
			NeighborPts = regionQuery(x)
			if len(NeighborPts) < MinPts:
				MarkArr[x] = 'Noise'   # mark P as NOISE
			else:
				C.append(cIndex)
				C[cIndex] = []
				expandCluster(x, NeighborPts, C[cIndex], cIndex, eps, MinPts)
				cIndex += 1

	print C
	print MarkArr



dataset = [(1,2), (2,1), (2,4),(4,3), (5,8), (6,7), (6,9) ,(7,9), (9,5), (1,12), (3,12), (5,12),(3,3)]
MarkArr = [0] * len(dataset) 
cluArr = [-1] * len(dataset) 

epsArr = init_prepare(dataset, 3)
DBSCAN(dataset, 3, 3)
