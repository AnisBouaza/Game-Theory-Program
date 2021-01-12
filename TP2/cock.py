def mixedNash2x2(gains):
    nash = []

    #Si 2 stratégie par joueur:  (Les probabilités sont p et 1-p)
    if len(gains[0]) == 2:
        for i in range(2):
            numerateur = gains[i, 1, 1] - gains[i, i, 1-i]
            denomi = gains[i, 0, 0] + gains[i, 1, 1] - gains[i, 1, 0] - gains[i, 0, 1]
            if denomi == 0:
                return None
            p = numerateur/denomi
            if p < 0 or p > 1:
                return None

            nash.append([p, (1-p)])

        return nash

def mixedNash(gains):
    nash = []

    #Si 2 stratégie par joueur:  (Les probabilités sont p et 1-p)
    if len(gains[0]) == 2:
        return mixedNash2x2(gains)
        
    elif len(gains[0]) == 3: #Si 3 stratégie par joueur:  (p1, p2 probabilité de J1 et q1, q2 probabilité de J2)
        failure = False
        A1 = np.array([ [ gains[1, 0, 0] - gains[1, 0, 1] - gains[1, 2, 0] + gains[1, 2, 1], #matrice d'équations pour J1 (inégalité du support du J2)
            gains[1, 1, 0] - gains[1, 1, 1] - gains[1, 2, 0] + gains[1, 2, 1] ], 
        [ gains[1, 0, 1] - gains[1, 2, 1] - gains[1, 0, 2] + gains[1, 2, 2], 
            gains[1, 1, 1] - gains[1, 2, 1] - gains[1, 1, 2] + gains[1, 2, 2] ] ])
        B1 = np.array([gains[1, 2, 1] - gains[1, 2, 0], gains[1, 2, 2] - gains[1, 2, 1]]) #matrice de résultats pour J1 (inégalité du support du J2)
        
        try:
            X = np.linalg.solve(A1, B1)
        except np.LinAlgError:
            failure = True

        if X[0] < 0 or X[1] < 0 or X[0]+X[1] > 1:
            failure = True

        if not failure:
            nash.append([X[0], X[1], 1-X[0]-X[1]])
        
        #Calcul de la stratégie de J2
        A2 = np.array([ [ gains[0, 0, 0] - gains[0, 0, 2] + gains[0, 1, 2] - gains[0, 1, 0], #matrice d'équations pour J2 (inégalité du support du J1)
            gains[0, 0, 1] - gains[0, 0, 2] + gains[0, 1, 2] - gains[0, 1, 1] ], 
        [ gains[0, 1, 0] - gains[0, 1, 2] -gains[0, 2, 0] + gains[0, 2, 2], 
            gains[0, 1, 1] - gains[0, 1, 2] - gains[0, 2, 1] + gains[0, 2, 2] ] ])
        B2 = np.array([gains[0, 1, 2] - gains[0, 0, 2], gains[0, 2, 2] - gains[0, 1, 2]]) #matrice de résultats pour J2 (inégalité du support du J1)
        
        try:
            X = np.linalg.solve(A2, B2)
        except np.LinAlgError:
            failure = True 

        if X[0] < 0 or X[1] < 0 or X[0]+X[1] > 1:
            failure = True

        if not failure:
            nash.append([X[0], X[1], 1-X[0]-X[1]])
            return nash
            
        else: #Tester toutes les combinaisons de supports
            supportsJ1 = [[0, 1], [0, 2], [1, 2]]
            supportsJ2 = [[0, 1], [0, 2], [1, 2]]
            for stratJ1 in supportsJ1:
                for stratJ2 in supportsJ2:
                    nash = mixedNash2x2(gains[np.ix_([0, 1], stratJ1, stratJ2)])
                    if nash is not None:
                        result = np.zeros((2, 3))
                        result[0][[stratJ1[0], stratJ1[1]]] = nash[0]
                        result[1][[stratJ2[0], stratJ2[1]]] = nash[1]
                        return result
            
            #Si aucun des cas n'a aboutit à un équilibre de nash alors erreur:
            raise Exception("L'équilibre de Nash mixte n'existe pas, veuillez entrer un jeu valide")
                    
    else: raise Exception("Nombre de joueurs invalide, veuillez entrer un jeu à 2 joueurs")