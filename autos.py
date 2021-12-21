import mysql.connector

class Autos:
    def __init__(self,numeroMotor, modelo, patente, kilometraje, marca):
        self.__modelo = modelo
        self.__patente = patente
        self.__kilometraje = kilometraje
        self.__numeroMotor = numeroMotor
        self.__marca = marca

        self.__conn = mysql.connector.connect(
            user='root', 
            password='',
            host='127.0.0.1',
            database='INACAP'
        )

        self.__cursor = self.__conn.cursor()
        tablas = []

        tablas.append("""
        create table if not exists TIPO (
        IDTIPO               int not null auto_increment,
        NOMBRETIPO           varchar(15),
        primary key (IDTIPO)
        );
        """)

        tablas.append("""
        create table if not exists MARCA (
        IDMARCA              int not null auto_increment,
        NOMBREMARCA          varchar(15),
        primary key (IDMARCA)
        );
        """)

        tablas.append("""
        create table if not exists MODELO (
        IDMODELO             int not null auto_increment,
        IDMARCA              int not null,
        NOMBREMODELO         varchar(15),
        primary key (IDMODELO),
        CONSTRAINT FK_MODELO_MARCA foreign key (IDMARCA) references MARCA (IDMARCA)
        );
        """)

        tablas.append("""
        create table if not exists AUTOMOVIL (
        IDAUTOMOVIL          int not null auto_increment,
        IDTIPO               int not null,
        NUMEROMOTOR          int not null,
        IDMODELO             int not null,
        PATENTE              varchar(6),
        KILOMETRAJE          int,
        ANYO                 int,
        UNIQUE(NUMEROMOTOR),
        primary key (IDAUTOMOVIL),
        CONSTRAINT FK_AUTO_MODELO foreign key (IDMODELO) references MODELO (IDMODELO),
        CONSTRAINT FK_AUTO_TIPO foreign key (IDTIPO) references TIPO(IDTIPO)
        ); 
        """)

        for sql in tablas:
            self.__cursor.execute(sql)

        self.__conn.commit()
        
    def getModelo(self):
        return self.__modelo

    def setModelo(self, nuevoModelo):
        self.__modelo = nuevoModelo

    def getPatente(self):
        return self.__patente

    def setPatente(self, patente):
        self.__patente = patente

    def getKilometraje(self):
        return self.__kilometraje

    def setKilometraje(self, kilometraje):
        self.__kilometraje = kilometraje

    def getNumeroMotor(self):
        return self.__numeroMotor

    def setNumeroMotor(self, numeroMotor):
        self.__numeroMotor = numeroMotor

    def getMarca(self):
        return self.__marca

    def setMarca(self, marca):
        self.__marca = marca

    def tearDown(self):
        self.__cursor.close()
        self.__conn.commit()
        self.__conn.close()

    def QueryDB(self, query, args):
        return self.__cursor.execute(query, args)

    def buscarAuto(self, numeroMotor):
        self.QueryDB("""
        SELECT 
            A.NUMEROMOTOR,
            T.NOMBRETIPO,
            M.NOMBREMODELO,
            MA.NOMBREMARCA,
            A.PATENTE,
            A.KILOMETRAJE,
            A.ANYO
        FROM AUTOMOVIL A 
        INNER JOIN MODELO M ON M.IDMODELO = A.IDMODELO
        INNER JOIN MARCA MA ON MA.IDMARCA = M.IDMARCA
        INNER JOIN TIPO T on T.IDTIPO = A.IDTIPO
        WHERE A.NUMEROMOTOR = %s
        """, (numeroMotor,))
        return self.__cursor.fetchone()

    def buscarModelo(self, nombreModelo):
        self.QueryDB("SELECT * FROM MODELO WHERE NOMBREMODELO = %s", (nombreModelo,))
        return self.__cursor.fetchone()

    def buscarTipo(self, nombreTipo):
        self.QueryDB("SELECT * FROM TIPO WHERE NOMBRETIPO = %s", (nombreTipo,))
        return self.__cursor.fetchone()

    def buscarMarca(self, nombreMarca):
        self.QueryDB("SELECT * FROM MARCA WHERE NOMBREMARCA = %s", (nombreMarca,))
        return self.__cursor.fetchone()

    def ingresarMarca(self, nombreMarca):
        marca = self.buscarMarca(nombreMarca)
        if marca != None:
            return f"Ya existe una marca con el nombre: {nombreMarca}"
        
        self.QueryDB("INSERT INTO MARCA (NOMBREMARCA) VALUES(%s)", (nombreMarca,))
        self.__conn.commit()
        return "se ha creado exitosamente la marca"

    def ingresarTipo(self, nombreTipo):
        tipo = self.buscarTipo(nombreTipo)
        if tipo != None:
            return f"Ya existe un tipo de automovil con el nombre {nombreTipo}"

        self.QueryDB("INSERT INTO TIPO (NOMBRETIPO) VALUES(%s)", (nombreTipo,))
        self.__conn.commit()
        return "se ha credo exitosamente el tipo"

    def ingresarModelo(self, nombreMarca, nombreModelo):
        marca = self.buscarMarca(nombreMarca)
        if marca == None:
            return f"no existe una marca con el nombre {nombreMarca}"

        modelo = self.buscarModelo(nombreModelo)
        if modelo != None:
            return f"Ya existe una marca con el nombre: {nombreModelo}"

        self.QueryDB("INSERT INTO MODELO (IDMARCA, NOMBREMODELO) VALUES(%s, %s)", (marca[0], nombreModelo))
        self.__conn.commit()
        return "se ha creado exitosamente el modelo"


    def ingresarAuto(self, numeroMotor, nombreTipo,nombreModelo, año, patente, kilometraje):
        modelo = self.buscarModelo(nombreModelo)
        if modelo == None:
            return f"no existe un modelo con el nombre {nombreModelo}"

        tipo = self.buscarTipo(nombreTipo)
        if tipo == None:
            return f"No existe un tipo de automovil con el nombre: {nombreTipo}"

        auto = self.buscarAuto(numeroMotor)
        if auto == None:
            dataAuto = (numeroMotor, tipo[0], modelo[0], patente, kilometraje, año)
            self.QueryDB("""
            INSERT INTO AUTOMOVIL (NUMEROMOTOR, IDTIPO, IDMODELO, PATENTE, KILOMETRAJE, ANYO)
            VALUES(%s, %s, %s, %s, %s, %s)
            """, dataAuto)
            self.__conn.commit()
            return "el auto se ha creado exitosamente"

        return f"ya existe un auto con numero de motor {numeroMotor}"     

    def modificarAuto(self, numeroMotor, nombreTipo, anyo ,nombreModelo, kilometraje):
        modelo = self.buscarModelo(nombreModelo)
        if modelo == None:
            return f"no existe un modelo con el nombre {nombreModelo}"

        tipo = self.buscarTipo(nombreTipo)
        if tipo == None:
            return f"No existe un tipo de automovil con el nombre: {nombreTipo}"

        auto = self.buscarAuto(numeroMotor)
        if auto == None:
            return f"no existe un auto con el numero de motor {numeroMotor}"

        self.QueryDB("""
        UPDATE AUTOMOVIL SET
        IDMODELO = %s, 
        IDTIPO = %s,
        KILOMETRAJE = %s,
        ANYO = %s
        WHERE NUMEROMOTOR = %s 
        """, (modelo[0], tipo[0], kilometraje, anyo,numeroMotor))
        self.__conn.commit()
        return f"se ha actualizado correctamente el automovil con numero de motor: {numeroMotor}"

    def eliminarAuto(self, numeroMotor):
        auto = self.buscarAuto(numeroMotor)
        if auto == None:
            return f"no existe ningun auto con el numero de motor: {numeroMotor}"

        self.QueryDB("DELETE FROM AUTOMOVIL WHERE NUMEROMOTOR = %s", (numeroMotor,))
        self.__conn.commit()
        return f"se ha eliminado exitosamente el automovil con numero de motor: {numeroMotor}"

    def mostrarAutosMarca(self, nombreMarca):
        self.QueryDB("""
        SELECT
            A.NUMEROMOTOR,
            T.NOMBRETIPO,
            M.NOMBREMODELO,
            MA.NOMBREMARCA,
            A.PATENTE,
            A.KILOMETRAJE,
            A.ANYO
        FROM AUTOMOVIL A
        INNER JOIN MODELO M ON M.IDMODELO = A.IDMODELO
        INNER JOIN MARCA MA ON MA.IDMARCA = M.IDMARCA
        INNER JOIN TIPO T ON T.IDTIPO = A.IDTIPO
        WHERE MA.NOMBREMARCA = %s
        """, (nombreMarca,))
        return self.__cursor.fetchall()

    def mostrarAutosAnyo(self, año):
        self.QueryDB("""
        SELECT
            A.NUMEROMOTOR,
            T.NOMBRETIPO,
            M.NOMBREMODELO,
            MA.NOMBREMARCA,
            A.PATENTE,
            A.KILOMETRAJE,
            A.ANYO
        FROM AUTOMOVIL A
        INNER JOIN MODELO M ON M.IDMODELO = A.IDMODELO
        INNER JOIN MARCA MA ON MA.IDMARCA = M.IDMARCA
        INNER JOIN TIPO T ON T.IDTIPO = A.IDTIPO
        WHERE A.ANYO = %s
        """, (año,))
        return self.__cursor.fetchall()