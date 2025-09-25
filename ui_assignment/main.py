import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestUI(unittest.TestCase):
    def setUp(self):
        self.ui_test_url = "https://github.com/hahow/hahow-recruit"

        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def test_get_contributors(self):
        expected_cnt = 14
        expected_names = {
            "@hrs113355",
            "@yinwilliam",
            "@yade-hahow",
            "@henry40408",
            "@tommy60703",
            "@jackblackevo",
            "@dannnyliang",
            "@choznerol",
            "@okischuang",
            "@weihanglo",
            "@gcobc12677",
            "@D50000",
            "@EastSun5566",
            "@SoftwareSing",
        }

        driver = self.driver
        driver.get(self.ui_test_url)

        wait = WebDriverWait(self.driver, 10)

        contributors_xpath = "//div[contains(@class, 'BorderGrid-cell')]//img"
        wait.until(EC.presence_of_element_located((By.XPATH, contributors_xpath)))
        contributors = driver.find_elements(By.XPATH, contributors_xpath)

        names = set()
        for c in contributors:
            alt_text = c.get_attribute("alt")
            names.add(alt_text)

        self.assertEqual(len(contributors), expected_cnt)
        self.assertEqual(names, expected_names)

        for name in names:
            print(name[1:])  # exclude the convension at ("@") mark

        driver.quit()

    def test_frontend_page(self):
        driver = self.driver
        driver.get(self.ui_test_url)

        wait = WebDriverWait(self.driver, 10)

        frontend_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "frontend.md"))
        )
        frontend_link.click()

        imgs_xpath = "//div[.//text()='Wireframe'][1]/following-sibling::*[following-sibling::div]//img"
        wait.until(EC.presence_of_element_located((By.XPATH, imgs_xpath)))
        # get list of images between two `divs` with first one is `Wireframe`
        imgs = driver.find_elements(By.XPATH, imgs_xpath)

        self.assertGreater(len(imgs), 0)

        driver.quit()

    def test_check_latest_committer(self):
        expected_name = "yinwilliam"

        driver = self.driver
        driver.get(self.ui_test_url)
        wait = WebDriverWait(self.driver, 10)
        latest_commit_a = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[contains(@class,'AuthorAvatar-module__authorHoverableLink')]",
                )
            )
        )
        self.assertEqual(latest_commit_a.text, expected_name)
        driver.quit()


if __name__ == "__main__":
    unittest.main()
