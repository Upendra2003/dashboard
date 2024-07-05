from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Set up the web driver with Brave browser
options = webdriver.ChromeOptions()
options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
driver_path = '/path/to/chromedriver'  # Replace with the path to your ChromeDriver executable
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# Open Twitter login page
driver.get('https://twitter.com/login')

# Allow time for the page to load
time.sleep(5)

# Enter username
username_input = driver.find_element(By.NAME, 'text')
username_input.send_keys('your_username')
username_input.send_keys(Keys.RETURN)

# Allow time for the password field to appear
time.sleep(5)

# Enter password
password_input = driver.find_element(By.NAME, 'password')
password_input.send_keys('your_password')
password_input.send_keys(Keys.RETURN)

# Allow time for the login process
time.sleep(5)

# Navigate to a specific profile or search page (e.g., Twitter's main feed)
driver.get('https://twitter.com/elonmusk')

# Allow time for the page to load
time.sleep(5)

# Scroll down to load more tweets
for _ in range(3):  # Adjust the range to scroll more or less
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(3)  # Wait for tweets to load

# Extract tweets
tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweet"]')

for tweet in tweets:
    try:
        content = tweet.find_element(By.XPATH, './/div[@lang]').text
        print(content)
    except Exception as e:
        print("Error extracting tweet content:", e)

# Close the driver
driver.quit()
