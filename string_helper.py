def exclude(s, t):
	res = ""
	for (i, c) in enumerate(s):
		suff = s[i:]
		if suff == t:
			return res
		res = res + c
	return res

def contains(s, t):
	return t in s