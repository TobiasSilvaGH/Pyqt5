import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QLineEdit,QLabel,QFrame,QGroupBox,QFormLayout,QComboBox,QSpinBox,QMessageBox,QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QIcon,QPalette,QColor,QPixmap,QFont
from PyQt5.QtCore import pyqtSlot, Qt,QRect
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QFrame, QGroupBox, QLabel, QLineEdit,
        QTabWidget, QVBoxLayout, QWidget)
from abm1 import *

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 pestañas'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.table_widget = TabDialog(self)
        self.setCentralWidget(self.table_widget)
 
        self.show()
class TabDialog(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        #self.setFixedSize(800, 600)

        tabWidget = QTabWidget()
        tabWidget.addTab(Registro1(), "Registro")
        tabWidget.addTab(Alta1(), "Alta")
        tabWidget.addTab(Busqueda1(), "Busqueda")


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)

        self.setWindowTitle("Electrobobinados")

        self.stylesheet= """

        QPushButton{
            background-color: #334CFF;
            color: #ffffff;
        }

        QLabel{
            font-family: "New Century Schoolbook", TeX Gyre Schola, serif;\
            font-size: 17px;
        }

        QGroupBox{
            font-family: "Times New Roman", Times, serif;\
            font-size: 30px;
        }

        QLabel#nombrecliente{
            font-family: "Times New Roman", Times, serif;\
            font-size: 30px;
        }

        """
        app.setStyleSheet(self.stylesheet)


class Registro1(QWidget):        
 
    def __init__(self, parent=None):   
        super(Registro1, self).__init__(parent)

        self.imagen = QLabel(self)
        self.imagen.setPixmap(QPixmap('electroimg.jpeg'))
        self.formGroupBox = QGroupBox("Registro")
        arb = QFormLayout()
        self.nombre = QLineEdit(self)
        nombre=self.nombre.text()
        self.nt = QLineEdit(self)
        self.nt.setValidator(QtGui.QIntValidator())
        nt=self.nt.text()
        self.enviarcliente= QPushButton(self)
        self.enviarcliente.setText("Registrar cliente")
        self.enviarcliente.clicked.connect(self.enviarformulariocliente)
        self.mdm= QLineEdit(self)
        self.enviarmotor=QPushButton(self)
        self.enviarmotor.setText("Registrar motor")
        self.enviarmotor.clicked.connect(self.enviarformulariomotor)

        arb.addRow(self.imagen)
        arb.addRow(QLabel("Nombre:"), self.nombre)
        arb.addRow(QLabel("Numero de telefono:"), self.nt)
        arb.addRow(QLabel("Registrar cliente:"), self.enviarcliente)
        arb.addRow(QLabel("Marca de motor:"), self.mdm)
        arb.addRow(QLabel("Registrar motor:"), self.enviarmotor)
        self.formGroupBox.setLayout(arb)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        self.setLayout(mainLayout)


    def enviarformulariocliente(self):
        nombre=self.nombre.text()
        nt=self.nt.text()
        estado=0
        insertar=Registro.RegistrarCliente(nombre,nt,estado)
        enviado=QMessageBox()
        enviado.setWindowTitle("Cliente Registrado")
        enviado.setText('El cliente ' +nombre+ ' ha sido registrado')
        enviado.setIcon(QMessageBox.Information)
        x=enviado.exec_()
        conexion.close()


    def enviarformulariomotor(self):
        dbConnect={
            'host':'localhost',
            'user':'root',
            'password':'',
            'database':'electrosilva',
        }
        conexion=mysql.connector.connect(**dbConnect)
        cursor=conexion.cursor()
        estado=0
        mdm=self.mdm.text()
        self.mdm.clear()
        fecha=(time.strftime("%y/%m/%d"))
        verids="select idcliente  from clientes"
        cursor.execute(verids)
        verid=cursor.fetchone()
        while verid != None:
            id=int(verid[0])
            verid=cursor.fetchone()
        insertar="insert into motores(idcliente,nombrem,fecha,estado)values(%s,%s,%s,%s)"
        cursor.execute(insertar,(id,mdm,fecha,estado))
        conexion.commit()
        conexion.close()

