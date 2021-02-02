# Game-Theory-Program
A PyQt UI to visualise the implementation of some Game Theory 


# Build
- Compile with python and install the needed librairies.


# the UI

**I** -The first UI is designed for **pure strategies**
<img src = "Screenshots\Screenshot_1.png" title = ui1 >

- **Add Player**  : This button allows to add a player with the given name in the **Player Name** field and a number of strategies in the **Strategies** field.

- **Generate CSV**  : Once the players are added with their strategies you can generate a CSV file that is editable to add the gains of each player.

- **Import CSV**  :  Allows to import a CSV file.

- **Player Infos** : Allows you to get the infos of the player selected in the combobox like the number of his strategies, gains, security level for each strategie.

- **Game Infos** : After the configuration of the game parameters shows the different implemented alogirthms like nash equilibrium, pareto optimum, strictly dominant  strategies and weakly dominant strategies.


**II** -The second UI is designed for **mixed strategies**
<img src = "Screenshots\Screenshot_2.png" title = ui2 >

- **Export CSV** : After filling the number of strategies relative to each player in the fields “Joueur 0” and “Joueur 1”, you can export a CSV editable file to add the gains.

- **Import CSV** : Import a CSV file.

- **Game Infos** : After finishing the configuration this button allows you to show the results of the implemented algorithms like nash equilibrium, if the null sum game box is checked it shows the informations relative to a null sum game.

