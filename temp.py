import pandas as pd
import math
import sklearn
from sklearn.neighbors import KNeighborsClassifier

def distance(data_loan, data_derogatory, test_loan, test_derogatory):
    return math.sqrt((data_loan - test_loan) ** 2 +
                     100000000 * (data_derogatory - test_derogatory) ** 2)

def UpdateNeighbors(neighbors, item, distance,
                                          k, ):
    if len(neighbors) < k:
        # List is not full, add
        # new item and sort
        neighbors.append([distance, item])
        neighbors = sorted(neighbors)
    else: 
        # List is full Check if new
        # item should be entered
        if neighbors[-1][0] > distance: 
            # If yes, replace the
            # last element with new item
            neighbors[-1] = [distance, item]
            neighbors = sorted(neighbors)
 
    return neighbors

def CalculateNeighborsClass(neighbors, k):
    count = {}
 
    for i in range(k):
        if neighbors[i][1] not in count:
 
            # The class at the ith index is
            # not in the count dict.
            # Initialize it to 1.
            count[neighbors[i][1]] = 1
        else:
 
            # Found another item of class
            # c[i]. Increment its counter.
            count[neighbors[i][1]] += 1
 
    return count

def FindMax(Dict):
 
    # Find max in dictionary, return
    # max value and max index
    maximum = -1
    classification = ''
 
    for key in Dict.keys():
         
        if Dict[key] > maximum:
            maximum = Dict[key]
            classification = key
 
    return (classification, maximum)

def application_approval(data, loan, derogatory_marks, k):
    """
    :param data: (pandas.DataFrame) A DataFrame that contains training data. 
                    It has the following columns: Loan, DerogatoryMarks, Accepted.
    :param loan: (int) Requested loan.
    :param derogatory_marks: (int) Number of derogatory marks for the customer.
    :param k: (int) Coeficient k in the k-nearest neighbors' algorithm.
    :returns: (boolean) True if the customer's loan can be accepted; False otherwise.
    """
    nbors = []
    loans = data["Loan"]
    marks = data["DerogatoryMarks"]
    accept = data["Accepted"]
    #print(loans)
    for i in range(len(loans)):
        dist = distance(loans[i],marks[i],loan,derogatory_marks)
        nbors = UpdateNeighbors(nbors,accept[i],dist,k)
    count = CalculateNeighborsClass(nbors,k)
    
    boo,max = FindMax(count)
    return boo

data = pd.DataFrame({
            'Loan' : [52000, 100000, 97000, 62000],
            'DerogatoryMarks' : [0, 2, 0, 5],
            'Accepted' : [True, True, False, True]
        }, 
        columns = ['Loan', 'DerogatoryMarks', 'Accepted']
    )
print(application_approval(data, 85000, 1, 1))






# Import necessary modules