class Alta1(QWidget):
    def __init__(self, parent=None):   
        super(Alta1, self).__init__(parent)

        self.imagen = QLabel(self)
        self.imagen.setPixmap(QPixmap('electroimg.jpeg'))
        self.imagen.setGeometry(20,20,50,50)
        self.formGroupBox = QGroupBox("Alta Motor")
        busqueda = QFormLayout()
        self.buscarcliente = QtWidgets.QComboBox(self)
        self.updatecliente=QPushButton(self)
        self.updatecliente.setText("ACTUALIZAR CLIENTE")
        self.updatecliente.clicked.connect(self.buscarclientecombobox)
        self.confirmar=QPushButton(self)
        self.confirmar.setText("CONFIRMAR")
        self.confirmar.clicked.connect(self.busquedapormarcacombobox)
        self.motor = QtWidgets.QComboBox(self)
        self.hp=QLineEdit(self)
        self.hp.setValidator(QtGui.QIntValidator())
        self.voltaje=QLineEdit(self)
        self.voltaje.setValidator(QtGui.QIntValidator())
        self.rpm=QLineEdit(self)
        self.rpm.setValidator(QtGui.QIntValidator())
        self.amp=QLineEdit(self)
        self.amp.setValidator(QtGui.QIntValidator())
        self.caracteristicas=QLineEdit(self)
        self.listo=QPushButton(self)
        self.listo.setText("DAR DE ALTA")
        self.listo.clicked.connect(self.daralta)
        a=self.buscarclientecombobox()
        busqueda.addRow(QLabel("ACTUALIZAR CLIENTE:"), self.updatecliente)
        busqueda.addRow(QLabel("QUE CLIENTE DESEA DAR DE ALTA:"), self.buscarcliente)
        busqueda.addRow(QLabel("CONFIRMAR :"), self.confirmar)
        busqueda.addRow(QLabel("QUE MOTOR DE CLIENTE DESEA DAR DE ALTA:"), self.motor)
        busqueda.addRow(QLabel("HP:"), self.hp)
        busqueda.addRow(QLabel("VOLTAJE:"), self.voltaje)
        busqueda.addRow(QLabel("RPM:"), self.rpm)
        busqueda.addRow(QLabel("AMP:"), self.amp)
        busqueda.addRow(QLabel("CARACTERISTICAS:"), self.caracteristicas)
        busqueda.addRow(QLabel("Dar de alta :"), self.listo)
        self.formGroupBox.setLayout(busqueda)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.imagen)
        mainLayout.addWidget(self.formGroupBox)
        self.setLayout(mainLayout)


    def buscarclientecombobox(self):
        dbConnect={
            'host':'localhost',
            'user':'root',
            'password':'',
            'database':'electrosilva',
        }
        conexion=mysql.connector.connect(**dbConnect)
        cursor=conexion.cursor()
        sql="select * from clientes"
        cursor.execute(sql)
        clientes=cursor.fetchone()
        lista=[]
        while clientes != None:
            idcliente=int(clientes[0])
            nombrec=clientes[1]
            lista.append(nombrec)
            clientes=cursor.fetchone()
        for a in (lista):
            self.buscarcliente.addItem(a)
        conexion.close()


    def busquedapormarcacombobox(self):
        dbConnect={
            'host':'localhost',
            'user':'root',
            'password':'',
            'database':'electrosilva',
        }
        conexion=mysql.connector.connect(**dbConnect)
        cursor=conexion.cursor()
        if self.motor !="":
            self.motor.clear()
            self.hp.clear()
            self.voltaje.clear()
            self.rpm.clear()
            self.amp.clear()
            self.caracteristicas.clear()
        nombrecli=self.buscarcliente.currentText()
        self.nombrealta=nombrecli
        sql="select * from clientes,motores"
        cursor.execute(sql)
        clientes=cursor.fetchone()
        lista=[]
        while clientes!= None:
            idcliente=int(clientes[0])
            nombrec=clientes[1]
            estadoc=int(clientes[3])
            idmotor=int(clientes[4])
            clienteid=int(clientes[5])
            nombrec=clientes[1]
            nombrem=clientes[6]
            estado=int(clientes[8])
            if nombrecli == nombrec:
                if idcliente==clienteid and estado ==0:
                    lista.append(nombrem)
            clientes=cursor.fetchone()
        for a in (lista):
            self.motor.addItem(a)
            
    def daralta(self):
        nombrec=self.nombrealta
        motorc=self.motor.currentText()
        hp=self.hp.text()
        voltaje=self.voltaje.text()
        rpm=self.rpm.text()
        amp=self.amp.text()
        caracteristicas=self.caracteristicas.text()
        if motorc and hp and voltaje and rpm and amp != "":
            insertar=Alta.AltaMotor(nombrec,motorc,hp,voltaje,rpm,amp,caracteristicas)
            self.motor.removeItem(self.motor.currentIndex())
            self.hp.clear()
            self.voltaje.clear()
            self.rpm.clear()
            self.amp.clear()
            self.caracteristicas.clear()
            enviado=QMessageBox()
            enviado.setWindowTitle("Motor en alta")
            enviado.setText('El motor ' +motorc+ ' ha sido dado de alta')
            enviado.setIcon(QMessageBox.Information)
            x=enviado.exec_()
        else:
            QMessageBox.warning(self, "No se puede dar de alta", "Completa los campos obligatorios", QMessageBox.Discard)

