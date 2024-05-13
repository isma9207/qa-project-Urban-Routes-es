import selenium.webdriver.common.devtools.v85.schema

import data
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


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
    # Localizador del campo 'Desde'
    from_field = (By.ID, 'from')
    # Localizador del campo 'Hacia'
    to_field = (By.ID, 'to')
    # Localizador del botón 'Pedir un taxi' en la sección de tarifa
    button_round = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    # Localizador de la tarifa 'Comfort'
    comfort_fare = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    # Localizador del campo 'Número de teléfono' del formulario de tarifa
    phone_number_field = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div')
    # Localizador del campo 'Número de teléfono' de la ventana emergente del campo 'Número de teléfono'
    phone_number_window = (By.NAME, 'phone')
    # Localizador del botón 'Siguiente' en la ventana emergente del campo 'Número de teléfono'
    phone_number_next_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    # Localizador del campo 'Introduce el código' en la ventana emergente 'Introduce el código del SMS'
    phone_number_code = (By.ID, 'code')
    # Localizador del botón 'Confirmar' en la ventana emergente 'Introduce el código del SMS'
    phone_number_code_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    # Localizador del campo 'Método de pago' del formulario de tarifa
    payment_method_field = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')
    # Localizador del campo 'Agregar tarjeta' en la ventana emergente
    add_card = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]')
    # Localizador del campo 'Número de tarjeta (no la tuya)'
    card_number = (By.ID, 'number')
    # Localizador del campo 'Código' de la tarjeta
    card_code = (By.NAME, 'code')
    # Localizador del botón 'Agregar'
    add_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    # Localizador del botón 'Cerrar' de la ventana emergente
    close_payment_method_window_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    # Localizador para el campo 'Mensaje para el conductor...'
    message_for_driver_field = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[3]/div')
    # Localizador para escribir mensaja para el conductor
    message_for_driver = (By.ID, 'comment')
    # Localizador para el campo 'Requisitos del pedido'
    order_requirments = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]')
    # Localizador del slide 'Manta y pañuelos'
    blanket_and_scarves = (By.CLASS_NAME, 'r-sw')
    # Localizador del boton agregar helado '+'
    icecream_counter_plus = (By.CLASS_NAME, 'counter-plus')
    # Localizador del botón 'Pedir taxi' una vez completado el formulario de tarifa
    order_a_taxi_button = (By.CLASS_NAME, 'smart-button')
    # Localizador del header 'Buscando automóvil' en la ventana emergente
    search_for_taxi = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[1]/div/div[1]')
    # Localizador del logo del conductor
    taxi_driver = (By.XPATH, '//*[@id="root"]/div/div[5]/div[2]/div[2]/div[1]/div[1]')

    def __init__(self, driver):
        self.driver = driver

    # Método para llenar el campo 'Desde'
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)
        time.sleep(1)
    # Método para llenar el campo 'Hacia'
    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)
        time.sleep(1)
    # Método que devuelve el valor del campo 'Desde'
    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')
    # Método que devuelve el valor del campo 'Hacia'
    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')
    # Paso para indicar la ruta del viaje, punto A -> punto B
    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    # Método para hacer clic en el botón 'Pedir un taxi'
    def click_button_ask_for_taxi(self):
        #self.click_button_round()
        # Tiempo de espera hasta visualizar el botón 'Pedir un taxi'
        WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located(self.button_round))
        self.driver.find_element(*self.button_round).click()
        time.sleep(1)
    # Método para hacer clic y seleccionar la tarifa Comfort
    def click_to_select_comfort_fare(self):
        # Tiempo de espera hasta visualizar la tarifa Comfort
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.comfort_fare))
        self.driver.find_element(*self.comfort_fare).click()

    # Método para hacer scroll y visualizar los campos 'Número de teléfono', 'Método de pago' y 'Mensaje para el conductor...'
    def scroll_down_for_view_phone_number_field(self):
        element = self.driver.find_element(*self.phone_number_field)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        # Definir la cantidad de scrolls que deseas realizar dentro de la sección
        scrolls = 2
        # Realizar scrolls hacia abajo dentro de la sección
        for _ in range(scrolls):
            self.driver.execute_script("arguments[0].scrollTop += 500;", element)  # Scroll vertical
            time.sleep(0.5)  # Pausa de 0.5 segundo para que la página cargue completamente

    # Método para hacer clic en el campo 'Número de teléfono'
    def click_phone_number_field(self):
        self.driver.find_element(*self.phone_number_field).click()
        time.sleep(1)
    # Método para llenar el campo 'Número de teléfono' en la ventana emergente
    def set_phone_number_window(self, phone_number):
        # Método de tiempo de espera para visualizar el campo 'Número de teléfono' en la ventana emergente
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.phone_number_window))
        self.driver.find_element(*self.phone_number_window).send_keys(phone_number)
        time.sleep(1)
    # Método para hacer clic en el botón 'Siguiente' de la ventana emergente
    def click_next_button_into_window_phone_number(self):
        self.driver.find_element(*self.phone_number_next_button).click()
    # Método para llenar el campo 'Introduce el código' en la ventana emergente
    def set_phone_number_code_window(self):
        # Método de tiempo de espera para visualizar el campo 'Introduce el código' en la ventana emergente
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.phone_number_code))
        phone_code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.phone_number_code).send_keys(phone_code)
        time.sleep(1)
    # Método para hacer clic en el botón 'Confirmar' de la ventana emergente
    def click_comfirm_button_code_window(self):
        self.driver.find_element(*self.phone_number_code_button).click()
    # Método que devuelve el valor del campo 'Número de teléfono'
    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_field).text
    # Paso para llenar el campo 'Número de telefono'
    def set_phone_number(self, phone_number):
        self.click_phone_number_field()
        self.set_phone_number_window(phone_number)
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.phone_number_next_button))
        self.click_next_button_into_window_phone_number()
        self.set_phone_number_code_window()
        self.click_comfirm_button_code_window()

    # Método para hacer clic en el campo 'Método de pago'
    def click_payment_method_field(self):
        self.driver.find_element(*self.payment_method_field).click()
        time.sleep(1)
    # Método para hacer clic en 'Agregar tarjeta' de la ventana emergente
    def click_add_card(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.add_card))
        self.driver.find_element(*self.add_card).click()
        time.sleep(1)
    # Método para agregar número de tarjeta en el campo 'Número de tarjeta (no la tuya)'
    def set_card_number(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.card_number))
        self.driver.find_element(*self.card_number).click()
        self.driver.find_element(*self.card_number).send_keys(data.card_number)
        time.sleep(1)
    def set_card_code(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.card_code))
        self.driver.find_element(*self.card_code).click()
        self.driver.find_element(*self.card_code).send_keys(data.card_code)
        self.driver.find_element(*self.card_code).send_keys(Keys.TAB)
        time.sleep(2)
    # Método para hacer clic en el botón 'Agregar' cuando ya esta habilitado
    def click_add_button(self):
        self.driver.find_element(*self.add_button).click()
    # Método para hacer clic en el botón 'Cerrar' de la ventana emergente
    def ciick_close_payment_method_window_button(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.close_payment_method_window_button))
        self.driver.find_element(*self.close_payment_method_window_button).click()
    # Paso para agregar método de pago
    def set_payment_method(self):
        self.click_payment_method_field()
        self.click_add_card()
        self.set_card_number()
        self.set_card_code()
        self.click_add_button()
        self.ciick_close_payment_method_window_button()

    # Método para hacer clic en el campo 'Mensaje para el conductor...'
    def click_message_for_driver_field(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.message_for_driver_field))
        self.driver.find_element(*self.message_for_driver_field).click()
        time.sleep(1)
    # Método para escribir un mensaje para el conductor
    def write_message_for_driver(self, message):
        self.driver.find_element(*self.message_for_driver).send_keys(message)
        time.sleep(1)
    # Paso para llenar el campo de 'Mensaje para el conductor...'
    def set_message_for_driver(self, message):
        self.click_message_for_driver_field()
        self.write_message_for_driver(message)

    # Método para hacer scroll y visualizar los 'Requisitos del pedido'
    def scroll_down_for_view_order_requirments_field(self):
        element = self.driver.find_element(*self.order_requirments)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        # Definir la cantidad de scrolls que deseas realizar dentro de la sección
        scrolls = 3
        # Realizar scrolls hacia abajo dentro de la sección
        for _ in range(scrolls):
            self.driver.execute_script("arguments[0].scrollTop += 500;", element)  # Scroll vertical
            time.sleep(0.5)  # Pausa de 0.5 segundo para que la página cargue completamente

    # Método para solicitar manta y pañuelos
    def request_blanket_and_scarves(self):
        self.scroll_down_for_view_order_requirments_field()
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.blanket_and_scarves))
        self.driver.find_element(*self.blanket_and_scarves).click()
        time.sleep(2)

    # Método para agregar dos helados al servicio
    def add_two_icecreams(self):
        self.driver.find_element(*self.icecream_counter_plus).click()
        time.sleep(1)
        self.driver.find_element(*self.icecream_counter_plus).click()

    # Método para hacer clic en 'Pedir un taxi' una vez llenado el formulario
    def click_order_a_taxi_button(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.element_to_be_clickable(self.order_a_taxi_button))
        self.driver.find_element(*self.order_a_taxi_button).click()
    # Paso para pedir el taxi una vez llenado el formulario con tiempo para encontrar un conductor
    def searching_a_taxi(self):
        self.click_order_a_taxi_button()
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(self.search_for_taxi))
        time.sleep(35)
    # Tiempo de espera hasta que aparezca la información del conductor en la ventana emergente
    def wait_for_taxi_driver(self):
        WebDriverWait(self.driver, 50).until(expected_conditions.visibility_of_element_located(self.taxi_driver))

