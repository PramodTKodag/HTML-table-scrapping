import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
import requests
import datetime
from selenium.webdriver.common.keys import Keys
import pprint
import urllib.request
import ssl
#from selenium.webdriver import ActionChains
from PIL import Image, ImageEnhance
from pytesseract import image_to_string
import PIL.ImageOps
import numpy as np
import matplotlib.pyplot as plt
from subprocess import check_output
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import schedule


ssl._create_default_https_context = ssl._create_unverified_context

THRESHOLD_VALUE = 100

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#userid = input('Enter shipping bill no.')
userid = "4706597"
#date = input('Enter shipping bill date (yyyy/mm/dd)')
date = '2018/05/07'
#'4706597'
#headless browser
chrome_path = './chromedriver'
#options = Options()
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')
#driver = webdriver.Chrome(chrome_path, chrome_options=options)

#if we want browser to be seen the use following line only and remove above 
driver = webdriver.Chrome(chrome_path)
url = "https://enquiry.icegate.gov.in/enquiryatices/sbTrack"
r = driver.get(url)
def image_process():
	#print("page title : "+driver.title)
	#print("driver name : "+driver.name)
	driver.save_screenshot(".\cap.png")
	img = Image.open("cap.png")
	img2 = img.crop((422, 414, 621, 480))
	img2.save("img2.png")

	img = Image.open("img2.png")

	basewidth = 900
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

	img = img.convert("L")

	imgData = np.asarray(img)
	thresholdedData = (imgData > THRESHOLD_VALUE) * 1.0

	img.save("abcd.png")
	img2 = Image.open("abcd.png")
	inverted_image = PIL.ImageOps.invert(img2)
	inverted_image.save("lmnop.png")
	abcde = Image.open("lmnop.png")
	enhancer = ImageEnhance.Contrast(abcde)
	lmnop2 = enhancer.enhance(2.0)
	lmnop2.save("lmnop2.png")

def image_process2():
	#path = driver.current_url
	#print("page title : "+driver.title)
	#print("driver name : "+driver.name)
	driver.save_screenshot(".\cap.png")
	img = Image.open("cap.png")
	img2 = img.crop((422, 460, 621, 520))
	img2.save("img2.png")

	img = Image.open("img2.png")

	basewidth = 900
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

	img = img.convert("L")

	imgData = np.asarray(img)
	thresholdedData = (imgData > THRESHOLD_VALUE) * 1.0

	img.save("abcd.png")
	img2 = Image.open("abcd.png")
	inverted_image = PIL.ImageOps.invert(img2)
	inverted_image.save("lmnop.png")
	abcde = Image.open("lmnop.png")
	enhancer = ImageEnhance.Contrast(abcde)
	lmnop2 = enhancer.enhance(2.0)
	lmnop2.save("lmnop2.png")
	
	
	
def enter_values():
	try:
		driver.implicitly_wait(6)
		print('UserID : '+userid)
		driver.find_element_by_xpath("""//*[@id="sbNO"]""").clear()
		select = Select(driver.find_element_by_xpath("""//*[@id="location"]"""))
		select.select_by_visible_text('NHAVA SHEVA SEA (INNSA1)')
		#driver.find_element_by_xpath("""//*[@id="location"]""").send_keys('NHAVA SHEVA SEA (INNSA1)')
		driver.find_element_by_xpath("""//*[@id="sbNO"]""").send_keys(userid)
		#driver.find_element_by_xpath("""//*[@id="sbDATE"]""").send_keys(dd)
		#driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[4]/td[2]/img""").click()
		#abc = driver.find_element_by_xpath("""//*[@id="capimg"]""")
		#driver.find_element_by_xpath("""//*[@id="datepicker"]/table/tbody/tr[5]/td[2]""").click()
		driver.execute_script('document.getElementsByName("SB_DT")[0].removeAttribute("readonly")')
		driver.find_element_by_xpath("""//*[@id="sbDATE"]""").send_keys(date)
		

		
		#text = ""
		driver.find_element_by_xpath("""//*[@id="captchaResp"]""").clear()   
		text2 = image_to_string(Image.open('lmnop2.png'),lang='eng')
		#print('extracted text 1 : '+text)
		text2 = text2.replace(" ", "")
		text2 = text2.replace("Z", "2")
		text2 = text2.replace("4", "2")
		print('extracted text 2 : '+text2)

		driver.find_element_by_xpath("""//*[@id="captchaResp"]""").send_keys(text2)
		ac = driver.find_element_by_xpath("""//*[@id="captchaResp"]""").text
		if not text2:
			driver.find_element_by_xpath("""//*[@id="captchaResp"]""").clear()
			driver.find_element_by_xpath("""//*[@id="captchaResp"]""").send_keys('abcd')
		#print('driver title : '+driver.title)
		#driver.implicitly_wait(90)
		driver.find_element_by_xpath("""//*[@id="SubB"]""").click()
		#time.sleep(10)
		
	except Exception as e:
		print('exception handled')
