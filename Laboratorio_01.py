import json
import os

def esperar_enter():
    input("Presiona Enter para continuar...")

def multiplicar_ascii(nombre,):
    resultado = 1  

    for caracter in nombre:
        valor_ascii = ord(caracter)  # obtiene el valor ascii por cada uno de los caracteres dentro de mi nombre
        resultado *= valor_ascii     # multiplica el calor ascii por los valores encontrados anteriormente

    return resultado
    
def limpiar_consola():
    sistema_operativo = os.name
    if sistema_operativo == 'posix':
        # Para sistemas basados en Unix/Linux/Mac
        os.system('clear')
    elif sistema_operativo == 'nt':
        # Para sistemas Windows
        os.system('cls')


# DATOS DE EL CLIENTE
class cliente:
    def __init__(self, unico, Nombre, Dpi, fecha_nacimiento, Direccion):
        self.Unico = unico
        self.Nombre = Nombre
        self.Dpi = Dpi
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = Direccion

# COSAS INICIALES DEL NODO
class Nodo:
    def __init__(self, cliente):
        self.cliente = cliente
        self.izquierda = None
        self.derecha = None

class ArbolAvl:
    def __init__(self):
        self.raiz = None
    
    def buscar_por_nombre(self, nombre):
        if self.raiz is not None:
            resultados = []
            self._buscar_nombre(self.raiz, nombre.upper(), resultados)
            if resultados:
                return resultados
            else:
                return None
        else:
            return None

    def _buscar_nombre(self, nodo, nombre, resultados):
        if nodo is not None:
            self._buscar_nombre(nodo.izquierda, nombre, resultados)
            if nodo.cliente.Nombre.upper() == nombre: 
                resultados.append({
                    "Nombre": nodo.cliente.Nombre,
                    "DPI": nodo.cliente.Dpi,
                    "Fecha de Nacimiento": nodo.cliente.fecha_nacimiento,
                    "Dirección": nodo.cliente.direccion
                })
            self._buscar_nombre(nodo.derecha, nombre, resultados)

    def _impresion_arbol(self, nodo):
        if nodo is not None:
            self._impresion_arbol(nodo.izquierda)
            print("Nombre:", nodo.cliente.Nombre + " DPI: ", nodo.cliente.Dpi + " Fecha de nacimiento: " + nodo.cliente.fecha_nacimiento + " Direccion: " + nodo.cliente.direccion)
            self._impresion_arbol(nodo.derecha)
    
    def imprimir(self):
        if self.raiz is not None:
            self._impresion_arbol(self.raiz)
    
    # Insertar un cliente en el árbol AVL
    def agregar(self, cliente):
        if not self.raiz:
            self.raiz = Nodo(cliente)
        else:
            self.raiz = self.__agregar_datos(self.raiz, cliente)

    def __agregar_datos(self, nodo, cliente):
        if nodo is None:
            return Nodo(cliente)
        
        if cliente.Unico < nodo.cliente.Unico:
            nodo.izquierda = self.__agregar_datos(nodo.izquierda, cliente)
        else:
            nodo.derecha = self.__agregar_datos(nodo.derecha, cliente)
        
        # Calcular el factor de equilibrio
        factor_equilibrio = self.__calcular_factor_equilibrio(nodo)
        
        # Rotaciones para reequilibrar el árbol AVL
        if factor_equilibrio > 1:
            if cliente.Unico < nodo.izquierda.cliente.Unico:
                return self.__rotacion_derecha(nodo)
            else:
                nodo.izquierda = self.__rotacion_izquierda(nodo.izquierda)
                return self.__rotacion_derecha(nodo)
        if factor_equilibrio < -1:
            if cliente.Unico > nodo.derecha.cliente.Unico:
                return self.__rotacion_izquierda(nodo)
            else:
                nodo.derecha = self.__rotacion_derecha(nodo.derecha)
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
    
    def eliminar(self, Unico):
        eliminado, self.raiz = self.__eliminar_dato(self.raiz, Unico)  # Cambia esta línea
        return eliminado

    def __eliminar_dato(self, nodo, Unico):  # Cambia esta línea
        if nodo is None:
            # No se encontró el nodo a eliminar
            return False, nodo

        if Unico < nodo.cliente.Unico:
            eliminado, nodo.izquierda = self.__eliminar_dato(nodo.izquierda, Unico)  # Cambia esta línea
        elif Unico > nodo.cliente.Unico:
            eliminado, nodo.derecha = self.__eliminar_dato(nodo.derecha, Unico)  # Cambia esta línea
        else:
            # Nodo encontrado, realizar eliminación
            if nodo.izquierda is None:
                return True, nodo.derecha
            elif nodo.derecha is None:
                return True, nodo.izquierda

            # Nodo con dos hijos, encontrar sucesor inorden
            sucesor = self.__encontrar_sucesor(nodo.derecha)
            nodo.cliente = sucesor.cliente
            eliminado, nodo.derecha = self.__eliminar_dato(nodo.derecha, sucesor.cliente.Unico)  # Cambia esta línea

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

    def buscar_por_unico(self, Unico):
        if self.raiz is not None:
            nodo, padre = self.__buscar_por_unico(self.raiz, Unico, None)
            return nodo, padre
        else:
            return None, None

    def __buscar_por_unico(self, nodo, Unico, padre):
        if nodo is None:
            return None, padre

        if Unico == nodo.cliente.Unico:
            return nodo, padre
        elif Unico < nodo.cliente.Unico:
            return self.__buscar_por_unico(nodo.izquierda, Unico, nodo)
        else:
            return self.__buscar_por_unico(nodo.derecha, Unico, nodo)

    def actualizar_datos_por_unico(self, Unico, nueva_fecha_nacimiento=None, nueva_direccion=None):
        nodo, _ = self.__buscar_por_unico(self.raiz, Unico, None)  # Cambia esta línea
        if nodo is not None:
            # Actualizar fecha de nacimiento si se proporciona
            if nueva_fecha_nacimiento is not None:
                nodo.cliente.fecha_nacimiento = nueva_fecha_nacimiento

            # Actualizar dirección si se proporciona
            if nueva_direccion is not None:
                nodo.cliente.direccion = nueva_direccion

            print(f"Datos actualizados para DPI {Unico}")
        else:
            print(f"No se encontró ningún cliente con DPI {Unico}, no se realizaron actualizaciones.")


