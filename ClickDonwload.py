import os
from selenium import webdriver
from time import sleep
os.system('export PATH=$PATH:/usr/local/bin') # path to geckodriver executable
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
binary = FirefoxBinary('/Applications/Firefox.app/Contents/MacOS/firefox-bin')

class SpringerBooks():
    def __init__(self, link):
        self.link = link
        self.driver = webdriver.Firefox(firefox_binary=binary)
        self.driver.get(self.link)
        self.base_window = self.driver.current_window_handle
        # Book name
        name = self.driver.find_element_by_class_name("page-title").text
        if '\n' in name:
            name = name.split('\n')[0]
        if ' ' in name:
            name = name.replace(' ', '_')
        if '(' in name:
            name = name.replace('(', '\(')
        if ')' in name:
            name = name.replace(')', '\)')
        if '&' in name:
            name = name.replace('&', '\&')
        self.name = name
        sleep(2)

    def Download(self, format='pdf',SaveFolder=None, SaveMethod='wget'):
        """
        Method to download files in the specified format
        INPUTS:
        format     : string among this options 'all', 'pdf' and 'epub'
        SaveFolder : absolute path of folder to save the book
        SaveMethod : Method to save the book, 'wget' or 'manualy'
        """
        self.method = SaveMethod
        self.path   = SaveFolder
        if self.path is None:
            self.path = '~/Downloads'
            print('The download folder is not especified... ')
            print('users Downloads folder will be used as the route to save the file')

        if format == 'all':
            self._DownloadPDF()
            sleep(2)
            self._DownloadEPUB()
        elif format == 'pdf':
            self._DownloadPDF()
        elif format == 'epub':
            self._DownloadEPUB()
        else:
            print('Stupid, write an available format in lower case...')
        if self.method == 'wget':
            # Quit Webdriver
            self.driver.quit()

    def _DownloadPDF(self):
        self.driver.switch_to.window(self.base_window)
        # pdf = self.driver.find_element_by_xpath('/html/body/div[4]/main/article[1]/div/div/div[2]/div[1]/a')

        self.pdf = self.driver.find_element_by_partial_link_text("book PDF")
        self.pdf.click()
        sleep(30)

        new_window = [window for window in self.driver.window_handles if window != self.base_window][0]
        self.driver.switch_to.window(new_window)
        pdf_url = self.driver.current_url

        sleep(2)
        if self.method == 'wget':
            os.system(f'wget -P {self.path} -O {os.path.join(self.path,self.name)}.pdf {pdf_url}')
            self._CloseAuxTabs()

    def _DownloadEPUB(self):
        self.driver.switch_to.window(self.base_window)
        try:

            # epub = self.driver.find_element_by_xpath('/html/body/div[4]/main/article[1]/div/div/div[2]/div[2]/a')
            self.epub = self.driver.find_element_by_partial_link_text("book EPUB")
            self.epub.click()
            sleep(30)
            epub_url = self.driver.current_url
            if self.method == 'wget':
                os.system(f'wget -P {self.path} -O {os.path.join(self.path,self.name)}.epub {pdf_url}')
                self._CloseAuxTabs()

        except:
            print('Epub format is not available')

    def _CloseAuxTabs(self):
        new_window = [window for window in self.driver.window_handles if window != self.base_window][0]
        # Switch to new window/tab
        self.driver.switch_to.window(new_window)
        # Close new window/tab
        self.driver.close()
        # Switch to initial window/tab
        self.driver.switch_to.window(self.base_window)




l = [
'http://doi.org/10.1007/978-3-319-58715-8',
'http://doi.org/10.1007/978-981-10-5218-7',
'http://doi.org/10.1007/978-94-024-1144-7',
'http://doi.org/10.1007/978-3-319-59978-6',
'http://doi.org/10.1007/978-3-662-55381-7',
'http://doi.org/10.1007/978-981-13-0399-9',
'http://doi.org/10.1007/978-3-319-89292-4',
'http://doi.org/10.1007/978-3-319-95762-3',
'http://doi.org/10.1007/978-3-662-56707-4',
'http://doi.org/10.1007/978-3-319-94313-8',
'http://doi.org/10.1007/978-3-319-96622-9',
'http://doi.org/10.1007/978-3-030-01279-3',
'http://doi.org/10.1007/978-3-030-13005-3',
'http://doi.org/10.1007/978-3-030-13020-6',
'http://doi.org/10.1007/978-3-319-68837-4',
]

for link in l:
    # Example wget
    Book = SpringerBooks(link)
    Book.Download(SaveFolder='/Users/cmcuervol/Desktop/Behavioral/')
    # # Exaample wget and specific folder
    # Book = SpringerBooks(link)
    # Book.Download(SaveFolder='/Users/cmcuervol/Desktop/')

    # # example manualy
    # Book = SpringerBooks(link)
    # Book.Download(format='all', SaveMethod='manualy')
    # x = input('Enter to close tabs:')
    # Book._CloseAuxTabs()
    # Book.driver.quit()
