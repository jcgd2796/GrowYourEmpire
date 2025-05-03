Para poder utilizar la aplicación correctamente, son necesarias las librerías de Python "django-crontab", "pymysql", "gevent", "whitenoise" y "django-nested-admin".
```
python -m pip install django-crontab
python -m pip install pymysql
python -m pip install django-nested-admin
python -m pip install gevent
python -m pip install whitenoise
```
También se deben generar certificados para que la aplicación se encuentre disponible a través de HTTPS
```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout privkey.pem -out cert.pem
```
A continuación, debemos instalar un gestor de bases de datos. Actualmente, la aplicación está preparada para utilizar MariaDB
```
sudo apt install mariadb-server
sudo mysql_secure_installation
```
Tras la instalación, accedemos al SGBD y creamos la base de datos "GrowYourEmpire"
```
mysql -u root -p
CREATE DATABASE GrowYourEmpire;
```
Para finalizar, generamos el resto de tablas de la base de datos
```
python3 manage.py migrate
```
Además, se debe crear un usuario de tipo administrador:
```
python3 manage.py createsuperuser
```
Una vez que se ha creado el usuario administrador, podemos acceder al área de administración (/admin) y crear nuevos usuarios.
Al crear entidades de tipo Student vinculadas a un usuario, se genera automáticamente la aldea del usuario, aunque deshabilitada.
Al estar deshabilitada, no genera recursos diariamente, aunque se puede habilitar si su propietario accede al área de gestión de su aldea (/GrowYourEmpire/manager).

Creado para la versión 5.1 de Django ([https://docs.djangoproject.com/en/5.1/releases/5.1/]), utilizando Python 3.10.12
