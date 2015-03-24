#coding=utf-8
from math import log

'''auth HeYecheng  fshyhyc@gmail.com
   2015 - 03 -16
   本算法是 CART ，决策树算法。 参考 C4.5 改造而成
   由于 CART 分类方法是构建 二叉树，不像 c45 可以构建 N叉树，所以所有的属性集分为两类，
   若某一列是连续数值型，则分为小于某一个数和大于某一个数两个集合。
   CART 决策树算法容易出现过度拟合情况，所以需要剪枝。
'''

trainTree = None # 表示训练得出的树
speNumericAttr = None  # 表示哪一列是连续型数值

class Node:
	'''Represents a decision tree node.'''
	def __init__(self, parent = None, dataset = None):
		self.dataset = dataset # 落在该结点的训练实例集
		self.result = None # 结果类标签
		self.attr = None # 该结点的分裂属性ID
		self.childs = {} # 该结点的子树列表，key-value pair: (属性attr的值, 对应的子树)
		self.parent = parent # 该结点的父亲结点
		self.split = None # 分裂点的属性

'''根据特征A的值把数据集D分裂为多个子集, A为目标属性在元组中的索引，根据分类标签构建一个树集合
	当 attrName 有值时，表示此数据集根据 某一属性 分为两类'''
def devide_set(D, A, attType = None, attrName = None):
	if (not isinstance(D, (set, list))):
		return None
	if (not type(A) is int):
		return None
	subset = {}

	if attType == None:
		for t in D:
			subset.setdefault(t[A], []).append(t)  # setdefault('key', value)  # 键key存在，则添加到集合里
	elif attType == 'multi':
		for t in D:
			if t[A] == attrName:
				subset.setdefault(t[A], []).append(t)  # setdefault('key', value)  # 键key存在，则添加到集合里
			else:
				subset.setdefault('other', []).append(t)  # setdefault('key', value)  # 键key存在，则添加到集合里
	elif attType == 'numberic':
		for t in D:
			if t[A] <= attrName:
				subset.setdefault(t[A], []).append(t)  # setdefault('key', value)  # 键key存在，则添加到集合里
			else:
				subset.setdefault('other', []).append(t)  # setdefault('key', value)  # 键key存在，则添加到集合里

	# for x in subset:
	# 	print x,subset[x]
	return subset

def cal_gini(attrClassCount):
	gini = 1.0 
	allNum = 0
	for i in attrClassCount:
		allNum = allNum + i

	for i in attrClassCount:
		temp = float(i) / allNum
		if temp != 0.0:
			gini = gini - temp * temp

	return gini

'attType 表示该属性的类型，normal 表示该属性只有 2 个分类，multi 表示该属性不止 2 个分类，numberic 表示该熟悉是数值型。'
def get_gini(D, A, attType, curAttr = None, T = -1):
	C = {} # 类别计数字典
	DA = {} # 特征 A 的取值计数字典
	CDA = {} # 类别和特征A的不同组合的取值计数字典

	if attType == 'normal':
		for t in D:
			C[t[T]] = C.get(t[T], 0) + 1
			DA[t[A]] = DA.get(t[A], 0) + 1   # dict.get(key, default=None) 表示查询字典里是否存在此 key 的 value值，若存在返回，否则赋值
			CDA[(t[T], t[A])] = CDA.get((t[T], t[A]), 0) + 1
	elif attType == 'multi':
		for t in D:
			C[t[T]] = C.get(t[T], 0) + 1
			if curAttr == t[A]:
				DA[t[A]] = DA.get(t[A], 0) + 1   # dict.get(key, default=None) 表示查询字典里是否存在此 key 的 value值，若存在返回，否则赋值
				CDA[(t[T], t[A])] = CDA.get((t[T], t[A]), 0) + 1
			else:
				DA['other'] = DA.get('other', 0) + 1  
				CDA[(t[T], 'other')] = CDA.get((t[T], 'other'), 0) + 1
	elif attType == 'numberic':
		for t in D:
			C[t[T]] = C.get(t[T], 0) + 1
			if curAttr >= t[A]:
				DA[curAttr] = DA.get(curAttr, 0) + 1   # dict.get(key, default=None) 表示查询字典里是否存在此 key 的 value值，若存在返回，否则赋值
				CDA[(t[T], curAttr)] = CDA.get((t[T], curAttr), 0) + 1
			else:
				DA['other'] = DA.get('other', 0) + 1  
				CDA[(t[T], 'other')] = CDA.get((t[T], 'other'), 0) + 1

	gini_D = cal_gini(C.values())

	PCDA = {} # 特征 A 的每个取值给定的条件下各个类别的概率（条件概率）
	for key, value in CDA.items():
		a = key[1] # 特征A
		pca = float(value) / DA[a]
		PCDA.setdefault(a, []).append(pca)

	# print PCDA
	condition_gini = 0.0
	for a, v in DA.items():
		p = float(v) / len(D)
		e = cal_gini(PCDA[a])
		condition_gini += e * p

	return gini_D - condition_gini

