import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_experimental_option("detach",True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

driver.get("http://www.neuralnine.com/")
driver.maximize_window()

links = driver.find_elements("xpath","//a[@href]")
for link in links:
    if "Books" in link.get_attribute("innerHTML"):
        link.click()
        break

book_links= driver.find_elements("xpath",
                                 "//div[contains(@class,'elementor-column-wrap')][.//h2[text()[contains(., '7 IN 1')]]][count(.//a)=2]//a")

for book_link in book_links:
    print (book_link.get_attribute("href"))

book_links[0].click()

driver.switch_to.window(driver.window_handles[1])

time.sleep(3)


buttons = driver.find_elements("xpath","//a[.//span[text()[contains(., 'Pasta blanda')]]]//span[text()[contains(.,'$')]]")

expected_price_range = "US$31.05 - US$39.99"

for button in buttons:
    print(button.get_attribute("innerHTML"))
    print()

@pytest.fixture(scope="session")
def price_Check():
    try:
        for button in buttons:
            button_text = button.get_attribute("innerHTML")
            print(button_text)
            assert expected_price_range in button_text, f"El rango de precio esperado no está presente en: {button_text}"
            print("Aserción exitosa:", button_text)
            return True
    except AssertionError as e:
        print("Error en la aserción:", str(e))
        return False


# Marcar el fixture como prueba
def test_price_Check(price_Check):
    if price_Check == True:
        pass
    else:
        pytest.fail("El test Fallo")

# Cerrar el driver al finalizar las pruebas
def teardown_module():
    driver.quit()