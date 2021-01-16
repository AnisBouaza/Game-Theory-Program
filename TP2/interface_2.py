import sys
import numpy as np
import pandas as pd
from itertools import product

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PyQt5.uic import loadUi

num_joueurs = 0
file_name = 'data_3.csv'
filedata = np.genfromtxt(file_name, delimiter = ',', dtype = 'int32')
all_strats = ()
nombre_strat = ()
matGains = []
final_nash = []

class Ui_MainWindow(object):
    
    def display_table(self):
        class PandasModel(QtCore.QAbstractTableModel):
            def __init__(self, data, parent=None):
                QtCore.QAbstractTableModel.__init__(self, parent)
                self._data = data

            def rowCount(self, parent=None):
                return len(self._data.values)

            def columnCount(self, parent=None):
                return self._data.columns.size

            def data(self, index, role=QtCore.Qt.DisplayRole):
                if index.isValid():
                    if role == QtCore.Qt.DisplayRole:
                        return str(self._data.values[index.row()][index.column()])
                return None

            def headerData(self, col, orientation, role):
                if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                    return self._data.columns[col]
                return None

        display = pd.read_csv(file_name)
        print(display)
        model = PandasModel(display)
        self.tableView.setModel(model)

    def create_csv(self):
        global num_joueurs
        global file_name

        num_strats = []
        num_strats.append(int(self.lineEdit_0.text()))
        num_strats.append(int(self.lineEdit_1.text()))
        print(num_strats)
        strats = []
        for i in num_strats:
            temp = np.arange(0, i, 1)
            strats.append(temp.tolist())
        print(strats)
        combinaisons = []
        temp_list = list(product(*strats))
        for x in temp_list:
            combinaisons.append(x)
        print(combinaisons)

        header_list = ['gain 0','gain 1']
        dataFrame = pd.DataFrame(combinaisons)
        print(dataFrame)
        dataFrame = dataFrame.reindex(columns=dataFrame.columns.tolist() + header_list)
        print(dataFrame)
        dataFrame.to_csv(file_name, index=None)
        
        self.display_table()

    def import_csv(self):
        self.display_table()
        global all_strats
        global num_joueurs
        global file_name
        global nombre_strat
        global matGains

        stratTemp = []
        data = pd.read_csv(file_name)
        names = list(data.columns)
        num_joueurs= int(len(names)/2)
        print("nombre de joueurs " + str(num_joueurs))
        self.textBrowser.append("Nombre de joueurs : " + str(num_joueurs))
        for i in range(num_joueurs):
            temp_list = []
            temp_col = data[str(i)].tolist()
            temp_len = len(set(temp_col))
            for j in range(temp_len):
                temp_list.append(j)
            stratTemp.append(temp_list)
        all_strats = tuple(stratTemp)
        print(all_strats)

        nombre_strat = nombre_strat + (len(all_strats[0]),len(all_strats[1]))
        print(nombre_strat)
        self.textBrowser.append("Nombre de strategies par joueurs : " + str(nombre_strat))
        self.textBrowser.append("Les strategies des joueurs : " + str(all_strats))
        def genMatGains(data, strategies):
            #Retourne la matrice qui contient les gains de tous les joueurs gains[0, 2, 1] représente le gain du joueur 0 pour le profil (2, 1)
            strategies = list(strategies)
            nbJoueurs = len(strategies)
            strategies.insert(0, len(strategies))
            gains = np.zeros(strategies, dtype='int32')

            for i in range(1, len(data)):
                for j in range(nbJoueurs):
                    indice = list(data[i][0:nbJoueurs])
                    indice.insert(0, j)
                    gains[tuple(indice)] = data[i][nbJoueurs + j]

            return gains
        print(genMatGains(filedata,nombre_strat))
        matGains = genMatGains(filedata,nombre_strat)
        self.textBrowser.append("La matrice de gains : ")
        self.textBrowser.append(str(matGains))

    
    def check_function(self):
        global matGains
        global final_nash

        if(self.checkBox_0.isChecked()):
            #chercher valeur somme nulle
            print("=======  Recherche de la valeur ========")
            self.textBrowser.append("=======  Recherche de la valeur ========")
            len_i = len(matGains[0][0]) #nb cols
            print(len_i)

            len_j = len(matGains[0])    #nb lignes
            print(len_j)

            #trouver les min de chaque lignes
            list_min = []
            for j in range(len_j):
                temp_list = []
                for i in range(len_i):
                    temp_list.append(matGains[0][j][i])
                print(temp_list)
                list_min.append(min(temp_list))
            print(list_min)
            self.textBrowser.append("Liste des minimums de chaque lignes : " + str(list_min))
            #trouver les max de chaque col
            list_max = []
            for i in range(len_i):
                temp_list = []
                for j in range(len_j):
                    temp_list.append(matGains[0][j][i])
                print(temp_list)
                list_max.append(max(temp_list))
            print(list_max)
            self.textBrowser.append("Liste des maximums de chaque lignes : " + str(list_max))
            if(max(list_min) == min(list_max)):
                print("la valeur du jeu en pure est  : " + str(max(list_min)))
                self.textBrowser.append("la valeur du jeu en pure est  : " + str(max(list_min)))
            else:
                print("ce jeu n'a pas de valeur en pur")
                self.textBrowser.append("ce jeu n'a pas de valeur en pure")
        else :

            #Si 2 stratégie par joueur:  (Les probabilités sont p et 1-p)
            self.textBrowser.append("=== Recherche de l'équilibre de nash en mixte ===" )
            def mixedNash2v2(gains):
                nash = []
                for i in range(2):
                    '''print("Joueur " + str(i))'''
                    nomi = gains[i, 1, 1] - gains[i, i, 1-i]
                    denomi = gains[i, 0, 0] + gains[i, 1, 1] - gains[i, 1, 0] - gains[i, 0, 1]
                    if denomi == 0:
                        return None
                    p = nomi/denomi
                    if p < 0 or p > 1:
                        return None

                    nash.append([p, (1-p)])
                    '''print(f"Stratégie: {p}, {1-p}")'''
                return nash

            if len(matGains[0]) == 2:
                final_nash = mixedNash2v2(matGains)
                if (mixedNash2v2(matGains) == None):
                    print("Ce jeu n'a pas d'équilibre de nash")
                    self.textBrowser.append("Ce jeu n'a pas d'équilibre de nash")
                else:
                    print('nash ' + str(final_nash))
                    self.textBrowser.append("L'équilibre de nash est : " +  str(final_nash) )
            
            #Si 3 stratégie par joueur : (p,q,1-p-q)
            if (len(matGains[0])==3 and len(matGains[1])==3):
                nash = []
                gains = matGains
                erreur = False

                # trouver les proba du joueur 1 (on varit le joueur 2)
                # 1 ere équation
                A1 = gains[1,0,0]-gains[1,2,0]- gains[1,0,1] +gains[1,2,1]  # xP
                B1 = gains[1,1,0]-gains[1,2,0]- gains[1,1,1] +gains[1,2,1]  # xQ
                C1 = gains[1,2,1] - gains[1,2,0]                            # cte1

                # 2 éme équation
                A2 = gains[1,0,1] - gains[1,2,1] - gains[1,0 ,2 ] + gains[1,2,2] #xP
                B2 = gains[1,1,1] - gains[1,2,1] - gains[1,1,2] + gains[1,2,2]   #xQ
                C2 = gains[1,2,2] - gains[1,2,1]                                 #cte2
                
                #Résolution des équations
                A = np.array([[A1, B1], [A2, B2]])
                B = np.array([C1,C2])
                try:
                    Resultat = np.linalg.solve(A,B)
                except np.LinAlgError:
                    erreur = True

                if(Resultat[0]<0 or Resultat[1]<0 or Resultat[0]+Resultat[1]>1):
                    erreur = True
                
                if(erreur == False):
                    temp=[]
                    temp.append(Resultat[0])
                    temp.append(Resultat[1])
                    temp.append(1-Resultat[0] - Resultat[1])
                    nash.append(temp)

                # trouver les proba du joueur 2 (on varit le joueur 2)
                # 1 ere équation
                A1 = gains[0, 0, 0] - gains[0, 0, 2] + gains[0, 1, 2] - gains[0, 1, 0]  # xP
                B1 = gains[0, 0, 1] - gains[0, 0, 2] + gains[0, 1, 2] - gains[0, 1, 1]  # xQ
                C1 = gains[0, 1, 2] - gains[0, 0, 2]                                    # cte1

                # 2 éme équation
                A2 = gains[0, 1, 0] - gains[0, 1, 2] -gains[0, 2, 0] + gains[0, 2, 2]    #xP
                B2 = gains[0, 1, 1] - gains[0, 1, 2] - gains[0, 2, 1] + gains[0, 2, 2]   #xQ
                C2 = gains[0, 2, 2] - gains[0, 1, 2]                                     #cte2
                
                #Résolution de l'équation
                A = np.array([[A1, B1], [A2, B2]])
                B = np.array([C1,C2])

                try:
                    Resultat = np.linalg.solve(A,B)
                except np.LinAlgError:
                    erreur = True

                if(Resultat[0]<0 or Resultat[1]<0 or Resultat[0]+Resultat[1]>1):
                    erreur = True

                if(erreur == False):
                    temp=[]
                    temp.append(Resultat[0])
                    temp.append(Resultat[1])
                    temp.append(1-Resultat[0] - Resultat[1])
                    nash.append(temp)
                    
                if(erreur == False) : 
                    print("Nash 1 : " + str(nash))
                    self.textBrowser.append("L'équilibre de nash en prenant en compte 3 stratégies : ")
                    self.textBrowser.append("Joueur 1 : "+ str(round(nash[0][0],2)) + " , "+ str(round(nash[0][1],2)) +" , " + str(round(nash[0][2],2)))
                    self.textBrowser.append("Joueur 2 : "+ str(round(nash[1][0],2)) + " , "+ str(round(nash[1][1],2)) +" , " + str(round(nash[1][2],2)))
                else : 
                    print("Nash pour un support de 3 n'existe pas, on essaye de prendre un support de Deux joueurs")
                    #recherche des strat 2 a 2 , dans un 3v3 strat
                    supportsJ1 = [[0, 1], [0, 2], [1, 2]]
                    supportsJ2 = [[0, 1], [0, 2], [1, 2]]
                    for stratJ1 in supportsJ1:
                        for stratJ2 in supportsJ2:
                            nash = mixedNash2v2(matGains[np.ix_([0, 1], stratJ1, stratJ2)])
                    
                            if nash is not None:
                                print("Equilibre de Nash pour un support de deux :" + str(nash))
                                self.textBrowser.append("Equilibre de Nash pour un support de deux :")
                                self.textBrowser.append("Joueur 1 : "+ str(round(nash[0][0],2)) + " , "+ str(round(nash[0][1],2)))
                                self.textBrowser.append("Joueur 2 : "+ str(round(nash[1][0],2)) + " , "+ str(round(nash[1][1],2)))
                                return                       
                            
                    print("Nash pour un support de 2 n'existe pas")
                    self.textBrowser.append("Nash pour un support de 2 n'existe pas")


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 598)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setGeometry(QtCore.QRect(80, 90, 70, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(12)
        self.label_0.setFont(font)
        self.label_0.setObjectName("label_0")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(80, 150, 70, 20))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(12)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.btn_export = QtWidgets.QPushButton(self.centralwidget)
        self.btn_export.setGeometry(QtCore.QRect(590, 30, 170, 40))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(20)
        self.btn_export.setFont(font)
        self.btn_export.setObjectName("btn_export")
        self.btn_import = QtWidgets.QPushButton(self.centralwidget)
        self.btn_import.setGeometry(QtCore.QRect(590, 110, 170, 40))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(20)
        self.btn_import.setFont(font)
        self.btn_import.setObjectName("btn_import")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(470, 330, 301, 131))
        self.textBrowser.setObjectName("textBrowser")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 240, 421, 311))
        self.tableView.setObjectName("tableView")
        self.btn_gameinfo = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gameinfo.setGeometry(QtCore.QRect(570, 480, 101, 31))
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(10)
        self.btn_gameinfo.setFont(font)
        self.btn_gameinfo.setObjectName("btn_gameinfo")
        self.checkBox_0 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_0.setGeometry(QtCore.QRect(10, 0, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(10)
        self.checkBox_0.setFont(font)
        self.checkBox_0.setObjectName("checkBox_0")
        self.lineEdit_0 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_0.setGeometry(QtCore.QRect(160, 90, 90, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_0.setFont(font)
        self.lineEdit_0.setObjectName("lineEdit_0")
        self.lineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_1.setGeometry(QtCore.QRect(160, 150, 90, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_1.setFont(font)
        self.lineEdit_1.setObjectName("lineEdit_1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #buttons
        self.btn_export.clicked.connect(self.create_csv)
        self.btn_import.clicked.connect(self.import_csv)

        self.btn_gameinfo.clicked.connect(self.check_function)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_0.setText(_translate("MainWindow", "Joueur 0"))
        self.label_1.setText(_translate("MainWindow", "Joueur 1"))
        self.btn_export.setText(_translate("MainWindow", "Export CSV"))
        self.btn_import.setText(_translate("MainWindow", "Import CSV"))
        self.btn_gameinfo.setText(_translate("MainWindow", "Game Infos"))
        self.checkBox_0.setText(_translate("MainWindow", "Somme Nulle"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