#heredar metodos de tablas
class Busqueda1(QWidget,Tablas):
    def __init__(self, parent=None):
        super(Busqueda1, self).__init__(parent)
        super.Clientetabla()
        super.MotorTabla()
        super.HpTabla()
        super.VolTabla()
        super.RpmTabla()
        super.AmpTabla()

        self.nombrecliente=QLabel()
        self.nombrecliente.setText("Busqueda por cliente")
        self.nombrecliente.setObjectName("nombrecliente")

        self.cliente=QtWidgets.QComboBox(self)
        self.buscarclientecombobox()
        self.addcliente=QPushButton(self)
        self.addcliente.setText("Buscar por cliente")
        self.addcliente.clicked.connect(self.Clientetabla)

        self.nombremotor=QLabel()
        self.nombremotor.setText("Busqueda por motor")

        self.motor=QtWidgets.QComboBox(self)
        self.busquedapormarcacombobox()
        self.addmotor=QPushButton(self)
        self.addmotor.setText("Busqueda por motor")
        self.addmotor.clicked.connect(self.MotorTabla)

        self.xhp=QLabel()
        self.xhp.setText("Busqueda por hp")

        self.hp=QtWidgets.QComboBox(self)
        self.busquedaporHp()
        self.addhp=QPushButton(self)
        self.addhp.setText("Busqueda por hp")
        self.addhp.clicked.connect(self.HpTabla)

        self.xv=QLabel()
        self.xv.setText("Busqueda por voltaje")

        self.voltaje=QtWidgets.QComboBox(self)
        self.busquedaporVoltaje()
        self.addv=QPushButton(self)
        self.addv.setText("Busqueda por voltaje")
        self.addv.clicked.connect(self.VolTabla)

        self.xrpm=QLabel()
        self.xrpm.setText("Busqueda por RPM")

        self.rpm=QtWidgets.QComboBox(self)
        self.busquedaporRpm()
        self.addrpm=QPushButton(self)
        self.addrpm.setText("Busqueda por RPM")
        self.addrpm.clicked.connect(self.RpmTabla)

        self.xamp=QLabel()
        self.xamp.setText("Busqueda por AMP")

        self.amp=QtWidgets.QComboBox(self)
        self.busquedaporAmp()
        self.addamp=QPushButton(self)
        self.addamp.setText("Busqueda por AMP")
        self.addamp.clicked.connect(self.AmpTabla)


        self.tab3 = QVBoxLayout(self)
        self.tab3.addWidget(self.nombrecliente)
        self.tab3.addWidget(self.cliente)
        self.tab3.addWidget(self.addcliente)
        self.tab3.addWidget(self.nombremotor)
        self.tab3.addWidget(self.motor)
        self.tab3.addWidget(self.addmotor)
        self.tab3.addWidget(self.xhp)
        self.tab3.addWidget(self.hp)
        self.tab3.addWidget(self.addhp)
        self.tab3.addWidget(self.xv)
        self.tab3.addWidget(self.voltaje)
        self.tab3.addWidget(self.addv)
        self.tab3.addWidget(self.xrpm)
        self.tab3.addWidget(self.rpm)
        self.tab3.addWidget(self.addrpm)
        self.tab3.addWidget(self.xamp)
        self.tab3.addWidget(self.amp)
        self.tab3.addWidget(self.addamp) 
        self.setLayout(self.tab3)


    def buscarclientecombobox(self):
        sql="select * from clientes"
        cursor.execute(sql)
        clientes=cursor.fetchone()
        lista=[]
        while clientes != None:
            nombrec=clientes[1]
            estadoc=int(clientes[3])
            if estadoc == 1:
                lista.append(nombrec)
            clientes=cursor.fetchone()
        for a in (lista):
            self.cliente.addItem(a)


    def busquedapormarcacombobox(self):
        sql="select * from motores"
        cursor.execute(sql)
        clientes=cursor.fetchone()
        lista=[]
        while clientes!= None:
            nombrem=clientes[2]
            estadom=int(clientes[4])
            if estadom == 1:
                lista.append(nombrem)
            clientes=cursor.fetchone()
        for a in (lista):
            self.motor.addItem(a)

