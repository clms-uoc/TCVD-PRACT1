import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent


# Your Glassdoor credentials
EMAIL = "alex.sanchez.casals@gmail.com"
PASSWORD = "RH@cvLDi!5!j!YU"


# Glassdoor URLs
LOGIN_URL = "https://www.glassdoor.es/index.htm"
JOBS_URL = "https://www.glassdoor.es/Empleo/espa%C3%B1a-data-scientist-empleos-SRCH_IL.0,6_IN219_KO7,21.htm"
REVIEWS_URL = "https://www.glassdoor.es/Opiniones/index.htm?filterType=RATING_OVERALL&locId=219&locType=N&locName=Espa%C3%B1a&occ=Data+Science&page=1&overall_rating_low=4"
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
        
        random_sleep(2, 4)  

        password_input = driver.find_element(By.ID, "inlineUserPassword")        
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)

        random_sleep(5, 10)  
        print("✅ Logged into Glassdoor")
    except Exception as e:
        print("❌ Login failed:", e)

# Function to scrape job details
def scrape_jobs():
    """Scrapes job offers (title, employer, rating, location, salary, job link, job age) and saves to CSV."""
    
    # Start WebDriver (Ensure you set up your ChromeDriver correctly)
    driver = webdriver.Chrome()

    JOBS_URL = "https://www.glassdoor.es/Empleo/espana-empleos-SRCH_IL.0,6_IN219.htm"
    driver.get(JOBS_URL)
    print("✅ Opened Jobs Page.")

    random_sleep()

    # Click "Stay on Web" button if needed
    try:
        stay_on_web_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "css-w7kqor")]'))
        )
        stay_on_web_button.click()
        print("🔵 Clicked 'Stay on Web' button.")
    except:
        print("🟡 'Stay on Web' button not found or not needed.")

    # Close alerts modal if present
    try:
        close_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Cancelar"]'))
        )
        close_button.click()
        print("🔵 Closed modal successfully.")
    except:
        print("🟡 No modal found or already closed.")

    random_sleep()
    
    # Locate the job listings container
    try:
        job_list = driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/ul')
        job_elements = job_list.find_elements(By.TAG_NAME, "li")  # Assuming each job is in an <li> tag
        print(f"✅ Found {len(job_elements)} jobs.")
    except Exception as e:
        print(f"❌ Error locating job list: {e}")
        return

    jobs_data = []  # List to store job details

    # Iterate through job listings
    for i, job in enumerate(job_elements[:10]):  # Limit to 10 jobs for demo
        try:
            # Print raw HTML of job element for debugging
            print(f"\n🔎 Job {i+1} raw HTML:\n{job.get_attribute('outerHTML')}\n")

            # Extract Job Title
            try:
                job_title = job.find_element(By.CLASS_NAME, "JobCard_jobTitle__GLyJ1").text
            except:
                job_title = "Title not available"

            # Extract Employer Name
            try:
                employer_name = job.find_element(By.CLASS_NAME, "EmployerProfile_compactEmployerName__9MGcV").text
            except:
                employer_name = "Employer not specified"

            # Extract Employer Rating
            try:
                employer_rating = job.find_element(By.CLASS_NAME, "rating-single-star_RatingText__XENmU").text
            except:
                employer_rating = "Rating not available"

            # Extract Job Location
            try:
                job_location = job.find_element(By.CLASS_NAME, "JobCard_location__Ds1fM").text
            except:
                job_location = "Location not available"

            # Extract Salary Info (if available)
            try:
                job_salary = job.find_element(By.CLASS_NAME, "css-1bluz6i").text
            except:
                job_salary = "Salary not specified"

            # Extract Job Link
            try:
                job_link = job.find_element(By.CLASS_NAME, "JobCard_jobTitle__GLyJ1").get_attribute("href")
            except:
                job_link = "No link available"

            # Extract Job Age (e.g., "15 días")
            try:
                job_age = job.find_element(By.CLASS_NAME, "JobCard_listingAge__jJsuc").text
            except:
                job_age = "Job age not available"

            # Print extracted details
            print(f"🔹 {i+1}. {job_title} at {employer_name}")
            print(f"   ⭐ Rating: {employer_rating}")
            print(f"   📍 Location: {job_location}")
            print(f"   💰 Salary: {job_salary}")
            print(f"   🔗 Link: {job_link}")
            print(f"   🕑 Job Age: {job_age}")

            # Store job details in list
            jobs_data.append({
                "Job Title": job_title,
                "Employer": employer_name,
                "Rating": employer_rating,
                "Location": job_location,
                "Salary": job_salary,
                "Job Link": job_link,
                "Job Age": job_age
            })

        except Exception as e:
            print(f"❌ Error extracting job {i+1}:", e)

    # Write data to CSV file
    csv_file = "jobs.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=jobs_data[0].keys())
        writer.writeheader()
        writer.writerows(jobs_data)

    print(f"✅ Job scraping complete. Data saved to {csv_file}.")

    # Close the browser
    driver.quit()


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
random_sleep(120,200)
scrape_jobs()
scrape_reviews()
scrape_salaries()

driver.quit()
print("✅ Scraping complete!")
