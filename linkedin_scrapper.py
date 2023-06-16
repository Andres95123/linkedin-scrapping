from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import openpyxl
import os
import appdirs
import threading
import multiprocessing
import time

def detect_page_error(errorCode,page_Source):
    sopa = BeautifulSoup(page_Source,'html.parser')
    errorObject = sopa.find('div',class_="error-code")
    if (errorObject is not None) and (str(errorCode) in errorObject.text):
        return True
    return False

def children_webdriver_network_page(urlNetworkPage,pagina):
    try:
        semaforo_tabs.acquire()
        driver.execute_script("window.open('"+urlNetworkPage+"', 'tab"+str(pagina)+"')")
        webwait = WebDriverWait(driver,10)
        semaforo_tabs.release()
        webwait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        semaforo_tabs.acquire()
        driver.switch_to.window("tab"+str(pagina))
        #Contenido tab
        pagesource = driver.page_source
        semaforo_tabs.release()
        #Obtener todos los usuarios de la pagina
        sopa = BeautifulSoup(pagesource,'html.parser')
        
        

        users = sopa.find_all('div',"entity-result")

        for user in users:
            link = user.find('a',class_="app-aware-link").get('href')
            link = link[:link.find("?")] + "/"
            try:
                get_info_from_user(link,pagina)
            except:
                print("No se pudo obtener los datos de : " + link)
        
        #Cerrar pestaña para que deje de consumir RAM
        semaforo_tabs.acquire()
        driver.execute_script("window.open('"+urlNetworkPage+"', 'tab"+str(pagina)+"')")
        semaforo_tabs.release()
        semaforo_hilos.release()
    except Exception as e:
        print("Error con el child de la pagina : " + str(pagina) + " ::\n" + str(e))

class Pestaña():
    def __init__(self,thread,page):
        self.thread = thread
        self.page = page

def get_users_network(urlNetwork,pagina,max_pag):
    Threads = []
    while pagina<max_pag:
        #Obtenemos la url añadiendo la pag &page=1&sid=
        urlNetwork = urlNetwork.replace("&sid=","&page="+str(pagina)+"&sid=")
        pagina+=1
        semaforo_hilos.acquire()
        thread = threading.Thread(target=children_webdriver_network_page,args=(urlNetwork,pagina))
        Threads.append(Pestaña(thread,pagina))
        thread.start()

    for thread in Threads:
        thread.thread.join()
        semaforo_tabs.acquire()
        driver.switch_to.window('tab'+str(thread.page))
        semaforo_tabs.release()

        


def get_info_from_user(urlUser,pagina):
    urlUserOriginal = urlUser
    urlUser = urlUser + "overlay/contact-info/"
    semaforo_tabs.acquire()
    driver.switch_to.window("tab"+str(pagina))
    #Obtenemos el driver de linkedin
    driver.get(urlUser)
    #Esperar a que cargue la web
    webwait = WebDriverWait(driver,10)
    semaforo_tabs.release()
    
    webwait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div")))
    time.sleep(tiempoEspera)

    semaforo_tabs.acquire()
    driver.switch_to.window("tab"+str(pagina))
    #Obtenemos info del sujeto
    page_source = driver.page_source
    semaforo_tabs.release()
    sopa = BeautifulSoup(page_source,'html.parser')
    panelContacto = sopa.find('div',class_="artdeco-modal artdeco-modal--layer-default")
    #Obtener nombre contacto
    nombre = eliminar_espacios(panelContacto.find('h1',id="pv-contact-info").text.replace("\n",""))

    #Obtener subdatos
    subDatos = panelContacto.find('div',class_="pv-profile-section__section-info section-info")
    subSecciones = subDatos.find_all('section')

    email = cumpleaños = telefono = twitter = web = ""

    for seccion in subSecciones:
        section_name = seccion.find('h3').text.lower()
        if "email" in section_name:
            subsections = seccion.find_all('a')
            for subsection in subsections:
                email += eliminar_espacios(subsection.text) + "\n"
        if "cumpleaños" in section_name:
            cumpleaños = eliminar_espacios(seccion.find('span').text)
        if ("telefono" in section_name) or ("tel" in section_name):
            subsections = seccion.find_all('span')
            for subsection in subsections:
                telefono += eliminar_espacios(subsection.text) + "\n"
        if "twitter" in section_name:
            twitter = eliminar_espacios(seccion.find('a').get('href'))
        if "web" in section_name:
            subsections = seccion.find_all('a')
            for subsection in subsections:
                web += eliminar_espacios(subsection.get('href')) + "\n"

    print("Recolectada info de : " + nombre)
    
    set_database_headers([nombre,email,telefono,web,twitter,cumpleaños,urlUserOriginal])

