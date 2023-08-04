"""
Script documentation

- Tool parameters are accessed using arcpy.GetParameter() or 
                                     arcpy.GetParameterAsText()
- Update derived parameter values using arcpy.SetParameter() or
                                        arcpy.SetParameterAsText()
"""
import arcpy
from arcpy import env
import os 

# Definir entorno
aprx = arcpy.mp.ArcGISProject("CURRENT")
aprxMap = aprx.listMaps()[0]
layers = aprxMap.listLayers()
layers = layers[0:len(layers)-2]
#Limpiar tabla de contenido, pero mantener mapa base
for layer in layers:
   aprxMap.removeLayer(layer)
#Limpiar tablas
tables = aprxMap.listTables()
for table in tables:
   aprxMap.removeTable(table)


def script_tool(predio, id_predio, humedad, id_hum, val_hum, precipitacion, id_pp, vap_pp, temperatura, id_tem, val_tem, 
                evapotranspiracion, id_evapo, val_evapo, outDirPred, outDirVal, outDirSal, usos, id_usos, val_usos):
    """Script code goes below"""

    return

if __name__ == "__main__":

    predio = arcpy.GetParameter(0)
    id_predio = arcpy.GetParameterAsText(1)
    humedad = arcpy.GetParameter(2)
    id_hum = arcpy.GetParameterAsText(3)
    val_hum = arcpy.GetParameterAsText(4)
    precipitacion = arcpy.GetParameter(5)
    id_pp = arcpy.GetParameterAsText(6)
    val_pp = arcpy.GetParameterAsText(7)
    temperatura = arcpy.GetParameter(8)
    id_tem = arcpy.GetParameterAsText(9)
    val_tem = arcpy.GetParameterAsText(10)
    evapotranspiracion = arcpy.GetParameter(11)
    id_evapo = arcpy.GetParameterAsText(12)
    val_evapo = arcpy.GetParameterAsText(13)
    usos = arcpy.GetParameter(14)
    id_usos = arcpy.GetParameterAsText(15)
    val_usos = arcpy.GetParameterAsText(16)    
    outDirPred = arcpy.GetParameterAsText(17)
    outDirVal = arcpy.GetParameterAsText(18)
    outDirSal = arcpy.GetParameterAsText(19)

    script_tool(predio, id_predio, humedad, id_hum, val_hum, precipitacion, id_pp, val_pp,temperatura, id_tem, 
                val_tem, evapotranspiracion, id_evapo, val_evapo, outDirPred, outDirVal, outDirSal, usos, id_usos, val_usos)
    arcpy.SetParameterAsText(19, "Result")

arcpy.AddMessage("Se iniciaron los parámetros de entrada")
arcpy.AddMessage("Tarea Iniciada")
arcpy.AddMessage(id_usos)
######################################################################################################
#RENOMBRAR
######################################################################################################
aprxMap = aprx.listMaps()[0]

rename = []
rename.append(humedad)
rename.append(precipitacion)
rename.append(temperatura)
rename.append(evapotranspiracion)
rename.append(usos)

nameVar = ["humedad", "precipitacion", "temperatura", "evapotranspiracion", "usos"]

def reName(fcIn, fcOut):
    output = os.path.join(outDirVal, fcOut)
    try:
        arcpy.management.Rename(fcIn, output, "FeatureClass")
        return fcOut
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        return None

for i in range(len(rename)):
    reName(rename[i], nameVar[i])

aprxMap.addDataFromPath(humedad)
aprxMap.addDataFromPath(precipitacion)
aprxMap.addDataFromPath(temperatura)
aprxMap.addDataFromPath(evapotranspiracion)
aprxMap.addDataFromPath(usos)

arcpy.AddMessage("Variables ingresadas correctamente")

parcela = "parcela"
output = "{}\{}".format(outDirSal, parcela)
arcpy.management.Copy(predio, output, "FeatureClass", None)

aprxMap.addDataFromPath(output)
arcpy.AddMessage(output)
arcpy.AddMessage("Parcela ingresada correctamente")
# ########################################################################################################
# #                                         DEFINCION DE FUNCIONES NUMERICAS                             #
# ########################################################################################################

