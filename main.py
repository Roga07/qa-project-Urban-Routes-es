import data
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


from methods import UrbanRoutesPage
from locators import UrbanRoutesLocators



class TestUrbanRoutes:

    driver = None
    met = None


    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.met = UrbanRoutesPage(cls.driver)

    #Origen y destino
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # 1.Configurar la dirección
        address_from = data.address_from
        address_to = data.address_to
        self.driver.implicitly_wait(10)
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        # 2.Seleccionar taxi y tarifa
    def test_select_rate(self):
        self.met.select_taxi()
        self.met.select_comfort_rate()

        # Verificar que la tarifa de confort se haya seleccionado correctamente
        comfort_rate_button = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(UrbanRoutesLocators.button_comfort_xpath)
        )
        assert 'tcard active' in comfort_rate_button.get_attribute('class'), "La tarifa comfort no fue seleccionada"

        # 3.Rellenar el número de teléfono y obtener código
    def test_get_tel_code(self):
         self.met.set_phone()
         self.met.click_on_next_button()
         self.met.code_number()
         self.met.send_cell_info()

         # Verificar que el teléfono ingresado es el esperado
         phone_number = self.met.get_phone()
         assert phone_number == data.phone_number,f"Número esperado {data.phone_number}, pero se tiene {phone_number}"

        # 4.Agregar una tarjeta de crédito
    def test_add_creditcard(self):
         self.met.card_register()
         self.met.add_card()
         self.met.close_modal()

         # Verificar que el número de tarjeta ingresado es el esperado
         card_number = self.met.get_card_input()
         assert card_number == data.card_number, f"credit card esperada {data.card_number}, pero se tiene {card_number}"

         # Verificar que el código CVV ingresado es el esperado
         cvv_code = self.met.get_cvv_card()
         assert cvv_code == data.card_code, f"CVV code esperado {data.card_code}, pero se tiene {cvv_code}"


        # 5.Escribir un mensaje para el conductor
    def test_send_message(self):
        message = data.message_for_driver
        self.met.set_message(message)

        # Verificar que el mensaje se haya ingresado correctamente
        entered_message = self.met.get_message()
        assert entered_message == message, f"Mensaje esperado {message}, pero se tiene {entered_message}"

        # 6.Pedir una manta y pañuelos
    def test_add_blanket_and_tissues(self):
        self.met.select_blanket_and_tissues()
        self.met.get_slider_status()

        # Verificar que la opción de manta y pañuelos se ha seleccionado
        assert self.met.get_slider_status() == True

        # 7.Pedir 2 helados
    def test_add_two_icecream(self):
        self.met.select_ice_cream()

        # Verificar que se han seleccionado dos helados
        assert self.met.get_icecream_counter() == '2'

        # 8.Aparece el modal para buscar un taxi
    def test_order_drive(self):
        self.met.select_order()
        order_header_title = self.met.get_order_header_title()
        assert 'Buscar automóvil' in order_header_title

        # 9.Esperar la información del conductor
    def test_driver_info(self):
        # Esperar a que el modal se actualice
        time.sleep(40)

        # Verifica actualiza con el conductor visible
        order_header_title = self.met.get_driver_modal_info()
        assert 'El conductor llegará' in order_header_title, f"Se esperaba 'El conductor llegará', pero se tiene: {order_header_title}"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()




