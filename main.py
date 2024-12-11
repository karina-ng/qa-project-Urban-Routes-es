import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time
from data import phone_number


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
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

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

# Prueba para configurar la direccion
    def test_set_route(self):
        # Ingresa los valores para seleccionar la ruta
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

# Prueba para seleccionar la tarifa Comfort
    def test_order_a_taxi(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(SelectRatesPage.taxi_button))
        rate_page = SelectRatesPage(self.driver)
        rate_page.select_comfort_rate()
        assert rate_page.check_if_comfort_rate_is_selected() == True

# Prueba para rellenar el campo de numero telefonico
    def test_insert_phone_number(self):
        phone_page = InsertPhoneNumber(self.driver)
        number = data.phone_number
        phone_page.insert_phone_number(number)
        assert phone_page.get_number() == phone_number

    def test_insert_code_sms(self):
        code_page = InsertCodeSMS(self.driver)
        code_sms = retrieve_phone_code(driver=self.driver)
        code_page.insert_code_sms(code_sms)
        return code_sms

# Prueba para agregar una tarjeta de credito
    def test_add_credit_card(self):
        payment_page = AddCreditCard(self.driver)
        card_number = data.card_number
        card_code = data.card_code
        payment_page.add_credit_card(card_number, card_code)
        assert payment_page.check_if_close_button_is_enabled()

# Prueba para escribir un mensaje al conductor
    def test_message_for_driver(self):
        message_page = MessageForDriver(self.driver)
        message_for_driver = data.message_for_driver
        message_page.set_message(message_for_driver)
        assert message_page.get_message() == message_for_driver

# Prueba para pedir manta y 2 helados
    def test_order_requirements(self):
        requirements_page = OrderRequirements(self.driver)
        requirements_page.set_order_requirements()
        assert requirements_page.check_if_blanket_is_selected()
        assert requirements_page.get_frozen_count() == 2

# Prueba para confirmar que aparece el modal de busqueda de taxi
    def test_wait_for_a_taxi(self):
        taxi_page = FindTaxi(self.driver)
        taxi_page.find_taxi_modal()
        assert taxi_page.wait_taxi_modal() == "Buscar automóvil"


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
