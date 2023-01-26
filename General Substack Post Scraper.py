import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def substack_post_scraper(url):

    #Open website
    browser = webdriver.Chrome()
    browser.get(url)

    #Sign in
    email = input('What is your Substack sign-in email?')
    password = input('What is your password?')
    signin = browser.find_element_by_css_selector('#main > div.main-menu.animated.with-nav > div.main-menu-content > div > div.topbar-content > div.navbar-buttons > button.button.sign-in-link.outline-grayscale')
    signin.click()
    browser.find_element_by_name('email').send_keys(email)
    signinwithemail = browser.find_element_by_css_selector('#substack-login > div.substack-login__body > div.substack-login__form > form > div:nth-child(5) > span > a')
    signinwithemail.click()
    browser.find_element_by_name('password').send_keys(password)
    signin2 = browser.find_element_by_css_selector('#substack-login > div.substack-login__body > div.substack-login__form > form > div:nth-child(6) > button')
    signin2.click()
    time.sleep(5)

    #Infinite scroll
    last_height = browser.execute_script("return document.body.scrollHeight")
    x = 0
    while x < 1000000:
        x += 1
        time.sleep(7)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    #Setup csv files (doing 2 files: file1 is for the post itself; file 2 is for the comments
    file1 = open(input('Name the file for post content data'), 'w')
    writer1 = csv.writer(file1)
    writer1.writerow(['Post Link', 'Word Count'])

    file2 = open(input('Name the file for post comment data'), 'w')
    writer2 = csv.writer(file2)
    writer2.writerow(['Post Link', 'Commenter', 'Commenter Writes'])

    #Scrape post
    linksraw = browser.find_elements_by_css_selector('a.post-preview-description')
    links = []
    for link in linksraw:
        links.append(link.get_attribute('href'))

    for link in links:
        browser.get(link)
        try:
            post_content = browser.find_element_by_css_selector('div.available-content > div').text
            wordcount = len(post_content.replace(',', '').split())
        except:
            try:
                post_content = browser.find_element_by_css_selector('td > div').text
                wordcount = len(post_content.replace(',', '').split())
            except:
                post_content = browser.find_element_by_class_name('body markup').text
                wordcount = len(post_content.replace(',', '').split())
        try:
            writer1.writerow([link, wordcount])
        except:
            writer1.writerow([link.encode('utf-8'), wordcount])
        try:
            comment_link_raw = browser.find_element_by_css_selector('div > div.single-post-section.comments-section > div.container > a')
            comment_link = comment_link_raw.get_attribute('href')
        except:
            comment_link = None
        #Scrape post comments
        try:
            browser.get(comment_link)
        except:
            pass
        time.sleep(2)
        comments = browser.find_elements_by_css_selector('div.comment-list > div > div')
        for comment in comments:
            try:
                commenter = comment.find_element_by_css_selector('td.comment-rest > div.comment-meta > span').text
            except:
                commenter = "Error"
            if commenter == 'Matt Taibbi':
                commenter_writes = "TK News by Matt Taibbi"
            else:
                try:
                    commenter_writes = comment.find_element_by_css_selector('a.commenter-publication > span').text
                except:
                    commenter_writes = ''
            try:
                writer2.writerow([link, commenter, commenter_writes])
            except:
                writer2.writerow([link.encode('utf-8'), commenter.encode('utf-8'), commenter_writes.encode('utf-8')])
    file.close()

data = substack_scraper(input('Put in the archive link of the writer you want to scrape?'))

#MattTaibbiSubstack = 'https://taibbi.substack.com/archive'