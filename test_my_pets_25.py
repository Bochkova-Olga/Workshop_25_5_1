import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/Users/X/driver./chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('nufnuf@mail.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    yield

    pytest.driver.quit()


def test_show_my_pets():
    pytest.driver.find_element(By.CSS_SELECTOR, 'span[class="navbar-toggler-icon"]').click()

    # проверка таблицы питомцев, явные ожидания элементов страницы.
    wait = WebDriverWait(pytest.driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"navbar-toggler-icon\"]")))

    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.CSS_SELECTOR, 'a[class="navbar-brand header2"]').text == "PetFriends"


def test_count_my_pets():
    pytest.driver.find_element(By.CSS_SELECTOR, 'span[class="navbar-toggler-icon"]').click()
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    count_rows = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    count_pets = pytest.driver.find_element(By.CSS_SELECTOR, 'div[class=".col-sm-4 left"]').text

    assert "Питомцев: " + len(count_rows).__str__() == count_pets.split('\n')[1]


def test_half_of_pet_photos():
    pytest.driver.find_element(By.CSS_SELECTOR, 'span[class="navbar-toggler-icon"]').click()
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    count_imgs = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    exists_images = 0
    # проверка карточек питомцев, неявные ожидания элемента - фото
    pytest.driver.implicitly_wait(10)
    myDynamicElement = pytest.driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')

    for i in range(len(count_imgs)):
        if count_imgs[i].get_attribute('src') != '':
            exists_images += 1

    assert len(count_imgs) / 2 < exists_images


def test_attribute_pets():
    pytest.driver.find_element(By.CSS_SELECTOR, 'span[class="navbar-toggler-icon"]').click()
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    # проверка карточек питомцев, неявные ожидания элемента - name
    pytest.driver.implicitly_wait(10)
    myDynamicElement = pytest.driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')

    breed = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    # проверка карточек питомцев, неявные ожидания элемента - breed
    pytest.driver.implicitly_wait(10)
    myDynamicElement = pytest.driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')

    ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    # проверка карточек питомцев, неявные ожидания элемента - ages
    pytest.driver.implicitly_wait(10)
    myDynamicElement = pytest.driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    for i in range(len(names)):
        assert names[i].text != ''
        assert breed[i].text != ''
        assert ages[i].text != ''


def test_diff_name_pets():
    pytest.driver.find_element(By.CSS_SELECTOR, 'span[class="navbar-toggler-icon"]').click()
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    list_names = []
    for i in range(len(names)):
        list_names.append(names[i].text)

    visited = set()
    dup = [x for x in list_names if x in visited or (visited.add(x) or False)]

    assert len(dup) > 0


def test_diff_attribute_pets():
    pytest.driver.find_element(By.CSS_SELECTOR, 'span[class="navbar-toggler-icon"]').click()
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    breed = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    list_attr = []

    for i in range(len(names)):
        list_attr.append(names[i].text + "" + breed[i].text + "" + ages[i].text)

    visited = set()
    dup = [x for x in list_attr if x in visited or (visited.add(x) or False)]

    assert len(dup) == 0





