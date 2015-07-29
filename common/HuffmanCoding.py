#!/usr/bin/python
# -*- coding: utf-8 -*-

'''auth HeYecheng  fshyhyc@gmail.com
   2015 - 04 -14
   本算法是 哈夫曼编码算法
   核心是找出最小的两个数作为最低等的结点，合并之后插入列表中，然后不断递归这个程序
'''
# http://blog.csdn.net/liufeng_king/article/details/8720896
# http://www.cnblogs.com/Jezze/archive/2011/12/23/2299884.html

class Node(object):
	"""docstring for Node"""
	def __init__(self, data = None, score = -1, parent = None, left = None, right = None):
		self.parent = parent
		self.left = left
		self.right = right
		self.score = score
		self.data = data
		self.code = -1
	

class HuffmanCoding(object):
	HT = None
	initNum = 0
	wholeNum = 0

	"""docstring for HuffmanCoding"""
	def __init__(self, data, weight):
		self.initNum = len(data)
		self.wholeNum = 2 * self.initNum - 1

		self.HT = [0] * self.wholeNum
		for idx, r in enumerate(data):
			self.HT[idx] = Node(r, weight[idx])
		
		for idx in xrange(self.initNum, self.wholeNum):
			self.HT[idx] = Node(None, -1)

		self.construct_tree()

	"""从集合中选择 2 个最小的数"""
	def select_two_min_score(self, stopIndex):
		k1 = -1 
		k2 = -1

		for i in xrange(0, stopIndex):
			if self.HT[i].parent == None:
				if k1 == -1 :
					min1 = self.HT[i].score
					k1 = i
				elif k2 == -1 :
					min2 = self.HT[i].score
					k2 = i
				elif self.HT[i].score < min1 or self.HT[i].score < min2:
					if min1 < min2:
						min2 = self.HT[i].score
						k2 = i
					else:
						min1 = self.HT[i].score
						k1 = i						

		return k1, k2

	"""构建哈夫曼树"""
	def construct_tree(self):
		for idx in xrange(self.initNum , self.wholeNum):
		# for idx in xrange(self.initNum , self.initNum + 1):
			k1, k2 = self.select_two_min_score(idx)
			# print 't',idx, ':', k1, k2
			self.HT[k1].parent = idx
			self.HT[k2].parent = idx
			self.HT[idx].left = k1
			self.HT[idx].right = k2
			self.HT[idx].score = self.HT[k1].score + self.HT[k2].score


	"""根据哈夫曼树 获取每个字母的编码"""
	def get_code(self, level = -1):
		if level == -1 :
			exCode = ''
		else:
			exCode = self.HT[level].code

		ltHT = self.HT[level].left
		rgHT = self.HT[level].right

		if ltHT != None:
			self.HT[ltHT].code = '%s0' % exCode
			self.get_code(ltHT)

		if rgHT != None:
			self.HT[rgHT].code = '%s1' % exCode
			self.get_code(rgHT)

		
def main():
	# data = ['a', 'b', 'c', 'd', 'e', 'f']
	# numSet = [45, 13, 12, 16, 9, 5]

	data = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	numSet = [5, 29, 7, 8, 14, 23, 3, 11]

	# data = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
	# numSet = [5, 3, 7, 12, 1, 6, 9]

	ht = HuffmanCoding(data, numSet)
	ht.get_code()
	for x in xrange(0, ht.wholeNum ):
		# print (x+1), ':' , ht.HT[x].score, ht.HT[x].parent, ht.HT[x].left, ht.HT[x].right, ht.HT[x].data, ht.HT[x].code
		print x, ':', ht.HT[x].score, ht.HT[x].parent, ht.HT[x].left, ht.HT[x].right, ht.HT[x].data, ht.HT[x].code

	print '\n\n'
	total = 0
	for x in xrange(0, len(data)):
		print ht.HT[x].score, ht.HT[x].data, ht.HT[x].code
		total += ht.HT[x].score * len(ht.HT[x].code)

	print total

main()