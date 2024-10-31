from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from sbvirtualdisplay import Display
from seleniumbase import Driver


from config import VISIBLE
# Cuando no encuentra el XPATH entonces hay que inspeccionar el boton y con el click derecho copiar en PATH

class SeleniumDriver():       
    def __init__(self, visible=VISIBLE):
        
        if not visible:
            self.virtual_display = Display(visible=0, size=(800, 600))
        else:
            self.virtual_display = Display(visible=1, size=(800, 600))
            
        self.virtual_display.start()

        self.Driver = Driver(
            uc=True,
            headless=False,
            chromium_arg="--force-device-scale-factor=0.70",
        )
        self.Driver.maximize_window()
        self.wait = WebDriverWait(self.Driver, 5)
         
    def detener(self):
        self.Driver.quit()
        if self.virtual_display:
            self.virtual_display.stop()
    