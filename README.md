# Substack-Web-Scraper

Motivation:
The Substack Web Scraper project is designed to extract and organize data from a writer's Substack so that one can perform data analysis to optimize the performance of said Substack.

Description:
The application logins with your Substack login and scrapes the writer's archive page as well as each individual post and their comment sections.

Data collected from the Archive page include the following types:
- Post Title
- Post Description
- Post Type
- Post Link
- Post Date
- Number of Post Likes
- Number of Post comments

Data collected from each individual post include the following types:
- Post Link
- Post Content
- Post Word Count

Data colelcted from each comment section of individual posts include the following types:
- Post Link
- Commenter
- Comment
- Commenter Writes

Data collected from all three different web pages share the same Post Link data type which serves as the primary key if one wants to use SQL to perform data analytics on the collected data.

Selenium is an important library for this application. Selenium was chosen over BeautifulSoup as it tackles the infinite scroll problem of the archive page while BeautifulSoup cannot.

This application uses chained for loops to iterate data extraction over every single post.
This application uses try/except to navigate through the different post types to ensure the data is collected without crashing.
