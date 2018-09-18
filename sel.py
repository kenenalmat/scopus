from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium
import json, time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import selenium.webdriver.chrome.service as service
from selenium.webdriver import DesiredCapabilities


# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys

SCOPUS_URL = "https://www.scopus.com/search/form.uri?display=advanced&origin=searchbasic&txGid=d63aa1335f3f9f275d51e0bece833ce1"

desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
desired_capabilities['authority'] = 'www.scopus.com'
desired_capabilities['method'] = 'GET'
desired_capabilities['path'] = '/search/form.uri?display=advanced&origin=searchbasic&txGid=d63aa1335f3f9f275d51e0bece833ce1'
desired_capabilities['scheme'] = 'https'
desired_capabilities['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
desired_capabilities['accept-encoding'] = 'gzip, deflate, br'
desired_capabilities['accept-language'] = 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
desired_capabilities['cache-control'] = 'max-age=0'
desired_capabilities['cookie'] = 'utt=bab22ab7ffe161e3ac8cc-62c5d69b3eff803a-9Ai; __cfduid=dd0bbd0a38d14c2fc62f2b6c8c026f4c51520428758; scopus.machineID=7CF51DB4463D0162656ABD06A0451BE0.wsnAw8kcdt7IPYLO0V48gA; homeAcc_cookie=0045004F006E00720071005500380073006E004A006B006C0046007800540051007A0039006B003500790047003100530032006B0036002F0068005500710063006300360061004D0042005A004D0041006C004900410062002B004800450063005800660044007600610077003D003D; optimizelyEndUserId=oeu1520493363085r0.17911425927077262; CARS_COOKIE=007000340062007A00410055007000630066007700460036002B00630070004100330077004F007000580043007100570032005A004900630043004A006A003900720053002B006500480039006F006A0079007500660069006A006D0077004E0051003300350049004C004100490070003600760051004D00500069006E00420061006E002F00610074004C004500520032004C00730062005700650053006400550037004A00590065007400440031007500420031007200440057004600370056006600370057002B00620073007400750069004500480048006D0075007900350034003800310067006C0032002B006B007600310076004F0071002B0056; _ga=GA1.2.1889307394.1521009526; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22search%22%7D; _pendo_accountId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A60090; _pendo_visitorId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A29924780; SCSessionID=DCCDB278CDF52A814B540BA513878183.wsnAw8kcdt7IPYLO0V48gA; AE_SESSION_COOKIE=1525250101772; __cfruid=3ea5558484310d0fe69b6c950016f07156cd87a7-1525250101; javaScript=true; _pk_ses.2316.d989=*; acw=c4049fdc69ccc445f569a680f72dde959bb4gxrqa%7C%24%7C140853D3BD6CA73EB8BDAA7BB325A518603ECF9FC8ECA3709FF8659AE2903E12A73D2258B8F7D179AA4EE598EF07897C8E13830C2BDF802F5B2791389D9DC89EE755B001AF5A0858787A139BC1C55061; xmlHttpRequest=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=1406116232%7CMCIDTS%7C17654%7CMCMID%7C07524392324548502004355208562042519364%7CMCAAMLH-1525854908%7C11%7CMCAAMB-1525854908%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1525257308s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17656%7CvVersion%7C2.5.0; s_cc=true; screenInfo=768:1366; _pendo_meta.7108b796-60e0-44bd-6a6b-7313c4a99c35=3141176879; optimizelyBuckets=%7B%2210338583043%22%3A%2210332894867%22%2C%2210520712389%22%3A%2210520021543%22%2C%2210678790238%22%3A%2210676600419%22%7D; _pk_id.2316.d989=a7b7bd8e21c2f4b4.1524816365.3.1525251393.1525250108.; optimizelyPendingLogEvents=%5B%5D; s_pers=%20v8%3D1525251394585%7C1619859394585%3B%20v8_s%3DLess%2520than%25207%2520days%7C1525253194585%3B%20c19%3Dsc%253Asearch%253Aadvanced%2520searchform%7C1525253194594%3B%20v68%3D1525251393251%7C1525253194628%3B; s_sq=%5B%5BB%5D%5D; s_sess=%20s_cpc%3D0%3B%20e41%3D1%3B%20s_ppvl%3Dsc%25253Asearch%25253Aadvanced%252520searchform%252C37%252C37%252C650%252C1299%252C650%252C1366%252C768%252C1%252CP%3B%20s_ppv%3Dsc%25253Asearch%25253Aadvanced%252520searchform%252C37%252C37%252C650%252C1299%252C223%252C1366%252C768%252C1%252CP%3B'
desired_capabilities['referer'] = 'https://www.scopus.com/search/form.uri?display=basic'
desired_capabilities['upgrade-insecure-requests'] = '1'
desired_capabilities['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
desired_capabilities['x-compress'] = 'null'
desired_capabilities['loggingPrefs'] = {'browser':'ALL'}


LINK_XPATH = "//tr[@id='resultDataRow0']/td/a"
VIEW_IN_SEARCH_RESULTS_FORMAT = "//a[@id='referenceSrhResults']"
AUTHOR_KEYWORDS_XPATH = "//section[@id='authorKeywords']/span"
JOURNAL_TITLE_XPATH = "//div[@class=\"querySrchText marginTopHalf\"]"
TOTAL_STRING_XPATH = "//span[@class='text-nowrap ellipsisOverflow truncateTitle']"
TITLE_XPATH = ".//label[@class=\"checkbox-label\"]"
NUMBER_XPATH = ".//button/span/span[@class=\"btnText\"]"
VISIBLE_XPATH = "//ul[@id='cluster_EXACTSRCTITLE']/li[@class='checkbox']"
HIDDEN_XPATH = "//ul[@id='hidden_EXACTSRCTITLE']/li[@class='checkbox']"
VIEW_MORE_XPATH = "//a[@href=\"javascript:viewMoreClusters('resultslist','rec','EXACTSRCTITLE','selectedSourceClusterCategories','11');\"]"
LI_FIND_XPATH = "//div[@id=\"overlayBody_EXACTSRCTITLE\"]/ul/li"


def find_element(driver, xpath):
	start_time = time.time()
	elem = None
	while True:
		period = time.time() - start_time
		if period > 30:
			return elem
		try:
			elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
		except:
			pass

		if elem is not None:
			return elem

def find_elements(driver, xpath):
	start_time = time.time()
	elems = None
	while True:
		period = time.time() - start_time
		if period > 30:
			return elems

		try:
			elems = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
		except:
			pass
		if elems is not None:
			elems = driver.find_elements(By.XPATH, xpath)
			return elems


def get_author_keywords(driver):
	author_keywords = driver.find_elements(By.XPATH, AUTHOR_KEYWORDS_XPATH)
	if author_keywords is None:
		return (False, [])

	return (True, [span.text.strip() for span in author_keywords])

def get_total_refs(driver):
	total_refs = find_element(driver, TOTAL_STRING_XPATH)
	if total_refs is None:
		return (False, "0")
	
	return (True, total_refs.text.split()[0].strip())

def get_number_of_paper_refs(driver):
	journal_title = find_element(driver, JOURNAL_TITLE_XPATH)
	if journal_title is None:
		return (False, "0")

	journal_title = journal_title.text.split(',')[1].strip()

	found = False
	visible_list = find_elements(driver, VISIBLE_XPATH)

	if visible_list is None:
		return (False, "0")

	for li in visible_list:
		title = li.find_element(By.XPATH, TITLE_XPATH).text.strip()
		number = li.find_element(By.XPATH, NUMBER_XPATH).text.strip()
		if title.lower() == journal_title.lower():
			found = True
			return (True, number.strip())
			break

	if not found:
		hidden_list = find_elements(driver, HIDDEN_XPATH)
		if hidden_list is None:
			return (False, "0")
		
		for li in hidden_list:
			title = li.find_element(By.XPATH, TITLE_XPATH).text.strip()
			number = li.find_element(By.XPATH, NUMBER_XPATH).text.strip()
			if title.lower() == journal_title.lower():
				found = True
				return (True, number.strip())
				break

		if not found:
			elem = find_elements(driver, VIEW_MORE_XPATH)[0]
			if elem is None:
				return (False, "0")
			elem.click()

			elem = find_elements(driver, VIEW_MORE_XPATH)[1]
			if elem is None:
				return (False, "0")
			elem.click()

			lis = find_elements(driver, LI_FIND_XPATH)
			if lis is None:
				return (False, "0")

			for li in lis:
				title = li.find_element(By.XPATH, TITLE_XPATH).text.strip()
				number = li.find_element(By.XPATH, NUMBER_XPATH).text.strip()
				if title.lower() == journal_title.lower():
					found = True
					return (True, number.strip())
					break
	return (False, "0")

def get(query, row_number):
	start_time = time.time()
	res = dict()
	res["aquery"] = query
	res['query_number'] = row_number
	res['paper_refs'] = "0"
	res['status'] = "Not processed"
	#executable_path = "C:\\Users\\o.parsero\\Downloads\\SCOPUS_PROJECT\\chromedriver.exe"
	
	executable_path = "/usr/lib/chromium-browser/chromedriver"

	found = False
	
	driver = webdriver.Chrome(executable_path=executable_path, desired_capabilities=desired_capabilities)

	for i in range(0, 5):
		if found:
			print ("Found, breaking: {}".format(str(i)))
			break

		print ("Try number {}".format(str(i + 1)))	

		try:
			
			driver.get(SCOPUS_URL)

			elem = driver.find_element_by_id("searchfield")
			driver.execute_script("arguments[0].innerHTML = '{}';".format(query), elem)

			btn = driver.find_element_by_id("advSearch")
			btn.click()

			try:
				driver.find_element(By.XPATH, LINK_XPATH).click()
			except Exception as e:
				res['status'] = "Problem 1: Scopus could not find any document with that query."
				print ("ASDASDSA")
				break


			(success, cur) = get_author_keywords(driver)
			if success:
				res['author_keywords'] = cur
			else:
				continue

			view_in_search_results_format_link = find_element(driver, VIEW_IN_SEARCH_RESULTS_FORMAT)
			if view_in_search_results_format_link is None:
				continue

			view_in_search_results_format_link.click()

			(success, cur) = get_total_refs(driver)
			if success:
				res["total_refs"] = cur
			else:
				continue

			res['execution_time'] = time.time() - start_time
			res['status'] = "OK"
			found = True

			print (json.dumps(res, indent=4))
			break

		except Exception as e:
			with open("errors.log", "a") as f:
				f.write("Error: {}\nQuery: {} \nRow number: {} \n\n".format(str(e), query, row_number))
	driver.close()

	return res