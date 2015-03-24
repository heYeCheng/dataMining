#coding=utf-8
import numpy as np
# from numpy import *  
import operator 
import init_data
  
def createDataSet():  
	group = np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])  
	labels = ['A','A','B','B']  
	return group, labels  


def classify(inX, dataSet, labels, k):  
	dataSetSize = dataSet.shape[0]  
	diffMat = np.tile(inX, (dataSetSize,1)) - dataSet    # tile : Numpy扩充数组函数   a=array([10,20]) , tile(a,(3,2))  构造3X2个copy
	sqDiffMat = diffMat**2  
	sqDistances = sqDiffMat.sum(axis=1)  
	distances = sqDistances**0.5  
	sortedDistIndicies = distances.argsort()  
	classCount = {}  
	for i in range(k):  
		voteIlabel = labels[sortedDistIndicies[i]]  
		classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1 

	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)  
	return sortedClassCount[0][0]  

# group,labels = createDataSet()
group,labels, testSet = init_data.get_data()

for x in testSet:
	print classify(x, group, labels, 10)