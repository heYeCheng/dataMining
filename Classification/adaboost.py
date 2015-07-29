#coding=utf-8
from numpy import *
from math import *

'''auth HeYecheng  fshyhyc@gmail.com
   2015 - 04 - 09
   本算法是 AdaBoost 算法，算法的核心思想是 三个臭皮匠胜过一个诸葛亮。 
   本算法的两个关键核心：
   1、 get_Data_by_weight  方法
   		从训练集中有目的地选取需要训练的样本数据，假如该样本数据经常被错误分类，则会提高被抽取的概率。 样本的抽取完全存在样本没有被抽取的可能性。
   2、 train_Data  方法
   		本方法可以调用其它分类方法，例如 决策树、贝叶斯分类、KNN 分类等，但必须返回对总体样本的分类结果以及分类方法
   3、 cal_mistake 、cal_weight  方法
   		计算每个分类器错误划分样本的数量以及计算其话事权
   4、 cal_final_classfy  方法
   		根据每个弱分类器的权值，对未知测试集合进行计算，对结果进行加权求和
'''


'''根据权重 Wt 的分布，通过对 D 进行有放回抽样产生训练集 Dt，重点训练被错误划分的数据'''
def get_Data_by_weight(D, W, t):
	if t == 1:
		D = [(1,1), (2,1), (3,1), (4,-1), (5,-1), (6,-1), (7, -1), (8,1), (9,1), (10, 1)]
	elif t == 2:
		D = [(1,1), (1,1), (2,1), (2,1), (2,1), (2,1), (3,1), (3,1), (3,1), (3,1)]
	elif t == 3:
		D = [(2,1), (2,1), (4,-1), (4,-1), (4,-1), (4,-1), (5,-1), (6,-1), (6,-1), (7, -1)]

	return D


'''训练样本集，并对原数据集进行分类，并返回分类结果'''
def train_Data(D, trainD, t):
	if t == 1:
		res = [-1, -1, -1, -1, -1, -1, -1, 1, 1, 1]
	elif t ==2:
		res = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	elif t ==3:
		res = [1, 1, 1, -1, -1, -1, -1, -1, -1, -1]

	return res

'''计算分类器 分类错误的次数'''
def cal_mistake(D, res, curW, lable = -1):
	curError = 0.0
	for i in xrange(0, len(D)):
		if D[i][lable] != res[i] :
			curError += curW[i]

	curError = float(curError) / len(D)

	return curError

'''计算此 弱分类器的权重'''
def cal_weight(D, res, curW, curA, lable = -1):
	temp = 0.0
	
	for i in xrange(0, len(D)):
		if D[i][lable] == res[i] :
			temp += curW[i] * exp(-1 * curA)
		else:
			temp += curW[i] * exp(curA)

	z = temp  # z 是正规因子，用于归一化参数

	tempW = []  # 用于存储本轮的权重
	for i in xrange(0, len(D)):
		if D[i][lable] == res[i] :
			tempW.append(curW[i] * exp(-1 * curA) / z)
		else:
			tempW.append(curW[i] * exp(curA) / z)

	return tempW


'''根据每个弱分类器的权值、 以及其分类结果，进行加权求和 得出最终预测结果'''
def cal_final_classfy(A_arr, res_arr):
	data_arr = [0] * len(res_arr[0])
	for x in xrange(0, len(A_arr)):
		for y in xrange(0, len(res_arr[0])):
			data_arr[y] += A_arr[x] * float(res_arr[x][y])

	print data_arr

"""docstring for AdaBoost
D 是样本数据集 ， T 是学习提升轮数，lable 表示分类结果所在属性列"""
def AdaBoost(D, T, lable = -1):
	lenthNum = len(D)  # 样本数量
	W = {}
	A_arr = []
	res_arr = []

	W[0] = [0] * lenthNum
	W[1] = [1.0 / lenthNum] * lenthNum

	for t in xrange(1, T + 1):
		curD = get_Data_by_weight(D, W, t)
		res = train_Data(D, curD, t)
		res_arr.append(res)
		curError = cal_mistake(D, res, W[t])
		# print 'reciece :',curError
		if curError > 0.5:
			print '必须重新计算'
		else:
			curA = 0.5 * log((1 - curError) / float(curError))  # 决定此 弱分类器的权重，相当于 权重因子
			A_arr.append(curA)
			W[t+1] = cal_weight(D, res, W[t], curA)

	cal_final_classfy(A_arr, res_arr)

	# print W
	# print A_arr
	# print res_arr


dataSet = [(1,1), (2,1), (3,1), (4,-1), (5,-1), (6,-1), (7, -1), (8,1), (9,1), (10, 1)]

AdaBoost(dataSet, 3)

# curError = 0.0038
# curA = 0.5 * log((1 - curError) / float(curError))
# print curA