'D 表示数据集， A表示正在计算第几列'
def CART(D, A, threshold = 0.0001, T = -1, Tree = None):
	if Tree == None:
	    Tree = Node(None, D)

	subset = devide_set(D, T)

	if len(subset) <= 1:
		# 如果只有一个分类，就没有必要进行计算了
		for key in subset.keys():
			Tree.result = key
		del(subset)
		return Tree
	else:
		curGini = 0
		maxGini = 0
		classfyFlag = ''
		attr_id = 0

		for a in A:
			subset = devide_set(D, a)
			if len(subset) < 3:
				curGini = get_gini(D, a, 'normal') 
				if curGini > maxGini:
					maxGini = curGini
					classfyFlag = subset.keys()[0]
					attr_id = a
				# print curGini
			else:
				if a in speNumericAttr:
					for x in subset:
						curGini = get_gini(D, a, 'numberic', x)
						if curGini > maxGini:
							maxGini = curGini
							classfyFlag = x
							attr_id = a
						# print x,curGini
				else:
					for x in subset:
						curGini = get_gini(D, a, 'multi', x)
						if curGini > maxGini:
							maxGini = curGini
							classfyFlag = x
							attr_id = a
						# print x,curGini

		# print maxGini , classfyFlag
		if attr_id in speNumericAttr:
			subD = devide_set(D, attr_id, 'numberic', classfyFlag)
		else:
			subD = devide_set(D, attr_id, 'multi', classfyFlag)

		del(D[:]) # 删除中间数据,释放内存
		Tree.attr = attr_id
		Tree.split = classfyFlag
		Tree.dataset = None
		A.discard(attr_id) # 从特征集中排查已经使用过的特征

		for key in subD.keys():
			# print key,'::', subD.get(key)
			tree = Node(Tree, subD.get(key))
			Tree.childs[key] = tree
			CART(subD.get(key), A, threshold, T, tree)

		return Tree

def classify(Tree, instance):
	if (None == Tree):
		return None
	if (None != Tree.result):
		return Tree.result

	hopeAttr = instance[Tree.attr]
	# print Tree.split
	if Tree.attr in speNumericAttr:
		# 表示该熟悉是数值型。
		if hopeAttr <= Tree.split:
			return classify(Tree.childs[Tree.split], instance)
		else:
			return classify(Tree.childs['other'], instance)
	else:
		if hopeAttr == Tree.split:
			return classify(Tree.childs[hopeAttr], instance)
		else:
			return classify(Tree.childs['other'], instance)

def train_data(dataSet, numericAttrSet):
	global speNumericAttr, trainTree
	speNumericAttr = numericAttrSet

	trainTree = CART(dataset, set(range(0, len(dataset[0]) - 1)))

def get_classify(testSet):
	for singleTest in testSet:
		print classify(trainTree, singleTest)



dataset = [
('yes', 'single', 125, 'no'),
('no', 'married', 100, 'no'),
('no', 'single', 70, 'no'),
('yes', 'married', 120, 'no'),
('no', 'divorced', 95, 'yes'),
('no', 'married', 60, 'no'),
('yes', 'divorced', 220, 'no'),
('no', 'single', 85, 'yes'),
('no', 'married', 75, 'no'),
('no', 'single', 90, 'yes')
]

numericAttrSet = [2]

train_data(dataset, numericAttrSet)
get_classify([('no', 'divorced', 751), ('no', 'divorced', 51)])