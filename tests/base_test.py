import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#run server
#run client
class Test(unittest.TestCase):
    def setUp(self):
        self.options = Options()
        self.options.add_experimental_option("detach",True)
        service=ChromeDriverManager(version="114.0.5735.90")
        service=service.install()#error
        service=Service(service)
        self.driver=webdriver.Chrome(service=service,options=self.options)
        self.driver.get("http://localhost:5173/")
    def test_click(self):
        links = self.driver.find_elements("xpath","//a[@href]")
        for link in links:
            if "Books" in link.get_attribute("innerHTML"):
                self.assertIsNotNone(link.click())
if __name__=="__main__":
    unittest.main()