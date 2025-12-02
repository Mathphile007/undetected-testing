# Import the random module for human-like delays
import time
import random
from contextlib import suppress
from seleniumbase import SB

# Function for random, non-fixed delay
def random_pause(min_sec=1.0, max_sec=3.0):
    time.sleep(random.uniform(min_sec, max_sec))

# --- SCRIPT EXECUTION ---

# Use the most stealthy configuration: 
# uc=True (Undetected Chrome), incognito=True (clean session), headless=False (for local dev)
# NOTE: Set headless=True when running in GitHub Actions!
with SB(uc=True, incognito=True, headless=False) as sb:
    
    url = "https://chatgpt.com/"
    query = "Best Analytics Firms in India"
    
    # 1. Set a common, non-default window size to bypass fingerprinting checks
    # This must be done BEFORE opening the URL.
    sb.set_window_size(1280, 800)

    # 2. Open URL and Activate CDP Mode
    # The reconnect_time argument is used for stability in older SB versions.
    sb.uc_open_with_reconnect(url, reconnect_time=20)
    sb.activate_cdp_mode(url)
    random_pause(1, 2) # Human-like pause after activation

    # 3. REMOVED OBSOLETE CAPTCHA HANDLERS
    # The uc_gui_click_captcha and uc_gui_handle_captcha methods are often designed 
    # for specific older CAPTCHAs and can break the session if not present.
    # We rely on UC/CDP to handle modern defenses seamlessly.
    
    # 4. Handle Modals
    sb.click_if_visible('button[aria-label="Close dialog"]')
    random_pause(0.5, 1.5)

    # 5. Type Query and Send
    print('*** Input for ChatGPT: ***\n"%s"' % query)
    
    # Use slower=True to simulate human typing speed (CRUCIAL for anti-detection)
    sb.press_keys("#prompt-textarea", query, slower=True)
    sb.click('button[data-testid="send-button"]')
    
    # Wait for the AI to start responding
    random_pause(3, 5)

    # 6. Wait for Response Completion
    with suppress(Exception):
        # Increased timeout to 45 seconds for robustness
        sb.wait_for_element_not_visible(
            'button[data-testid="stop-button"]', timeout=45
        )

    # 7. Scrape and Clean the Response
    try:
        chat = sb.find_element('[data-message-author-role="assistant"] .markdown')
        # Use get_text("\n") to better preserve markdown structure (lists, etc.)
        soup = sb.get_beautiful_soup(chat.get_html()).get_text("\n").strip()
        
        # Cleaning the text
        soup = soup.replace("\n\n\n", "\n\n")
        print("\n*** Response from ChatGPT: ***\n%s" % soup)
        
    except Exception as e:
        print(f"\n❌ Error: Failed to find or scrape the final message element: {e}")
        sb.save_screenshot("scraping_failure.png")
    
    random_pause(3, 5)
