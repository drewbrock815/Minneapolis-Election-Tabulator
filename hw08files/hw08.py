import statistics
import math

#Problem A
def count_votes(csvfile, candidate):
    """  
    Purpose:
        Count the number of first, second, and third place votes there are for a certain candidate in a list
    Parameters:
        csvfile: the file name that you are pulling data from
        candidate: the name of the candidate you want the number of votes from
    Return:
        Return a list of the number of first, second, and third place votes
    """
    #Check that file is correct
    try:
        fp = open(csvfile)
    except FileNotFoundError:
        print("File not found")
        return None
    #Get each line of the CSV
    lines = fp.readlines()
    #Vote counter for candidate
    first = 0
    second = 0
    third = 0
    #Iterate through each line
    for line in lines[1:]:
        line = line.replace('\n', '') #Remove each new line so split function works
        votes = line.split(',')[1:] #Start in the second row
        for vote in votes:
            if vote == candidate and vote == votes[0]: #Verify the candidate and the ranking
                first += 1
            elif vote == candidate and vote == votes[1]:
                second += 1
            elif vote == candidate and vote == votes[2]:
                third += 1
    return [first, second, third]

#Problem B
def remove_candidate(csvfilein, csvfileout, candidate):
    """ 
    Purpose:
        To remove a particular candidate from contention by removing their name from any votes
        The function should output a new csv file with the given name
        and include the same column headers as the original.
    Parameters:
        csvfilein: the csvfile of votes that is inputted
        csvfileout: a new csvfile with the same headers and rows; remove votes containing the input candidate
        candidate: an inputted candidate that will be in csvfilein and removed in csvfileout
    Return value:
        Return the number of votes that were affected
    """
    with open(csvfilein, 'r') as fp:
        
        lines = fp.readlines()
        dataList = []
        lines[0] = lines[0].replace('\n', '') #Remove \n from first line
        x = lines[0].split(',')
        dataList.append(x) #Add edited first row as list
        affectedCounter = 0
        
        for line in lines[1:]:
            
            line = line.replace('\n', '')
            votes = line.split(',')[1:]
            x = []
            
            x.append(line.split(',')[0]) #Add category number to the list
            
            for vote in votes:
                if vote != candidate:
                    x.append(vote) #Add non deleted candidate to list
                if vote == candidate:
                    affectedCounter += 1
            dataList.append(x)
        
        with open(csvfileout, 'w') as fp:
            
            for ballot in dataList:
                for vote in ballot:
                    if vote != ballot[-1]:
                        fp.write(vote + ',')
                    else:
                        fp.write(vote)
                fp.write('\n')
                
    return affectedCounter

#Problem C

def ranked_choice_full(csvfile, candidate_list):
    """  
    Purpose:
        Take a csvfile name and list of candidate names. Function should return the winner of the election
        by the ranked choice process. Use each funtion in the steps
    Parameters:
        csvfile: 
            one of the given data sets of ballots that will be used in combination with the
            candidate list to determine the winner
        candidate_list: 
            a list of candidate names
    Return Value:
        return the name of the winner
    """
    originalCSV = str(csvfile)
    roundCounter = 0
    tempCandidateList = candidate_list[:]
    i = 0
    
    while i < len(candidate_list):
        leastVotes = float('inf')
        candidateLeastVotes = ''
        numFirstVotes = []
        totalFirstVotes = 0 # Counter of votes so you can figure out 50%
        
        for candidate in tempCandidateList:
            numVotes = count_votes(csvfile, candidate)
            numFirstVotes.append(numVotes[0]) 
        for votes in numFirstVotes:
            totalFirstVotes += votes
        
        for candidate in tempCandidateList:
            numVotes = count_votes(csvfile, candidate)
            if numVotes[0] > (totalFirstVotes // 2):
                return candidate
            if numVotes[0] < leastVotes:
                leastVotes = numVotes[0]
                candidateLeastVotes = candidate
            
                
        roundCounter += 1
        remove_candidate(csvfile, 'round' + str(roundCounter) + '_' + originalCSV, candidateLeastVotes)
        csvfile = 'round' + str(roundCounter) + '_' + originalCSV
        print("In round {}, {} is eliminated".format(roundCounter, candidateLeastVotes))
        if candidateLeastVotes in tempCandidateList:
            tempCandidateList.remove(candidateLeastVotes)
        i += 1

print(ranked_choice_full('mayor2.csv',  ['Marcus Harcus',  'Kate Knuth', 'Bob Carney Jr', 'Laverne Turner',
                                   'Troy Benjegerdes', 'Paul E. Johnson','Doug Nelson', 'Sheila Nezhad',
                                   'AJ Awed','Nate Atkins', 'Christopher W David','Mike Winter','Jacob Frey',
                                   'Kevin Ward','Clint Conner','Mark Globus', 'Jerrell Perry']))