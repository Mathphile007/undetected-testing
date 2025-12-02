import time
import random
from contextlib import suppress
from seleniumbase import Driver # IMPORTANT: Use 'Driver' instead of 'SB'

def random_pause(min_sec=1.0, max_sec=3.0):
    time.sleep(random.uniform(min_sec, max_sec))

# 1. Initialize the driver object outside the try block
# Pass the necessary arguments (uc=True, incognito=True, headless=True) here
driver = Driver(uc=True, incognito=True, headless=False)

try:
    url = "https://chatgpt.com/"
    query = "Best Analytics Firms in India"
    
    # Use the driver object (renamed from sb) for all actions
    driver.set_window_size(1280, 800)
    
    # 2. Open URL and Activate CDP Mode
    driver.uc_open_with_reconnect(url, reconnect_time=20)
    
    # Manual activation of CDP Mode using the driver object
    driver.activate_cdp_mode(url)
    random_pause(1, 2)
    
    # 3. Actions
    driver.click_if_visible('button[aria-label="Close dialog"]')
    random_pause(0.5, 1.5)
    print('*** Input for ChatGPT: ***\n"%s"' % query)
    
    driver.press_keys("#prompt-textarea", query, slower=True)
    driver.click('button[data-testid="send-button"]')
    random_pause(3, 5)

    # 4. Wait and Scrape
    with suppress(Exception):
        driver.wait_for_element_not_visible(
            'button[data-testid="stop-button"]', timeout=45
        )
        
        chat = driver.find_element(
            '[data-message-author-role="assistant"] .markdown'
        )
        
        soup = driver.get_beautiful_soup(chat.get_html()).get_text("\n").strip()
        soup = soup.replace("\n\n\n", "\n\n")
        print("\n*** Response from ChatGPT: ***\n%s" % soup)
    
    random_pause(3, 5)

except Exception as e:
    print(f"\nAn error occurred: {e}")

finally:
    # 5. MANUALLY QUIT THE BROWSER
    if 'driver' in locals() and driver:
        print("\n*** Closing browser session. ***")
        driver.quit()
