#!/usr/bin/python
# coding=utf-8

'''auth HeYecheng  fshyhyc@gmail.com
   2015 - 04 -19
   跳表的实现，基本原理是 N 个链表的拼凑，跳表之所以速度快，是因为跳表是有索引的链表，不需要重头开始逐个检索
'''
import random


class Node(object):
	"""docstring for Node"""
	def __init__(self, data, level, child = None, nextNode = None):
		self.data = data
		self.level = level
		self.next = nextNode  # 同一个层级的下一个节点
		self.child = child    # 下一个层级的下一个节点


class skipList(object):
	"""wholeLevel 表示总层数，  probable 表示属于某一层的概率"""
	def __init__(self, wholeLevel, probable, dataSet = None ):
		self.wholeLevel = wholeLevel
		self.probable = probable

		self.skipArr = [0] * wholeLevel
		
		
	def cal_belong_level(self):
		'用于计算某一个数属于哪一个层级'
		i = 0
		while random.random() < self.probable and i < self.wholeLevel - 1:
			i = i + 1

		# print 'level:',i
		return i

	def insert_node(self, data):
		'插入值，首先随机分配该值属于哪一层级， 然后插入到该层级以下的所有层'
		belevel = self.cal_belong_level()
		tempX = belevel

		# 构建同一个 data 的节点递进关系链
		for x in xrange(0, tempX + 1):
			if x == 0:
				childNode = Node(data, 0)
			else:
				childNode = Node(data, x, childNode)

		res = 0
		while tempX >= 0:
			if res == 0:
				res = self.find_range(tempX, data)
			else:
				res = self.find_range(tempX, data, res.child)

			# print 'insert res:',res
			if res == 0:
				if self.skipArr[tempX] != 0:
					prevNode = self.skipArr[tempX]
					childNode.next = prevNode

				self.skipArr[tempX] = childNode
			else:
				prevNode = res.next
				childNode.next = prevNode
				res.next = childNode

			tempX = tempX - 1
			childNode = childNode.child


	def find_range(self, curLevel, data, parentNode = None):
		'查找某一个值在某一层中的上一个节点，如果 parent 不为空，表示是由上一层传递下来继续查找的，  跳表的核心是跳着查找数据'
		'本结果返回 3 种结果。 1：若本层没有数据，则为空  2：若本层有数据，但找不到这个值，则返回最接近这个值的上一个节点  3：若找到这个值，则直接返回这个节点'
		if parentNode:
			nextNode = parentNode
			
			while True:
				if nextNode.next:
					if nextNode.next.data <= data:
						nextNode = nextNode.next
					else:
						return nextNode
				else:
					return nextNode
		else:
			if self.skipArr[curLevel] == 0:
				# 表示要从第一个位置插入
				return 0
			else:
				if self.skipArr[curLevel].data > data:
					# 表示此层的第一个元素比给定的值还大
					return 0
				elif self.skipArr[curLevel].data == data:
					# 如果相等，直接返回这个结点，一般见于搜索节点
					return self.skipArr[curLevel]
				else:
					nextNode = self.skipArr[curLevel]

				while True:
					if nextNode.next:
						if nextNode.next.data < data:
							nextNode = nextNode.next
						else:
							return nextNode
					else:
						return nextNode

	def search_node(self, data):
		'根据给定的元素查找某个值'
		tempX = self.wholeLevel - 1
		res = 0

		while tempX >= 0:
			if res == 0:
				res = self.find_range(tempX, data)
			else:
				res = self.find_range(tempX, data, res.child)

			print 'search res:',res,
			if res != 0:
				print res.data
				if self.skipArr[tempX] != 0:
					if data == res.data:
						print 'I find it', res.data, res.level
						break;
					elif tempX == 0:
						print 'counld not'
					
			elif tempX == 0:
				print 'counld not'


			print
			tempX = tempX - 1



	def del_node(self):
		pass

	def print_node(self):
		print ''
		for x in xrange(0, self.wholeLevel):
			print x, ':',
			node = self.skipArr[x]
			
			while node:
				print node.data,
				node = node.next

			print ''
		
sk = skipList(3, 0.5)

dataSet = [7,21,14,-1,37,32,85,71,117]
dataSet = [23,43,34,50,66,59,14,72]
for x in dataSet:
	sk.insert_node(x)

sk.print_node()

print 
sk.search_node(59)

