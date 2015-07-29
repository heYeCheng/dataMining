#-*- coding: utf-8 -*-
import codecs
from math import sqrt

'''auth HeYecheng  fshyhyc@gmail.com
   2015 - 03 -16
    pearson距离, 如果数据相关性较好，使用该算法
    相关性分析只能说明二者具有共同变化关系，一个变大，另一个也变大或变小，但是具体二者是什么样的精确关系并不知道，例如A和B正相关，我们只知道A得分越高，
    B得分也越高，但我们并不了解当A=某个得分时，B的得分是多少，也就是A和B没有建立精确的方程或函数。回归分析就是要建立相关变量之间的精确关系，
    就是方程或模型，这样就能知道二者的关系了，例如可以用A来精确预测B。
'''

#pearson 距离 
def pearson(rate1,rate2):
	sum_xy = 0
	sum_x=0
	sum_y=0
	sum_x2=0
	sum_y2=0
	n=0 
	for key in rate1:
		if key in rate2:
			n+=1
			x=rate1[key]
			y=rate2[key]
			sum_xy += x*y
			sum_x +=x
			sum_y +=y
			sum_x2 +=x*x
			sum_y2 +=y*y
	#计算距离
	if n==0:
		return 0
	else:
		sx=sqrt(sum_x2-(pow(sum_x,2)/n))
		sy=sqrt(sum_y2-(pow(sum_y,2)/n))
		if sx<>0 and sy<>0:
			denominator=(sum_xy-sum_x*sum_y/n)/sx/sy
		else:
			denominator=0
	# print denominator
	return denominator

#返回最近距离用户
def computeNearestNeighbor(username,users):
	distances = []
	for key in users:
		if key<>username:   # <> 表示不等于
			distance = pearson(users[username],users[key])
			distances.append((distance,key))
	distances.sort()
	return distances

#推荐
def recommend(username,users):
	#获得最近用户的name
	nearest = computeNearestNeighbor(username,users)[0][1]
	recommendations =[]
	#得到最近用户的推荐列表
	neighborRatings = users[nearest]
	for key in neighborRatings:
		if not key in users[username]:
			recommendations.append((key,neighborRatings[key]))
	
	recommendations.sort(key=lambda rat:rat[1], reverse=False)  # 排序输出
	return recommendations

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        } 
     
if __name__ == '__main__':
	print computeNearestNeighbor('Hailey',users)
	print recommend('Hailey', users)
	