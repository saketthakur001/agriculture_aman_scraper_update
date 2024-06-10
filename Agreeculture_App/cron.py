import time
from django_cron import CronJobBase, Schedule
import requests
from bs4 import BeautifulSoup
import re
from .models import *  # Import the Article model

def get_news_articles(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    article_links = soup.find_all("a", class_="sub-news-story")
    articles = []

    for article in article_links:
        title = article.find("div", class_="story-title").text.strip()
        article_url = article["href"]
        articles.append((title, article_url))

    return articles

def extract_article_data(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        heading_div = soup.find('h1')
        if heading_div:
            article_title = heading_div.get_text().strip()
        else:
            article_title = None

        # Extract article content
        article_div = soup.find('div', class_='abp-story-article')
        if article_div:
            article_text = ''
            for p in article_div.find_all('p'):
                article_text += p.get_text() + '\n'
            article_text = re.sub(r'<\[^>]+>', '', article_text)
            article_text = article_text.strip()
            return {'title': article_title, 'content': article_text}
        else:
            return {'title': article_title, 'content': "Unable to find the article content on the page."}
    except requests.exceptions.RequestException as e:
        return {'title': None, 'content': f"Error: {e}"}

def get_language_data(languages_urls):
    language_data = []
    for language_url in languages_urls:
        for language, url in language_url.items():
            print(f"Fetching news articles for {language}...")
            news_articles = get_news_articles(url)

            # Iterate through each link and extract article data
            all_article_data = []
            for title, link in news_articles:
                article_data = extract_article_data(link)
                all_article_data.append(article_data)

            language_data.append({"language": language, "articles": all_article_data})

            # Print the data for the current language
            print(f"Language: {language}")
            for article in all_article_data:
                print(f"Title: {article['title']}")
                print(f"Content: {article['content']}")
                print("-" * 30)

    return language_data

# Example usage
languages_urls = [
    {"marathi": "https://marathi.abplive.com/agriculture"},
    {"bengali": "https://bengali.abplive.com/agriculture"},
    {"punjabi": "https://punjabi.abplive.com/news/agriculture"},
    {"gujarati": "https://gujarati.abplive.com/news/agriculture"},
    {"telugu": "https://telugu.abplive.com/news/agriculture"},
    {"tamil": "https://tamil.abplive.com/news/agriculture"},
    {"english": "https://news.abplive.com/agriculture"},
    {"hindi": "https://www.abplive.com/agriculture"}
]

# class MyCronJob(CronJobBase):
#     RUN_EVERY_MINS = 60  # Run every hour
#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'Agreeculture_App.my_scheduled_job'  # a unique code

#     def do(self):
#         language_data = get_language_data(languages_urls)
#         print(language_data)

# MyCronJob.register()



## krishakjagat
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrape_section_page(section_url, class_names):
    response = requests.get(section_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    section_posts = []
    for class_name in class_names:
        if class_name == "none":
            continue
        news_list_section = soup.find_all('div', class_=class_name)
        for news_div in news_list_section:
            news_links = news_div.find_all('a', href=True, title=True)
            for link in news_links:
                post_title = link['title'].strip()
                post_url = urljoin(section_url, link['href'])
                if is_valid_url(post_url):
                    section_posts.append({'title': post_title, 'url': post_url})
                else:
                    print(f"Invalid URL found: {post_url}")
    return section_posts


def scrape_post_content(post_url):
    response = requests.get(post_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove unwanted elements
    for auth_div in soup.find_all('div', class_='auth-name-dt'):
        auth_div.decompose()
    for author_div in soup.find_all('div', class_='h-author'):
        author_div.decompose()
    for author_div in soup.find_all('div', class_='col-md-4'):
        author_div.decompose()
    for author_div in soup.find_all('div', class_='d-mags'):
        author_div.decompose()
    for author_div in soup.find_all('div', class_='d-social'):
        author_div.decompose()
    for author_div in soup.find_all('div', class_='d-nav-item-info'):
        author_div.decompose()

    # Extract content
    paragraphs = soup.find_all('p')
    content = "\n\n".join([p.text.strip() for p in paragraphs])
    return content

def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


# Define the base URLs and class names for each language
language_urls = {
    "hindi": {
        "base": "https://www.krishakjagat.org/",
        "main_class": ["cm-first-post","cm-posts"],
        "news_classes": ["cm-post-content","cm-posts"],
        "weather_class": ["weather-home mt-5 mb-3"],
        "khati_badi_class": ["home-2-3-lst"],
        "government_class":["col-xs-12 col-sm-6 col-md-4 col-lg-4 cat-flex"]
     },
    "english": {
        "base": "https://www.en.krishakjagat.org/",
        "main_class": ["cm-first-post","cm-posts"],
        "news_classes": ["cm-post-content","cm-posts"],
        "weather_class": ["none"],
        "khati_badi_class": ["home-2-3-lst"],
        "government_class":["none"]
    },
    "punjabi": {
        "base": "https://punjabi.krishijagran.com/",
        "main_class": ["none"],
        "news_classes": ["home-top-news-lst"],
        "weather_class": ["home-top-l"],
        "khati_badi_class": ["three"],
        "government_class":["home-2-3-lst"]
    },
    "marathi": {
        "base": "https://marathi.krishijagran.com/",
        "main_class": ["home-top-l"],
        "news_classes": ["home-top-news-lst"],
        "weather_class": ["weather-home mt-5 mb-3"],
        "khati_badi_class": ["none"],
        "government_class":["home-2-3-lst"],
  
     },
    "tamil": {
        "base": "https://tamil.krishijagran.com/",
        "main_class": ["home-top-l"],
        "news_classes": ["home-top-news-lst"],
        "weather_class": ["none"],
        "khati_badi_class": ["home-2-3-lst"],
        "government_class":["news-list-wide shadow-sm"]
    },
    "malayam": {
        "base": "https://malayalam.krishijagran.com/",
        "main_class": ["home-top-l"],
        "news_classes": ["home-top-news-lst"],
        "weather_class": ["none"],
        "khati_badi_class": ["none"],
        "government_class":["h-cat-lst shadow-sm"]
    },
    "bengali": {
        "base": "https://bengali.krishijagran.com/",
        "main_class": ["home-top-l"],
        "news_classes": ["home-top-news-lst"],
        "weather_class": ["weather-home mt-5 mb-3"],
        "khati_badi_class": ["none"],
        "government_class":["h-cat-lst shadow-sm"]
    },
    "kannada": {
        "base": "https://kannada.krishijagran.com/",
        "main_class": ["home-top-l"],
        "news_classes": ["home-top-news-lst"],
        "weather_class": ["none"],
        "khati_badi_class": ["none"],
        "government_class":["h-cat-lst shadow-sm"]
    },
    "odia": {
        "base": "https://odia.krishijagran.com/",
        "main_class": ["home-top-l"],
        "news_classes": ["home-top-news-lst"],
        "weather_class": ["none"],
        "khati_badi_class": ["three-boxes"],
        "government_class":["h-cat-lst shadow-sm"]
    },
    "asomiya": {
        "base": "https://asomiya.krishijagran.com/",
        "main_class": ["home-top-l"],
        "news_classes": ["home-top-news-lst"],
        "weather_class": ["none"],
        "khati_badi_class": ["none"],
        "government_class":["h-cat-lst shadow-sm"]
     },
    }


def main(language_urls):
    all_results = {}

    for lang, urls in language_urls.items():
        print(f"Scraping data for language: {lang}")
        
        base_url = urls["base"]
        weather_class = urls["weather_class"]
        khati_class = urls["khati_badi_class"]
        main_class = urls["main_class"]
        news_classes = urls["news_classes"]
        government_classes = urls["government_class"]
        
        # Scrape the main page
        main_posts = scrape_section_page(base_url, main_class)
        khabar_posts = scrape_section_page(base_url, news_classes)

        #Scrape the weather page if available
        weather_posts = scrape_section_page(base_url, weather_class)

       # Scrape the Khati Badi page
        khati_posts = scrape_section_page(base_url, khati_class)

        government_post = scrape_section_page(base_url, government_classes)

        # Set to track processed URLs
        processed_urls = set()

        # Dictionary to store the results for this language
        results = {
            "Main Page Posts": [],
            "Khabar Section Posts": [],
            "Weather Posts": [],
            "Khati Badi Posts": [],
            "government posts":[]
        }

        # Process main page posts
        for post in main_posts:
            if post['url'] not in processed_urls:
                content = scrape_post_content(post['url'])
                results["Main Page Posts"].append({
                    "title": post['title'],
                    "link": post['url'],
                    "content": content
                })
                processed_urls.add(post['url'])     

        # Process "Khabar" section posts
        for post in khabar_posts:
            if post['url'] not in processed_urls:
                content = scrape_post_content(post['url'])
                results["Khabar Section Posts"].append({
                    "title": post['title'],
                    "link": post['url'],
                    "content": content
                })
                processed_urls.add(post['url'])

        #Process weather posts
        for post in weather_posts:
            if post['url'] not in processed_urls:
                content = scrape_post_content(post['url'])
                results["Weather Posts"].append({
                    "title": post['title'],
                    "link": post['url'],
                    "content": content
                })
                processed_urls.add(post['url'])

        # Process Khati Badi posts
        for post in khati_posts:
            if post['url'] not in processed_urls:
                content = scrape_post_content(post['url'])
                results["Khati Badi Posts"].append({
                    "title": post['title'],
                    "link": post['url'],
                    "content": content
                })
                processed_urls.add(post['url'])
       
        for post in government_post:         
            if post['url'] not in processed_urls:
                content = scrape_post_content(post['url'])
                results["government posts"].append({
                    "title": post['title'],
                    "link": post['url'],
                    "content": content
                })
                processed_urls.add(post['url'])

        all_results[lang] = results
    print('done scraping '* 100)
    return all_results


# def store_scraped_data():
#     scraped_data = main(language_urls)

#     for lang, results in scraped_data.items():
#         # Get or create the Language instance
#         language, created = Language.objects.get_or_create(name=lang)

#         for section, posts in results.items():
#             for post in posts:
#                 content = post['content']
#                 post_instance = Post.objects.create(
#                     title=post['title'],
#                     link=post['link '],
#                     content=content,
#                     section=section,
#                     language=language
#                 )

def store_scraped_data():
    scraped_data = main(language_urls)

    for lang, results in scraped_data.items():
        # Get or create the Language instance
        language, created = Language.objects.get_or_create(name=lang)

        for section, posts in results.items():
            for post in posts:
                content = post['content']
                post_instance = NewsPost.objects.create(
                    title=post['title'],
                    link=post['link'],  # Remove the extra space after 'link'
                    content=content,
                    section=section,
                    language=language
                )

def MyCronJob(): #CronJobBase
    # print('yellowr bobosdifsfidl')
    # RUN_EVERY_MINS = 0  # Run every hour
    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # code = 'Agreeculture_App.cron.MyCronJob'  # a unique code

    # def do():
    language_data = get_language_data(languages_urls)
    print(language_data)

    # Save the fetched articles to the database
    for language in language_data:
        for article_data in language['articles']:
            title = article_data['title']
            content = article_data['content']
            url = article_data.get('url', '')  # Assuming the URL is not available
            language_code = language['language']

            # Create or update the Article model instance
            article, created = Article.objects.get_or_create(
                title=title,
                content=content,
                url=url,
                language=language_code,
                defaults={'url': url}
            )

            if not created:
                # Update the existing article if it already exists
                article.content = content
                article.save()
                
        # scraped_data = main(language_urls)
        # print(scraped_data)
    # do()
    store_scraped_data()


while True:
    MyCronJob()
    # Call the function to store the scraped data
    print('sleeping for 60 min')
    time.sleep(60)


# def MyCronJob():
#     RUN_EVERY_MINS = 0  # Run every hour
#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'Agreeculture_App.cron.MyCronJob'  # a unique code

#     def do():
#         print('Scraping data from krishakjagat.org...')
#         scraped_data = main(language_urls)

#         # Save the scraped data to the database
#         for language, results in scraped_data.items():
#             for section, posts in results.items():
#                 for post in posts:
#                     title = post['title']
#                     link = post['link']
#                     content = post['content']

#                     # Create or update the Post model instance
#                     post_obj, created = Post.objects.get_or_create(
#                         title=title,
#                         link=link,
#                         content=content,
#                         section=section,
#                         language=language,
#                         defaults={'content': content}
#                     )

#                     if not created:
#                         # Update the existing post if it already exists
#                         post_obj.content = content
#                         post_obj.save()

#         print('Data scraping and storing completed.')

#     do()

# while True:
#     MyCronJob()
#     time.sleep(60 * 60)  # Run every hour

# def add_text():
#     print('hey'*129)
#     Text.objects.create(text='this is text')

# MyCronJob.register()
