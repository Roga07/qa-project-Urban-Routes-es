import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from locators import UrbanRoutesLocators

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

    #Constructor
    def __init__(self, driver):
        self.driver = driver

    #Punto de pàrtida y punto de llegada
    def set_from(self, from_address):
        self.driver.find_element(*UrbanRoutesLocators.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*UrbanRoutesLocators.to_field).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
    def get_from(self):
        return self.driver.find_element(*UrbanRoutesLocators.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*UrbanRoutesLocators.to_field).get_property('value')


    #Seleciona el tipo de taxi
    def select_taxi(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*UrbanRoutesLocators.select_taxi_xpath).click()

    def select_comfort_rate(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*UrbanRoutesLocators.button_comfort_xpath).click()

    #Agregar nuemero de telefono
    def select_number_button(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*UrbanRoutesLocators.set_phone_number).click()

    def add_phone_number(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*UrbanRoutesLocators.number).send_keys(data.phone_number)

    def set_phone(self):
        self.driver.implicitly_wait(20)
        self.select_number_button()
        self.driver.implicitly_wait(20)
        self.add_phone_number()

    def click_on_next_button(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*UrbanRoutesLocators.button_next_xpath).click()

    def send_cell_info(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*UrbanRoutesLocators.button_confirm_xpath).click()

    def get_phone(self):
        return self.driver.find_element(*UrbanRoutesLocators.input_phone_number).get_property('value')

    def code_number(self):
        self.driver.implicitly_wait(15)
        phone_code = retrieve_phone_code(driver=self.driver)
        self.driver.implicitly_wait(15)
        self.driver.find_element(*UrbanRoutesLocators.input_code).send_keys(phone_code)

    #Agregar metodo de pago

    def payment_method(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*UrbanRoutesLocators.button_payment_method).click()

    def add_card_option(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*UrbanRoutesLocators.button_add_card).click()

    def card_register(self):
        self.driver.implicitly_wait(20)
        self.payment_method()
        self.driver.implicitly_wait(20)
        self.add_card_option()

    def select_number(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*UrbanRoutesLocators.set_credit_card).click()

    def input_number(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*UrbanRoutesLocators.input_credit_card_xpath).send_keys(data.card_number)

    def card_input(self):
        self.driver.implicitly_wait(15)
        self.select_number()
        self.driver.implicitly_wait(15)
        self.input_number()

    def get_card_input(self):
        return self.driver.find_element(*UrbanRoutesLocators.input_credit_card_xpath).get_property('value')


    def code_card_input(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*UrbanRoutesLocators.input_card_cvv_xpath).send_keys(data.card_code)

    def cvv_code(self):
        self.driver.implicitly_wait(15)
        self.code_card_input()

    def get_cvv_card(self):
        return self.driver.find_element(*UrbanRoutesLocators.input_card_cvv_xpath).get_property('value')

    def registered_card(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*UrbanRoutesLocators.submit_card_xpath).click()

    def add_card(self):
        self.driver.implicitly_wait(20)
        self.card_input()
        self.driver.implicitly_wait(20)
        self.cvv_code()
        self.driver.implicitly_wait(20)
        self.registered_card()

    def close_modal(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*UrbanRoutesLocators.button_close_xpath).click()

    #Enviar mensaje al conductor
    def set_message(self, message):
        self.driver.implicitly_wait(15)
        message_field = self.driver.find_element(*UrbanRoutesLocators.input_comment_css)
        message_field.send_keys(message)

    def get_message(self):
        return self.driver.find_element(*UrbanRoutesLocators.input_comment_css).get_property('value')


    #Solicitud de manta y pañuelos

    def select_blanket_and_tissues(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*UrbanRoutesLocators.checkbox_bket_scrvs_xpath).click()

    def get_slider_status(self):
        return self.driver.find_element(*UrbanRoutesLocators.checkbox_slide_bket_scrvs_xpath).is_selected()

    #Agregar 2 helados

    def select_ice_cream(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*UrbanRoutesLocators.counter_ice_cream).click()
        self.driver.find_element(*UrbanRoutesLocators.counter_ice_cream).click()

    def get_icecream_counter(self):
        return self.driver.find_element(*UrbanRoutesLocators.counter_ice_cream_value_2).text

    #Buscando Conductor
    def select_order(self):
        self.driver.implicitly_wait(15)
        self.driver.find_element(*UrbanRoutesLocators.button_smart_order).click()

    def get_order_header_title(self):
        return self.driver.find_element(*UrbanRoutesLocators.order_header_title).text

    # Informacion del conductor
    def get_driver_modal_info(self):
        return self.driver.find_element(*UrbanRoutesLocators.order_header_title).text