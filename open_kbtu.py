import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

USERNAME = os.getenv("KBTU_USERNAME")
PASSWORD = os.getenv("KBTU_PASSWORD")
REFRESH_INTERVAL = 35  # секунд

def main():
    print("Starting...")
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")  # без GUI для сервера
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    print("Launching Chrome (headless)...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)

    try:
        # Логин
        driver.get("https://wsp.kbtu.kz/RegistrationOnline")
        print("Page opened successfully!")

        username_xpath = "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div[2]/div/table/tbody/tr[1]/td[3]/div/input"
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, username_xpath)))

        password_xpath = "/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div[2]/div/table/tbody/tr[2]/td[3]/input"
        password_field = driver.find_element(By.XPATH, password_xpath)

        username_field.clear()
        username_field.send_keys(USERNAME)
        print(f"Entered username: {USERNAME}")

        password_field.clear()
        password_field.send_keys(PASSWORD)
        print("Entered password")

        login_button = driver.find_element(By.XPATH, "//div[contains(@class, 'v-button') and contains(@class, 'primary')]")
        login_button.click()
        print("Clicked login button")

        time.sleep(3)
        print(f"Logged in! URL: {driver.current_url}")

        # Цикл обновления
        refresh_count = 0
        while True:
            refresh_count += 1
            print(f"\n[{time.strftime('%H:%M:%S')}] Refresh #{refresh_count}")

            driver.refresh()
            time.sleep(3)  # ждём загрузку страницы

            # Ищем кнопку "Отметиться"
            try:
                otmetitsya_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@class='v-button-caption' and text()='Отметиться']/ancestor::div[contains(@class, 'v-button')]"))
                )
                print(">>> FOUND 'Отметиться' button! Clicking...")
                otmetitsya_button.click()
                print(">>> CLICKED! <<<")
                time.sleep(2)
            except:
                print("Button 'Отметиться' not available")

            print(f"Waiting {REFRESH_INTERVAL} seconds...")
            time.sleep(REFRESH_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    main()
