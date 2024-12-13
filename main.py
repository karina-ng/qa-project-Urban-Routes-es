import data
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from data import phone_number
from helpers import retrieve_phone_code
from Pages import UrbanRoutesPage
from Pages import SelectRatesPage
from Pages import InsertPhoneNumber
from Pages import InsertCodeSMS
from Pages import AddCreditCard
from Pages import MessageForDriver
from Pages import OrderRequirements
from Pages import FindTaxi

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
