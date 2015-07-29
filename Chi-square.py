#coding=utf-8
# http://baike.baidu.com/link?url=YMAzP4r13QVaBvcE4vDbJcXPE54OvzddDYTplXc8hVQfFy-3S70ak-5PgC7gkoVcSIFMTUGjbTIbCc206cNtJq
# http://www.cnblogs.com/zhangchaoyang/articles/2642032.html
import math
'''
Pearson χ2 计算  χ2 = Σ ((Ai- nPi)2 / nPi)  (i=1，2，3，…，k)    Ei为i水平的期望频数，n为总频数，pi为i水平的期望频率 , Ei = nPi
四格表资料卡方检验的卡方值计算  (ad - bc)2 * n / (a+b)(c+d)(a+c)(b+d)
自由度v = (行数-1)(列数-1) 
参考 http://wiki.mbalib.com/zh-cn/卡方检验#

# 统一性检验
　　检验两个或两个以上总体的某一特性分布，也就是各“类别”的比例是否统一或相近，
一般称为卡方统一性检验或者卡方同质性检验。下面一例便是利用卡方统一性检验的例子。 
H0：南京和北京居民对最低生活保障满意程度的比例相同。 

独立性检验

　　卡方独立性检验是用来检验两个属性间是否独立。一个变量作为行，另一个变量作为列。下面一例便是介绍卡方独立性检验的方法。 
H0：性别与收入无关。 



适合度检验

　　实际执行多项式试验而得到的观察次数，与虚无假设的期望次数相比较，称为卡方适度检验，即在于检验二者接近的程度，利用样本
数据以检验总体分布是否为某一特定分布的统计方法。这里以掷骰子为例介绍适度检验的方法。 

H0：观察分布等于期望分布。 
'''
kaFan = [(6.63, 9.21, 11.34, 13.28, 15.09, 16.81, 18.48, 20.09, 21.67, 23.21),
         (3.84, 5.99, 7.81, 9.49, 11.07, 12.59, 14.07, 15.51, 16.92, 18.31),
         (2.71, 4.61, 6.25, 7.78, 9.24, 10.64, 12.02, 13.36, 14.68, 15.99)]


pps = [(5,0,0,2,0), (0,3,3,0,2)]
dataSet = [(100, 110), (150,160), (180, 170), (170, 160)]
dataSet = [(30567, 33651), (2976, 3698)]
sumRow = []
sumCol = ''
totalNum = 0

def cal_row(dataSet):
	'计算每一行的和'
	global sumRow
	for singleRow in dataSet:
		sumRow.append(reduce(lambda x, y: x + y, singleRow))
	print sumRow

def cal_col(dataSet):
	'计算每一列的和'
	global sumCol, totalNum
	tempCol = [0] * len(dataSet[0])
	for singleRow in dataSet:
		for x in xrange(0, len(singleRow)):
			tempCol[x] += singleRow[x]

	sumCol = tempCol
	totalNum = reduce(lambda x, y: x + y, sumCol)
	print sumCol, totalNum


def cal_kafan(dataSet):
	'计算卡方'
	expSet = [[0] * len(dataSet[0])] * len(dataSet)  # 表示实际期望值
	gapSet = [[0] * len(dataSet[0])] * len(dataSet)  # 表示标准差数据
	rowGapSet = [0] * len(dataSet)   # 表示每一行的标准差数据

	for i in xrange(0, len(dataSet)):
		for j in xrange(0, len(dataSet[0])):
			expSet[i][j] = float(sumRow[i] * sumCol[j]) / totalNum  # 先计算该值的期望数
			gapSet[i][j] = math.pow((dataSet[i][j] - expSet[i][j]), 2) / expSet[i][j]  # 计算该值与期望之间的差距
			rowGapSet[i] += gapSet[i][j]

	print rowGapSet
	kaFan = reduce(lambda x, y: x + y, rowGapSet)
	print kaFan
	return kaFan

def cal_dF(dataSet):
	'dF = degrees  of freedom， 计算自由度   v = (行数-1)(列数-1) '
	v = (len(dataSet[0]) - 1) * (len(dataSet) - 1) 
	return v

def get_chi(creditArea, dFv):
	'creditArea 表示置信水平， 本函数用于查 卡方分布 表'
	n = int(creditArea / 0.05)
	
	chi = kaFan[n][dFv - 1]

	return chi

def main(dataSet, creditArea):
	cal_row(dataSet)
	cal_col(dataSet)
	cal_kafan(dataSet)
	dFv = cal_dF(dataSet)
	print get_chi(creditArea, dFv)

main(dataSet, 0.05)