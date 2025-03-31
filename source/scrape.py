import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

# Your Glassdoor credentials
EMAIL = "alex.sanchez.casals@gmail.com"
PASSWORD = "RH@cvLDi!5!j!YU"

# Glassdoor URLs (Modify as needed)
LOGIN_URL = "https://www.glassdoor.com/profile/login_input.htm"
JOBS_URL = "https://www.glassdoor.com/Job/software-engineer-jobs-SRCH_KO0,17.htm"
REVIEWS_URL = "https://www.glassdoor.com/Reviews/Google-Reviews-E9079.htm"
SALARY_URL = "https://www.glassdoor.com/Salaries/software-engineer-salary-SRCH_KO0,17.htm"

# Launch Chrome with stealth settings
options = uc.ChromeOptions()
options.headless = False  # Set to True if you don't want a visible browser
options.add_argument(f"user-agent={UserAgent().random}")
driver = uc.Chrome(options=options)

def login():
    """Logs into Glassdoor"""
    driver.get(LOGIN_URL)
    time.sleep(random.uniform(3, 6))
    
    email_input = driver.find_element(By.ID, "userEmail")
    password_input = driver.find_element(By.ID, "userPassword")
    
    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(random.uniform(5, 10))  # Wait for login to process
    print("✅ Logged into Glassdoor")

def scrape_jobs():
    """Scrapes job listings from Glassdoor"""
    driver.get(JOBS_URL)
    time.sleep(random.uniform(3, 6))
    
    jobs = driver.find_elements(By.CLASS_NAME, "react-job-listing")
    
    for job in jobs[:10]:  # Limit to 10 for demo
        try:
            title = job.find_element(By.CLASS_NAME, "jobTitle").text
            company = job.find_element(By.CLASS_NAME, "css-87uc0g").text
            location = job.find_element(By.CLASS_NAME, "css-1buaf54").text
            print(f"🔹 {title} at {company} ({location})")
        except Exception as e:
            print("❌ Job scraping error:", e)

def scrape_reviews():
    """Scrapes company reviews"""
    driver.get(REVIEWS_URL)
    time.sleep(random.uniform(3, 6))
    
    reviews = driver.find_elements(By.CLASS_NAME, "gdReview")
    
    for review in reviews[:5]:  # Limit to 5 for demo
        try:
            rating = review.find_element(By.CLASS_NAME, "ratingNumber").text
            summary = review.find_element(By.CLASS_NAME, "summary").text
            print(f"⭐ {rating} - {summary}")
        except Exception as e:
            print("❌ Review scraping error:", e)

def scrape_salaries():
    """Scrapes salary information"""
    driver.get(SALARY_URL)
    time.sleep(random.uniform(3, 6))
    
    salaries = driver.find_elements(By.CLASS_NAME, "salaryRow")
    
    for salary in salaries[:5]:  # Limit to 5 for demo
        try:
            role = salary.find_element(By.CLASS_NAME, "css-1lcgc3v").text
            pay = salary.find_element(By.CLASS_NAME, "css-1bluz6i").text
            print(f"💰 {role} earns {pay}")
        except Exception as e:
            print("❌ Salary scraping error:", e)

# Run the scraping functions
login()
scrape_jobs()
scrape_reviews()
scrape_salaries()

driver.quit()
print("✅ Scraping complete!")
