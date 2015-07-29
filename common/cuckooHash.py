import random

#setting the hashtable size and a large prime p, cardinality of universe cannot exceed that prime
m = 8192 
p = 15486347
#initializing the hashtable
hashtable = [None]*m

#creating a list of parameters for at most 3 hash functions
params = [(random.randint(0,p-1), random.randint(1,p-1)), (random.randint(0,p-1), random.randint(1,p-1)),\
(random.randint(0,p-1), random.randint(1,p-1))]

#the hash funtions
def hashfunc(x, i, params):
	return ((params[i][0]*x + params[i][1]) % p) % m


def cuckoo(key):	
	counter = 0
	#checks if can hash key with any of the three hash functions
	#if key is hashed, it returns
	for i in range(3):
		if hashtable[hashfunc(key, i, params)] == None:
 			hashtable[hashfunc(key, i, params)] = key 
			return True
		elif hashtable[hashfunc(key, i, params)] == key :
			return True
	#choose a random hash function
	rh = random.randrange(3)
	#store the position where it hashes key
	pos = hashfunc(key, rh, params)	
	while 1:
		#break the infinite loop when 20 colisions
		if counter > 20:
			return False 
		counter += 1
		#tries to hash the key
		if hashtable[pos] == None:
			hashtable[pos] = key
			return True
		#hash the key and take the evicted item as a new key
		hashtable[pos], key = key, hashtable[pos]
		#checks for alternative options to hash the new key
		if hashfunc(key, 0, params) == pos:
			if hashfunc(key, 1, params) == pos:
				pos = hashfunc(key, 2, params)
			else:
				pos = hashfunc(key, 1, params)
		else:
			pos = hashfunc(key, 0, params)
		#rehash?
	
s = 0.0
n = 1000
for i in range(n):
	while 1:
		a = random.randrange(200000)
		if not cuckoo(a):
			break
#print "load:", 100.0*(1.0-1.0*hashtable.count(-1)/m)
	s += (100.0*(1.0 - 1.0*hashtable.count(None)/m))
print s/n