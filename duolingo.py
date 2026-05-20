import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Headless Chrome Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

USERNAME = os.environ.get("DUOLINGO_USERNAME")
PASSWORD = os.environ.get("DUOLINGO_PASSWORD")

if not USERNAME or not PASSWORD:
    print("❌ Error: Secrets are missing!")
    exit(1)

driver = webdriver.Chrome(options=chrome_options)

try:
    print("🌐 Opening Duolingo...")
    driver.get("https://www.duolingo.com")
    time.sleep(3)

    print("🖱️ Clicking login button...")
    login_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='have-account']"))
    )
    login_btn.click()
    time.sleep(2)

    print("⌨️ Entering credentials...")
    user_input = driver.find_element(By.CSS_SELECTOR, "input[data-test='email-input']")
    pass_input = driver.find_element(By.CSS_SELECTOR, "input[data-test='password-input']")
    
    user_input.send_keys(USERNAME)
    pass_input.send_keys(PASSWORD)
    time.sleep(1)

    print("🚀 Submitting credentials...")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[data-test='register-button']")
    submit_btn.click()
    
    print("⏳ Waiting for dashboard to load...")
    time.sleep(10)  # Give the dashboard a solid 10 seconds to fully process the login redirect

    # Check multiple common dashboard elements to confirm we are in
    current_url = driver.current_url
    print(f"📍 Current page URL: {current_url}")
    
    if "learn" in current_url or "setup" in current_url:
        print("🎉 Successfully logged in as a real browser user! Streak session synced.")
    else:
        # Save a picture of the page to find layout changes
        driver.save_screenshot("error_page.png")
        print("⚠️ Dashboard layout mismatch. Saved 'error_page.png' for verification.")

except Exception as e:
    print(f"❌ Automation failed: {str(e)}")
    try:
        driver.save_screenshot("crash_page.png")
    except:
        pass
    exit(1)

finally:
    driver.quit()