# FUNCION QUE RECIBE LA CAPA DEL PREDIO Y LA VARIABLE Y RETORNA EL ESTADÍSTICO RELEVANTE
def mapp(nVar, idCapa, valCapa, out):
    mappings = arcpy.FieldMappings()    
    
    cCamposVar = []
    cCamposVar.append(str(idCapa))
    cCamposVar.append(str(valCapa))
    groupby = "{} MEAN".format(str(valCapa))        
    cCamposPred = []
    cCamposPred.append(str(id_predio))    
    spacial_join = out + "\\" + "sp_{}".format(nVar)
    prom_campo = "MEAN_{}".format(valCapa)
    campo_parcelas = arcpy.FieldMap()
    campo_parcelas.addInputField(parcela, cCamposPred[0])
    mappings.addFieldMap(campo_parcelas)
    
    for i in cCamposVar:
        campo_variable = arcpy.FieldMap()
        campo_variable.addInputField(nVar, i)
        mappings.addFieldMap(campo_variable)
            
    arcpy.analysis.SpatialJoin(parcela, nVar, spacial_join, "JOIN_ONE_TO_MANY", "KEEP_ALL", mappings, "INTERSECT")
    aprxMap.addDataFromPath(spacial_join)
    
    gdb = os.path.dirname(out)
    outTemp = gdb + "\\" + "outTemp"
    arcpy.analysis.Statistics(spacial_join, outTemp, groupby, cCamposPred[0],"")
    arcpy.management.JoinField(parcela, cCamposPred[0], outTemp, cCamposPred[0], prom_campo,"NOT_USE_FM",None)
    
    #donde sea nulo reemplazar con 0
    exp = "format(!{}!)".format(str(prom_campo))
    code_block="""def format(a):
    if a is not None and a >= 0:
        return a
    else:
        return 0"""
    arcpy.management.CalculateField(parcela, prom_campo, exp,"PYTHON3",code_block, "TEXT", "NO_ENFORCE_DOMAINS")
    return parcela
    
########################################################################################################
#                                         CALCULOS NUMERICOS                                          #
########################################################################################################
mapp(nameVar[0], id_hum, val_hum, outDirSal)
mapp(nameVar[1], id_pp, val_pp, outDirSal)
mapp(nameVar[2], id_tem, val_tem, outDirSal)
mapp(nameVar[3], id_evapo, val_evapo, outDirSal)

arcpy.AddMessage("hasta aqui")
# ########################################################################################################
# #                                         CALCULOS CATEGORICOS                                          #
# ########################################################################################################
#para usos
mappings = arcpy.FieldMappings()
c_usos = []
c_usos.append(id_usos)
c_usos.append(val_usos)

variable = nameVar[4]
campos_variable = [str(id_predio)]
spacial_join = outDirSal + "\\" + "sp_usos"
gdb = os.path.dirname(outDirSal)
outTemp = gdb + "\\" + "outTemp"

#Fieldmappings para los campos
for i in campos_variable:
    campo_parcelas = arcpy.FieldMap()
    campo_parcelas.addInputField(parcela, i)
    mappings.addFieldMap(campo_parcelas)

for i in c_usos:
    campo_usos = arcpy.FieldMap()
    campo_usos.addInputField(variable, i)
    mappings.addFieldMap(campo_usos)

#spacialjoin entre parcelas y la variable
arcpy.analysis.SpatialJoin(parcela, variable, spacial_join, "JOIN_ONE_TO_MANY", "KEEP_ALL", mappings, "INTERSECT")
#Frecuencia
arcpy.analysis.Frequency(spacial_join, outTemp, "{};{}".format(str(val_usos), str(id_predio), id_usos))

#groupby
#crear tabla
outTemp1 = "outTemp1"
arcpy.management.CreateTable(gdb, outTemp1, outTemp)

# Crear una lista para almacenar los registros de la tabla de entrada
registros = []

# Utilizar un cursor de búsqueda para recorrer la tabla de entrada y obtener los registros
with arcpy.da.SearchCursor(outTemp, [str(id_predio), str(val_usos), "FREQUENCY"]) as cursor:
    frecuencia = {}   
    for a, b, c in cursor:
        if a in frecuencia and c > frecuencia[a]["FREQUENCY"]:
            frecuencia[a] = {str(val_usos): b, "FREQUENCY": c}
        elif a not in frecuencia:
            frecuencia[a] = {str(val_usos): b, "FREQUENCY": c}

with arcpy.da.InsertCursor(outTemp1, [str(id_predio), str(val_usos), "FREQUENCY"]) as cursor_insert:
    for a, info in frecuencia.items():
        cursor_insert.insertRow((a, info[str(val_usos)], info["FREQUENCY"]))
    
