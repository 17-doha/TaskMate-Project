# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.remote.webelement import WebElement
# import time


# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.get("http://127.0.0.1:8000/")
# driver.maximize_window()


# #  sign up
# time.sleep(1)

# signup: WebElement = driver.find_element(By.XPATH, '/html/body/div/a[1]')
# signup.click()

# time.sleep(1)

# firstname: WebElement = driver.find_element(By.XPATH,'//*[@id="first-name"]')
# firstname.send_keys("mariam")

# lastname: WebElement = driver.find_element(By.XPATH,'//*[@id="last-name"]')
# lastname.send_keys("yasser")

# email: WebElement = driver.find_element(By.XPATH,'//*[@id="email"]')
# email.send_keys("s-mariam.elghandour@zewailcity.edu.eg")

# password: WebElement = driver.find_element(By.XPATH,'//*[@id="password"]')
# password.send_keys("12345678")

# pass_conf: WebElement = driver.find_element(By.XPATH,'//*[@id="confirm-password"]')
# pass_conf.send_keys("12345678")

# time.sleep(1)

# confirm: WebElement = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/button')
# confirm.click()

# time.sleep(2)

# # login

# email_login: WebElement = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/input[2]')
# email_login.send_keys("s-mariam.elghandour@zewailcity.edu.eg")

# pas: WebElement = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/input[3]')
# pas.send_keys("12345678")

# time.sleep(1)

# start: WebElement = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/button')
# start.click()


# time.sleep(3)

# # profile tests

# # # enter
# # profile: WebElement = driver.find_element(By.XPATH, '/html/body/div/main/header/div[2]/div/a/i')
# # profile.click()

# # time.sleep(1)

# # # edit with right stuff

# # edit: WebElement = driver.find_element(By.XPATH, '//*[@id="editBtn"]/i')
# # edit.click()

# # time.sleep(1)

# # fname_right: WebElement = driver.find_element(By.XPATH,'//*[@id="firstName"]')
# # fname_right.send_keys("testname")

# # phone_right: WebElement = driver.find_element(By.XPATH,'//*[@id="phone_number"]')
# # phone_right.send_keys("0101233")

# # lname_right: WebElement = driver.find_element(By.XPATH,'//*[@id="lastName"]')
# # lname_right.send_keys("testname")

# # age_right: WebElement = driver.find_element(By.XPATH,'//*[@id="age"]')
# # age_right.clear()
# # age_right.send_keys("12")

# # save_right: WebElement = driver.find_element(By.XPATH, '//*[@id="saveBtn"]')
# # save_right.click()


# # time.sleep(1)

# # # edit with wrong stuff


# # # try 1
# # edit: WebElement = driver.find_element(By.XPATH, '//*[@id="editBtn"]/i')
# # edit.click()

# # time.sleep(1)

# # fname_wrong: WebElement = driver.find_element(By.XPATH,'//*[@id="firstName"]')
# # fname_wrong.send_keys("")

# # save_wrong: WebElement = driver.find_element(By.XPATH, '//*[@id="saveBtn"]')
# # save_wrong.click()

# # time.sleep(1)


# # # try 2

# # edit: WebElement = driver.find_element(By.XPATH, '//*[@id="editBtn"]/i')
# # edit.click()

# # phone_wrong: WebElement = driver.find_element(By.XPATH,'//*[@id="phone_number"]')
# # phone_wrong.send_keys("scsc")

# # save_wrong: WebElement = driver.find_element(By.XPATH, '//*[@id="saveBtn"]')
# # save_wrong.click()

# # time.sleep(1)



# # # try 3
# # edit: WebElement = driver.find_element(By.XPATH, '//*[@id="editBtn"]/i')
# # edit.click()

# # lname_wrong: WebElement = driver.find_element(By.XPATH,'//*[@id="lastName"]')
# # lname_wrong.send_keys("")

# # save_wrong: WebElement = driver.find_element(By.XPATH, '//*[@id="saveBtn"]')
# # save_wrong.click()

# # time.sleep(1)


# # # try 4
# # edit: WebElement = driver.find_element(By.XPATH, '//*[@id="editBtn"]/i')
# # edit.click()

