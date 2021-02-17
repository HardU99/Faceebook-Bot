from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random

# Enter Facebook Username
user_name = ""

# Enter Facebook Password
password = ""

# Enter Facebook Post Text
post_text = ""

# Enter Facebook Comment Text
comment_text = ""

# Path of ChromeDriver.exe
ChromeDriverPath = ""

# Configuration for blocking unwanted notifications
chrome_options = Options()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=ChromeDriverPath)

# -----------------------
# Login
# -----------------------

driver.get("https://www.facebook.com") 
element = driver.find_element_by_id("email")
element.send_keys(user_name)
element = driver.find_element_by_id("pass")
element.send_keys(password)
element.send_keys(Keys.RETURN)

time.sleep(10)

# ------------------------------------
# Adding a friend from same location
# ------------------------------------

driver.get("https://www.facebook.com/{}/".format(user_name))

time.sleep(10)

# Scrapying Location from your facebook profile
location = driver.find_element_by_xpath("//div[@class='nc684nl6']")
location = location.text.split(",")[0]

# Finding people using the location
driver.get("https://www.facebook.com/search/people/?q={}".format(location))

time.sleep(10)

# Scrapying all the IDs available
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
new_user_profiles = []
for link in soup.findAll("a", { "class" : "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p dkezsu63" }):
	new_profile = link.get('href')
	if "facebook" in new_profile:
		new_user_profiles.append(new_profile)

user_profile = random.choice(new_user_profiles)
driver.get(user_profile)

time.sleep(10)

# Sending friend request
send_friend_request = driver.find_element_by_xpath("//div[@class='h676nmdw buofh1pr rwwkvi1h']")
send_friend_request.click()

time.sleep(10)

# -----------------------
# Update Status
# -----------------------

driver.get("https://www.facebook.com")

time.sleep(10)

driver.find_element_by_xpath("//div[@class='k4urcfbm g5gj957u buofh1pr j83agx80 ll8tlv6m']").click()

time.sleep(10)

ele = driver.switch_to.active_element
ele.send_keys(post_text)
time.sleep(5)
driver.find_element_by_xpath("//div[@aria-label='Post']").click()

time.sleep(10)

# -------------------------------------
# Commenting random friends recent post
# -------------------------------------

driver.get("https://www.facebook.com/{}/friends".format(user_name))

time.sleep(10)

# Scrapying the friendlist
friends_list = driver.find_element_by_xpath("//div[@class='j83agx80 btwxx1t3 lhclo0ds i1fnvgqd']")
friends_list = str(friends_list.text).split("\n")[::3]
friend = random.choice(friends_list)

driver.find_element_by_link_text(friend).click()
time.sleep(10)

# Commenting the most recent post
init_post = driver.find_element_by_xpath("//div[@aria-posinset='1']")
time.sleep(10)
ele = init_post.find_element_by_xpath("//div[@aria-label='Write a comment']")
ele.send_keys(comment_text)
ele.send_keys(Keys.RETURN)
