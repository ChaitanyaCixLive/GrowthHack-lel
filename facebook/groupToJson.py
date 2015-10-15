# Created by Alex Crisara on Oct. 2 2015
# This script scrapes member names from public or private FaceBook groups

# Input is the url of the FaceBook group (ie. https://www.facebook.com/search/20835777216/2019/class/students)
# Output is an array of objects (filename is facebook group)
# Usage: python groupToJson.py <outputname> <groupUrl>

# test public FB group -> https://www.facebook.com/groups/CyrptoCurrency/
# test private FB group -> https://www.facebook.com/groups/159371267555750/

import re, time, json, sys
simplejson = json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

login_email = "chmodspam@gmail.com"
login_password = "Test12345"

driver = webdriver.Chrome()
driver.set_window_size(550, 550)

# the real script starts below

outName = sys.argv[1] + '.json'
inUrl = sys.argv[2]

# init info
print '+' + ('-' * (len('Input URL -> ') + (len(inUrl)) + 3)) + '+'
print 'Group To JSON'
print 'Filename -> %s' % outName
print 'Input URL -> %s' % inUrl
print '+' + ('-' * (len('Input URL -> ') + (len(inUrl)) + 3)) + '+'

profile_list = []
groupType = "null"
iterator_count = 0

def json_out(outlist, filename):	
	with open(filename, 'w') as outfile:
		outfile.write("{}\n".format(json.dumps(outlist, indent = 4)))
		print ('Output written to file -> %s') % filename

def signIn(email, passwrd):
	try:
		print 'Logging into FaceBook...' 
		driver.get("http://www.facebook.com")
		driver.find_element_by_id("email").send_keys(email)
		driver.find_element_by_id("pass").send_keys(passwrd)
		driver.find_element_by_id("u_0_x").submit()
		print ('>> login succesful <<')
	except:
		print '>> login info incorrect <<'
		print 'exiting script in 3s...'
		time.sleep(2)
		driver.quit()

# grab profiles from private group
def logPrivateProfiles():
	#grab rendered html
	content = driver.page_source
	member_info_raw = Selector(text=content).xpath(".//div[@class='fbProfileBrowserList fbProfileBrowserListContainer']//li").extract()
	print '%d -- members found in group' % len(member_info_raw)
	for i in range(len(member_info_raw)):
		name = Selector(text=content).xpath(".//div[@class='fsl fwb fcb']/a/text()")[i].extract()
		facebookURL = Selector(text=content).xpath(".//div[@class='fsl fwb fcb']/a/@href")[i].extract()
		print '%s -- %s @@ %d\n' % (name, facebookURL, i)

		personObj = {
		"name": name,
		"url": facebookURL
		}

		profile_list.append(personObj)

# grab profile info from public group
# one workflow for single-page another for mukti-page
def logPublicProfiles(iterator_count):
	#grab rendered html
	content = driver.page_source

def logProfiles(groupType, iterator_count):
	if (groupType == "Public"):
		logPublicProfiles(iterator_count):

	else: 
		logPrivateProfiles():

def findMembers():
	global groupType
	# first modify inUrl to check if public or private group
	membersUrl = inUrl + 'members/'
	driver.get(membersUrl)

	print 'navigated to group members page @ %s' % driver.current_url
	print 'opening dialogue...\n'

	try:
		profile_set_link = driver.find_element_by_xpath(".//div[@class='uiHeaderActions fsm fwn fcg']//a[@ajaxify]").get_attribute('href')
		print '>> group is PRIVATE <<'
		groupType = "private"
		print'/nnavigating to profile_set_link'
		driver.get(profile_set_link)

		# might not even need to scroll to query profile list
		# first check if "see more" button is present
		iterator_count = 1
		while True:
			try:
				assert driver.find_element_by_xpath(".//div[@class='fbProfileBrowserList expandedList fbProfileBrowserNoMoreItems']")
				print '- all profiles identified @ iterator %d -' % iterator_count
				break
			
			except:
				time.sleep(5)
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				print 'iterator %d found' % iterator_count
				iterator_count += 1

	
	except:
		print '>> group is PUBLIC <<'
		groupType = "public"

		try:
			assert driver.find_element_by_xpath(".//a[@class='pam uiBoxLightblue uiMorePagerPrimary']")
			print 'iterator found - proceding to iterate'
			iterator_count = 0
			while True:
				try:
					driver.find_element_by_xpath(".//a[@class='pam uiBoxLightblue uiMorePagerPrimary']").click()
					iterator_count += 1
					print '~ iterator %d clicked ' % iterator_count
					print 'update'
					time.sleep(5)
				except:
					print '- all profiles identified @ iterator %d -' % iterator_count
					break

		except:
			print '- all profiles found on first page -'
			
		

signIn(login_email, login_password)
print ('current url --> ',  driver.current_url)

findMembers()
logProfiles()
json_out(profile_list, outName)
time.sleep(5)
driver.quit()
