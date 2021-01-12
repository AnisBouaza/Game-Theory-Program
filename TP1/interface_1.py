import sys
import numpy as np
import pandas as pd
from itertools import product

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PyQt5.uic import loadUi


players_name = []
strategies = []
combinaisons = []
gains = []
playerStrats = {}
playerGains = {}
num_players = 0

class Ui_MainWindow(object):

    def add_player(self):
        players_name.append(self.le_player.text())
        self.le_player.setText('')
        
    def add_strats(self):
        temp = np.arange(0, int(self.le_strategie.text()), 1)
        strategies.append(temp.tolist())
        self.le_strategie.setText('')
    
    def create_combin(self):
        temp_list = list(product(*strategies))
        for x in temp_list:
            combinaisons.append(x)

    def create_csv(self):
        self.comboBox1.addItems(players_name)
        header_list = []
        for i in players_name:
            header_list.append("Gain " + i)
            


        resultsDataFrame = pd.DataFrame(combinaisons)
        '''print(resultsDataFrame)'''
        resultsDataFrame.columns = players_name
        '''print(resultsDataFrame)'''
        resultsDataFrame = resultsDataFrame.reindex(columns=resultsDataFrame.columns.tolist() + header_list)
        print(resultsDataFrame)
        resultsDataFrame.to_csv("params.csv", index=None)

        
    def import_csv(self):
        players_name.clear()
        data = pd.read_csv("params.csv")
        names = list(data.columns)
        num_players= int(len(names)/2)
        for i in range(num_players):
            players_name.append(names[i])
        print(players_name)
        self.comboBox1.addItems(players_name)
        for i in players_name:
            temp_list = []
            temp_col = data[i].tolist()
            temp_len = len(set(temp_col))
            for j in range(temp_len):
                temp_list.append(j)
                
            strategies.append(temp_list)
        print(strategies)


        temp_list = list(product(*strategies))
        for x in temp_list:
            combinaisons.append(x)
        print(combinaisons)
        
        for i in range(num_players):
            gains.append(list(data['Gain '+ players_name[i]]))
        print(gains)

    def info_player(self):
        self.textBrowser1.clear()
        self.textBrowser1.append('player name : ' + players_name[self.comboBox1.currentIndex()-1])
        self.textBrowser1.append('strategies : ' + str(strategies[self.comboBox1.currentIndex()-1]))
        self.textBrowser1.append('gains : ' + str(gains[self.comboBox1.currentIndex()-1]))

    def create_profils(self):
        self.textBrowser1.clear()
        self.textBrowser1.append('nom des joueurs :' + str(players_name))
        global playerStrats
        data = pd.read_csv("params.csv")
        for i in players_name:
            e=int(i.replace('p', ''))
            playerStrats[e-1]= np.unique(list(data[i]))
        print("Strategie: ", playerStrats)
        self.textBrowser1.append("Strategie: "+ str(playerStrats))

        global playerGains
        for i in players_name:
            e = int(i.replace('p', ''))
            playerGains[e-1] = []
            for s in playerStrats[e-1]:
                temp_DF = data[data[i] == int(s)]
                playerGains[e-1].append(list(temp_DF["Gain p"+ str(e)]))
        print(playerGains)
        self.textBrowser1.append("Gains: "+ str(playerGains))
        self.textBrowser1.append("Combinaisons :" + str(combinaisons))

    def StrictDom(self):
        self.textBrowser1.clear()
        data = pd.read_csv("params.csv")
        headers = list(data.head())
        playersArr = headers[0:(len(headers) // 2)]
        print("Players: ", playersArr)
        self.textBrowser1.append("Players: " + str(playersArr))
        playerStrats = {}
        for e in playersArr:
            playerStrats[e] = np.unique(list(data[e]))
        print("Strategies: ", playerStrats)
        self.textBrowser1.append("Strategies: " + str(playerStrats))
        playerGains = {}
        for e in playersArr:
            playerGains[e] = []
            for s in playerStrats[e]:
                print("Player ", e, "Strategie ", s)
                interDF = data[data[e] == int(s)]
                print(interDF)
                playerGains[e].append(list(interDF["Gain " + e]))
                print("==================================")
        print("Gains: ", playerGains)
        self.textBrowser1.append("Gains: " + str(playerGains))
        self.textBrowser1.append("================ Recherche des Strategies Strictement Dominantes : ================")
        for p in playerGains:
            for s in playerGains[p]:
                otherStrats = playerGains[p].copy()
                currentStrat = otherStrats.pop(otherStrats.index(s))
                dom = True
                for e in otherStrats:
                    for i in range(len(currentStrat)):
                        if e[i] >= currentStrat[i]:
                            dom = False
                    if dom == True:
                        self.textBrowser1.append("Joueur " + str(p))
                        self.textBrowser1.append("La Strategie: " + str(currentStrat) + "(" + str(playerGains[p].index(
                            s)) + ") domine la Strategie: " + str(e) + "(" + str(playerGains[p].index(
                            e)) + ")")
                        print("La Strategie: ", currentStrat, "(", playerGains[p].index(s), ") domine la Strategie: ", e,"(", playerGains[p].index(
                            e), ")")
                if dom == True:
                    self.textBrowser1.append("La Strategie: " + str(currentStrat) + "(" + str(playerGains[p].index(s)) + ")" + " est une strategie strictement dominante pour le Joueur " + str(p))
                    print("La Strategie: ", currentStrat, "(", playerGains[p].index(s), ")", " est un strategie strictement dominante pour le Joueur ", p)

    def faibleDom(self):
        data = pd.read_csv("params.csv")
        headers = list(data.head())
        playersArr = headers[0:(len(headers) // 2)]
        print("Players: ", playersArr)
        '''self.textBrowser1.append("Players: " + str(playersArr))'''
        playerStrats = {}
        for e in playersArr:
            playerStrats[e] = np.unique(list(data[e]))
        print("Strategies: ", playerStrats)
        '''self.textBrowser1.append("Strategies: " + str(playerStrats))'''
        playerGains = {}
        for e in playersArr:
            playerGains[e] = []
            for s in playerStrats[e]:
                print("Player ", e, "Strategie ", s)
                interDF = data[data[e] == int(s)]
                print(interDF)
                playerGains[e].append(list(interDF["Gain " + e]))
                print("================================")
        print("Gains: ", playerGains)
        print("================================")
        self.textBrowser1.append(" ================  Recherche des Strategies Faiblement Dominantes : ================")
        '''self.textBrowser1.append("Gains: " + str(playerGains))'''
        for p in playerGains:
            for s in playerGains[p]:
                otherStrats = playerGains[p].copy()
                currentStrat = otherStrats.pop(otherStrats.index(s))
                dom = True
                for e in otherStrats:
                    for i in range(len(currentStrat)):
                        if e[i] > currentStrat[i]:
                            dom = False
                    if dom == True:
                        self.textBrowser1.append("Joueur " + str(p))
                        self.textBrowser1.append("La Strategie: " + str(currentStrat) + "(" + str(playerGains[p].index(
                            s)) + ") domine la Strategie: " + str(e) + "(" + str(playerGains[p].index(
                            e)) + ")")
                        print("La Strategie: ", currentStrat, "(", playerGains[p].index(s), ") domine la Strategie: ", e,"(", playerGains[p].index(
                            e), ")")
                if dom == True:
                    self.textBrowser1.append("La Strategie: " + str(currentStrat) + "(" + str(playerGains[p].index(s)) + ")" + " est une strategie faiblement dominante pour le Joueur " + str(p))
                    print("La Strategie: ", currentStrat, "(", playerGains[p].index(s), ")", " est un strategie faiblement dominante pour le Joueur ", p)

    def niv_secu(self):
        self.textBrowser1.append('niveau de sécurité du joueur ' + self.comboBox1.currentText()+ ':')
        strat_num = 0
        for i in playerGains[self.comboBox1.currentIndex()-1]:
            self.textBrowser1.append('Strat ' + str(strat_num) + ' : ' + str(i) + ' -> le niveau de sécurité : ' + str(min(i)))
            strat_num += 1

    def equilibre_nash(self):
        data = pd.read_csv('params.csv')
        data = data.to_numpy()
        print(" Recherche de l'Equilibre de Nash ")
        self.textBrowser1.append(" ================ Recherche de l'Equilibre de Nash ================")
        n_strategie = []
        for i in strategies:
            n_strategie.append(len(i))

        def meilleurReponses(line,matrix,player,n_players):
            plays = [str(list(l[line,0:n_players])) for l in matrix]
            responses = [l[line,player+n_players] for l in matrix]
            res = dict(zip(plays,responses))
            return res
        
        def keyswithmaxval(d):
            mx_tuple = max(d.items(),key = lambda x:x[1]) 
            max_list =[i[0] for i in d.items() if i[1]==mx_tuple[1]]
            return max_list


        nash_equlibre = []
        d = []
        for i in range(len(players_name)):
                for p in players_name:
                    e=int(p.replace('p', ''))-1
                    matrix = []
                    strat = n_strategie[e]
                    for i in range(strat):
                        matrix.append(data[np.where(data[:,e]==i)])
                    l = matrix[0]
                    meilleur = []
                    for i in range(len(l)):
                        meilleurChoix = keyswithmaxval(meilleurReponses(i,matrix,e,len(players_name)))
                        for b in meilleurChoix:
                            meilleur.append(b)
                    d.append(meilleur)
        nash_equlibre = list(set.intersection(*map(set,d)))
        if not nash_equlibre:
            self.textBrowser1.append("Il n y a pas d'equlibre de nash")
        else:
            self.textBrowser1.append("Les equilibres de nash :" + str(nash_equlibre))

    def optimum_pareto(self):
        self.textBrowser1.append('================ Recherche Optimum de pareto ================')
        def paretoDomine(A, B):
            pareto = False
            for i in range(len(A)):
                if A[i] < B[i]:
                    return False
                elif A[i] > B[i]:
                    pareto = True
            return pareto

        data = np.genfromtxt('params.csv', delimiter = ',', dtype ='int32')
        listOptimums = []
        nbJoueurs = len(data[0])//2
        for i in range(1,len(data)):
            domine = True
            for j in range(1, len(data)):
                if paretoDomine(data[j, nbJoueurs:], data[i, nbJoueurs:]):
                    domine = False
                    break
            if domine:
                listOptimums.append(list(data[i, 0:nbJoueurs]))
        
        self.textBrowser1.append('Optimum de pareto ' + str(listOptimums))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("TP Stratégies Pures")
        MainWindow.setFixedSize(800, 600)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_addplayer = QtWidgets.QPushButton(self.centralwidget)
        self.btn_addplayer.setGeometry(QtCore.QRect(580, 40, 170, 40))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.btn_addplayer.setFont(font)
        self.btn_addplayer.setObjectName("btn_addplayer")
        self.btn_addcsv = QtWidgets.QPushButton(self.centralwidget)
        self.btn_addcsv.setGeometry(QtCore.QRect(580, 110, 170, 40))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(20)
        self.btn_addcsv.setFont(font)
        self.btn_addcsv.setObjectName("btn_addcsv")
        self.btw_importcsv = QtWidgets.QPushButton(self.centralwidget)
        self.btw_importcsv.setGeometry(QtCore.QRect(580, 180, 170, 40))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(20)
        self.btw_importcsv.setFont(font)
        self.btw_importcsv.setObjectName("btw_importcsv")
        self.comboBox1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox1.setGeometry(QtCore.QRect(30, 300, 81, 21))
        self.comboBox1.setObjectName("comboBox1")
        self.comboBox1.addItem("")
        self.lbl_player = QtWidgets.QLabel(self.centralwidget)
        self.lbl_player.setGeometry(QtCore.QRect(30, 100, 120, 30))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(15)
        self.lbl_player.setFont(font)
        self.lbl_player.setObjectName("lbl_player")
        self.lbl_strategie = QtWidgets.QLabel(self.centralwidget)
        self.lbl_strategie.setGeometry(QtCore.QRect(30, 160, 120, 30))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        font.setPointSize(15)
        self.lbl_strategie.setFont(font)
        self.lbl_strategie.setObjectName("lbl_strategie")
        self.le_player = QtWidgets.QLineEdit(self.centralwidget)
        self.le_player.setGeometry(QtCore.QRect(170, 100, 150, 30))
        self.le_player.setObjectName("le_player")
        self.le_strategie = QtWidgets.QLineEdit(self.centralwidget)
        self.le_strategie.setGeometry(QtCore.QRect(170, 160, 150, 30))
        self.le_strategie.setObjectName("le_strategie")
        self.btn_playerinfo = QtWidgets.QPushButton(self.centralwidget)
        self.btn_playerinfo.setGeometry(QtCore.QRect(320, 300, 120, 20))
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(10)
        self.btn_playerinfo.setFont(font)
        self.btn_playerinfo.setObjectName("btn_playerinfo")
        self.btn_gameinfo = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gameinfo.setGeometry(QtCore.QRect(600, 300, 120, 20))
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(10)
        self.btn_gameinfo.setFont(font)
        self.btn_gameinfo.setObjectName("btn_gameinfo")
        self.textBrowser1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser1.setGeometry(QtCore.QRect(20, 360, 731, 192))
        self.textBrowser1.setObjectName("textBrowser1")
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
        self.btn_addplayer.clicked.connect(self.add_player)
        self.btn_addplayer.clicked.connect(self.add_strats)

        self.btn_addcsv.clicked.connect(self.create_combin)
        self.btn_addcsv.clicked.connect(self.create_csv)
        
        self.btw_importcsv.clicked.connect(self.import_csv)
        self.btw_importcsv.clicked.connect(self.create_combin)
        self.btw_importcsv.clicked.connect(self.create_profils)

        self.btn_gameinfo.clicked.connect(self.StrictDom)
        self.btn_gameinfo.clicked.connect(self.faibleDom)
        self.btn_gameinfo.clicked.connect(self.equilibre_nash)
        self.btn_gameinfo.clicked.connect(self.optimum_pareto)

        self.btn_playerinfo.clicked.connect(self.info_player)
        self.btn_playerinfo.clicked.connect(self.niv_secu)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_addplayer.setText(_translate("MainWindow", "Add Player"))
        self.btn_addcsv.setText(_translate("MainWindow", "Generate CSV"))
        self.btw_importcsv.setText(_translate("MainWindow", "Import CSV"))
        self.comboBox1.setItemText(0, _translate("MainWindow", "Players"))
        self.lbl_player.setText(_translate("MainWindow", "Player Name"))
        self.lbl_strategie.setText(_translate("MainWindow", "Strategies"))
        self.btn_playerinfo.setText(_translate("MainWindow", "Player Infos"))
        self.btn_gameinfo.setText(_translate("MainWindow", "Game Infos"))
    




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


