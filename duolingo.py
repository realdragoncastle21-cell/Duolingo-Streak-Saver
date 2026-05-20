import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Setup Headless Chrome Options (Crucial for GitHub Actions)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Runs without a physical screen
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

# Grab secrets
USERNAME = os.environ.get("DUOLINGO_USERNAME")
PASSWORD = os.environ.get("DUOLINGO_PASSWORD")

if not USERNAME or not PASSWORD:
    print("❌ Error: Secrets are missing!")
    exit(1)

driver = webdriver.Chrome(options=chrome_options)

try:
    print("🌐 Opening Duolingo...")
    driver.get("https://www.duolingo.com")
    time.path(3)

    # Click "I ALREADY HAVE AN ACCOUNT"
    print("🖱️ Clicking login button...")
    login_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='have-account']"))
    )
    login_btn.click()
    time.sleep(2)

    # Type Username and Password
    print("⌨️ Entering credentials...")
    user_input = driver.find_element(By.CSS_SELECTOR, "input[data-test='email-input']")
    pass_input = driver.find_element(By.CSS_SELECTOR, "input[data-test='password-input']")
    
    user_input.send_keys(USERNAME)
    pass_input.send_keys(PASSWORD)
    time.sleep(1)

    # Submit Login
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[data-test='register-button']")
    submit_btn.click()
    
    print("⏳ Waiting for dashboard to load...")
    # Wait until the main learning path shows up to confirm a successful login session
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test='player-next'], [data-test='home-nav']"))
    )
    
    print("🎉 Successfully logged in as a real browser user! Streak session synced.")

except Exception as e:
    print(f"❌ Automation failed: {str(e)}")
    exit(1)

finally:
    driver.quit()