# #unir a parcelas
arcpy.management.JoinField(parcela, str(id_predio), outTemp1, str(id_predio), str(val_usos),"NOT_USE_FM", None)

# exp = "format(!{}!)".format(val_usos)
# code_block = """def format(a):
#     if a is not None and a >= 0:
#         return a
#     else:
#         return 0 if a is None else a"""
# arcpy.management.CalculateField(parcela, val_usos, exp, "PYTHON3", code_block, "TEXT", "NO_ENFORCE_DOMAINS")



del cursor
del cursor_insert
#######################################################################################################################
# Campo a normalizar
parcela = "parcela"
campo_a = "MEAN_{}".format(str(val_hum))

# Calcular el valor máximo del campo_a
max_value = 0
with arcpy.da.SearchCursor(parcela, campo_a) as cursor:
    for row in cursor:
        if row[0] > max_value:
            max_value = row[0]
del cursor
            
# Normalizar el campo_a y almacenar los resultados en una lista
lista_valores_normalizados = []
with arcpy.da.SearchCursor(parcela, campo_a) as cursor:
    for row in cursor:
        valor_normalizado = row[0] / max_value
        lista_valores_normalizados.append(valor_normalizado)
del cursor       
# Nuevo campo para almacenar los valores normalizados
campo_normalizado = "norm_hum"

# Agregar el nuevo campo a la parcela
arcpy.AddField_management(parcela, campo_normalizado, "DOUBLE")

# Actualizar los registros de la parcela con los valores normalizados
with arcpy.da.UpdateCursor(parcela, [campo_a, campo_normalizado]) as cursor:
    for row, valor_normalizado in zip(cursor, lista_valores_normalizados):
        row[1] = valor_normalizado
        cursor.updateRow(row)

del cursor
# Precipitacion

# Campo a normalizar 
campo_a = "MEAN_{}".format(str(val_pp))

# Calcular el valor máximo del campo_a
max_value = 0
with arcpy.da.SearchCursor(parcela, campo_a) as cursor:
    for row in cursor:
        if row[0] > max_value:
            max_value = row[0]
del cursor

# Normalizar el campo_a y almacenar los resultados en una lista
lista_valores_normalizados = []
with arcpy.da.SearchCursor(parcela, campo_a) as cursor:
    for row in cursor:
        valor_normalizado = row[0] / max_value
        lista_valores_normalizados.append(valor_normalizado)
del cursor
       
# Nuevo campo para almacenar los valores normalizados
campo_normalizado = "norm_pp"

# Agregar el nuevo campo a la parcela
arcpy.AddField_management(parcela, campo_normalizado, "DOUBLE")

# Actualizar los registros de la parcela con los valores normalizados
with arcpy.da.UpdateCursor(parcela, [campo_a, campo_normalizado]) as cursor:
    for row, valor_normalizado in zip(cursor, lista_valores_normalizados):
        row[1] = valor_normalizado
        cursor.updateRow(row)

del cursor

# Temperatura
# Campo a normalizar 
campo_a = "MEAN_{}".format(str(val_tem))

# Calcular el valor máximo del campo_a
max_value = 0
with arcpy.da.SearchCursor(parcela, campo_a) as cursor:
    for row in cursor:
        if row[0] > max_value:
            max_value = row[0]
del cursor

# Normalizar el campo_a y almacenar los resultados en una lista
lista_valores_normalizados = []
with arcpy.da.SearchCursor(parcela, campo_a) as cursor:
    for row in cursor:
        valor_normalizado = row[0] / max_value
        lista_valores_normalizados.append(valor_normalizado)

del cursor
        
# Nuevo campo para almacenar los valores normalizados
campo_normalizado = "norm_temp"

# Agregar el nuevo campo a la parcela
arcpy.AddField_management(parcela, campo_normalizado, "DOUBLE")

# Actualizar los registros de la parcela con los valores normalizados
with arcpy.da.UpdateCursor(parcela, [campo_a, campo_normalizado]) as cursor:
    for row, valor_normalizado in zip(cursor, lista_valores_normalizados):
        row[1] = valor_normalizado
        cursor.updateRow(row)

del cursor

# Evapotranspiración

# Campo a normalizar 
campo_a = "MEAN_{}".format(str(val_evapo))

# Calcular el valor máximo del campo_a
max_value = 0
with arcpy.da.SearchCursor(parcela, campo_a) as cursor:
    for row in cursor:
        if row[0] > max_value:
            max_value = row[0]