# # age_wrong: WebElement = driver.find_element(By.XPATH,'//*[@id="age"]')
# # age_wrong.send_keys("dsds")

# # save_wrong: WebElement = driver.find_element(By.XPATH, '//*[@id="saveBtn"]')
# # save_wrong.click()

# # time.sleep(1)


# # # badges

# # seeall: WebElement = driver.find_element(By.XPATH, '//*[@id="showAllBtn"]')
# # seeall.click()

# # time.sleep(1)


# # # delete account

# # delete: WebElement = driver.find_element(By.XPATH, '//*[@id="deleteBtn"]')
# # delete.click()

# # time.sleep(1)

# # cancel: WebElement = driver.find_element(By.XPATH, '//*[@id="cancelBtn"]')
# # cancel.click()

# # time.sleep(1)

# # delete: WebElement = driver.find_element(By.XPATH, '//*[@id="deleteBtn"]')
# # delete.click()

# # time.sleep(1)

# # confirm_delete: WebElement = driver.find_element(By.XPATH, '//*[@id="confirmBtn"]')
# # confirm_delete.click()

# # time.sleep(1)


# # # login in invalid


# # email_login: WebElement = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/input[2]')
# # email_login.send_keys("s-mariam.elghandour@zewailcity.edu.eg")

# # pas: WebElement = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/input[3]')
# # pas.send_keys("12345678")

# # time.sleep(1)

# # start: WebElement = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/button')
# # start.click()


# # time.sleep(1)


# # # sign up invalid 

# # # try 1

# # go_signup: WebElement = driver.find_element(By.XPATH, '/html/body/div/div[2]/p[2]/a')
# # go_signup.click()

# # time.sleep(1)


# # firstname: WebElement = driver.find_element(By.XPATH,'//*[@id="first-name"]')
# # firstname.send_keys("mariam")

# # lastname: WebElement = driver.find_element(By.XPATH,'//*[@id="last-name"]')
# # lastname.send_keys("yasser")

# # email: WebElement = driver.find_element(By.XPATH,'//*[@id="email"]')
# # email.send_keys("s-mariam.elghandour@zewailcity.edu.eg")

# # # not matching

# # password: WebElement = driver.find_element(By.XPATH,'//*[@id="password"]')
# # password.send_keys("12345")

# # pass_conf: WebElement = driver.find_element(By.XPATH,'//*[@id="confirm-password"]')
# # pass_conf.send_keys("12345678")

# # time.sleep(1)

# # confirm: WebElement = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/button')
# # confirm.click()

# # time.sleep(2)


# # # try 2

# # firstname: WebElement = driver.find_element(By.XPATH,'//*[@id="first-name"]')
# # firstname.send_keys("mariam")

# # # no last name
# # lastname: WebElement = driver.find_element(By.XPATH,'//*[@id="last-name"]')
# # lastname.clear()
# # # lastname.send_keys("yasser")

# # email: WebElement = driver.find_element(By.XPATH,'//*[@id="email"]')
# # email.send_keys("s-mariam.elghandour@zewailcity.edu.eg")


# # password: WebElement = driver.find_element(By.XPATH,'//*[@id="password"]')
# # password.send_keys("12345678")

# # pass_conf: WebElement = driver.find_element(By.XPATH,'//*[@id="confirm-password"]')
# # pass_conf.send_keys("12345678")

# # time.sleep(1)

# # confirm: WebElement = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/button')
# # confirm.click()

# # time.sleep(2)


# # # reenter right stuff
# # lastname: WebElement = driver.find_element(By.XPATH,'//*[@id="last-name"]')
# # lastname.send_keys("yasser")


# # confirm: WebElement = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/button')
# # confirm.click()

# # time.sleep(2)

# # #  login with wrong password

# # email_login: WebElement = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/input[2]')
# # email_login.send_keys("s-mariam.elghandour@zewailcity.edu.eg")

# # pas: WebElement = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/input[3]')
# # pas.send_keys("12348")

# # time.sleep(1)

# # start: WebElement = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/button')
# # start.click()


# # time.sleep(1)