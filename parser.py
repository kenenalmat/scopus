import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import selenium.webdriver.chrome.service as service
from selenium.webdriver import DesiredCapabilities

from sel import get
import json, time
import collections


DESIRED_CAPABILITIES = DesiredCapabilities.PHANTOMJS.copy()
DESIRED_CAPABILITIES['authority'] = 'www.scopus.com'
DESIRED_CAPABILITIES['method'] = 'GET'
DESIRED_CAPABILITIES['path'] = '/search/form.uri?display=advanced&origin=searchbasic&txGid=d63aa1335f3f9f275d51e0bece833ce1'
DESIRED_CAPABILITIES['scheme'] = 'https'
DESIRED_CAPABILITIES['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
DESIRED_CAPABILITIES['accept-encoding'] = 'gzip, deflate, br'
DESIRED_CAPABILITIES['accept-language'] = 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
DESIRED_CAPABILITIES['cache-control'] = 'max-age=0'
DESIRED_CAPABILITIES['cookie'] = 'utt=bab22ab7ffe161e3ac8cc-62c5d69b3eff803a-9Ai; __cfduid=dd0bbd0a38d14c2fc62f2b6c8c026f4c51520428758; scopus.machineID=7CF51DB4463D0162656ABD06A0451BE0.wsnAw8kcdt7IPYLO0V48gA; homeAcc_cookie=0045004F006E00720071005500380073006E004A006B006C0046007800540051007A0039006B003500790047003100530032006B0036002F0068005500710063006300360061004D0042005A004D0041006C004900410062002B004800450063005800660044007600610077003D003D; optimizelyEndUserId=oeu1520493363085r0.17911425927077262; CARS_COOKIE=007000340062007A00410055007000630066007700460036002B00630070004100330077004F007000580043007100570032005A004900630043004A006A003900720053002B006500480039006F006A0079007500660069006A006D0077004E0051003300350049004C004100490070003600760051004D00500069006E00420061006E002F00610074004C004500520032004C00730062005700650053006400550037004A00590065007400440031007500420031007200440057004600370056006600370057002B00620073007400750069004500480048006D0075007900350034003800310067006C0032002B006B007600310076004F0071002B0056; _ga=GA1.2.1889307394.1521009526; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22search%22%7D; _pendo_accountId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A60090; _pendo_visitorId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A29924780; SCSessionID=DCCDB278CDF52A814B540BA513878183.wsnAw8kcdt7IPYLO0V48gA; AE_SESSION_COOKIE=1525250101772; __cfruid=3ea5558484310d0fe69b6c950016f07156cd87a7-1525250101; javaScript=true; _pk_ses.2316.d989=*; acw=c4049fdc69ccc445f569a680f72dde959bb4gxrqa%7C%24%7C140853D3BD6CA73EB8BDAA7BB325A518603ECF9FC8ECA3709FF8659AE2903E12A73D2258B8F7D179AA4EE598EF07897C8E13830C2BDF802F5B2791389D9DC89EE755B001AF5A0858787A139BC1C55061; xmlHttpRequest=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=1406116232%7CMCIDTS%7C17654%7CMCMID%7C07524392324548502004355208562042519364%7CMCAAMLH-1525854908%7C11%7CMCAAMB-1525854908%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1525257308s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17656%7CvVersion%7C2.5.0; s_cc=true; screenInfo=768:1366; _pendo_meta.7108b796-60e0-44bd-6a6b-7313c4a99c35=3141176879; optimizelyBuckets=%7B%2210338583043%22%3A%2210332894867%22%2C%2210520712389%22%3A%2210520021543%22%2C%2210678790238%22%3A%2210676600419%22%7D; _pk_id.2316.d989=a7b7bd8e21c2f4b4.1524816365.3.1525251393.1525250108.; optimizelyPendingLogEvents=%5B%5D; s_pers=%20v8%3D1525251394585%7C1619859394585%3B%20v8_s%3DLess%2520than%25207%2520days%7C1525253194585%3B%20c19%3Dsc%253Asearch%253Aadvanced%2520searchform%7C1525253194594%3B%20v68%3D1525251393251%7C1525253194628%3B; s_sq=%5B%5BB%5D%5D; s_sess=%20s_cpc%3D0%3B%20e41%3D1%3B%20s_ppvl%3Dsc%25253Asearch%25253Aadvanced%252520searchform%252C37%252C37%252C650%252C1299%252C650%252C1366%252C768%252C1%252CP%3B%20s_ppv%3Dsc%25253Asearch%25253Aadvanced%252520searchform%252C37%252C37%252C650%252C1299%252C223%252C1366%252C768%252C1%252CP%3B'
DESIRED_CAPABILITIES['referer'] = 'https://www.scopus.com/search/form.uri?display=basic'
DESIRED_CAPABILITIES['upgrade-insecure-requests'] = '1'
DESIRED_CAPABILITIES['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
DESIRED_CAPABILITIES['x-compress'] = 'null'
DESIRED_CAPABILITIES['loggingPrefs'] = {'browser':'ALL'}
#EXECUTABLE_PATH = "C:\\Users\\o.parsero\\Downloads\\SCOPUS_PROJECT\\chromedriver.exe"	
EXECUTABLE_PATH = "/usr/lib/chromium-browser/chromedriver"

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


driver = webdriver.Chrome(executable_path=EXECUTABLE_PATH, desired_capabilities=DESIRED_CAPABILITIES)

for q in queries:

	(identifier, q) = process(q.strip())
	row_number = get_numb(identifier)
	res = get(driver, q.strip(), row_number)
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
		# print (json.dumps(res, indent=4))
	else:
		print ("!!!")
		print (q)
		print ("!!!")
		with open("not_processed.txt", "a") as f:
			f.write(q)
	idx += 1


print ("FINISHED. Excution took {} hours.".format(str(1.0 * (time.time() - start_time) / 3600)))