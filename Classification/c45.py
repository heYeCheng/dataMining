#coding=utf-8
from math import log

# http://shiyanjun.cn/archives/428.html
# http://blog.sciencenet.cn/blog-261330-593036.html

log2 = lambda x:log(x)/log(2) # an anonymous function

class Node:
	'''Represents a decision tree node.

	'''
	def __init__(self, parent = None, dataset = None):
		self.dataset = dataset # 落在该结点的训练实例集
		self.result = None # 结果类标签
		self.attr = None # 该结点的分裂属性ID
		self.childs = {} # 该结点的子树列表，key-value pair: (属性attr的值, 对应的子树)
		self.parent = parent # 该结点的父亲结点

# int *attrClassCount 这是一个按照某一个类别分类的元素统计
def entropy(attrClassCount): 
	# 计算 信息熵  Info(D) = -9/14 * log2(9/14) - 5/14 * log2(5/14) = 0.940
	iEntropy = 0.0 
	allNum = 0
	for i in attrClassCount:
		allNum = allNum + i

	for i in attrClassCount:
		temp = (i * 1.0) / allNum
		if temp != 0.0:
			iEntropy = iEntropy - temp * log2(temp)

	return iEntropy

# int classNum, vector<int *> attriCount, double pEntropy
def info_gain(D, A, T = -1):
	# 计算 信息增益值
	'''特征A对训练数据集D的信息增益 g(D,A)
	g(D,A)=entropy(D) - entropy(D|A)  假设数据集 D 的每个元组的最后一个特征为类标签
	T为目标属性的ID，-1表示元组的最后一个元素为目标'''
	if (not isinstance(D, (set, list))):  # 判断实例是否是这个类或者object是变量  
		return None
	if (not type(A) is int):
		return None

	C = {} # 类别计数字典
	DA = {} # 特征 A 的取值计数字典
	CDA = {} # 类别和特征A的不同组合的取值计数字典
	for t in D:
		C[t[T]] = C.get(t[T], 0) + 1
		DA[t[A]] = DA.get(t[A], 0) + 1   # dict.get(key, default=None) 表示查询字典里是否存在此 key 的 value值，若存在返回，否则赋值
		CDA[(t[T], t[A])] = CDA.get((t[T], t[A]), 0) + 1
	
	entropy_D = entropy(C.values())

	PCDA = {} # 特征 A 的每个取值给定的条件下各个类别的概率（条件概率）
	for key, value in CDA.items():
		a = key[1] # 特征A
		pca = value*1.0 / DA[a]
		PCDA.setdefault(a, []).append(pca)

	condition_entropy = 0.0
	for a, v in DA.items():
		p = v*1.0 / len(D)
		e = entropy(PCDA[a])
		condition_entropy += e * p

	return (entropy_D - condition_entropy) / entropy_D

def devide_set(D, A):
	'''根据特征A的值把数据集D分裂为多个子集, A为目标属性在元组中的索引，根据分类标签构建一个树集合'''
	if (not isinstance(D, (set, list))):
		return None
	if (not type(A) is int):
		return None
	subset = {}

	for t in D:
		# setdefault('key', value)  # 键key存在，则添加到集合里
		subset.setdefault(t[A], []).append(t)

	return subset

def build_tree(D, A, threshold = 0.0001, T = -1, Tree = None):
	'''根据数据集D和特征集A构建决策树.
	T为目标属性在元组中的索引 . 目前支持C4.5算法'''
	if (Tree != None and not isinstance(Tree, Node)):
	    return None
	if (not isinstance(D, (set, list))):
	    return None
	if (not type(A) is set):
	    return None

	if (None == Tree):
	    Tree = Node(None, D)

	subset = devide_set(D, T)

	if len(subset) <= 1:
		# 如果只有一个分类，就没有必要进行计算了
		for key in subset.keys():
			Tree.result = key
		del(subset)
		return Tree

	if len(A) <= 0:
		# 如果训练集只有一个记录，就不需要继续运算了
		Tree.result = get_result(D)
		return Tree

	max_gain = 0.0

	for a in A:
		# 表示第几个特征集列， a 为 int
		gain = info_gain(D, a)
		if (gain > max_gain):
		    max_gain = gain
		    attr_id = a # 获取信息增益最大的特征

	if max_gain < threshold:
	    Tree.result = get_result(D)
	    return Tree
	Tree.attr = attr_id
	subD = devide_set(D, attr_id)
	del(D[:]) # 删除中间数据,释放内存
	Tree.dataset = None
	A.discard(attr_id) # 从特征集中排查已经使用过的特征
	for key in subD.keys():
	    tree = Node(Tree, subD.get(key))
	    Tree.childs[key] = tree
	    build_tree(subD.get(key), A, threshold, T, tree)
	return Tree

def classify(Tree, instance):
	if (None == Tree):
		return None
	if (None != Tree.result):
		return Tree.result
	return classify(Tree.childs[instance[Tree.attr]], instance)

def print_brance(brance, target):
	odd = 0 
	for e in brance:
		if odd == 0:
			end = '='
		else:
			end = '=^'
		print e, end
		odd = 1 - odd
	print "target =", target

def print_tree(Tree, stack = []): 
	if (None == Tree):
		return
	if (None != Tree.result):
		print_brance(stack, Tree.result)
		return
	stack.append(Tree.attr)
	for key, value in Tree.childs.items():
		stack.append(key)
		print_tree(value, stack)
		stack.pop()
	stack.pop()

# dataset = [
#    ("青年", "否", "否", "一般", "否")
#    ,("青年", "否", "否", "好", "否")
#    ,("青年", "是", "否", "好", "是")
#    ,("青年", "是", "是", "一般", "是")
#    ,("青年", "否", "否", "一般", "否")
#    ,("中年", "否", "否", "一般", "否")
#    ,("中年", "否", "否", "好", "否")
#    ,("中年", "是", "是", "好", "是")
#    ,("中年", "否", "是", "非常好", "是")
#    ,("中年", "否", "是", "非常好", "是")
#    ,("老年", "否", "是", "非常好", "是")
#    ,("老年", "否", "是", "好", "是")
#    ,("老年", "是", "否", "好", "是")
#    ,("老年", "是", "否", "非常好", "是")
#    ,("老年", "否", "否", "一般", "否")
# ]

# T = build_tree(dataset, set(range(0, len(dataset[0]) - 1)))
# # print_tree(T)
# print classify(T, ("老年", "否", "否", "一般"))