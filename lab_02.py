import json
import os

class Cliente:
    def __init__(self, Nombre, Dpi, fecha_nacimiento, direccion, empresas, codificacion):
        self.Nombre = Nombre
        self.Dpi = Dpi
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.empresas = empresas
        self.codificacion = codificacion

def comprimir_lzw(data):
    diccionario = {chr(i): i for i in range(256)}  # Inicializar el diccionario con caracteres ASCII
    resultado = []
    codigo_actual = 256
    cadena = ""

    for caracter in data:
        cadena_actual = cadena + caracter
        if cadena_actual in diccionario:
            cadena = cadena_actual
        else:
            resultado.append(diccionario[cadena])  # Agregar el código numérico al resultado
            diccionario[cadena_actual] = codigo_actual
            codigo_actual += 1
            cadena = caracter

    if cadena:
        resultado.append(diccionario[cadena])  # Agregar el código numérico del último carácter

    return resultado

def descomprimir_lzw(comprimido):
    diccionario = {i: chr(i) for i in range(256)}  # Inicializar el diccionario con caracteres ASCII
    codigo_actual = 256
    cadena_actual = ""
    resultado = []

    for codigo_numerico in comprimido:
        if codigo_numerico in diccionario:
            entrada = diccionario[codigo_numerico]
        elif codigo_numerico == codigo_actual:
            entrada = cadena_actual + cadena_actual[0]
        else:
            raise ValueError("Código desconocido en la secuencia comprimida")

        resultado.extend(entrada)
        if cadena_actual:
            diccionario[codigo_actual] = cadena_actual + entrada[0]
            codigo_actual += 1
        cadena_actual = entrada

    return ''.join(resultado)

def concatenar_dpi_empresas(Dpi, empresas):
    return [f"{empresa} + {Dpi}" for empresa in empresas]

def esperar_enter():
    input("Presiona Enter para continuar...")

def limpiar_consola():
    sistema_operativo = os.name
    if sistema_operativo == 'posix':
        # Para sistemas basados en Unix/Linux/Mac
        os.system('clear')
    elif sistema_operativo == 'nt':
        # Para sistemas Windows
        os.system('cls')


class Nodo:
    def __init__(self, cliente):
        self.cliente = cliente
        self.izquierda = None
        self.derecha = None

class ArbolAvl:
    def __init__(self):
        self.raiz = None
#*********************
    def _impresion_arbol(self, nodo):
        if nodo is not None:
            self._impresion_arbol(nodo.izquierda)
            print("Nombre:", nodo.cliente.Nombre  + " Fecha de nacimiento: " + nodo.cliente.fecha_nacimiento + " Direccion: " + nodo.cliente.direccion)
            self._impresion_arbol(nodo.derecha)
    
    def imprimir(self):
        if self.raiz is not None:
            self._impresion_arbol(self.raiz)
    
    def _impresion_arbol_codificado(self, nodo):
        if nodo is not None:
            self._impresion_arbol_codificado(nodo.izquierda)
            print("DATOS PRIVADOS:", nodo.cliente.codificacion)
            self._impresion_arbol_codificado(nodo.derecha)