def eliminar_espacios(nombre):
    # Eliminar espacios antes y después del nombre
    nombre_sin_espacios = " ".join(nombre.split()).strip()
    return nombre_sin_espacios

def init_sesion_linkedin():
    linkedin_url = "https://www.linkedin.com/login/es"

    #Enviamos a linkedin login
    driver.get(linkedin_url)

    driver_wait_ind(linkedin_url)    

    if "linkedin" in driver.current_url:
        print("Has salido del Login !")
    else:
        print("Debes Iniciar Sesion, ¡GRANUJA!")
        exit(0)

def driver_wait_ind(url):
    # Esperar hasta que se haya salido de la página actual
    while detect_page_error(429,driver.page_source):
        time.sleep(30)
        driver.get(url)
    WebDriverWait(driver, float("inf")).until(lambda driver: driver.current_url != url)
    
def start_selenium():
    global driver
    
    #Opciones
    navegador_options = Options()
    edge_profile_dir = os.path.join(appdirs.user_data_dir(), "Microsoft", "Edge", "Default")

    # Establece la ruta del perfil de usuario de Microsoft Edge
    navegador_options.add_argument("user-data-dir=" + edge_profile_dir)
    #Argumentos para seguridad
    #navegador_options.add_argument("inprivate")
    navegador_options.add_argument("start-maximized")

    driver = webdriver.Edge(options=navegador_options)
    

def start_database():

    global database
    global database_tab     
    
    database = openpyxl.Workbook()
    database_tab = database.active

    set_database_headers(["Nombre","Correo","Telefono","Web","Redes Sociales","Cumpleaños","Linkedin"])

def stop_driver():
    driver.quit()

def stop_database():
    database.save("database_contactos_linkedin.xlsx")

def stop_program():
    stop_database()
    stop_driver()
    

def set_database_headers(array):
    letra_header = 'A'
    global fila
    semaforo_database.acquire()
    for valor in array:
        database_tab[letra_header+str(fila)] = valor
        letra_header=chr(ord(letra_header) + 1)
    fila+=1
    semaforo_database.release()

#Obtener Url network
print("Introduce la URL de la network ¡SIN PAGINA= EN LA URL!")
urlInput = input()
print("Introduce la pagina por la cual deseas comenzar la busqueda, ej: 1,2...99")
primeraPag = int(input())
print("Introduce la ultima pagina por la cual deseas comenzar la busqueda")
ultimaPag = int(input())

print("Introduce un tiempo de espera en (segundos) para la recolección, recomendamos 30s, cuanto más tarde, más seguro será\n 0s será a máxima velocidad")
tiempoEspera = int(input())
print("Se leerá de la pagina " + str(primeraPag) + " hasta la pagina " + str(ultimaPag) + " de la url " + urlInput)
print("Iniciando...link")

if(primeraPag == 0):
    primeraPag = 1

#Variables globales
global fila,pagina
fila = pagina= 1
#Semaforos para multihilo
semaforo_database = threading.Semaphore(1)
semaforo_tabs = threading.Semaphore(1)
semaforo_hilos = threading.Semaphore(multiprocessing.cpu_count())

start_database()
start_selenium()
init_sesion_linkedin()
get_users_network(urlInput,primeraPag,ultimaPag)
stop_program()