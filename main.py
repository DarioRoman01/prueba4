from autos import Autos
from os import system
from time import sleep

class Menu:
    def validarDato(self, mensaje, maximo):
        while True:
            data = input(mensaje)
            if len(data) < 3 or len(data) > maximo:
                print("Cantidad de caracteres invalida intente de nuevo!")
                continue
            
            return data

    def validarOpcion(self, mensaje, rango=None):
        while True:
            try:
                num = int(input(mensaje))
                if rango is not None:
                    if num not in rango:
                        print("Ingrese una opcion valida!")
                        continue
                
                    
                return num

            except:
                print("Solo se permiten caracteres numericos :(")

    def validarAccion(self, mensaje):
        res = input(mensaje)
        if res.lower() == "si":
            return True

        return False

    def __init__(self) -> None:
        self.crud = Autos(492653, "uwu", "4K54JE", 100, "toyota")

    def ingresarAuto(self):
        numeroMotor = self.validarOpcion("Ingrese el numero de motor del automovil: ")
        año = self.validarOpcion("Ingrese el año del auto: ")
        tipo = self.validarDato("Ingrese el nombre del tipo de automovil: ", 15)
        modelo = self.validarDato("Ingrese el nombre del modelo del auto: ", 15)
        patente = self.validarDato("Ingrese la patente del auto: ", 6)
        kilometraje = self.validarOpcion("Ingrese el kilometraje del auto: ")
        res = self.crud.ingresarAuto(numeroMotor, tipo, modelo, año,patente, kilometraje)
        print(res)

    def actualizarAuto(self):
        numeroMotor = self.validarOpcion("Ingrese el numero de motor del automovil a actualizar: ")
        año = self.validarOpcion("Ingrese el nuevo año del auto: ")
        tipo = self.validarDato("Ingrese el nombre del nuevo tipo del automovil: ", 15)
        nombreModelo = self.validarDato("Ingrese el nuevo nombre del modelo del auto: ", 15)
        kilometraje = self.validarOpcion("Ingrese el nuevo kilometraje del auto: ")
        res = self.crud.modificarAuto(numeroMotor, tipo, año, nombreModelo, kilometraje)
        print(res)

    def buscarAuto(self):
        numeroMotor = self.validarOpcion("Ingrese el numero de motor del automovil: ")
        auto = self.crud.buscarAuto(numeroMotor)
        print(f"""
            Numero motor: {auto[0]},
            Tipo: {auto[1]},
            Modelo: {auto[2]},
            Marca: {auto[3]},
            Patente: {auto[4]},
            Kilometraje: {auto[5]},
            Año: {auto[6]}
        """)

    def eliminarAuto(self):
        numeroMotor = self.validarOpcion("Ingrese el numero de motor del automovil: ")
        print(f"esta seguro de eliminar el auto con numero: {numeroMotor}")
        if self.validarAccion("ingrese si para aceptar. cualquier otro caracter para cancelar: "):
            res = self.crud.eliminarAuto(numeroMotor)
            print(res)
        else:
            print("se ha cancelado la eliminacion del auto")

    def mostrarPorMarca(self):
        marca = self.validarDato("Ingrese el nombre de la marca a filtrar: ", 15)
        autos = self.crud.mostrarAutosMarca(marca)
        if len(autos) == 0:
            print("no hay auntos ingresados con esta marca")
            return

        for auto in autos:
            print(f"""
            Numero motor: {auto[0]},
            Tipo: {auto[1]},
            Modelo: {auto[2]},
            Marca: {auto[3]},
            Patente: {auto[4]},
            Kilometraje: {auto[5]},
            Año: {auto[6]}
            """)

    def mostrarAutosPorAño(self):
        año = self.validarOpcion("Ingrese el año del automovil a filtrar: ")
        autos = self.crud.mostrarAutosAnyo(año)
        for auto in autos:
            print(f"""
            Numero motor: {auto[0]},
            Tipo: {auto[1]},
            Modelo: {auto[2]},
            Marca: {auto[3]},
            Patente: {auto[4]},
            Kilometraje: {auto[5]},
            Año: {auto[6]}
            """)
    
    def ingresarMarca(self):
        nombreMarca = self.validarDato("Ingrese el nombre de la marca a ingresar: ", 15)
        res = self.crud.ingresarMarca(nombreMarca)
        print(res)
    
    def ingresarModelo(self):
        nombreMarca = self.validarDato("Ingrese el nombre de la marca a la que pertenece el modelo: ", 15)
        nombreModelo = self.validarDato("Ingrese el nombre del modelo: ", 15)
        res = self.crud.ingresarModelo(nombreMarca, nombreModelo)
        print(res)

    def ingresarTipo(self):
        nombreModelo = self.validarDato("Ingrese el nombre del tipo de automovil: ", 15)
        res = self.crud.ingresarTipo(nombreModelo)
        print(res)


    def menuPrincipal(self):
        print("recuerde que si la base de datos esta vacia debe crear primero una marca y modelo antes de crear un automovil\n")
        while True:
            print("""
            =========================================
                        CRUD AUTOMOTORA
            =========================================

            1) Ingresar Marca

            2) Ingresar Modelo

            3) Ingresar Tipo

            4) Ingresar Automovil

            5) Modificar automovil

            6) Eliminar automovil

            7) Mostrar Autos por Marca

            8) Mostrar Autos por año

            9) Salir
            """)

            opcion = self.validarOpcion("Ingrese una opcion: ", range(1, 10))
            if opcion == 1:
                self.ingresarMarca()
            
            elif opcion == 2:
                self.ingresarModelo()

            elif opcion == 3: 
                self.ingresarTipo()

            elif opcion == 4:
                self.ingresarAuto()

            elif opcion == 5:
                self.actualizarAuto()
            
            elif opcion == 6:
                self.eliminarAuto()

            elif opcion == 7:
                self.mostrarPorMarca()

            elif opcion == 8:
                self.mostrarAutosPorAño()

            else:
                self.crud.tearDown()
                break

            sleep(4)
            system("cls")


if __name__ == "__main__":
    menu = Menu()
    menu.menuPrincipal()