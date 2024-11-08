import time
from selenium.webdriver.common.by import By

class SharePoint:
    
    
    def handle_login(self,credentials=list,drive=str):
        url='https://nskkogyo.sharepoint.com/sites/2021'
        
        self.driver = drive
        # Assuming the login page has input fields with IDs 'username' and 'password'
        self.driver.get(url)

        username = credentials[0]
        password = credentials[1]
        time.sleep(2.5)
        # Find the username input field on the login page
        self.driver.find_element(By.XPATH, '//*[@id="i0116"]').clear()

        self.driver.find_element(By.XPATH, '//*[@id="i0116"]').send_keys(username)
        self.driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
        time.sleep(1.5)
        # Find the password input field on the login page
        if self.driver.find_element(By.XPATH, '//*[@id="i0118"]').text:
            self.driver.find_element(By.XPATH, '//*[@id="i0118"]').clear()
        self.driver.find_element(By.XPATH, '//*[@id="i0118"]').send_keys(password)
        self.driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
        self.driver.find_element(By.XPATH, '//*[@id="KmsiCheckboxField"]').click()
        time.sleep(1.5)
        self.driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
        time.sleep(2)
        print('Logged in to Sharepoint\nPlease wait.....')
        
        