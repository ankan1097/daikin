from selenium import webdriver
import time

webpage = r"https://gps-coordinates.org/"
place = "kolkata" #change this for place name

driver = webdriver.Chrome(executable_path=r"C:/Users/c-ankan/Desktop/chromedriver_win32/chromedriver") #put your path for chromedriver
driver.get(webpage)

input_box = driver.find_element_by_id("address")
input_box.clear()
input_box.send_keys(place)


submit = driver.find_element_by_xpath("//*[contains(text(), 'Get GPS Coordinates')]")
submit.click()

time.sleep(3)
lat_box = driver.find_element_by_id("latitude")
lat = lat_box.get_attribute("value")

lng_box = driver.find_element_by_id("longitude")
lng = lng_box.get_attribute("value")

print(lat, lng)

driver.close()