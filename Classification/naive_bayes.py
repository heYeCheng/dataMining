#coding=utf-8
from math import log

'''auth HeYecheng  fshyhyc@gmail.com
   2015 - 03 -14
   本算法是朴素贝叶斯
   参考 http://blog.csdn.net/cyningsun/article/details/8765536
'''

log2 = lambda x:log(x)/log(2) # an anonymous function

classPro = ''
probArr = []

'''计算一共有多少个 class 的分类，并且计算每个类别的概率，如 P{y=yes}，P{y=no}
	classSet 表示分类结果集合   index  表示元组的最后一个元素为目标'''
def cal_class(classSet, index = -1):
	global classPro
	C = {}
	for t in classSet:
		C[t[index]] = C.get(t[index], 0) + 1
	
	allNum = len(classSet)
	classPro = {}
	for t in C:
		classPro[t] = (C[t], C[t] / float(allNum) )  # [0] 是统计数量  [1] 是统计概律

	return classPro

'''计算一共有多少个 class 的分类，并且计算每个类别的概率，如 P{y=yes}，P{y=no}
	classSet 表示分类结果集合   atI = attrIndex 表示要计算哪一列的属性值'''
def cal_attr_class(D, atI, index = -1):
	CDA = {} # 类别和特征A的不同组合的取值计数字典
	for t in D:
		CDA[(t[index], t[atI])] = CDA.get((t[index], t[atI]), 0) + 1

	PCDA = {} # 特征 A 的每个取值给定的条件下各个类别的概率（条件概率）
	for key, value in CDA.items():
		# print key
		a = '%s|%s' % (key[1], key[0]) # 特征A
		pca = float(value) / classPro[key[0]][0]
		# print pca
		PCDA.setdefault(a, []).append(pca)

	# print PCDA
	return PCDA

''' log P( X|Ci ) = log P( Ci ) + Σ log P( Xk|Ci ) 将求积转为求和解决溢出问题（由于多个小数相乘会容易导致结果为 0 ）
	当在数据中找不到 像 P(是否有房=yes | 拖欠贷款=yes) = 0，此时使用 laplace 平滑定理，即假定了统一先验概率。事实上，分子加1和分母*2（分母是该分类的数量） 
	背后的基本原理是这样的：在执行实际的试验之前，我们假设已经有 N*2 次试验，只有一次成功和其它都失败'''
def classify(testSet):
	# sg 是 single 的简拼
	for sgSet in testSet:
		maxRes = -10000     # 最大概率值
		finalFlag = '' # 最后结果
		for sgClPro in classPro:
			tempRes = log(classPro[sgClPro][1])  # [0] 表示统计的数量， [1] 表示该分类下的概率
			for xIndex in xrange(0, len(sgSet)):
				if '%s|%s' % (sgSet[xIndex], sgClPro) in probArr[xIndex]:
					curPro = probArr[xIndex]['%s|%s' % (sgSet[xIndex], sgClPro)][0]
				else:		
					curPro = (0 + 1)/float(2 * classPro[sgClPro][0])  # 注释
				
				tempRes = tempRes + log(curPro)

			if maxRes < tempRes:
				maxRes = tempRes
				finalFlag = sgClPro

		print finalFlag

def train_data(dataSet):
	global probArr
	print cal_class(dataSet)

	for x in xrange(0, (len(dataSet[0]) - 1)):
		probArr.append(cal_attr_class(dataSet, x))
	
	# print probArr
	
dataset = [
   ("青年", "否", "否", "一般", "否")
   ,("青年", "否", "否", "好", "否")
   ,("青年", "是", "否", "好", "是")
   ,("青年", "是", "是", "一般", "是")
   ,("青年", "否", "否", "一般", "否")
   ,("中年", "否", "否", "一般", "否")
   ,("中年", "否", "否", "好", "否")
   ,("中年", "是", "是", "好", "是")
   ,("中年", "否", "是", "非常好", "是")
   ,("中年", "否", "是", "非常好", "是")
   ,("老年", "否", "是", "非常好", "是")
   ,("老年", "否", "是", "好", "是")
   ,("老年", "是", "否", "好", "是")
   ,("老年", "是", "否", "非常好", "是")
   ,("老年", "否", "否", "一般", "否")
]
testSet = [("老年", "否", "是", "一般"),("老年", "否", "否", "一般"),("青年", "否", "否", "好")]


train_data(dataset)
classify(testSet)