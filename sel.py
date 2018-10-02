import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import selenium.webdriver.chrome.service as service
from selenium.webdriver import DesiredCapabilities

import json, time
import string_helper

# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
NA = "N/A"
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

PAGE_XPATH = "//ul[@class='pagination']/li/a[contains(@data-value, '{}')]"

RESULTS_TABLE_ROWS_XPATH = "//tr[@class='searchArea']"

DOT = "."

DOCUMENT_TITLE_DUMMY_XPATH = ".//td/span[@class='txtOnlyDummy']" #
DOCUMENT_TITLE_LINKED_XPATH = ".//td/a[contains(@title, 'Show document details')]" #
AUTHORS_DUMMY_XPATH = ".//td/span[@class='Dummy']" #
AUTHORS_LINKED_XPATH = ".//td/span/a[contains(@title, 'Show author details')]" #
YEAR_XPATH = ".//td[@class='textRight']" #
SOURCE_TITLE_LINKED_XPATH = ".//td/a[contains(@title, 'Show source title details')]" #
NEXT_SIBLING_XPATH = "following-sibling::*[1]" 
ADDITIONAL_CONTENT_XPATH = ".//td/div[@class='additionalContent']" #
CITED_BY_XPATH = ".//td/a[contains(@title, 'View the documents that references this one')]" #

AUTHORS_LIST_XPATH = "//section[@id='authorlist']/ul/li/a/span[@class='anchorText']"
AFFILIATIONS_XPATH = ".//sup"

AUTHORS_SPAN_XPATH = ".//td[2]/span"
PARENTHESIS_PATTERN = "(...)"

GLOBAL_DRIVER = None

def find_element(driver, xpath, fast=False):
	if fast:
		try:
			elem = driver.find_element(By.XPATH, xpath)
			return elem
		except:
			return None

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

def find_elements(driver, xpath, fast=False):
	if fast:
		try:
			elems = driver.find_elements(By.XPATH, xpath)
			return elems
		except:
			return None

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

def find_elem_from_elem(driver, elem, xpath):
	try:
		res = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
		res = elem.find_element(By.XPATH, DOT + xpath)
		return res
	except:
		return None

def find_elems_from_elem(driver, elem, xpath):
	try:
		res = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
		res = elem.find_elements(By.XPATH, xpath)
		return res
	except:
		return None

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




def get_authors_list(driver, link):
	main_window = driver.current_window_handle
	link.send_keys(Keys.CONTROL + Keys.ENTER)
	driver.switch_to_window(driver.window_handles[1])

	authors = find_elements(driver, AUTHORS_LIST_XPATH)
	authors_list = []
	
	for author in authors:		
		unnec = ""
		author_name = author.text.strip()

		try:
			affs = author.find_elements(By.XPATH, AFFILIATIONS_XPATH)
			for aff in affs:
				unnec = unnec + aff.text.strip()
			author_name = string_helper.exclude(author_name, unnec)
		except:
			pass
		authors_list.append(author_name)

	driver.close()
	driver.switch_to_window(main_window)

	return authors_list

