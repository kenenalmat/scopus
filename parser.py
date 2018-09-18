from sel import get
import json, time
import collections


start_time = time.time()

queries = open("queries.txt", "r")

cnt = 10
idx = 1
ar = []


def process(q):
	identifier = ""
	query = ""
	ok = False
	for c in q:
		if c == ',' and ok == False:
			ok = True
			continue
		if ok:
			query = query + c
		else:
			identifier = identifier + c
	return (identifier, query)

def get_numb(identifier):
	info = identifier.split('_')
	numb = info[1]
	return numb

for q in queries:

	(identifier, q) = process(q.strip())
	row_number = get_numb(identifier)
	res = get(q.strip(), row_number)
	ordered_res = collections.OrderedDict(sorted(res.items()))
	res = ordered_res
	
	query_number = res["query_number"]
	query = res["aquery"]
	author_keywords = res.get("author_keywords")
	paper_refs = res["paper_refs"]
	total_refs = res.get("total_refs")
	status = res["status"]
	res["identifier"] = identifier

	if status == "OK":
		with open("res.json", "a") as f:
			f.write(json.dumps(res))
			f.write("\n")
		print (json.dumps(res, indent=4))
	else:
		print ("!!!")
		print (q)
		print ("!!!")
		with open("not_processed.txt", "a") as f:
			f.write(q)
	idx += 1


print ("FINISHED. Excution took {} hours.".format(str(1.0 * (time.time() - start_time) / 3600)))