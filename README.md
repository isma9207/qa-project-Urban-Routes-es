## Proyecto Sprint 8

El presente proyecto tiene como finalidad la automatización de ciertas pruebas dentro de la aplicación 
Urban Routes donde se solicita un servicio de taxi para llevar al usuario a un destino especificado
con ciertos adicionales para hacer el viaje más ameno a petición del usuario tales como agregar pañuelos, 
una manta y helados. 

Dentro del código se implemento la **Programación Orientada a Objetos (POO)** mediante el uso
de clases e instanacias de clases a tráves del **Modelo de Objetos de Página (POM)** utilizando 
el paquete **Selenium** para el lenguaje de programación **Python**.

##Consideraciones para la ejecución de las pruebas:
* Necesitas tener instalados los paquetes pytest y selenium.
* Es necesario actualizar el valor de la variable 'urban_routes_url' del archivo 'data.py' iniciando el servidor de Urban Routes para ejecutar las pruebas.
* Ejecuta todas las pruebas con el comando 'pytest main.py' desde la terminal.

##Observaciones:
- Las pruebas se ejecutarán una por una, reiniciandoce y comenzando por indicar la ruta cada vez que comience una prueba.
- Es un total de ocho pruebas más una opcional lo que satisface esta automatización.
- Prueba 1. Configurar la dirección de la ruta.
- Prueba 2. Seleccionar la tarifa Comfort.
- Prueba 3. Rellenar el campo de número de teléfono.
- Prueba 4. Agregar un método de pago (Tarjeta de crédito).
- Prueba 5. Escribir un mensaje para el conductor.
- Prueba 6. Añadir una manta y pañuelos al servicio.
- Prueba 7. Añadir dos helados al servicio.
- Prueba 8 y 9. Aparece una ventana emergente en búsqueda de un taxi, cuando finaliza el tiempo en el temporizador aparece la información del conductor.

**NOTA:** La última prueba se compone de dos (Prueba 8 y 9) donde la primera de ellas es solamente donde aparece la ventana emergente
de búsqueda de taxi o automóvil donde aparece un temporizador hasta encontrar uno; mientras que la segunda es donde
aparece la información del conductor. Para fines prácticos se unificaron para que se ejecuten en una sola ya que aparecen
dentro de la misma ventana emergente.