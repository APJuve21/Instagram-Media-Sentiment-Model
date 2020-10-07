from selenium import webdriver
from time import sleep
from secrets import pw
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from input import TERM
import pandas as pd

class Bot():
	links = []
	my_dict = {
		"profile": [],
		"followersLink": [],
		"total_posts": []
	}


	def __init__(self):

		self.driver = webdriver.Chrome()
		self.driver.get('https://www.instagram.com/')
		sleep(3)
		username_input = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
		username_input.send_keys('mr_3.1415')

		password_input = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
		password_input.send_keys(pw)

		submit_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]/button')
		submit_btn.click()

		sleep(5)

		save_login_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/button')
		save_login_btn.click()

		sleep(5)

		not_now_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
		not_now_btn.click()
		 #Get usernames based on word
		
		for search_term in TERM:
			try:
				search_input = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
				search_input.send_keys(search_term)

				sleep(2)

				select_first_search = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]')
				select_first_search.click()

				sleep(2)

			#collect profile names #collect followers

				profile = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2').text
				sleep(2)
				self.my_dict["profile"].append(profile)

				followersLink = self.driver.find_element_by_css_selector('ul li a span').text
				sleep(2)
				self.my_dict["followersLink"].append(followersLink)

				total_posts = self.driver.find_element_by_css_selector('ul li span span').text
				self.my_dict["total_posts"].append(total_posts)
				print(self.my_dict)

			except NoSuchElementException:
				pass

			#scrapepostcontent
			links = self.driver.find_elements_by_tag_name('a')
			def condition(link):
				return '.com/p/' in link.get_attribute('href')
			valid_links = list(filter(condition, links))

			for i in range(10): #how many posts to hunt for
				link = valid_links[i].get_attribute('href')
				if link not in self.links:
					self.links.append(link)

		how = len(self.my_dict["profile"])

		perpage_dict = dict((el, []) for el in self.my_dict["profile"])
		print(perpage_dict)
		count = 0

		for link in self.links:

			self.driver.get(link)
			sleep(2)

			try:
				post_likes = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[2]/div/div/button/span').text
			except NoSuchElementException:
				views_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[2]/div/span')
				views_button.click()
				post_likes = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[2]/div/div/div[4]/span').text

			perpage_dict[self.my_dict["profile"][count]].append(post_likes)


			sleep(2)

			post_time = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/div[2]/a/time').text

			perpage_dict[self.my_dict["profile"][count]].append(post_time)
			print(perpage_dict)
			count += 1
			if count == how:
				break



def main():
	my_bot = Bot()

if __name__ == '__main__':
	main() 