class TestUrbanRoutes:

    driver = None
    routes_page = None
    address_from = data.address_from
    address_to = data.address_to
    phone_number = data.phone_number
    message = data.message_for_driver

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        # Insertar 'desired_capabilities=capabilities' en la linea de arriba en 'webdriver'

    # Prueba 1
    # Configurar la dirección de la ruta.
    def test_set_route(self):
        self.routes_page = UrbanRoutesPage(self.driver)
        self.driver.get(data.urban_routes_url)
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.routes_page.from_field))
        self.routes_page.set_route(self.address_from, self.address_to)
        assert self.routes_page.get_from() == self.address_from
        assert self.routes_page.get_to() == self.address_to
        time.sleep(2)

    # Prueba 2
    # Seleccionar la tarifa Comfort.
    def test_select_comfort_fare(self):
        self.test_set_route()
        self.routes_page.click_button_ask_for_taxi()
        self.routes_page.click_to_select_comfort_fare()
        time.sleep(2)

    # Prueba 3
    # Rellenar el campo de número de teléfono.
    def test_set_phone_number(self):
        self.test_select_comfort_fare()
        self.routes_page.scroll_down_for_view_phone_number_field()
        self.routes_page.set_phone_number(self.phone_number)
        assert self.routes_page.get_phone_number() == self.phone_number
        time.sleep(2)

    # Prueba 4
    # Agregar un método de pago (Tarjeta de crédito).
    def test_set_payment_method(self):
        self.test_set_phone_number()
        self.routes_page.set_payment_method()
        time.sleep(2)

    # Prueba 5
    # Escribir un mensaje para el conductor.
    def test_message_to_driver(self):
        self.test_set_payment_method()
        self.routes_page.set_message_for_driver(self.message)
        time.sleep(2)

    # Prueba 6
    # Añadir una manta y pañuelos al servicio.
    def test_request_blanket_and_scarves(self):
        self.test_message_to_driver()
        self.routes_page.request_blanket_and_scarves()
        time.sleep(2)

    # Prueba 7
    # Añadir dos helados al servicio.
    def test_add_two_icecreams(self):
        self.test_message_to_driver()
        self.routes_page.add_two_icecreams()
        time.sleep(2)

    # Prueba 8 y 9
    '''Aparece una ventana emergente en búsqueda de un taxi, cuando finaliza el tiempo 
       en el temporizador aparece la información del conductor'''
    def test_searching_a_taxi_window(self):
        self.test_message_to_driver()
        self.routes_page.scroll_down_for_view_order_requirments_field()
        self.routes_page.searching_a_taxi()
        self.routes_page.wait_for_taxi_driver()
        time.sleep(5)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
