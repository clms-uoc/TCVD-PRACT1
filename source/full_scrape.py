import csv
import re 
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
JOBS_URL = "https://www.glassdoor.es/Empleo/index.htm"

# Set up ChromeDriver path (Modify this for your system)
CHROMEDRIVER_PATH = "resources/chromedriver-linux64/chromedriver"

# Job titles to search
JOB_TITLES = [
    "Data Scientist", "Data Engineer", "Data Analyst", "Machine Learning Engineer",
    "AI Engineer", "Business Intelligence Analyst", "Big Data Engineer",
    "NLP Engineer", "Data Architect"
]

LOCATIONS = ['España']


def get_total_jobs_count():
    try:
        header_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="left-column"]/div[1]/span/div/h1'))
        )
        header_text = header_element.text
        match = re.search(r"(\d+)", header_text)
        if match:
            total_jobs = int(match.group(1))
            print(f" Total job offers found: {total_jobs}")
            return total_jobs
        else:
            print(" Could not extract job count from header text.")
            return 0
    except Exception as e:
        print(f" Failed to extract total job count: {e}")
        return 0

def close_cookie_banner():
    try:
        # Clica "Aceptar" o equivalent del banner de cookies (OneTrust)
        accept_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Aceptar")]'))
        )
        accept_button.click()
        print("Cookie banner closed.")
        random_sleep(1, 2)
    except:
        # Si no hi ha banner, tot bé
        pass

# Set up WebDriver options
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
        print(" Logged into Glassdoor")
    except Exception as e:
        print(" Login failed:", e)

def scrape_jobs():
    """Scrapes job listings for multiple job titles."""
    all_jobs_data = []


    # Click "Stay on Web" button if needed
    try:
        stay_on_web_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "css-w7kqor")]'))
            )
        stay_on_web_button.click()
        print(" Clicked 'Stay on Web' button.")
    except:
            print(" 'Stay on Web' button not found or not needed.")
            
    
    for location in LOCATIONS:
        # Enter location "España"
       

        for job_title in JOB_TITLES:
            print(f"\n🔍 Searching for: {job_title}")

            # Open the Glassdoor job search page
            driver.get(JOBS_URL)
            random_sleep()

            # Locate search bar and enter job title
            try:
                search_bar = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="searchBar-jobTitle"]'))
                )
                search_bar.clear()
                search_bar.send_keys(job_title)
                search_bar.send_keys(Keys.RETURN)
                print(f" Entered '{job_title}' in search bar and initiated search.")
            except Exception as e:
                print(f"Could not enter job title {job_title}: {e}")
                continue

            random_sleep()
            

            
            try:
                location_box = driver.find_element(By.XPATH, '//*[@id="searchBar-location"]')
                location_box.clear()
                location_box.send_keys(location)
                location_box.send_keys(Keys.RETURN)
                print(" Entered location: España")
            except Exception as e:
                print(f" Failed to enter location: {e}")
                continue        
            
            # Close modal pop-ups if needed
            try:
                close_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Cancelar"]'))
                )
                close_button.click()
                print(" Closed modal successfully.")
            except:
                print(" No modal found or already closed.")

            random_sleep()
           
            JOBS_COUNT = get_total_jobs_count()
            no_more_jobs = 0
            #load more jobs

            for scroll_round in range(int(JOBS_COUNT/30)):
                if no_more_jobs > 5: 
                    no_more_jobs = 0
                    break
                try:
                    close_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Cancelar"]'))
                    )
                    close_button.click()
                    print(" Closed modal successfully.")
                except:
                    print(" No modal found or already closed.")
                   
                random_sleep()
                    
                print(f"\n Scroll round {scroll_round + 1}...")

                # Simula scroll gradual com un usuari
                for scroll_step in range(3):
                    driver.execute_script("window.scrollBy(0, window.innerHeight * 0.7);")
                    print(f"     Scrolled down {scroll_step + 1}")
                    random_sleep(1, 2)

                    # Esperar càrrega de nous elements
                    random_sleep(2, 3)

                # Buscar i clicar el botó "Más empleos" si apareix
            
                    try:
                        close_cookie_banner()  

                        more_button = WebDriverWait(driver, 4).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="left-column"]/div[2]/div/div/button[1]'))
                        )
                        driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
                        random_sleep(1, 2)
                        more_button.click()
                        print(" Clicked 'Más empleos' to load more jobs.")
                        random_sleep(4, 6)
                    except Exception as e:
                        print(f" No more 'Más empleos' button or unable to click. ({e})")
                        no_more_jobs += 1
                        break
                        
                    
            # Locate the job listings container
            try:
                job_list = driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/ul')
                job_elements = job_list.find_elements(By.TAG_NAME, "li")  # Assuming each job is in an <li> tag
                print(f" Found {len(job_elements)} jobs for {job_title}.")
            except Exception as e:
                print(f" Error locating job list for {job_title}: {e}")
                continue
            
            # Iterate through job listings
            for i, job in enumerate(job_elements[:]):  
                try:
                    # Extract Job Title
                    try:
                        extracted_title = job.find_element(By.CLASS_NAME, "JobCard_jobTitle__GLyJ1").text
                    except:
                        extracted_title = "Title not available"

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

                    # Extract Salary Info
                    try:
                        job_salary = job.find_element(By.CLASS_NAME, "css-1bluz6i").text
                    except:
                        job_salary = "Salary not specified"

                    # Extract Job Link
                    try:
                        job_link = job.find_element(By.CLASS_NAME, "JobCard_jobTitle__GLyJ1").get_attribute("href")
                    except:
                        job_link = "No link available"

                    # Extract Job Age
                    try:
                        job_age = job.find_element(By.CLASS_NAME, "JobCard_listingAge__jJsuc").text
                    except:
                        job_age = "Job age not available"

                    # Print extracted details
                    print(f"🔹 {i+1}. {extracted_title} at {employer_name}")
                    print(f"   Rating: {employer_rating}")
                    print(f"   Location: {job_location}")
                    print(f"   Salary: {job_salary}")
                    print(f"   Link: {job_link}")
                    print(f"   Job Age: {job_age}")

                    # Store job details
                    all_jobs_data.append({
                        "Searched Job Title": job_title,
                        "Extracted Job Title": extracted_title,
                        "Employer": employer_name,
                        "Rating": employer_rating,
                        "Location": job_location,
                        "Salary": job_salary,
                        "Job Link": job_link,
                        "Job Age": job_age
                    })

                except Exception as e:
                    print(f" Error extracting job {i+1}: {e}")

        # Write data to CSV file
        csv_file = "glassdoor_jobs.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=all_jobs_data[0].keys())
            writer.writeheader()
            writer.writerows(all_jobs_data)

        print(f"\n Job scraping complete. Data saved to {csv_file}.")
        driver.quit()



# Run the scraping functions
login()
random_sleep(15,25)
scrape_jobs()


driver.quit()
print(" Scraping complete!")

