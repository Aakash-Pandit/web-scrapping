from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import csv
import random
from itertools import zip_longest


driver_path = 'C:/ChromeWebDriver/chromedriver.exe'
url = 'https://main.sci.gov.in/case-status'
years_before = 20

driver = webdriver.Chrome(driver_path)
driver.get(url)

def submit_form():
    ###########################################################################################################################
    captcha_data = driver.find_element_by_id('cap').text.replace(" ", '')
    captcha_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='ansCaptcha']")))
    captcha_input.clear()
    captcha_input.send_keys(captcha_data)
    ###########################################################################################################################
    dairy_number = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='CaseDiaryNumber']")))
    dairy_number.clear()
    dairy_number_value = random.randint(1, 100)
    dairy_number.send_keys(dairy_number_value)
    ###########################################################################################################################
    select = Select(driver.find_element_by_id('CaseDiaryYear'))
    for index, op in enumerate(select.options):
        if index == years_before:
            select.select_by_value(op.text)
            break
    ###########################################################################################################################
    submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='getCaseDiary']"))).click()
###########################################################################################################################

def capture_value():
    row_title = []
    count = 1
    while True:
        
        try:
            row = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='collapse1']/div/table/tbody/tr[{count}]/td[1]")))
            row_title.append(row.text)
            count += 1
        except:
            break
    ###########################################################################################################################
    description = []
    count = 1
    while count < len(row_title) + 1:
        
        try:

            if count == 1 or count == 2:
                row_info = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='collapse1']/div/table/tbody/tr[{count}]/td[2]/div")))
                row_data = row_info.text
                description.append(row_data)

            elif count == 3 or count == 4 or count == 5 or count == 6 or count == 7:
                row_info = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='collapse1']/div/table/tbody/tr[{count}]/td[2]")))
                row_data = row_info.text
                description.append(row_data)

            elif count == 8 or count == 9 or count == 10 or count == 11:
                row_info = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='collapse1']/div/table/tbody/tr[{count}]/td[2]/p")))
                row_data = row_info.text
                description.append(row_data)

            elif count == 12:
                row = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='collapse1']/div/table/tbody/tr[{count}]/td[2]")))
                row_data = row.text
                description.append(row_data)

            else:
                pass

            count += 1
        except Exception as msg:
            break

    return (row_title, description)

###########################################################################################################################

def export_to_csv(row_title, description):
    final_output = zip_longest(row_title, description)
    with open('myfile.csv', 'w') as f_pointer:
        writer = csv.writer(f_pointer)
        for l in final_output:
            writer.writerow(l)

###########################################################################################################################
if __name__ == "__main__":
    submit_form()
    row_title, description = capture_value()
    export_to_csv(row_title, description)
###########################################################################################################################
