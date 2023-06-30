import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
#run server
#run client
class Test(unittest.TestCase):
    def setUp(self):
        self.options = Options()
        self.options.add_experimental_option("detach",True)
        self.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=self.options)
        self.driver.get("https://www.youtube.com/")
    def test_click(self):
        links = self.driver.find_elements("xpath","//a[@href]")
        for link in links:
            if "Books" in link.get_attribute("innerHTML"):
                self.assertIsNotNone(link.click())
if __name__=="__main__":
    unittest.main()


