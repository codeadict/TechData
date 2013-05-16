# -*- coding: utf-8 -*-#
import ConfigParser, os
from ftplib import FTP
import wx
from wx.lib.wordwrap import wordwrap
#importar scripts de scrappers
from techdata import Techdata
from uni import Uni

settings = ConfigParser.ConfigParser()
settings.read('scrape.conf')

ROOT = os.path.dirname(os.path.abspath(os.path.join(__file__)))
path = lambda *a: os.path.join(ROOT, *a)

class Application(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Tech Scrappers', size=(300, 130), 
                          style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        techdataBtn = wx.Button(panel, label='Extraer data de techdata.com.uy')
        techdataBtn.Bind(wx.EVT_BUTTON, self.scrapeTD)
        uniBtn = wx.Button(panel, label='Extraer data de uni.com.uy')
        uniBtn.Bind(wx.EVT_BUTTON, self.scrapeUNI)
        aboutBtn = wx.Button(panel, label='Acerca de...')
        aboutBtn.Bind(wx.EVT_BUTTON, self.doAboutBox)
        sizer.Add(techdataBtn, 0, wx.TOP|wx.CENTER, 10)
        sizer.Add(uniBtn, 0, wx.TOP|wx.CENTER, 10)
        sizer.Add(aboutBtn, 0, wx.TOP|wx.CENTER, 10)
        self.Centre()
        self.Show(True)
        
    def doAboutBox(self, event):
        """
        Mostrar Acerca De..
        """
        info = wx.AboutDialogInfo()
        info.Name = "Tech Scrappers"
        info.Version = "0.1"
        info.Copyright = "(C) 2013 Dairon Medina"
        info.Description = wordwrap(
            u"Scrapper para obtener datos de productos informáticos.",
            350, wx.ClientDC(self))
        info.WebSite = ("http://codeadict.org", u"www.codeadict.org")
        info.Developers = ["Dairon Medina Caro <dairon.medina@gmail.com>"]
        wx.AboutBox(info)
        
    def scrapeTD(self, event):     
        #sacar datos de techdata.com.uy
        td = Techdata()
        td.Login()
        td.Listado()
        #conectarse al servidor FTP
        ftp = FTP(settings.get('FTP', 'SERVER'))
        #logearse
        ftp.login(settings.get('FTP', 'USER'), settings.get('FTP', 'PASS'))
        #Leer ne archivo generado por los scrappers
        f = open(path("data/service.txt"), "r")
        #Abrir el directorio en el ftp
        ftp.cwd(settings.get('FTP', 'DIR'))
        #Guardar el archivo al FTP
        ftp.storlines("STOR listado-tech data.txt", f) 
        ftp.quit()
        f.close()        
        wx.MessageBox('Scrapping Finalizado. Archivo TXT guardado en el Servidor.', 'Info', wx.OK | wx.ICON_INFORMATION)
        
    def scrapeUNI(self, event):
        #sacar datos de uni.com.uy
        uni = Uni()
        uni.Login()
        uni.Listado()
        #conectarse al servidor FTP
        ftp = FTP(settings.get('FTP', 'SERVER'))
        #logearse
        ftp.login(settings.get('FTP', 'USER'), settings.get('FTP', 'PASS'))
        #Leer ne archivo generado por los scrappers
        f = open(path("data/data.txt"), "r")
        #Abrir el directorio en el ftp
        ftp.cwd(settings.get('FTP', 'DIR'))
        #Guardar el archivo al FTP
        ftp.storlines("STOR listado-unicom.txt", f) 
        ftp.quit()
        f.close()
        wx.MessageBox('Scrapping Finalizado. Archivo TXT guardado en el Servidor.', 'Info', wx.OK | wx.ICON_INFORMATION)

app = wx.App(0)
Application(None)
app.MainLoop()