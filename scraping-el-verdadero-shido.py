#MFGC
# -*- encoding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import codecs

#Incognito MODE -.-
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")

#Instance of Chrome
# -- <executable_path> is the path that points to where was downloaded and
#saved ChromeDriver.
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
                            chrome_options=option)
#Second Instance of Chrome
# -- Used in line 37.
confession_page = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
                            chrome_options=option)

# ------------------  FUNCTIONS -----------------------------------------------

#Take the substring of the link which indicates the confession category.
def get_category(link):
	ns = link.split('/')[3].split('-')
	if ns[0] == 'a':
		return ' '.join(ns[1:])
	return ns[0]

# ------------------  REQUEST  ------------------------------------------------

#Number of pages for scraping
pages = 2

# -- WEKA configuration
weka = codecs.open('confession.arff','w',"utf-8")
cabecera = str("% confessions \n@relation 'confessions'"+
            "\n%ATRIBUTOS POR ORDEN DE APARICION EN LA DESCRIPCION "+
            "\n@attribute 'confession' string \n@attribute categoria "+
            "{pain, dream, fantasy, first experience, guilt, lie, pain, "+
            "random feeling, truth, wild experience, other} \n@data \n ")
weka.write(cabecera)
# --

#Get the confession of each page.
for page in range(1,pages+1):

    #Open the page of the website.
    browser.get("http://simplyconfess.com/page/"+str(page))
    #Take the first parent (of the content that we want) that have an id.
    parents = browser.find_elements_by_class_name("modern-grid-content")

    #Get the <a> tag for each parent.
    for parent in parents:
        #Here we gonna save the link to each confession.
        link = parent.find_element_by_css_selector("p a").get_attribute("href")
        print("linkss:"+link)
        #Open the page with the confession.
        confession_page.get(link)
        #Take the first parent (of the content that we want) that have an id.
        article = confession_page.find_element_by_tag_name("article")
        #Get the tag with the confession (-)
        confession = article.find_element_by_css_selector("p")
        #Get the confession category
        category = get_category(link)

        #Write (-)
        weka.write('"'+confession.text+'"'+', '+category+'\n')
