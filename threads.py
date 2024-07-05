from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import WebDriverException
import time

def login_to_threads(username, password):
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    driver = webdriver.Chrome(options=options)

    driver.get('https://www.threads.net/login')

    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'x1e56ztr')))
        print("Login form loaded.")

        username_input = driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]')
        username_input.send_keys(username)
        print("Username entered.")

        password_input = driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="current-password"]')
        password_input.send_keys(password)
        print("Password entered.")

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="button"][tabindex="0"] .xwhw2v2.x1xdureb'))
        )
        login_button.click()
        print("Login button clicked.")

        time.sleep(5)

        WebDriverWait(driver, 30).until(EC.url_contains('https://www.threads.net/'))
        print("Login successful.")
    except Exception as e:
        print(f"Error during login: {e}")
    return driver

import time
from bs4 import BeautifulSoup
import pandas as pd

import time
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data(driver):
    if driver is None or not driver.window_handles:
        print("Driver is not valid or window is closed.")
        return None
    
    news_providers = [
        "washingtonpost",
        "thegatewaypundit",
        "childrenshealthdefense",
        "theconservativetreehouse",
        "cdc",
        "judicialwatch",
        "naturalnews",
        "dailymail",
        "bitchute",
        "reuters",
        "nypost",
        "nytimes",
        "wsj",
        "technocracy",
        "theguardian",
        "cnn",
        "theblaze",
        "thehighwire",
        "foxnews",
        "npr",
        "zerohedge",
        "who",
        "newswars",
        "gellerreport",
        "usatoday",
        "usawatchdog",
        "apnews",
        "newspunch",
        "msnbc",
        "dailycaller",
        "thelibertydaily",
        "independent",
        "globaltimes",
        "breitbart",
        "ukcolumn",
        "infowars",
        "thenationalpulse",
        "globalresearch",
        "chinadaily",
        "newstarget",
        "davidicke",
        "newsweek",
        "wnd",
        "dailywire",
        "cbn",
        "time",
        "activistpost",
        "washingtontimes",
        "pjmedia",
        "gnews"
    ]

    base_url = 'https://www.threads.net'

    usernames = []
    hashtags = []
    likes = []
    comments = []
    shares = []
    headings = []
    replies = []

    for provider in news_providers:
        url = f'{base_url}/@{provider}'
        driver.get(url)
        time.sleep(5)  # Adjust as necessary
        
        scroll_pause_time = 10
        last_height = driver.execute_script("return document.body.scrollHeight")

        scroll_count = 0
        max_scrolls = 5

        while scroll_count < max_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_count += 1

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        posts = soup.find_all('div', class_='x1a2a7pz x1n2onr6')
        print(f"Number of posts found for {provider}: {len(posts)}")

        for post in posts:
            username_tag = post.find('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xjohtrz x1s688f xp07o12 x1yc453h')
            username = username_tag.text.strip('@') if username_tag else 'NA'
            usernames.append(username)

            hashtags_tags = post.find_all('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xjohtrz xo1l8bm xp07o12 x1yc453h xat24cr x1anpbxc')
            hashtags_list = [tag.text.strip('#') for tag in hashtags_tags] if hashtags_tags else ['NA']
            hashtags.append(hashtags_list)

            heading_tag = post.find('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xjohtrz xo1l8bm xp07o12 x1yc453h xat24cr xdj266r')
            heading = heading_tag.text.strip() if heading_tag else 'NA'
            headings.append(heading)

            like_tag = post.find('div', class_='xu9jpxn x1n2onr6 xqcsobp x12w9bfk x1wsgiic xuxw1ft x17fnjtu')
            like_count = like_tag.text.strip() if like_tag else 'NA'
            likes.append(like_count)

            comment_tag = post.find('svg', {'aria-label': 'Reply'}).find_next('span', class_='x10l6tqk x17qophe x13vifvy')
            comment_count = comment_tag.text.strip() if comment_tag else 'NA'
            comments.append(comment_count)

            share_tag = post.find('svg', {'aria-label': 'Repost'}).find_next('span', class_='x10l6tqk x17qophe x13vifvy')
            share_count = share_tag.text.strip() if share_tag else 'NA'
            shares.append(share_count)

            replies_tag = post.find('div', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xjohtrz xo1l8bm xp07o12 x1yc453h xat24cr xdj266r')
            replies_text = replies_tag.text.strip() if replies_tag else 'NA'
            replies.append(replies_text)

    data = {
        'Username': usernames,
        'Hashtags': hashtags,
        'Headings': headings,
        'Likes': likes,
        'Comments': comments,
        'Repost': shares,
        'Replies': replies
    }

    df = pd.DataFrame(data)

    return df



def append_to_csv(df, csv_file):
    try:
        existing_data = pd.read_csv(csv_file)
        updated_data = pd.concat([existing_data, df], ignore_index=True)
        updated_data.to_csv(csv_file, index=False)
        print(f"Data appended to {csv_file}.")
    except FileNotFoundError:
        df.to_csv(csv_file, index=False)
        print(f"{csv_file} created with initial data.")

if __name__ == "__main__":
    username = '*********'
    password = '*********'

    driver = login_to_threads(username, password)

    if driver:
        new_data = scrape_data(driver)

        append_to_csv(new_data, 'threads_news_data.csv')

        driver.quit()
    else:
        print("Login failed. Check your credentials and try again.")
