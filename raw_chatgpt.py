import time
import random
from contextlib import suppress
from seleniumbase import SB


# E302 FIX: Two blank lines before function definition
def random_pause(min_sec=1.0, max_sec=3.0):
    time.sleep(random.uniform(min_sec, max_sec))


# E305 FIX: Two blank lines after function definition
with SB(uc=True, incognito=True, headless=False) as sb:
    url = "https://chatgpt.com/"
    query = "Best Analytics Firms in India"
    sb.set_window_size(1280, 800)
    
    # Fixed line 30, 34, 38 by removing whitespace
    sb.uc_open_with_reconnect(url, reconnect_time=20)
    sb.activate_cdp_mode(url)
    random_pause(1, 2)
    sb.click_if_visible('button[aria-label="Close dialog"]')
    random_pause(0.5, 1.5)
    print('*** Input for ChatGPT: ***\n"%s"' % query)
    sb.press_keys("#prompt-textarea", query, slower=True)
    sb.click('button[data-testid="send-button"]')
    random_pause(3, 5)

    with suppress(Exception):
        # E501 FIX: Line split for compliance
        sb.wait_for_element_not_visible(
            'button[data-testid="stop-button"]', timeout=45
        )
        
        # E501 FIX: Line split for compliance
        chat = sb.find_element(
            '[data-message-author-role="assistant"] .markdown'
        )
        
        soup = sb.get_beautiful_soup(chat.get_html()).get_text("\n").strip()
        soup = soup.replace("\n\n\n", "\n\n")
        print("\n*** Response from ChatGPT: ***\n%s" % soup)
    
    random_pause(3, 5)
