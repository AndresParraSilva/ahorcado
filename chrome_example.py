import time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=\home\andres")
driver = webdriver.Chrome(options=chrome_options)

driver.get('http://www.google.com/');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
