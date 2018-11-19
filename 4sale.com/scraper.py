from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

# A Scraper class to scrape BBMP complaints
class Scraper:
    # initalize with the chrome object
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='bin/chromedriver')
    
    # A function to scrape complaints from a given number of pages
    def scrape_complaints(self,numberOfPages=200):
        # go to the page to scrape the complaints from
        self.browser.get("http://www.vigeyegpms.in/bbmp/index.php?module=helpdeskpublic&action=view-complaints")
        l = []
        for i in range(numberOfPages):
            elems = self.browser.find_elements_by_class_name('alt')
            for elem in elems[1:]:
                locality = elem.find_elements_by_tag_name('td')[2].text
                complaints = elem.find_elements_by_tag_name('td')[4].text
                # Scrape the locality and complaints
                l.append([locality,complaints])
            # Press the 'NEXT' button to go to next page
            buttons = self.browser.find_elements_by_class_name('texts')[5]
            buttons.click()
        # Store complaints in a csv file
        with open('db/input_csv_files/complaints3.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(l)
            
    