#*********************

    def imprimir_codificado(self):
        if self.raiz is not None:
            self._impresion_arbol_codificado(self.raiz)
    
    # Insertar un cliente en el árbol AVL
    def agregar(self, cliente):
        if not self.raiz:
            self.raiz = Nodo(cliente)
        else:
            self.raiz = self.__agregar_datos(self.raiz, cliente)

    def __agregar_datos(self, nodo, cliente):
        if nodo is None:
            return Nodo(cliente)
        
        if cliente.Dpi < nodo.cliente.Dpi:
            nodo.izquierda = self.__agregar_datos(nodo.izquierda, cliente)
        else:
            nodo.derecha = self.__agregar_datos(nodo.derecha, cliente)
        
        # Calcular el factor de equilibrio
        factor_equilibrio = self.__calcular_factor_equilibrio(nodo)
        
        # Rotaciones para reequilibrar el árbol AVL
        if factor_equilibrio > 1:
            if cliente.Dpi < nodo.izquierda.cliente.Dpi:
                return self.__rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.__rotacion_izquierda(nodo.izquierda)
                return self.__rotacion_derecha(nodo)
        if factor_equilibrio < -1:
            if cliente.Dpi > nodo.derecha.cliente.Dpi:
                return self.__rotacion_izquierda(nodo)
            else:
                nodo.Dpi = self.__rotacion_derecha(nodo.derecha)
                return self.__rotacion_izquierda(nodo)
        
        return nodo
    
    def __calcular_factor_equilibrio(self, nodo):
        return self.__altura(nodo.izquierda) - self.__altura(nodo.derecha)
    
    def __altura(self, nodo):
        if nodo is None:
            return 0
        return max(self.__altura(nodo.izquierda), self.__altura(nodo.derecha)) + 1
    
    def __rotacion_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        
        y.derecha = z
        z.izquierda = T3
        
        return y
    
    def __rotacion_izquierda(self, y):
        x = y.derecha
        T2 = x.izquierda
        
        x.izquierda = y
        y.derecha = T2
        
        return x
    
    def eliminar(self, Dpi):
        eliminado, self.raiz = self.__eliminar_dato(self.raiz, Dpi)  # Cambia esta línea
        return eliminado

    def __eliminar_dato(self, nodo, Dpi):  # Cambia esta línea
        if nodo is None:
            # No se encontró el nodo a eliminar
            return False, nodo

        if Dpi < nodo.cliente.Dpi:
            eliminado, nodo.izquierda = self.__eliminar_dato(nodo.izquierda, Dpi)  # Cambia esta línea
        elif Dpi > nodo.cliente.Dpi:
            eliminado, nodo.derecha = self.__eliminar_dato(nodo.derecha, Dpi)  # Cambia esta línea
        else:
            # Nodo encontrado, realizar eliminación
            if nodo.izquierda is None:
                return True, nodo.derecha
            elif nodo.derecha is None:
                return True, nodo.izquierda

            # Nodo con dos hijos, encontrar sucesor inorden
            sucesor = self.__encontrar_sucesor(nodo.derecha)
            nodo.cliente = sucesor.cliente
            eliminado, nodo.derecha = self.__eliminar_dato(nodo.derecha, sucesor.cliente.Dpi)  # Cambia esta línea

        # Actualizar el factor de equilibrio y equilibrar el árbol
        nodo = self.__actualizar_factor_equilibrio(nodo)

        return eliminado, nodo


    def __encontrar_sucesor(self, nodo):
        if nodo.izquierda is None:
            return nodo
        return self.__encontrar_sucesor(nodo.izquierda)

    def __actualizar_factor_equilibrio(self, nodo):
        factor_equilibrio = self.__calcular_factor_equilibrio(nodo)

        if factor_equilibrio > 1:
            if self.__calcular_factor_equilibrio(nodo.izquierda) >= 0:
                return self.__rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.__rotacion_izquierda(nodo.izquierda)
                return self.__rotacion_derecha(nodo)
        elif factor_equilibrio < -1:
            if self.__calcular_factor_equilibrio(nodo.derecha) <= 0:
                return self.__rotacion_izquierda(nodo)
            else:
                nodo.derecha = self.__rotacion_derecha(nodo.derecha)
                return self.__rotacion_izquierda(nodo)

        return nodo

    def buscar_por_Dpi(self, Dpi):
        if self.raiz is not None:
            nodo, padre = self.__buscar_por_Dpi(self.raiz, Dpi, None)
            return nodo, padre
        else:
            return None, None

    def __buscar_por_Dpi(self, nodo, Dpi, padre):
        if nodo is None:
            return None, padre

        if Dpi == nodo.cliente.Dpi:
            return nodo, padre
        elif Dpi < nodo.cliente.Dpi:
            return self.__buscar_por_Dpi(nodo.izquierda, Dpi, nodo)
        else:
            return self.__buscar_por_Dpi(nodo.derecha, Dpi, nodo)
        

    def actualizar_datos_por_Dpi(self, Dpi, nueva_fecha_nacimiento=None, nueva_direccion=None):
        nodo, _ = self.__buscar_por_Dpi(self.raiz, Dpi, None)  # Cambia esta línea
        if nodo is not None:
            # Actualizar fecha de nacimiento si se proporciona
            if nueva_fecha_nacimiento is not None:
                nodo.cliente.fecha_nacimiento = nueva_fecha_nacimiento

            # Actualizar dirección si se proporciona
            if nueva_direccion is not None:
                nodo.cliente.direccion = nueva_direccion

            print(f"Datos actualizados para DPI {Dpi}")
        else:
            print(f"No se encontró ningún cliente con DPI {Dpi}, no se realizaron actualizaciones.")


