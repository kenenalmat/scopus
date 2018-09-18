import json

content = ""

with open("res1.json", "r") as f:
	content = f.read()

d = json.loads(content)

result = d["result"]

np = 0
p1 = 0
ok = 0
tr = 0

for ind, r in enumerate(result):
	
	query_number = r["query_number"]
	query = r["aquery"]
	author_keywords = r.get("author_keywords")
	paper_refs = r["paper_refs"]
	total_refs = r.get("total_refs")
	status = r["status"]

	if status == "Not processed":
		np += 1
		with open("not_processed.log", "a") as f:
			f.write(query)
			f.write("\n")
	elif status == "Problem 1: Scopus could not find any document with that query.":
		p1 += 1
		with open("not_found.log", "a") as f:
			f.write(query)
			f.write("\n")
	elif status == "OK":
		ok += 1


print ("OK: {}".format(ok))
print ("Not processed: {}".format(np))
print ("Could not find: {}".format(p1))