def ret():		
	try:
		aw = driver.find_element_by_xpath("""//*[@id="sub_content"]/h3""").text
		if aw == 'SHIPPING BILL':
			ap = driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[2]/td[1]""").text
			print('Location : '+ap)
			ap2 = driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[2]/td[2]""").text
			print('Shipping Bill No. : '+ap2)
			ap3 = driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[2]/td[3]""").text
			print('Shipping Bill Date : '+ap3)
			print('-------------------------------------------------------')
			driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[1]/td/a""").click()
			print('-------------------------------------------------------')
			print('SB Details : ')
			aaa = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[1]""").text
			print("IEC : "+aaa)
			aaa2 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[2]""").text
			print("CHA No. : "+aaa2)
			aaa3 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[3]""").text
			print("job No. : "+aaa3)
			aaa4 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[4]""").text
			print("job date. : "+aaa4)
			aaa5 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[5]""").text
			print("Port of discharge. : "+aaa5)
			aaa6 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[6]""").text
			print("Total Packages : "+aaa6)
			aaa7 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[7]""").text
			print("Gross Weight : "+aaa7)
			aaa8 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[8]""").text
			print("FOB : "+aaa8)
			aaa9 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[9]""").text
			print("Total Cess : "+aaa9)
			aaa10 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[10]""").text
			print("Drawback : "+aaa10)
			aaa11 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[11]""").text
			print("STR : "+aaa11)
			aaa12 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[12]""").text
			print("Total (DBK + STR) : "+aaa12)
			aaa13 = driver.find_element_by_xpath("""//*[@id="sbICES_Details"]/center/div/table/tbody/tr[2]/td[13]/a""").text
			print("Reward Flag : "+aaa13)
			print('-------------------------------------------------------')
			print('Item wise Reward Details : ')
			driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[3]/td/a""").click()
			bbb = driver.find_element_by_xpath("""//*[@id="itemWiseRewardTdId"]/center/div/table/tbody/tr[2]/td[1]""").text
			print("Invoice No. : "+bbb)
			bbb2 = driver.find_element_by_xpath("""//*[@id="itemWiseRewardTdId"]/center/div/table/tbody/tr[2]/td[2]""").text
			print("Item No. : "+bbb2)
			bbb3 = driver.find_element_by_xpath("""//*[@id="itemWiseRewardTdId"]/center/div/table/tbody/tr[2]/td[3]""").text
			print("Reward flag : "+bbb3)
			print('-------------------------------------------------------')
			
			print('Current Status : ')
			driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[5]/td/a""").click()
			ccc1 = driver.find_element_by_xpath("""//*[@id="sbICES_CurrStus"]/center/div/table/tbody/tr[2]/td[1]""").text
			print("Current Que : "+ccc1)
			ccc2 = driver.find_element_by_xpath("""//*[@id="sbICES_CurrStus"]/center/div/table/tbody/tr[2]/td[2]""").text
			print("LEO Date : "+ccc2)
			ccc3 = driver.find_element_by_xpath("""//*[@id="sbICES_CurrStus"]/center/div/table/tbody/tr[2]/td[3]""").text
			print("EP Copy Print Status : "+ccc3)
			ccc4 = driver.find_element_by_xpath("""//*[@id="sbICES_CurrStus"]/center/div/table/tbody/tr[2]/td[4]""").text
			print("DBK Scroll No : "+ccc4)
			ccc5 = driver.find_element_by_xpath("""//*[@id="sbICES_CurrStus"]/center/div/table/tbody/tr[2]/td[5]""").text
			print("Scroll Date : "+ccc5)
			ccc6 = driver.find_element_by_xpath("""//*[@id="sbICES_CurrStus"]/center/div/table/tbody/tr[2]/td[6]""").text
			print("EGM Integration Status : "+ccc6)
			print('-------------------------------------------------------')
			print('')
			
			print('EGM Status : ')
			driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[7]/td/a""").click()
			ddd1 = driver.find_element_by_xpath("""//*[@id="sbICES_EgmStus"]/center/div/table/tbody/tr[2]/td[1]""").text
			print("EGM No. : "+ddd1)
			ddd2 = driver.find_element_by_xpath("""//*[@id="sbICES_EgmStus"]/center/div/table/tbody/tr[2]/td[2]""").text
			print("EGM No. : "+ddd2)
			ddd3 = driver.find_element_by_xpath("""//*[@id="sbICES_EgmStus"]/center/div/table/tbody/tr[2]/td[3]""").text
			print("Container No. : "+ddd3)
			ddd4 = driver.find_element_by_xpath("""//*[@id="sbICES_EgmStus"]/center/div/table/tbody/tr[2]/td[4]""").text
			print("Seal No. : "+ddd4)
			ddd5 = driver.find_element_by_xpath("""//*[@id="sbICES_EgmStus"]/center/div/table/tbody/tr[2]/td[5]""").text
			
			print("Error Message : "+ddd5)
			print('-------------------------------------------------------')
			print('')
			print('Drawback Query Details : ')
			driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[9]/td/a""").click()
			print('')
			print('')
			#print('Record not found')
			try:
				rnf = driver.find_element_by_xpath("""//*[@id="sbICES_DBKqurydtls"]/center/div/table/tbody/tr[2]/th""").text
				if rnf == 'No Record found':
					print(rnf)
				else:
					print('data found')
					eee1 = driver.find_element_by_xpath("""//*[@id="sbICES_DBKqurydtls"]/center/div/table/tbody/tr[2]/td[1]""").text
					print("Query No : "+eee1)
					eee2 = driver.find_element_by_xpath("""//*[@id="sbICES_DBKqurydtls"]/center/div/table/tbody/tr[2]/td[2]""").text
					print("Query Date : "+eee2)
					eee3 = driver.find_element_by_xpath("""//*[@id="sbICES_DBKqurydtls"]/center/div/table/tbody/tr[2]/td[3]""").text
					print("Query Text : "+eee3)
					eee4 = driver.find_element_by_xpath("""//*[@id="sbICES_DBKqurydtls"]/center/div/table/tbody/tr[2]/td[4]""").text
					print("Pending With : "+eee4)
					eee5 = driver.find_element_by_xpath("""//*[@id="sbICES_DBKqurydtls"]/center/div/table/tbody/tr[2]/td[5]""").text
					print("Officer Name : "+eee5)
					eee6 = driver.find_element_by_xpath("""//*[@id="sbICES_DBKqurydtls"]/center/div/table/tbody/tr[2]/td[6]""").text
					print("Reply Date : "+eee6)
			except exception as e:
				print(str(e))
			print('-------------------------------------------------------')
			print('')
			
			print('ROSL Status : ')
			driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[11]/td/a""").click()
			print('')
			#print('Record not found')
				
				
				
				
				
				
				
				
				
				
				
				
			
			
			
			
			
			
			
			
			
			
			
			
			#driver.close()
		else:
			print('N')
			
		#driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[1]/td/a""").click()
		#print('driver title : '+driver.title)
		#driver.implicitly_wait(200)
		
		#url = 'https://enquiry.icegate.gov.in/enquiryatices/SBTrack_Ices_action'
		#driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[1]/td/a/span""").click()
		
		#driver.find_element_by_xpath("""//*[@id="SubB"]""").click()
		#abcc = driver.find_element_by_class_name('errorMessage').text
		abcc = driver.find_element_by_xpath("""//*[@id="pagetable"]/tbody/tr[5]/td[2]/ul/li/span""").text
		#print(abcc)
		if abcc =='Invalid Code! Please try again!':
			image_process2()
			enter_values()
			ret()
		elif not abcc:
			print('break')
	except Exception as e:
		print('Exception handled')
		
def ref():
	driver.refresh()
	ret()

image_process()
enter_values()
ret()
schedule.every(1).minutes.do(ref)

while True:
	schedule.run_pending()
	time.sleep(2)

	


#https://enquiry.icegate.gov.in/enquiryatices/SBTrack_Ices_action




	
#try:
	#gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
#	mm = urllib.request.urlretrieve("https://enquiry.icegate.gov.in/enquiryatices/CaptchaImg.jpg","C:\\Users\\pramod\\Desktop\\icegate\\cap.jpg")
#	print('hello')
#except Exception as e:
#	print(str(e))

#driver.find_element_by_xpath("""//*[@id="capimg"]""").click()   

#driver.find_element_by_xpath("""//*[@id="SubB"]""").click()