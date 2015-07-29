#!/usr/bin/python
# coding=utf-8

'''auth HeYecheng  fshyhyc@gmail.com
   2015 - 04 -15
   本算法是 Detecting Near-Duplicates for Web Crawling 算法，用于查找海明距离相差为 3 的文章
   核心思想： 首先建立索引，
   		1、将64位的二进制串等分成四块
		2、调整上述64位二进制，将任意一块作为前16位，总共有四种组合，生成四份table
		3、采用精确匹配的方式查找前16位
		4、如果样本库中存有2^34（差不多10亿）的哈希指纹，则每个table返回2^(34-16)=262144个候选结果，大大减少了海明距离的计算成本 
   # http://blog.163.com/jackylau_v/blog/static/17575404020118312853830/
   # http://www.codesky.net/article/201003/122890.html
'''

class leave(object):
	"""这个是链表，用于存放 具有相同 hash 值的 simhash code"""
	def __init__(self, sgLeave):
		self.leaves = []
		self.leaves.append(sgLeave)


class duplicates_table(object):
	"""本索引使用 hash 字典序列， 也可以使用顺序表作为索引列"""
	# totalNum = 1 << 15
	totalNum = 1 << 4

	def __init__(self, dataSet, start = 0, stop = 16):
		self.dataSet = dataSet
		self.DT = {}  # hash 索引列
		self.start = start  # 字符串起始截至位
		self.stop = stop	#字符串终止截至位

	def make_index(self):
		for x in self.dataSet:
			x = str(x)[self.start : self.stop]
			curHash = int(str(x), 2)
			# print curHash
			biasIdx = curHash % self.totalNum
			if self.DT.has_key(biasIdx):
				curLeave = self.DT.get(biasIdx).leaves
				curLeave.append(x)
			else:
				curLeave = leave(x)
				self.DT.setdefault(biasIdx, curLeave)

	def find_relative(self, fingerprint):
		curHash = int(str(fingerprint), 2)
		biasIdx = curHash % self.totalNum

		if self.DT.has_key(biasIdx):
			curLeave = self.DT.get(biasIdx).leaves
			print curLeave
			for tempFingerprint in curLeave:
				res = hamming_distance(fingerprint, tempFingerprint)
				if res:
					print tempFingerprint
		else:
			print 'no'

def format_hash(temp):
	'''格式化字符串，将 十进制 变为 二进制输出'''
	temp = bin(int(temp))
	temp = temp[2:]
	print temp
	return temp

def replenish_int(temp, outLen = 64):
	'''将二进制 的长度补充为 固定长度，就是通过添加 0 , outLen 要求输出的二进制长度'''
	if len(temp) < outLen:
		temp = '0' * (outLen - len(temp)) + temp

	print temp
	return temp


def hamming_distance(s1, s2, hamming_distance = 3):
	"""Return the Hamming distance between equal-length sequences"""
	s1 = str(s1)
	s2 = str(s1)

	if len(s1) != len(s2):
		s1 = replenish_int(s1, 6)
		s2 = replenish_int(s2, 6)
	dis = sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

	if dis <= hamming_distance:
		'表示海明距离在 3 以内'
		return True
	else:
		return False

print hamming_distance(110100, 000101)

# ds = [110101, 110101, 110100, 101, 110011, 1]
# dt = duplicates_table(ds)
# dt.make_index()
# for x in dt.DT:
# 	print x, dt.DT[x].leaves

# dt.find_relative(110101)


# a = 4424057391
# format_hash(a)
# a = 442405739123
# x = format_hash(a)
# print x


# dup_dict = {}
# print type(dup_dict)
# dup_dict.setdefault(a, 'sdf')
# print dup_dict