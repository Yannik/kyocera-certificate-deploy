#!/usr/bin/env python3

import os
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import sys
from time import sleep

def set_background(driver):
    driver.execute_script("""(function() {
        var style = document.createElement('style'), text = document.createTextNode('body { background: #fff }');
        style.setAttribute('type', 'text/css');
        style.appendChild(text);
        document.head.insertBefore(style, document.head.firstChild);
    })();""")

def stepshot(driver, screenshots, suffix):
#    set_background(driver)
    if screenshots:        
        driver.save_screenshot('selenium_printer' + str(suffix) + '.png')

screenshots = True
host = sys.argv[1]
certfile = sys.argv[2]
password = sys.argv[3]

logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(ch)


#driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])

options = Options()
options.add_argument("--headless")

profile = webdriver.FirefoxProfile()
profile.DEFAULT_PREFERENCES['frozen']['security.tls.version.enable-deprecated'] = True

capabilities = DesiredCapabilities.FIREFOX.copy()
capabilities['acceptInsecureCerts'] = True
driver = webdriver.Firefox(capabilities=capabilities, firefox_profile=profile, options=options)
driver.set_window_size(1024, 768)

driver.get(host)
stepshot(driver, screenshots, 1)

WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it("main"))

# Click "Anmelden" button
print("Clicking anmelden")
driver.find_element_by_class_name('w10pt').click()
stepshot(driver, screenshots, 2)

print("Entering password and submitting form")
password_field = driver.find_element_by_css_selector('input[name="arg02_Password"]')
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)
WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it("main"))
stepshot(driver, screenshots, 3)

print('Clicking "Allgemein" nav-button')
allgemein_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//div[@id="nav"]//a[contains(@onclick, "basic.htm")]'))
)
allgemein_button.click()
stepshot(driver, screenshots, 4)

print('Hovering "Zertifikate" menu')
certificate_nav_top_menu = driver.find_element_by_xpath('//div[@id="Certificates"]/parent::div')
action_chains = ActionChains(driver).move_to_element(certificate_nav_top_menu).perform()
stepshot(driver, screenshots, 5)

print('Click "Geraetezertifikat" button')
certificate_nav_submenu_elements = driver.find_elements_by_css_selector('div#Certificates a')
certificate_nav_submenu_elements[0].click()
stepshot(driver, screenshots, 6)

delete_button = driver.find_element_by_xpath('//input[contains(@onclick, "CtfDelConf")]')
if delete_button.get_attribute('disabled') is None:
  print('Click "Delete Certificate" button')
  delete_button.click()
  stepshot(driver, screenshots, 8)
  driver.find_element_by_css_selector('input[name="Delete"]').click()
  # Hier gibt's jetzt einen alert
  driver.switch_to.alert.accept()
  stepshot(driver, screenshots, 9)

print('Click "Importieren" button')
import_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[contains(@onclick, "Import")]'))
)
import_button.click()
stepshot(driver, screenshots, 10)

print('Selecting file and submitting form')
file_input = driver.find_element_by_css_selector('input[name="arg04_inputFile"]')
password_input = driver.find_element_by_css_selector('input#arg02_password')
file_input.send_keys(os.path.abspath(certfile))
stepshot(driver, screenshots, 11)
password_input.send_keys(Keys.RETURN)
# hier gibt's umgehend nach button click einen alert
driver.switch_to.alert.accept()
stepshot(driver, screenshots, 12)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//input[contains(@onclick, "Import") and @disabled]'))
)
stepshot(driver, screenshots, 13)

print('Opening "Zurücksetzen" page')
driver.find_element_by_xpath('//div[@id="leftcolmn"]//a[contains(@onclick, "Reset.htm")]').click()
stepshot(driver, screenshots, 14)

print('Clicking "Netzwerk neustarten" button')
driver.find_element_by_xpath('//input[@name="func" and @value="restartNetworkInterface"]/../input[@type="submit"]').click()

WebDriverWait(driver, 45).until_not(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src="../images/meter_45sec.gif"]'))
)
stepshot(driver, screenshots, 15)

driver.quit()
