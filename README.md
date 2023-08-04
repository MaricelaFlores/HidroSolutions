# HidroSolutions
![Hidro Solutions](https://github.com/MaricelaFlores/HIDRO_SOLUTIONS1/blob/main/logo2.jpg)

Indice de riego para la región de Coquimbo
## Table of Contents
1. [Información General](#info-general)
2. [Descripción del código](#descripción-del-código)
3. [Tecnologías](#tecnologias)
### General Info
La dinámica de la agricultura y la optimización del uso del recurso hídrico, son importantes en el contexto actual, dado que el escenario a nivel mundial muestra cambios abruptos en cuanto al clima, lo cual motiva a la implementación de soluciones. Es por esto que Hidro Solutions busca calcular el índice de riego, mediante un análisis preciso de la relación entre el agua y la agricultura, para poder dar soluciones a la gestión del recurso. 
### Descripción del código

1. FUNCION QUE RECIBE LA CAPA DEL PREDIO Y LA VARIABLE Y RETORNA EL ESTADÍSTICO RELEVANTE
   
![image](https://github.com/MaricelaFlores/HIDRO_SOLUTIONS1/blob/main/COD_1.png)

   - Esta primera parte del código realiza un análisis espacial y estadístico entre dos capas geográficas y realiza cálculos para obtener un valor promedio en una 
     de las capas, luego lo une y agrega a la capa original con el campo "id_predio" como identificador único. Además, asegura que los valores calculados no sean 
     nulos o negativos, reemplazándolos por ceros si es necesario.

     
2. NORMALIZACIÓN DE DATOS
   
![image](https://github.com/MaricelaFlores/HIDRO_SOLUTIONS1/blob/main/COD_2.png)

   - Esta contianuación de código normaliza los valores del campo especificado en la capa de parcelas dividiéndolos por el valor máximo encontrado en 
     dicho campo. Los valores normalizados se almacenan en un nuevo campo llamado campo_normalizado. La normalización permite que los valores se expresen en una 
     escala relativa entre 0 y 1, lo que facilita la comparación y el análisis de los datos, este proceso es realizado para cada variable numérica (temperatura, 
     precipitación, humedad y evapotranspiración).

     
3. CALCULAR CAMPOS DE ACUERDO A LA PONDERACION

![image](https://github.com/MaricelaFlores/HIDRO_SOLUTIONS1/blob/main/COD_3.png)

   -  Finalmente este código realiza cálculos y actualizaciones en diferentes campos de una capa de parcelas, utilizando las ponderaciones de Saaty designadas 
      definidas en el código para calcular el campo del índice. Los cálculos y actualizaciones se realizan utilizando cursores de actualización para recorrer los 
      registros en la capa. Los resultados finales proporcionarán una evaluación compuesta de los valores de las variables de cada parcela de acuerdo a las 
      ponderaciones establecidas.

### Technologies

A list of technologies used within the project:
* [ArcGIS Pro](https://www.esri.cl/es-cl/productos/arcgis-pro/overview): Version 3.0 
* [ArcPy](https://desktop.arcgis.com/es/arcmap/latest/analyze/arcpy/what-is-arcpy-.htm#:~:text=ArcPy%20es%20un%20paquete%20de,automatizaci%C3%B3n%20de%20mapas%20con%20Python.): Version 3.0
* [ArcGIS Online](https://www.esri.com/en-us/arcgis/products/arcgis-online/overview): Version 3.0
  




© [Hidro Solutions] - Todos los derechos reservados.
