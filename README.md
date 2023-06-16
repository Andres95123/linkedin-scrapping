# LinkedIn Scraper

Este proyecto es una aplicación en Python que permite realizar web scraping en la red social profesional LinkedIn para extraer información de perfiles de usuario. Utilizando técnicas de automatización, este script accede a la plataforma de LinkedIn, navega a través de los perfiles y recopila datos relevantes de cada uno de ellos.

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instalado lo siguiente:

- Python 3.x: [Descargar Python](https://www.python.org/downloads/)
- Requisitos: `pip install -r requirements.txt`
- WebDriver: El driver del navegador web que vayas a utilizar (por ejemplo, ChromeDriver para Google Chrome o EdgeDriver para Microsoft Edge)

## Configuración

1. Descarga el WebDriver correspondiente a tu navegador y versión compatible. Asegúrate de colocar el archivo ejecutable en una ubicación accesible desde la línea de comandos o en la ubicación del script.

2. Instala los requisitos de requirements.txt

## Uso

1. Ejecuta el archivo `linkedin_scrapper.py` para iniciar la aplicación.

2. La consola te pedirá el numero de paginas a hacer scrapping, el tiempo de retardo entre cada recolección (Recomendamos valores altos como 30s), la url de la network que quieres hacer scrapping, dale la url sin un 'pag=' al final de la url.

3. La aplicación abrirá una ventana del navegador y te mostrará una página de inicio de sesión de LinkedIn. Ingresa tus credenciales y haz clic en "Iniciar sesión".

4. El script comenzará a visitar cada perfil y extraerá información de contacto como el nombre, email, telefono y redes sociales. Los resultados se almacenarán en un archivo `database_contactos_linkedin.xlsm` en formato Excel.

## Limitaciones y precauciones

- El uso de web scraping en LinkedIn puede violar los términos de servicio de la plataforma. Asegúrate de utilizar esta aplicación con responsabilidad y ética, respetando la privacidad y derechos de los usuarios.

- LinkedIn puede aplicar restricciones o mecanismos de seguridad para detectar actividades de web scraping automatizado. Utiliza el script con moderación y ajusta los tiempos de espera entre solicitudes para evitar bloqueos o suspensión de tu cuenta.

- Este proyecto se proporciona "tal cual" y no garantiza la funcionalidad continua debido a los posibles cambios en la estructura del sitio web de LinkedIn. Realiza las actualizaciones necesarias en el código si es necesario para adaptarlo a las modificaciones en la interfaz de LinkedIn.


## Responsabilidad

Este proyecto se proporciona con fines educativos y de aprendizaje. Al utilizar esta aplicación, comprendes y aceptas que cualquier acción que realices con ella, incluyendo el scraping de datos de LinkedIn, se realiza bajo tu propia responsabilidad.

Debido a los posibles cambios en los términos de servicio de LinkedIn y las políticas de uso, así como a las posibles medidas de seguridad implementadas por la plataforma, no nos hacemos responsables de cualquier baneo, bloqueo o pérdida de cuenta que puedas experimentar como resultado del uso de esta aplicación.

Te recomendamos utilizar este proyecto de manera ética y respetar los términos de servicio y privacidad de LinkedIn. Es importante que comprendas y cumplas las políticas de uso y restricciones establecidas por la plataforma y tomes las precauciones necesarias para evitar el uso indebido de esta aplicación.

Recuerda que la extracción de datos de sitios web puede ser un área legalmente compleja y está sujeta a regulaciones y leyes locales. Asegúrate de comprender y cumplir con todas las leyes y regulaciones aplicables antes de utilizar esta aplicación para cualquier propósito.

## Contribuciones

Si deseas contribuir a este proyecto, por favor, siéntete libre de enviar tus sugerencias, ideas o correcciones mediante la creación de un pull request. ¡Estaremos encantados de recibir tu aportación!

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