file = "C:/Users/Saul/Downloads/datos (1).txt"
arbol = ArbolAvl()



# Ruta del archivo CSV
csv_file = r"C:\Users\Saul\Downloads\input (1).csv"

# Ruta del archivo JSON
json_file = r"C:\Users\Saul\Downloads\datos (1).txt"

# Función para procesar la línea de entrada
def procesar_linea(line):
    parts = line.strip().split(';')

    if len(parts) < 2:
        print(f"Error en línea: {line}")
        return

    action = parts[0]
    json_data = parts[1]

    try:
        data = json.loads(json_data)
        Nombre = data["name"]
        Dpi = data["dpi"]
        fecha_nacimiento = data.get("datebirth")
        direccion = data.get("address")
        empresas = data.get("companies")

        # Modificar la estructura de empresas
        if empresas is not None and isinstance(empresas, list):
            empresas_con_dpi = concatenar_dpi_empresas(Dpi, empresas)
        else:
            empresas_con_dpi = []

        # Insertar
        if action == "INSERT":

            data = ' '.join(empresas_con_dpi)
            resultado_lzw = comprimir_lzw(data)
            nuevo_cliente = Cliente(Nombre, Dpi, fecha_nacimiento, direccion, empresas_con_dpi,resultado_lzw)
            arbol.agregar(nuevo_cliente)
            print("INSERTADO:")
            # data_descomprimida = descomprimir_lzw(resultado_lzw)

        # Patch
        elif action == "PATCH":
                if fecha_nacimiento is not None or direccion is not None:
                    arbol.actualizar_datos_por_Dpi(Dpi, nueva_fecha_nacimiento=fecha_nacimiento, nueva_direccion=direccion)
                    print("SE ACTUALIZARON LOS DATOS")
                else:
                    print(f"No se proporcionaron datos válidos para actualizar en la línea: {line}")
#eliminar

        # Eliminar
        elif action == "DELETE":
            eliminado = arbol.eliminar(Dpi)
            if eliminado:
                print("ELIMINADO:")
            else:
                print(f"No se encontró ningún cliente con DPI {Dpi}")
        else:
            print(f"Acción no reconocida en línea: {line}")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON en la línea: {line}")
        print(f"Detalles del error: {e}")

# Lectura de CSV
with open(csv_file, "r") as f:
    for line in f:
        procesar_linea(line)
        
limpiar_consola()
opcion = 0

#menu
while opcion != 4:  # El bucle se ejecutará mientras opcion sea diferente de 3
    print("*********************BIENVENIDO A TALENTHUB*********************")
    print("                     **********************                     ")
    
    # Validación de entrada
    opcion_valida = False
    while not opcion_valida:
        opcion_str = input("INGRESE EL NUMERO DE LA OPCION AL CUAL QUIERA INGRESAR \n 1.IMPRIMIR TODOS LOS DATOS GUARDADOS  \n 2.IMPRIMIR TODOS LOS DATOS GUARDADOS CODIFICADOS \n 3.BUSCAR POR NOMBRE \n 4.SALIR \n***************************************************************** \n")
        if opcion_str.isdigit():
            opcion = int(opcion_str)
            opcion_valida = True
        else:
            print("Por favor, ingrese un número válido.")
            esperar_enter()
            limpiar_consola()

    if opcion == 1:
        arbol.imprimir()
        esperar_enter()
        limpiar_consola()
    
    elif opcion == 2:
        arbol.imprimir_codificado()
        esperar_enter()
        limpiar_consola()


    elif opcion == 3:
        dpi_a_buscar = input("INGRESE EL DPI DE LA PERSONA QUE QUIERE BUSCAR")
        resultados = arbol.buscar_por_Dpi(dpi_a_buscar)
        if resultados:
            print(resultados)
            nombre_archivo = "datosBuscados_arbol.txt"
            esperar_enter()
            limpiar_consola()
        else:
            print("NO SE ENCONTRÓ A LA PERSONA QUE USTED BUSCA")
            esperar_enter()
            limpiar_consola()

    elif opcion == 4:
        # El bucle se detendrá automáticamente al salir
        pass

    else:
        print("*Por favor, ingrese un número válido*")
        esperar_enter()
        limpiar_consola()

limpiar_consola()