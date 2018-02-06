from selenium import webdriver
import pyvirtualdisplay

with pyvirtualdisplay.Display(visible=True):
    browser = webdriver.Firefox()

    # Sets the width and height of the current window
    browser.set_window_size(1366, 768)

    # Open the URL
    browser.get('http://www.vionblog.com/')

    # set timeouts
    browser.set_script_timeout(30)
    browser.set_page_load_timeout(30)  # seconds

    # Take screenshot
    browser.save_screenshot('vionblog.png')

    # quit browser
    browser.quit()

