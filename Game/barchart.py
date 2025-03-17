import pandas #Imports the necessary modules
import matplotlib.pyplot as plt

with open ("scores/sim_scores_lower_speed.csv", 'r') as file: #Reads the file
    data = pandas.read_csv(file) #Sets the data to be the data read from the file
    score_2 = data['score1'].tolist() #Puts the two columns from the csv file into lists
    score_1 = data['score2'].tolist()
score_1_5 = score_1.count(5) #Counts how many times the score of 5 is present in each list
score_2_5 = score_2.count(5)
x = ['Paddle speed of 6 ','Paddle speed of 8'] #Sets the two lists to be graphed against each other
y = [score_1_5, score_2_5]

plt.title('How the AI paddle speed affects its win-rate (ball speed of 9)') #Sets the labels of the graph
plt.xlabel('Speed of the paddle')
plt.ylabel('Amount of wins')
plt.bar(x,y)
plt.show()