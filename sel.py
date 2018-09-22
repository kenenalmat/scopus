import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import selenium.webdriver.chrome.service as service
from selenium.webdriver import DesiredCapabilities

import json, time

# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
SCOPUS_URL = "https://www.scopus.com/search/form.uri?display=advanced&origin=searchbasic&txGid=d63aa1335f3f9f275d51e0bece833ce1"

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

RESULTS_PER_PAGE_XPATH = "//span[@id='resultsPerPage-button']"
LIST_XPATH = "//tr[@class='searchArea']"
RESULTS_PER_PAGE_200_XPATH = "//div[@id='ui-id-4']"
PAGINATION_LIST_XPATH = "//ul[@class='pagination']/li"
ANCHOR_HREF_XPATH = ".//a"

PAGES_XPATH = "//ul[@class='pagination']/li/a[@href='#']"

def find_element(driver, xpath):
	start_time = time.time()
	elem = None
	while True:
		period = time.time() - start_time
		if period > 30:
			return elem
		try:
			elem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
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
			elems = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
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

def get_paper_list(driver):
	pages = find_elements(driver, PAGES_XPATH)
	
	cnt = 0
	max_page = 0

	for a in pages:
		value = (int)(a.text.strip())
		if value > max_page:
			max_page = data-value

	print ("max_page = {}".format(max_page))
	return (True, [])

# TODO: on page where we click on view in search format smth is wrong, even if there is link, it terminates and starts again

def get(driver, query, row_number):
	start_time = time.time()
	res = dict()
	res["aquery"] = query
	res['query_number'] = row_number
	res['paper_refs'] = "0"
	res['status'] = "Not processed"
	
	found = False

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

			# (success, cur) = get_total_refs(driver)
			# if success:
			# 	res["total_refs"] = cur
			# else:
			# 	continue

			# results_per_page = find_element(driver, RESULTS_PER_PAGE_XPATH)
			# if results_per_page is None:
			# 	continue
			# results_per_page.click()
			# results_per_page_200 = find_element(driver, RESULTS_PER_PAGE_200_XPATH)
			# if results_per_page_200 is None:
			# 	continue
			# results_per_page_200.click()

			(success, paper_list) = get_paper_list(driver)

			res['execution_time'] = time.time() - start_time
			res['status'] = "OK"
			found = True
			
			# print (json.dumps(res, indent=4))
			break

		except Exception as e:
			with open("errors.log", "a") as f:
				f.write("Error: {}\nQuery: {} \nRow number: {} \n\n".format(str(e), query, row_number))
	driver.close()

	return res