# -*- coding: utf-8 -*-#
import ConfigParser, os
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time, re, codecs

settings = ConfigParser.ConfigParser()
settings.read('scrape.conf')

ROOT = os.path.dirname(os.path.abspath(os.path.join(__file__)))
path = lambda *a: os.path.join(ROOT, *a)

class Uni():
    """
    Scrapper para obtener datos de productos en stock
    de www.uni.com.uy
    """
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.uni.com.uy"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def Login(self):
        """
        Logearse
        """
        driver = self.driver
        driver.get(self.base_url + "/home/index.aspx")
        driver.find_element_by_name('ctrlLogin:usuario').send_keys(settings.get('UNI', 'USUARIO'))
        driver.find_element_by_name('ctrlLogin:clave').send_keys(settings.get('UNI', 'PASS'))
        driver.find_element_by_name('ctrlLogin:btnImage').click()
        time.sleep(30)
        
    def Listado(self):
        if os.path.exists(path('data/service.txt')):
            os.remove(path('data/data.txt'))
        driver = self.driver
        #listado de categorias a Iterar
        cats = ['00', '01', '02', '03', '04', '06', '08', '10', '20', '30', '40', '45', '50', '60']
        for c in cats:
            url_end = "/paginas/producto_tipo.aspx?tipo=1&id=%s&sinStock=true" % (c)
            print url_end
            driver.get(self.base_url + url_end)
            for tr in driver.find_elements_by_xpath("//table[@id='Log']/tbody/tr[contains(@class, 'search')]"):
                tds = tr.find_elements_by_tag_name('td')
                    
                data = [td for td in tds]
                
                #obtener atributo href donde esta el codigo
                code_href = data[0].find_elements_by_tag_name('a')[0].get_attribute("href")
                
                #Patron para encontrar el codigo del producto en la URL
                regex = re.compile('\S=([^"]+)')
                
                codigo = regex.findall(code_href)
                
                price = data[6].text
                
                #eliminar caracteres del precio
                rm = 'U$S '
                pfinal = filter(lambda x: not (x in rm), price)
                #Remplazar comas por puntos
                pfinal = pfinal.replace(',', '.')         
                    
                line = "%s#%s\n" %(codigo[0], pfinal)
                
                self.write(line)
        #Cerrar el driver
        self.driver.close()
                
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
                
    def write(self, line) :
        with codecs.open(path('data/data.txt'), 'a', 'utf-8') as outfile:
            outfile.write(line)
                
                
if __name__ == "__main__":
    uni = Uni()
    uni.Login()
    uni.Listado()
