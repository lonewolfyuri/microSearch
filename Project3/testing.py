from collections import defaultdict, OrderedDict

if __name__ == "__main__":
	vals = ['blah', 'blahtoo', 'blahthree']
	defdict = defaultdict(OrderedDict)
	for val in vals:
		if val not in defdict:
			print("not in")
