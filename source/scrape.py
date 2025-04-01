import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent


# Your Glassdoor credentials
EMAIL = "alex.sanchez.casals@gmail.com"
PASSWORD = "RH@cvLDi!5!j!YU"


# Glassdoor URLs
LOGIN_URL = "https://www.glassdoor.es/index.htm"
JOBS_URL = "https://www.glassdoor.es/Empleo/espa%C3%B1a-data-scientist-empleos-SRCH_IL.0,6_IN219_KO7,21.htm"
REVIEWS_URL = "https://www.glassdoor.es/Opiniones/index.htm?filterType=RATING_OVERALL&locId=219&locType=N&locName=Espa%C3%B1a&page=1&overall_rating_low=4"
SALARY_URL = "https://www.glassdoor.es/Sueldos/espa%C3%B1a-data-scientist-sueldo-SRCH_IL.0,6_IN219_KO7,21.htm"

# Set up ChromeDriver path (Modify this for your system)
CHROMEDRIVER_PATH = "resources/chromedriver-linux64/chromedriver"  # Change this to your ChromeDriver path

# Launch Chrome with stealth settings
options = Options()
options.add_argument(f"user-agent={UserAgent().random}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument("--start-maximized")

# Set up WebDriver service
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

def random_sleep(min_time=3, max_time=6):
    """Generates a random sleep interval to prevent bot detection."""
    time.sleep(random.uniform(min_time, max_time))

def login():
    """Logs into Glassdoor."""
    driver.get(LOGIN_URL)
    random_sleep()
    
    try:
        email_input = driver.find_element(By.ID, "inlineUserEmail")
        email_input.send_keys(EMAIL)
        email_input.send_keys(Keys.RETURN)
        
        random_sleep(2, 4)  # Wait for login to process

        password_input = driver.find_element(By.ID, "inlineUserPassword")        
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)

        random_sleep(5, 10)  # Wait for login to process
        print("✅ Logged into Glassdoor")
    except Exception as e:
        print("❌ Login failed:", e)

def scrape_jobs():
    """Scrapes job listings from Glassdoor."""
    driver.get(JOBS_URL)
    random_sleep()
    
    jobs = driver.find_elements(By.CLASS_NAME, "react-job-listing")
    
    for i, job in enumerate(jobs[:10]):  # Limit to 10 for demo
        try:
            title = job.find_element(By.CLASS_NAME, "jobTitle").text
            company = job.find_element(By.CLASS_NAME, "css-87uc0g").text
            location = job.find_element(By.CLASS_NAME, "css-1buaf54").text
            print(f"🔹 {i+1}. {title} at {company} ({location})")
        except Exception as e:
            print("❌ Job scraping error:", e)

def scrape_reviews():
    """Scrapes company reviews."""
    driver.get(REVIEWS_URL)
    random_sleep()
    
    reviews = driver.find_elements(By.CLASS_NAME, "gdReview")
    
    for i, review in enumerate(reviews[:5]):  # Limit to 5 for demo
        try:
            rating = review.find_element(By.CLASS_NAME, "ratingNumber").text
            summary = review.find_element(By.CLASS_NAME, "summary").text
            print(f"⭐ {i+1}. {rating} - {summary}")
        except Exception as e:
            print("❌ Review scraping error:", e)

def scrape_salaries():
    """Scrapes salary information."""
    driver.get(SALARY_URL)
    random_sleep()
    
    salaries = driver.find_elements(By.CLASS_NAME, "salaryRow")
    
    for i, salary in enumerate(salaries[:5]):  # Limit to 5 for demo
        try:
            role = salary.find_element(By.CLASS_NAME, "css-1lcgc3v").text
            pay = salary.find_element(By.CLASS_NAME, "css-1bluz6i").text
            print(f"💰 {i+1}. {role} earns {pay}")
        except Exception as e:
            print("❌ Salary scraping error:", e)

# Run the scraping functions
login()
scrape_jobs()
scrape_reviews()
scrape_salaries()

driver.quit()
print("✅ Scraping complete!")
