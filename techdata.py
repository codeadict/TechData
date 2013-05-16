# -*- coding: utf-8 -*-#
import os
import ConfigParser, codecs
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time

settings = ConfigParser.ConfigParser()
settings.read('scrape.conf')

ROOT = os.path.dirname(os.path.abspath(os.path.join(__file__)))
path = lambda *a: os.path.join(ROOT, *a)

class Techdata():
    """
    Scrapper para obtener datos de productos en stock
    de www.techdata.com.uy
    """
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.techdata.com.uy/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def Login(self):
        driver = self.driver
        driver.get(self.base_url + "/intouch/cliente/entrada.aspx")
        driver.find_element_by_name('ingreso1$CodUsu').send_keys(settings.get('TECHDATA', 'USUARIO'))
        driver.find_element_by_name('ingreso1$PassUsu').send_keys(settings.get('TECHDATA', 'PASS'))
        driver.find_element_by_name('ingreso1$btnLogin').click()
        time.sleep(30)
        
    def Listado(self):
        if os.path.exists(path('data/service.txt')):
            os.remove(path('data/service.txt'))
        driver = self.driver
        driver.get(self.base_url + "/intouch/main_listado.aspx")
        time.sleep(5)
        driver.switch_to_frame("wd_resultados_contenido")
        #mientras haya mas paginas segir
        while self.is_element_present(By.ID, "btnSiguienteSuperior"):
            for tr in driver.find_elements_by_xpath("//div[@id='iuPanelListado']/table[2]/tbody/tr[preceding-sibling::tr]"):
                tds = tr.find_elements_by_tag_name('td')
                
                data = [td.text for td in tds]
                
                #si tiene stock
                try:
                    print data[4]
                    if data[4] != '0':
                        #eliminar caracteres del precio
                        rm = 'U$S '
                        pfinal = filter(lambda x: not (x in rm), data[5])
                        #Remplazar comas por puntos
                        pfinal = pfinal.replace(',', '.')         
                        line = "%s#%s\n" %(data[0], pfinal)
                        self.write(line)
                except IndexError:
                    continue
                
            #ir proxima pagina
            driver.find_element_by_id("btnSiguienteSuperior").click()
        #Cerrar el driver
        self.driver.close()
                
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
                
    def write(self, line):
        with codecs.open(path('data/service.txt'), 'a', 'utf-8') as outfile:
            outfile.write(line)
                
                
if __name__ == "__main__":
    td = Techdata()
    td.Login()
    td.Listado()