#desde este punto los datos buscamos desde datos motores

    def busquedaporHp(self):
        sql="select * from datosmotores"
        cursor.execute(sql)
        clientes=cursor.fetchone()
        lista=[]
        while clientes!= None:
            hpe=int(clientes[1])
            lista.append(hpe)
            clientes=cursor.fetchone()
        listaor=sorted(set(lista))
        for a in (listaor):
            self.hp.addItem(str(a))

    def busquedaporVoltaje(self):
        sql="select * from datosmotores"
        cursor.execute(sql)
        clientes=cursor.fetchone()
        lista=[]
        while clientes!= None:
            volt=int(clientes[2])
            lista.append(volt)
            clientes=cursor.fetchone()
        listaor=sorted(set(lista))
        for a in (listaor):
            self.voltaje.addItem(str(a))

    def busquedaporRpm(self):
        sql="select * from datosmotores"
        cursor.execute(sql)
        clientes=cursor.fetchone()
        lista=[]
        while clientes!= None:
            rpem=int(clientes[3])
            lista.append(rpem)
            clientes=cursor.fetchone()
        listaor=sorted(set(lista))
        for a in (listaor):
            self.rpm.addItem(str(a))

    def busquedaporAmp(self):
        sql="select * from datosmotores"
        cursor.execute(sql)
        clientes=cursor.fetchone()
        lista=[]
        while clientes!= None:
            amper=int(clientes[4])
            lista.append(amper)
            clientes=cursor.fetchone()
        listaor=sorted(set(lista))
        for a in (listaor):
            self.amp.addItem(str(a))

#-----------------------------------------------------------------------------------------------------
#------------------------------------------Nueva Clase tabla------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