del cursor

# Normalizar el campo_a y almacenar los resultados en una lista
lista_valores_normalizados = []
with arcpy.da.SearchCursor(parcela, campo_a) as cursor:
    for row in cursor:
        valor_normalizado = row[0] / max_value
        lista_valores_normalizados.append(valor_normalizado)

del cursor        
# Nuevo campo para almacenar los valores normalizados
campo_normalizado = "norm_evap"

# Agregar el nuevo campo a la parcela
arcpy.AddField_management(parcela, campo_normalizado, "DOUBLE")

# Actualizar los registros de la parcela con los valores normalizados
with arcpy.da.UpdateCursor(parcela, [campo_a, campo_normalizado]) as cursor:
    for row, valor_normalizado in zip(cursor, lista_valores_normalizados):
        row[1] = valor_normalizado
        cursor.updateRow(row)

del cursor
##########################################################################################################################
# LIMPIAR CONTENIDO
##########################################################################################################################
#ELIMINAR TABLAS TEMPORALES
eliminar = ["outTemp", "outTemp1"]
for i in eliminar:
    i_completo = gdb + "\\" + i
    arcpy.management.Delete(i_completo)
#ELIMINAR CAPAS TEMPORALES
eliminar = ["sp_humedad", "sp_precipitacion", "sp_temperatura", "sp_evapotranspiracion", "sp_usos"]
for i in eliminar:
    i_completo = outDirSal + "\\" + i
    arcpy.management.Delete(i_completo)
        
###########################################################################################################################
# CALCULAR CAMPOS DE ACUERDO A LA PONDERACION
###########################################################################################################################
#PONDERACIONES SEGÚN SAATY
pond_hum = 0.07
pond_pp = 0.1
pond_tem = 0.21
pond_evapo = 0.15
pond_suelo = 0.47
tipo_suelo = [0.49, 0.35, 0.1, 0.06]

#COLUMNAS A AGREGAR
campo_suelo = "suelo"
c_hum = "valor_humedad"
c_pp = "valor_precipitacion"
c_tem = "valor_temperatura"
c_ev = "valor_evapotranspiracion"
c_su = "valor_suelo"
campo_ev = "valor_evaluacion"
tyCampo = "FLOAT"
cam_agregar = [campo_suelo, c_hum, c_pp, c_tem, c_ev, c_su, campo_ev]

for i in range(len(cam_agregar)):
    arcpy.management.AddField(parcela, cam_agregar[i], tyCampo)

#CALCULAR EL NUEVO CAMPO DE USO DE SUELO
camposc = [val_usos, campo_suelo]
cursor = arcpy.da.UpdateCursor(parcela, camposc)

for row in cursor:
    if (row[0] == "01"):
        row[1] = 0.49
    elif (row[0] == "02"):
        row[1] = 0.35
    elif (row[0] == "03"):
        row[1] = 0.1
    elif (row[0] == "04"):
        row[1] = 0.06
    else:
        row[1] = 0
    cursor.updateRow(row)
    arcpy.AddMessage(row[0])
del cursor

campos_norm = ["norm_hum", "norm_pp", "norm_temp", "norm_evap"]

#PONDERACIONES DE CADA CAMPO NUMERICO
def calculo_campo(campo1, campo2, pp, ponderacion):
    cursor = arcpy.UpdateCursor(pp)
    for row in cursor:
        row.setValue(campo2, row.getValue(campo1) * ponderacion)
        cursor.updateRow(row)

calculo_campo(campos_norm[0], c_hum,  parcela, pond_hum)
calculo_campo(campos_norm[1], c_pp,  parcela, pond_pp)
calculo_campo(campos_norm[2], c_tem, parcela, pond_tem)
calculo_campo(campos_norm[3], c_ev,  parcela, pond_evapo)
calculo_campo(str(campo_suelo), c_su,  parcela, pond_suelo)

#####################################################################################################
campo1 = "valor_humedad"
campo2 = "valor_evaluacion"
campo3 = "valor_precipitacion"
campo4 = "valor_temperatura"
campo5 = "valor_evapotranspiracion"
campo6 = "valor_suelo"

cursor = arcpy.UpdateCursor(parcela)
for row in cursor:
    row.setValue(campo2, row.getValue(campo1) +row.getValue(campo3) +row.getValue(campo4) +row.getValue(campo5) +row.getValue(campo6)) 
    cursor.updateRow(row)