def get_papers(driver):
	rows = find_elements(driver, RESULTS_TABLE_ROWS_XPATH)
	res = []
	index = 0
	for row in rows:
		# link, title, authors, year, source, additional
		#   Y,    Y,       N,    Y,     Y,       N
		paper = dict()
		link = NA
		document_title = NA
		authors = NA
		year = NA
		source_title = NA
		additional_content = NA
		cited_by_count = NA


		# Year
		# TODO
		
		textRight = row.find_elements(By.XPATH, YEAR_XPATH)[0]
		year = textRight.text.strip()

		# Source title
		try:
			source_title = row.find_element(By.XPATH, SOURCE_TITLE_LINKED_XPATH).text.strip()
		except:
			source_title = textRight.find_element(By.XPATH, NEXT_SIBLING_XPATH).text.strip()
		source_title = source_title.split("\n")[0].strip()

		# Additional content
		try:
			additional_content = row.find_element(By.XPATH, ADDITIONAL_CONTENT_XPATH).text.strip()
		except:
			pass

		# Cited by

		cited_by_count = row.find_element(By.XPATH, CITED_BY_XPATH).text.strip()


		# Link, Document title, Authors
		
		try:

			# TODO
			
			document_link = row.find_element(By.XPATH, DOCUMENT_TITLE_LINKED_XPATH)
			link = document_link.get_attribute("href").strip()
			
			document_title = document_link.text.strip()

			span = row.find_element(By.XPATH, AUTHORS_SPAN_XPATH)
			txt = span.text.strip()
			
			if string_helper.contains(txt, PARENTHESIS_PATTERN):
				authors_list = get_authors_list(driver, document_link)
				authors = ", ".join(authors_list)
			else:
				authors = txt
		except Exception as e:
			
			# TODO
			# document_title = find_elem_from_elem(driver, row, DOCUMENT_TITLE_DUMMY_XPATH).text.strip()
			# authors = find_elem_from_elem(driver, row, AUTHORS_DUMMY_XPATH).text.strip()
			try:

				document_title = row.find_element(By.XPATH, DOCUMENT_TITLE_DUMMY_XPATH).text.strip()
				authors = row.find_element(By.XPATH, AUTHORS_DUMMY_XPATH).text.strip()
			except Exception as ex:
				with open("errors.log"):
					print ("ERROR: {}".format(str(e)))
				exit()

		# --- Collecting and appending
		paper['link'] = link
		paper['document_title'] = document_title
		paper['authors'] = authors
		paper['year'] = year
		paper['source_title'] = source_title
		paper['additional_content'] = additional_content
		paper['cited_by'] = cited_by_count

		res.append(paper)

	return (True, res)

# TODO: on page where we click on view in search format smth is wrong, even if there is link, it terminates and starts again


def get(driver, query, row_number):
	start_time = time.time()
	res = dict()
	res['aquery'] = query
	res['query_number'] = row_number
	res['paper_refs'] = "0"
	res['status'] = "Not processed"
	res['papers'] = []

	found = False
	print ("Processing query {}.".format(row_number))
	for i in range(0, 5):
		if found:
			print ("Found, breaking: {}".format(str(i)))
			break

		print ("Try number {}".format(str(i + 1)))	

		try:
			
			driver.get(SCOPUS_URL)

			try:
				elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"searchfield")))
				driver.execute_script("arguments[0].innerHTML = '{}';".format(query), elem)
			except:
				continue

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

			# GETTING NUMBER OF TOTAL REFS
			# (success, cur) = get_total_refs(driver)
			# if success:
			# 	res["total_refs"] = cur
			# else:
			# 	continue


			# SHRINKING THE RESULTS TO 200
			results_per_page = find_element(driver, RESULTS_PER_PAGE_XPATH)
			if results_per_page is None:
				continue
			results_per_page.click()
			results_per_page_200 = find_element(driver, RESULTS_PER_PAGE_200_XPATH)
			if results_per_page_200 is None:
				continue
			results_per_page_200.click()

			papers_all = []
			page_num = 2

			while True:
				(success, papers_chunk) = get_papers(driver)
				for paper in papers_chunk:
					papers_all.append(paper)

				# TODO: get rid of break
				# break

				try:
					next_page_link = find_element(driver, PAGE_XPATH.format(page_num), fast=True)
					next_page_link.click()
					
					page_num = page_num + 1
				except:
					break

			

			for paper in papers_all:
				res['papers'].append(paper)

			res['execution_time'] = time.time() - start_time
			res['status'] = "OK"
			found = True
			break
		except Exception as e:
			with open("errors.log", "a") as f:
				f.write("Error: {}\nQuery: {} \nRow number: {} \n\n".format(str(e), query, row_number))

	return res