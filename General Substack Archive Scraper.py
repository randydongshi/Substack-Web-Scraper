import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv

ChuckSubstack = 'https://chuckpalahniuk.substack.com/archive'
MattTaibbiSubstack = 'https://taibbi.substack.com/archive'

def substack_scraper(url):
    # Open website
    browser = webdriver.Chrome()
    browser.get(url)

    # Sign in
    email = input('What is your Substack sign-in email?')
    password = input('What is your password?')
    signin = browser.find_element_by_css_selector(
        '#main > div.main-menu.animated.with-nav > div.main-menu-content > div > div.topbar-content > div.navbar-buttons > button.button.sign-in-link.outline-grayscale')
    signin.click()
    browser.find_element_by_name('email').send_keys(email)
    signinwithemail = browser.find_element_by_class_name(
        'substack-login > div.substack-login__body > div.substack-login__form > form > div:nth-child(5) > span > a')
    signinwithemail.click()
    browser.find_element_by_name('password').send_keys(password)
    signin2 = browser.find_element_by_css_selector(
        '#substack-login > div.substack-login__body > div.substack-login__form > form > div:nth-child(6) > button')
    signin2.click()

    #setup csv file
    file = open(input('''What do you want to name the file?(Don't forget to add '.csv' at the end of the file name)'''), 'w')
    writer = csv.writer(file)
    writer.writerow(['post_title', 'post_preview_description', 'post_type', 'post_link', 'post_date_raw', 'post_likes', 'post_comments'])

    #infinite scroll
    last_height = browser.execute_script("return document.body.scrollHeight")
    x = 0
    while x < 10000000:
        x += 1
        time.sleep(1)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    #scrape
    posts = browser.find_elements(By.CSS_SELECTOR, '#main > div.archive-page.typography.use-theme-bg > div > div > div.portable-archive-list > div')
    time.sleep(2)
    for post in posts:
        try:
            post_title = post.find_element(By.CSS_SELECTOR, "div.post-preview-content > a.post-preview-title.newsletter").text
            post_type = "Newsletter"
        except:
            try:
                post_title = post.find_element(By.CSS_SELECTOR, "div.post-preview-content > a.post-preview-title.video").text
                post_type = "Video"
            except:
                try:
                    post_title = post.find_element(By.CSS_SELECTOR, "div.post-preview-content > a.post-preview-title.thread").text
                    post_type = "Discussion"
                except:
                    post_title = post.find_element(By.CSS_SELECTOR, "div.post-preview-content > a.post-preview-title.podcast").text
                    post_type = "Podcast"
        post_preview_description = post.find_element(By.CSS_SELECTOR, "div.post-preview-content > a.post-preview-description").text
        post_link_raw = post.find_element(By.CSS_SELECTOR, "div.post-preview-content > a.post-preview-description")
        post_link = post_link_raw.get_attribute('href')
        post_date_raw = post.find_element(By.CSS_SELECTOR, "div.post-preview-content > div > div.ufi-preamble.themed > div.ufi-preamble-label.post-date > time").text
        try:
            post_likes = post.find_element(By.CSS_SELECTOR, "div.post-preview-content > div > a:nth-child(2) > div").text
        except:
            post_likes = '0'
        try:
            post_comments = post.find_element(By.CSS_SELECTOR, "div.post-preview-content > div > a.post-ufi-button.style-compressed.post-ufi-comment-button.has-label.with-border > div").text
        except:
            post_comments = '0'
        #print(post_title)
        #print(post_preview_description)
        #print(post_type)
        #print(post_link)
        #print(post_date_raw)
        #print('Likes:', post_likes)
        #print('Comments:', post_comments)
        try:
            writer.writerow([post_title, post_preview_description, post_type, post_link, post_date_raw, post_likes, post_comments])
        except:
            writer.writerow(
                [post_title.encode('utf-8'),
                 post_preview_description.encode('utf-8'),
                 post_type.encode('utf-8'),
                 post_link.encode('utf-8'),
                 post_date_raw.encode('utf-8'),
                 post_likes.encode('utf-8'),
                 post_comments.encode('utf-8')])
    file.close()

data = substack_scraper(input('Put in the archive link of the writer you want to scrape?'))