class Tablas(Busqueda1):
    def __init__(self, parent=None):
        super(Tablas, self).__init__(parent)
        Busqueda1.__init__(cliente,motor,voltaje,hp,rpm,amp)

        #En esta parte sacamos los atributos de Busqueda que queremos
        self.tablewidget=QTableWidget(self)
        self.tablewidget.setRowCount(6)
        #las filas voy a ir agregando a medida que busco en la base de datos
        self.tablewidget.setColumnCount(6)
        self.tablewidget.setHorizontalHeaderLabels(["Nombre","Marca","Hp","Voltaje","Rpm","Amp"])
        self.tablewidget.horizontalHeaderItem( 0 ) . setTextAlignment ( Qt . AlignHCenter )
        self.tablewidget.horizontalHeaderItem( 1 ) . setTextAlignment ( Qt . AlignHCenter )
        self.tablewidget.horizontalHeaderItem( 2 ) . setTextAlignment ( Qt . AlignHCenter )
        self.tablewidget.horizontalHeaderItem( 3 ) . setTextAlignment ( Qt . AlignHCenter )
        self.tablewidget.horizontalHeaderItem( 4 ) . setTextAlignment ( Qt . AlignHCenter )
        self.tablewidget.horizontalHeaderItem( 5 ) . setTextAlignment ( Qt . AlignHCenter )

        self.tab4 = QVBoxLayout(self)
        self.tab4.addWidget(self.tablewidget)
        self.setLayout(self.tab4)

    def Clientetabla(self):
        if self.tablewidget !="":
            self.tablewidget.clear()
        sql="select * from clientes,motores,datosmotores"
        cursor.execute(sql)
        self.tablewidget.setRowCount(0)
        nc=self.cliente.currentText()
        clientes=cursor.fetchone()
        lista=[]
        while clientes != None:
            idcliente=int(clientes[0])
            idmotor=int(clientes[4])
            clienteid=int(clientes[5])
            nombrec=clientes[1]
            nombrem=clientes[6]
            fecha=clientes[7]
            estado=int(clientes[8])
            motor=int(clientes[9])
            hp=int(clientes[10])
            v=int(clientes[11])
            rpm=int(clientes[12])
            amp=int(clientes[13])
            datos=clientes[14]
            if  nc == nombrec:
                if idcliente == clienteid and idmotor==motor:
                    registro=nombrec,nombrem,str(hp),str(v),str(rpm),str(amp)
                    lista.append(registro)
            clientes=cursor.fetchone()
        c=0
        for a in (lista):
            self.tablewidget.setRowCount(c+1)
            self.tablewidget.setHorizontalHeaderLabels(["Nombre","Marca","Hp","Voltaje","Rpm","Amp"])
            self.tablewidget.setItem(c,0, QTableWidgetItem(a[0]))
            self.tablewidget.setItem(c,1, QTableWidgetItem(a[1]))
            self.tablewidget.setItem(c,2, QTableWidgetItem(str(a[2])))
            self.tablewidget.setItem(c,3, QTableWidgetItem(str(a[3])))
            self.tablewidget.setItem(c,4, QTableWidgetItem(str(a[4])))
            self.tablewidget.setItem(c,5, QTableWidgetItem(str(a[5])))
            c+=1

    def MotorTabla(self):
        if self.tablewidget !="":
            self.tablewidget.clear()
        sql="select * from clientes,motores,datosmotores"
        cursor.execute(sql)
        self.tablewidget.setRowCount(0)
        nm=self.motor.currentText()
        clientes=cursor.fetchone()
        lista=[]
        while clientes != None:
            idcliente=int(clientes[0])
            idmotor=int(clientes[4])
            clienteid=int(clientes[5])
            nombrec=clientes[1]
            nombrem=clientes[6]
            fecha=clientes[7]
            estado=int(clientes[8])
            motor=int(clientes[9])
            hp=int(clientes[10])
            v=int(clientes[11])
            rpm=int(clientes[12])
            amp=int(clientes[13])
            datos=clientes[14]
            if  nm == nombrem:
                if idcliente == clienteid and idmotor==motor:
                    registro=nombrec,nombrem,str(hp),str(v),str(rpm),str(amp)
                    lista.append(registro)
            clientes=cursor.fetchone()
        c=0
        for a in (lista):
            self.tablewidget.setRowCount(c+1)
            self.tablewidget.setHorizontalHeaderLabels(["Nombre","Marca","Hp","Voltaje","Rpm","Amp"])
            self.tablewidget.setItem(c,0, QTableWidgetItem(a[0]))
            self.tablewidget.setItem(c,1, QTableWidgetItem(a[1]))
            self.tablewidget.setItem(c,2, QTableWidgetItem(str(a[2])))
            self.tablewidget.setItem(c,3, QTableWidgetItem(str(a[3])))
            self.tablewidget.setItem(c,4, QTableWidgetItem(str(a[4])))
            self.tablewidget.setItem(c,5, QTableWidgetItem(str(a[5])))
            c+=1

    def HpTabla(self):
        if self.tablewidget !="":
            self.tablewidget.clear()
        sql="select * from clientes,motores,datosmotores"
        cursor.execute(sql)
        self.tablewidget.setRowCount(0)
        nhp=int(self.hp.currentText())
        clientes=cursor.fetchone()
        lista=[]
        while clientes != None:
            idcliente=int(clientes[0])
            idmotor=int(clientes[4])
            clienteid=int(clientes[5])
            nombrec=clientes[1]
            nombrem=clientes[6]
            fecha=clientes[7]
            estado=int(clientes[8])
            motor=int(clientes[9])
            hp=int(clientes[10])
            v=int(clientes[11])
            rpm=int(clientes[12])
            amp=int(clientes[13])
            datos=clientes[14]
            if  nhp == hp:
                if idcliente == clienteid and idmotor==motor:
                    registro=nombrec,nombrem,str(hp),str(v),str(rpm),str(amp)
                    lista.append(registro)
            clientes=cursor.fetchone()
        c=0
        for a in (lista):
            self.tablewidget.setRowCount(c+1)
            self.tablewidget.setHorizontalHeaderLabels(["Nombre","Marca","Hp","Voltaje","Rpm","Amp"])
            self.tablewidget.setItem(c,0, QTableWidgetItem(a[0]))
            self.tablewidget.setItem(c,1, QTableWidgetItem(a[1]))
            self.tablewidget.setItem(c,2, QTableWidgetItem(str(a[2])))
            self.tablewidget.setItem(c,3, QTableWidgetItem(str(a[3])))
            self.tablewidget.setItem(c,4, QTableWidgetItem(str(a[4])))
            self.tablewidget.setItem(c,5, QTableWidgetItem(str(a[5])))
            c+=1

    def VolTabla(self):
        if self.tablewidget !="":
            self.tablewidget.clear()
        sql="select * from clientes,motores,datosmotores"
        cursor.execute(sql)
        self.tablewidget.setRowCount(0)
        vol=int(self.voltaje.currentText())
        clientes=cursor.fetchone()
        lista=[]
        while clientes != None:
            idcliente=int(clientes[0])
            idmotor=int(clientes[4])
            clienteid=int(clientes[5])
            nombrec=clientes[1]
            nombrem=clientes[6]
            fecha=clientes[7]
            estado=int(clientes[8])
            motor=int(clientes[9])
            hp=int(clientes[10])
            v=int(clientes[11])
            rpm=int(clientes[12])
            amp=int(clientes[13])
            datos=clientes[14]
            if  vol == v:
                if idcliente == clienteid and idmotor==motor:
                    registro=nombrec,nombrem,str(hp),str(v),str(rpm),str(amp)
                    lista.append(registro)
            clientes=cursor.fetchone()
        c=0
        for a in (lista):
            self.tablewidget.setRowCount(c+1)
            self.tablewidget.setHorizontalHeaderLabels(["Nombre","Marca","Hp","Voltaje","Rpm","Amp"])
            self.tablewidget.setItem(c,0, QTableWidgetItem(a[0]))
            self.tablewidget.setItem(c,1, QTableWidgetItem(a[1]))
            self.tablewidget.setItem(c,2, QTableWidgetItem(str(a[2])))
            self.tablewidget.setItem(c,3, QTableWidgetItem(str(a[3])))
            self.tablewidget.setItem(c,4, QTableWidgetItem(str(a[4])))
            self.tablewidget.setItem(c,5, QTableWidgetItem(str(a[5])))
            c+=1

    def RpmTabla(self):
        if self.tablewidget !="":
            self.tablewidget.clear()
        sql="select * from clientes,motores,datosmotores"
        cursor.execute(sql)
        self.tablewidget.setRowCount(0)
        xrpm=int(self.rpm.currentText())
        clientes=cursor.fetchone()
        lista=[]
        while clientes != None:
            idcliente=int(clientes[0])
            idmotor=int(clientes[4])
            clienteid=int(clientes[5])
            nombrec=clientes[1]
            nombrem=clientes[6]
            fecha=clientes[7]
            estado=int(clientes[8])
            motor=int(clientes[9])
            hp=int(clientes[10])
            v=int(clientes[11])
            rpm=int(clientes[12])
            amp=int(clientes[13])
            datos=clientes[14]
            if  xrpm == rpm:
                if idcliente == clienteid and idmotor==motor:
                    registro=nombrec,nombrem,str(hp),str(v),str(rpm),str(amp)
                    lista.append(registro)
            clientes=cursor.fetchone()
        c=0
        for a in (lista):
            self.tablewidget.setRowCount(c+1)
            self.tablewidget.setHorizontalHeaderLabels(["Nombre","Marca","Hp","Voltaje","Rpm","Amp"])
            self.tablewidget.setItem(c,0, QTableWidgetItem(a[0]))
            self.tablewidget.setItem(c,1, QTableWidgetItem(a[1]))
            self.tablewidget.setItem(c,2, QTableWidgetItem(str(a[2])))
            self.tablewidget.setItem(c,3, QTableWidgetItem(str(a[3])))
            self.tablewidget.setItem(c,4, QTableWidgetItem(str(a[4])))
            self.tablewidget.setItem(c,5, QTableWidgetItem(str(a[5])))
            c+=1

    def AmpTabla(self):
        if self.tablewidget !="":
            self.tablewidget.clear()
        sql="select * from clientes,motores,datosmotores"
        cursor.execute(sql)
        self.tablewidget.setRowCount(0)
        ampe=int(self.amp.currentText())
        clientes=cursor.fetchone()
        lista=[]
        while clientes != None:
            idcliente=int(clientes[0])
            idmotor=int(clientes[4])
            clienteid=int(clientes[5])
            nombrec=clientes[1]
            nombrem=clientes[6]
            fecha=clientes[7]
            estado=int(clientes[8])
            motor=int(clientes[9])
            hp=int(clientes[10])
            v=int(clientes[11])
            rpm=int(clientes[12])
            amp=int(clientes[13])
            datos=clientes[14]
            if  ampe == amp:
                if idcliente == clienteid and idmotor==motor:
                    registro=nombrec,nombrem,str(hp),str(v),str(rpm),str(amp)
                    lista.append(registro)
            clientes=cursor.fetchone()
        c=0
        for a in (lista):
            self.tablewidget.setRowCount(c+1)
            self.tablewidget.setHorizontalHeaderLabels(["Nombre","Marca","Hp","Voltaje","Rpm","Amp"])
            self.tablewidget.setItem(c,0, QTableWidgetItem(a[0]))
            self.tablewidget.setItem(c,1, QTableWidgetItem(a[1]))
            self.tablewidget.setItem(c,2, QTableWidgetItem(str(a[2])))
            self.tablewidget.setItem(c,3, QTableWidgetItem(str(a[3])))
            self.tablewidget.setItem(c,4, QTableWidgetItem(str(a[4])))
            self.tablewidget.setItem(c,5, QTableWidgetItem(str(a[5])))
            c+=1

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())