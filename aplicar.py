import json
import os
import webbrowser
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#parametros para el script
api_base_url = 'http://www.elempleo.com/';
api_url = 'co/ofertas-empleo/?&trabajo=';
endsearch = '{ jobOfferUrl }}';
clink = '<a class="text-ellipsis js-offer-title"';
clinkf = '"';
itm = 75;
arrempleos = []

def use_requests(api_url):

    response = requests.get(api_url)
    #json_response = json.loads(response.text)
    #photo_url = json_response['url']
    #webbrowser.open_new_tab(photo_url)

    return response.text;

def analizarTexto(text, st):
    #nombre de clase donde se pone el link del trabajo 
    #fin = len(texto);
    n1 = text.find(clink, st) + itm
    n2 = text.find(clinkf, n1)

    print(text, file=open('output.txt', 'a'))
    #print(text)
    print("n1:"+str(n1))
    print("n2:"+str(n2))
        
    linkempleo = text[n1:n2].strip();
    arrempleos.append(linkempleo)
    
    return [n2, linkempleo];

def mainFunc(term):
    url = api_base_url+api_url+term;
    print(url);

    texto = use_requests(url);

    st = 0
    iteracion = 0

    while True:
        iteracion+=1;

        if iteracion==1: 
            st = analizarTexto(texto, 0)[0];
        else:
            an = analizarTexto(texto, st);
            st = an[0];
            tx = an[1]
            
            if tx==endsearch:
                break;

def abrirChrome():
    #driv = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #s = Service(ChromeDriverManager().install())
    #driv = webdriver.Chrome(service=s)
    #s.start();
    #driv = webdriver.Chrome(s);
    #driv.maximize_window();
    chromeOptions = Options()
    #option para ejecutar en background
    #chromeOptions.headless = True
    driv = webdriver.Chrome(executable_path="./drivers/chromedriver", options=chromeOptions)
    return driv;

def abrirFirefox():
    #driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driv = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driv.maximize_window()
    return driv;

def loginSession(driv, email, passw):

    try:
        #get iniciar session web
        driv.get(api_base_url+'co/iniciar-sesion')

        #send the email information
        emailfield = driv.find_element(By.NAME, 'EmailField');
        print('emailfield:'+emailfield.get_attribute('class'));
        emailfield.send_keys(email);
        
        #send the password information
        passfield = driv.find_element(By.NAME, 'PasswordField');
        print('passfield:'+passfield.get_attribute('class'));
        passfield.send_keys(passw);
        
        #send the enter key to chrome
        passfield.send_keys(Keys.ENTER)
        
        #wait until the session is completely open
        #driv.explicitly_wait(30)
        el = WebDriverWait(driv, timeout=20).until(lambda d: d.find_element(By.CLASS_NAME, 'pruebaToolTip js-my-resumee-link'))
        #assert el.text == "Hello from JavaScript!"
    except:
        print('an exception occurred')
        
def aplicar(driv, empleo):

    #url de trabajo
    url1 = api_base_url+empleo;

    # get geeksforgeeks.org
    driv.get(url1);

    try:
        # waits for loading page
        el = WebDriverWait(driv, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME, bclassname));
    except:
        print('timeout exception');

        try:
            botones = driv.find_elements(By.TAG_NAME, "button");
            aplicarb = botones[1];

            try:

                print('antes de location once scrolled into view:');
                print(aplicarb.location_once_scrolled_into_view);
            
                aplicarb.click();
                print('luego del click linea 129');
            except Exception as er:
                print(er);
                
            #buttons = WebDriverWait(driv, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
            #element = driver.find_element_by_id("dropDown")
            
            try:
                print('antes de la linea de ejecucion de javascript linea 134');
                #driv.execute_script("arguments[0].click();console.log('registrado desde funcion javascript')",aplicarb);
                #aplicarb.send_keys(Keys.ENTER)
                
                WebDriverWait(driv, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "aplicar-oferta-detalle"))).click()

                #pausar la ejecucion del script por dos segundos mientras termina de postular
                time.sleep(2);
                
            except Exception as er:
                print(er);

            #print(aplicarb);
            #button send keys
            #aplicarb.click();
            #aplicarb.send_keys(Keys.ENTER);
            
        except Exception as e:
            print(e);

try:
        
    #terminos de busqueda de trabajo para aplicar, cambiar los terminos para busqueda de trabajo
    terminos=[
        #'proyectos',
        #'nodejs',
        'python',
        'pandas',
        'keras',
        'matplotlib',
        'gestion de proyectos'
    ];

    for i in terminos:
        mainFunc(i);

    #get driver    
    driver = abrirChrome();
    #driver = abrirFirefox();
        
    #abrir sesion del usuario, cambiar aqui las credenciales propias
    loginSession(driver, 'email@email.com', 'password');
        
    #aplicar a todos los empleos usando chrome
    for i in arrempleos:
            
        try:
            aplicar(driver, i);
        except Exception as e:
            print('an exception ocurred applying job:'+str(i));
            print(e);
                
except Exception as e:
    print(e)
