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


# Glassdoor credentials
EMAIL = "alex.sanchez.casals@gmail.com"
PASSWORD = "RH@cvLDi!5!j!YU"

# URLs
LOGIN_URL = "https://www.glassdoor.es/index.htm"
JOBS_URL = "https://www.glassdoor.es/Empleo/index.htm"

# ChromeDriver path
CHROMEDRIVER_PATH = "resources/chromedriver-linux64/chromedriver"

# Job Titles and Locations
JOB_TITLES = [
    "Data Scientist", "Data Engineer", "Data Analyst", "Machine Learning Engineer",
    "AI Engineer", "Business Intelligence Analyst", "Big Data Engineer",
    "NLP Engineer", "Data Architect"
]
LOCATIONS = ['España']

# Chrome Options
options = Options()
options.add_argument(f"user-agent={UserAgent().random}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument("--start-maximized")

# Setup WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)


def random_sleep(min_time=3, max_time=6):
    time.sleep(random.uniform(min_time, max_time))


def login():
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


def scrape_jobs():
    all_jobs_data = []

    for location in LOCATIONS:
        for job_title in JOB_TITLES:
            # Tancar pop-ups si existeixen
            try:
                stay_on_web_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "css-w7kqor")]'))
                )
                stay_on_web_button.click()
                print("🔵 Clicked 'Stay on Web'")
            except:
                pass


            total_jobs_collected = 0
            seen_jobs = set()
            print(f"\n🔍 Searching for: {job_title}")

            driver.get(JOBS_URL)
            random_sleep()

            # Introduir lloc
            try:
                location_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(locator=(By.XPATH, '//*[@id="searchBar-location"]'))
                )
                location_box.clear()
                location_box.send_keys(location)
                location_box.send_keys(Keys.RETURN)
                print(f"✅ Entered location: {location}")
            except Exception as e:
                print(f"❌ Could not enter location: {e}")
                continue

            # Introduir títol
            try:
                search_bar = driver.find_element(By.XPATH, value='//*[@id="searchBar-jobTitle"]')
                search_bar.clear()
                search_bar.send_keys(job_title)
                search_bar.send_keys(Keys.RETURN)
                print(f"✅ Entered '{job_title}' and started search.")
            except Exception as e:
                print(f"❌ Could not search job title {job_title}: {e}")
                continue

            random_sleep()

            try:
                close_modal = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Cancelar"]'))
                )
                close_modal.click()
                print("🔵 Closed modal")
            except:
                pass            

            for scroll_round in range(4):  # Max 4 * 30 = 120
                random_sleep()
                try:
                    job_list = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="left-column"]/div[2]/ul'))
                    )
                    job_elements = job_list.find_elements(By.TAG_NAME, "li")
                except Exception as e:
                    print(f"❌ Could not load job list: {e}")
                    break

                print(f"🔄 Round {scroll_round+1}: Found {len(job_elements)} jobs.")

                for i, job in enumerate(job_elements):
                    if total_jobs_collected >= 120:
                        break

                    try:
                        job_link = job.find_element(By.CLASS_NAME, "JobCard_jobTitle__GLyJ1").get_attribute("href")
                        if job_link in seen_jobs:
                            continue
                        seen_jobs.add(job_link)

                        extracted_title = job.find_element(By.CLASS_NAME, "JobCard_jobTitle__GLyJ1").text
                        employer_name = job.find_element(By.CLASS_NAME, "EmployerProfile_compactEmployerName__9MGcV").text
                        employer_rating = job.find_element(By.CLASS_NAME, "rating-single-star_RatingText__XENmU").text
                        job_location = job.find_element(By.CLASS_NAME, "JobCard_location__Ds1fM").text
                        job_salary = job.find_element(By.CLASS_NAME, "css-1bluz6i").text
                        job_age = job.find_element(By.CLASS_NAME, "JobCard_listingAge__jJsuc").text

                        print(f"🔹 {total_jobs_collected+1}. {extracted_title} at {employer_name}")

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

                        total_jobs_collected += 1

                    except Exception as e:
                        print(f"⚠️ Skipping one job: {e}")

                # Intentar clicar "Más empleos"
                try:
                    more_button = driver.find_element(By.XPATH, '//*[@id="left-column"]/div[2]/div/div/button')
                    driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
                    random_sleep(1, 2)
                    more_button.click()
                    print("🟢 Clicked 'Más empleos' to load more jobs.")
                except:
                    print("🔚 No more 'Más empleos' button or unable to click.")
                    break

    # Guardar CSV
    if all_jobs_data:
        csv_file = "glassdoor_jobs.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=all_jobs_data[0].keys())
            writer.writeheader()
            writer.writerows(all_jobs_data)

        print(f"\n✅ Job scraping complete. Data saved to {csv_file}.")
    else:
        print("⚠️ No job data collected.")

    driver.quit()


# RUN
login()
random_sleep(10, 20)
scrape_jobs()
print("✅ Scraping finished.")
