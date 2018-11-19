from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import csv

browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
#browser.get("https://www.99acres.com/search/property/buy/residential-all/bangalore-all?search_type=QS&search_location=CP20&lstAcn=CP_R&lstAcnId=20&src=CLUSTER&preference=S&selected_tab=1&city=20&res_com=R&property_type=R&isvoicesearch=N&keyword_suggest=bangalore%20(all)%3B&fullSelectedSuggestions=bangalore%20(all)&strEntityMap=W3sidHlwZSI6ImNpdHkifSx7IjEiOlsiYmFuZ2Fsb3JlIChhbGwpIiwiQ0lUWV8yMCwgUFJFRkVSRU5DRV9TLCBSRVNDT01fUiJdfV0%3D&texttypedtillsuggestion=Bangalore&refine_results=Y&Refine_Localities=Refine%20Localities&action=%2Fdo%2Fquicksearch%2Fsearch&suggestion=CITY_20%2C%20PREFERENCE_S%2C%20RESCOM_R&searchform=1&price_min=null&price_max=null")
browser.get("https://www.99acres.com/search/property/buy/independent-house/bangalore-all?search_type=QS&search_location=SH&lstAcn=SEARCH&lstAcnId=9532695904381129&src=CLUSTER&preference=S&city=20&res_com=R&property_type=2&selected_tab=1&isvoicesearch=N&keyword_suggest=bangalore%20(all)%3B&fullSelectedSuggestions=bangalore%20(all)&strEntityMap=W3sidHlwZSI6ImNpdHkifSx7IjEiOlsiYmFuZ2Fsb3JlIChhbGwpIiwiQ0lUWV8yMCwgUFJFRkVSRU5DRV9TLCBSRVNDT01fUiJdfV0%3D&refine_results=Y&Refine_Localities=Refine%20Localities&action=%2Fdo%2Fquicksearch%2Fsearch&searchform=1&price_min=null&price_max=null")
l = [['availability','size','total_sqft','bath','locality','price']]

for i in range(10):
	elems = browser.find_elements_by_class_name('srpWrap')
	for elem in elems:
		locality = elem.find_element_by_class_name('_srpttl').text.split('in')[1].strip()
		print(locality)
		availability = elem.find_element_by_class_name('_auto_possesionLabel').text
		
		if(availability == "Ready To Move" or availability == "Immediate Possession" or availability == "New Launch"):
			pass
					
		else:
			availability = availability.split('in')[1].strip()				
		
		print(availability)

		price = elem.find_element_by_class_name('srpNw_price').text
		print(price)
		area = elem.find_element_by_class_name('_auto_areaValue').find_element_by_tag_name('b').text
		print(area)

		try:
			bedrooms = elem.find_element_by_class_name('_auto_bedroom').text
			print(bedrooms)

		except NoSuchElementException as exception:
    			continue
			
		bathrooms = elem.find_element_by_class_name('_auto_bath_balc_roadText').text
		print(bathrooms)
		#perSquareFeet = elem.find_element_by_class_name('_auto_ppu_area').text
		#print(perSquareFeet)
		print('\n')		
		l.append([availability,bedrooms,area,bathrooms,locality,price])
	browser.get('https://www.99acres.com/independent-house-in-bangalore-ffid-page-' + str(i + 2))

with open('property3.csv','w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(l)