file = "C:/Users/Saul/Downloads/datos (1).txt"
arbol = ArbolAvl()

#lectura de json
with open(file, "r") as f:
    for line in f:
        # Split the line into parts
        parts = line.strip().split(';')
        
        if len(parts) < 2:
            print(f"Error en línea: {line}")
            continue
        
        action = parts[0]
        json_data = parts[1]
            
        try:
            data = json.loads(json_data)
            Nombre = data["name"]
            Dpi = data["dpi"]
            fecha_nacimiento = data.get("dateBirth")
            direccion = data.get("address")
            Unico = multiplicar_ascii(Nombre) + int(Dpi)
#insertar
            if action == "INSERT":
                nuevo_cliente = cliente(Unico, Nombre, Dpi, fecha_nacimiento, direccion)
                arbol.agregar(nuevo_cliente)
                print("INSERTADO:")
#patch
            elif action == "PATCH":
                if fecha_nacimiento is not None or direccion is not None:
                    arbol.actualizar_datos_por_unico(Unico, nueva_fecha_nacimiento=fecha_nacimiento, nueva_direccion=direccion)
                    print("SE ACTUALIZARON LOS DATOS")
                else:
                    print(f"No se proporcionaron datos válidos para actualizar en la línea: {line}")
#eliminar
            elif action == "DELETE":
                eliminado = arbol.eliminar(int(Unico))
                if eliminado:
                    print("ELIMINADO:")
                else:
                    print(f"No se encontró ningún cliente con DPI {Dpi}")
            else:
                print(f"Acción no reconocida en línea: {line}")
                
            print("name: " + Nombre + " dpi: " + Dpi + " date_birth: " + str(fecha_nacimiento) + " Adress: " + str(direccion))
            
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON en la línea: {line}")
            print(f"Detalles del error: {e}")

limpiar_consola()
opcion = 0



#menu
while opcion != 3:  # El bucle se ejecutará mientras opcion sea diferente de 3
    print("*********************BIENVENIDO A TALENTHUB*********************")
    print("                     **********************                     ")
    
    # Validación de entrada
    opcion_valida = False
    while not opcion_valida:
        opcion_str = input("INGRESE EL NUMERO DE LA OPCION AL CUAL QUIERA INGRESAR \n 1.IMPRIMIR TODOS LOS DATOS GUARDADOS \n 2.BUSCAR POR NOMBRE \n 3.SALIR \n***************************************************************** \n")
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
        nombre_a_buscar = input("INGRESE EL NOMBRE DE LA PERSONA DE LA CUAL QUIERE EL REGISTRO DE INFORMACIÓN: ")
        nombre_a_buscar = nombre_a_buscar.upper()
        resultados = arbol.buscar_por_nombre(nombre_a_buscar)
        if resultados:
            print(resultados)
            nombre_archivo = "datosBuscados_arbol.txt"
            esperar_enter()
            limpiar_consola()
        else:
            print("NO SE ENCONTRÓ A LA PERSONA QUE USTED BUSCA")
            esperar_enter()
            limpiar_consola()
    elif opcion == 3:
        # El bucle se detendrá automáticamente al salir
        pass

    else:
        print("*Por favor, ingrese un número válido*")
        esperar_enter()
        limpiar_consola()

limpiar_consola()