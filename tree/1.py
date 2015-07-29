# [3, 8, 15, 32, 4, 11, 21, 2, 4, 34, 6, 13, 25, 16, 30, 1, 17,\
#           18, 24, 9, 22, 23, 5, 7, 19, 20, 39, 26, 31, 30]:


#                                                                   [21]
#                             [8, 15] [25] 
#                             [4, 6] [11] [17, 19] [23] [30, 32] 
# [1, 2, 3]->[4, 5]->[6, 7]->[8, 9]->[11, 13]->[15, 16]->[17, 18]->[19, 20]->[21, 22]->[23, 24]->[25, 26]->[30, 31]->[32, 34, 39]

#coding=utf-8
# from bisect import bisect_left, bisect_right




def space_increase(i):
	if (i % 2) == 1:
		return i * i * (-1)
	else:
		return i * i
	


increment = [(i, space_increase(i)) for i in range(5)]
print increment

res = min(increment, key = lambda x:x[1])

print res