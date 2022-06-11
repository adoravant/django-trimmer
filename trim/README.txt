****************Las plantillas DIVIDIDAS con sections.
OK <section id="about"></section> ( bootstrapmade.com )
MAL <div id="about"><div>************


1. Pone las plantillas html que quieras dentro
de la carpeta __BOOTSTRAP.


(CONSOLA)
2. cd a carpeta trim

3.
run_all.py
le hace trim con todas las plantillas dentro de __BOOTSTRAP
y te crea una carpeta de django con el nombre de la plantilla
en minuscula por cada una.

run_single.py
te deja tipiar para elegir una de las plantiilas  
dentro de __BOOTSTRAP y te crea una carpeta de django
con el nombre de la plantilla en minuscula.

4. 
CD "la carpeta que te creo"
manage.py runserver
(chrome)
http://localhost:8000 


***Fijate que los links css "bootstrap-icons, remixicons, boxicons" están comentados en el base html.
***eso porque use CDNs para traer esos iconos en vez de los archivos locales.
***si lo decomentas empieza a haber comportamientos raros porque trae estilos de los dos lados (CDN, y archivos locales).
