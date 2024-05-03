from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("localhost:8000")

text_box = driver.find_element_by_id('send_textarea')
text_box.clear()
text_box.send_keys("question")
text_box.send_keys(Keys.RETURN)

driver.close()
