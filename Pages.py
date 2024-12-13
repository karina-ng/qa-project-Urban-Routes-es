from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


class UrbanRoutesPage:
    # Localizadores y funciones de la paginas
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver
        time.sleep(3)

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

# clase para la pagina de seleccion de tarifa
class SelectRatesPage:
    taxi_button = (By.CLASS_NAME, 'button.round')
    comfort_icon = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]/div[2]')
    select_phone = (By.CLASS_NAME, 'np-text')

    def __init__(self, driver):
        self.driver = driver

    def order_a_taxi(self):
        self.driver.find_element(*self.taxi_button).click()
        WebDriverWait(self.driver, 3).until(expected_conditions.presence_of_element_located(self.comfort_icon))

    def click_comfort_rate(self):
        self.driver.find_element(*self.comfort_icon).click()

    def check_if_comfort_rate_is_selected(self):
        return self.driver.find_element(*self.comfort_icon).is_displayed()

    def select_number(self):
        self.driver.find_element(*self.select_phone).click()

    def select_comfort_rate(self):
        self.order_a_taxi()
        self.click_comfort_rate()
        self.check_if_comfort_rate_is_selected()
        self.select_number()


# clase para la ventana de introducir numero telefonico
class InsertPhoneNumber:
    phone_field = (By.XPATH, '//*[@id="phone"]')
    submit_button = (By.CLASS_NAME, 'button.full')

    def __init__(self, driver):
        self.driver = driver

    def set_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_field).send_keys(phone_number)

    def submit_number(self):
        self.driver.find_element(*self.submit_button).click()

    def get_number(self):
        return self.driver.find_element(*self.phone_field).get_property('value')

    def insert_phone_number(self, phone_number):
        self.set_phone_number(phone_number)
        self.submit_number()


# clase para ventana de introducir el codigo SMS
class InsertCodeSMS:
    code_field = (By.CSS_SELECTOR, '[placeholder="xxxx"]')
    submit_code = (By.XPATH, '//*[text()="Confirmar"]')

    def __init__(self, driver):
        self.driver = driver
        time.sleep(3)

    def set_code_sms(self, code):
        self.driver.find_element(*self.code_field).send_keys(code)

    def submit_code_sms(self):
        self.driver.find_element(*self.submit_code).click()

    def insert_code_sms(self, code):
        self.set_code_sms(code)
        self.submit_code_sms()

# clase para ventana "Agregar tarjeta de credito"
class AddCreditCard:
    payment_button = (By.CLASS_NAME, 'pp-text')
    add_card = (By.CSS_SELECTOR, '[class="pp-plus"]')
    card_field = (By.CSS_SELECTOR, '[id="number"]')
    card_code_field = (By.CSS_SELECTOR, '[name="code"]')
    outside_section = (By.CLASS_NAME, 'card-wrapper')
    add_button = (By.XPATH, '//*[text()="Agregar"]')
    close_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')

    def __init__(self, driver):
        self.driver = driver

    def set_payment_method(self):
        self.driver.find_element(*self.payment_button).click()

    def add_new_card(self):
        self.driver.find_element(*self.add_card).click()

    def set_card_number(self, card_number):
        self.driver.find_element(*self.card_field).send_keys(card_number)

    def set_card_code(self, card_code):
        self.driver.find_element(*self.card_code_field).send_keys(card_code)

    def click_outside(self):
        self.driver.find_element(*self.outside_section).click()

    def select_add_button(self):
        self.driver.find_element(*self.add_button).click()

    def check_if_close_button_is_enabled(self):
        return self.driver.find_element(*self.close_button).is_enabled()

    def close_card_window(self):
        self.driver.find_element(*self.close_button).click()

    def add_credit_card(self, card_number, card_code):
        self.set_payment_method()
        self.add_new_card()
        self.set_card_number(card_number)
        self.set_card_code(card_code)
        self.click_outside()
        self.select_add_button()
        self.close_card_window()


# clase para agregar un mensaje al conductor
class MessageForDriver:
    message_field = (By.ID, 'comment')

    def __init__(self, driver):
        self.driver = driver

    def set_message(self, message_for_driver):
        self.driver.find_element(*self.message_field).send_keys(message_for_driver)

    def get_message(self):
        return self.driver.find_element(*self.message_field).get_property('value')

# clase para seleccionar los requisitos del pedido
class OrderRequirements:
    blanket_slider = (By.CSS_SELECTOR, '.reqs-body .r-type-switch:nth-of-type(1) .slider')
    frozen_counter = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')

    def __init__(self, driver):
        self.driver = driver

    def select_blanket(self):
        self.driver.find_element(*self.blanket_slider).click()

    def check_if_blanket_is_selected(self):
        return self.driver.find_element(*self.blanket_slider).is_enabled()

    def add_two_frozen(self):
        self.driver.find_element(*self.frozen_counter).click()

    def set_order_requirements(self):
        self.select_blanket()
        self.add_two_frozen()
        self.add_two_frozen()

    def get_frozen_count(self):
        counter_value = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')
        frozen_count = int(counter_value.text)
        return frozen_count

# clase para la ventana "Buscar un taxi"
class FindTaxi:
    order_taxi_button = (By.CLASS_NAME, 'smart-button-main')
    find_taxi = (By.CLASS_NAME, 'order-header-title')

    def __init__(self,driver):
        self.driver = driver

    def order_a_taxi(self):
        self.driver.find_element(*self.order_taxi_button).click()

    def wait_taxi_modal(self):
        self.driver.find_element(*self.find_taxi).is_enabled()
        return self.driver.find_element(*self.find_taxi).text

    def find_taxi_modal(self):
        self.order_a_taxi()
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(FindTaxi.find_taxi))
        self.wait_taxi_modal()