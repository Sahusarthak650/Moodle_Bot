#BEFORE USE
#API KEY MUST BE FILLED AT LINE 13
#MOODLE LOGIN CREDENTILAS MUST BE FILLED AT LINES 61 62

#importing webdriver 
from selenium import webdriver 
from selenium.webdriver.common.by import By 

import sys
from math import trunc 
import re
import time
import openai
openai.api_key = "Your API key"

def extract_id_of_radio_button(input_string):
    pattern = r'"([^"]*)"'
    matches = re.findall(pattern, input_string)
    print(matches)
    return matches

def getAns(i):
    max_attempts = 5  # Set a maximum number of attempts to avoid infinite looping
    
    for _ in range(max_attempts):
        try:
            driver.implicitly_wait(5)
            que = (driver.find_elements(By.CLASS_NAME, "qtext")[i].get_attribute("innerHTML")) + (driver.find_elements(By.CLASS_NAME, "ablock")[i].get_attribute("innerHTML")) # get question's HTML
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Give id of radio button of correct answer in double quotes:\n" + que}],
            )
            print(type(que))
            print("-------------------")
            print(response.choices[0].message.content)
            answer_id = extract_id_of_radio_button(response.choices[0].message.content)
            return answer_id
        
        except Exception as e:
            print("Error:", e)
            print("Waiting....")
            time.sleep(21)
            print("Done Waiting")
    
    print("Maximum attempts reached, exiting without answer.")
    return None




ts=time.time() 
trunc(ts)  

#initializing webdriver variable
driver = webdriver.Chrome()
#URL of the website
#opening moodle Dashboard in the browser 
url = "http://moodle.mitsgwalior.in/my/" 
driver.get(url) 

#find login fields and fill credentials
driver.find_element(By.ID,"username").send_keys('Your Username') 
driver.find_element(By.ID,"password").send_keys('Your Password') 
# click login button 
driver.find_element(By.ID,"loginbtn").click()  
 
driver.implicitly_wait(8)
quizzes = driver.find_elements(By.LINK_TEXT,"Attempt quiz now")  #looking for ongoing quizzes
if len(quizzes)==0:
    print("No ongoing quizzes")
    driver.quit()
    sys.exit()

quizzes[0].click()
driver.find_element(By.XPATH,"//button[@type='submit']").click()  #clicked attempt quiz
driver.find_element(By.XPATH,"//input[@value='Start attempt']").click()  #clicked confirm button

#mark answers until finished
while("Attempt summary" not in driver.title):
    
    for i in range(len(driver.find_elements(By.CLASS_NAME,"qtext"))):
        ans = getAns(i)  #get answer using openai api
        driver.find_element(By.ID,ans[0]).click()
    if len(driver.find_elements(By.XPATH,"//input[@value='Next page']")) == 0:
        driver.find_element(By.XPATH,"//input[@name='next']").click()
    else:
        driver.find_element(By.XPATH,"//input[@value='Next page']").click()    #next question

driver.find_elements(By.XPATH,"//button[@type='submit']")[1].click()  #summary wale pe click
driver.find_element(By.XPATH,"//input[@value='Submit all and finish']").click()    #last click

driver.find_element(By.LINK_TEXT,"Finish review")

driver.quit()