from django.shortcuts import render
from .virtual_files.CLA import CLA
from .form import VirtualElectionForm
from django.contrib import messages
from django.shortcuts import render, redirect
import random
import time
from django.views import View
from collections import Counter



def SocialSecurity(request):
    if request.method == "POST":
        print("What is your name?")
        name = request.POST['name']
        if name:
        # Generate SSN
            random.seed(time.time())
            SSN = random.randint(100000000, 1000000000)

            # Give user their SSN
            messages.success(request,f'Your social security number is: {SSN}')
            print("Your social security number is: ")
            print(SSN)

            # Print SSN to file
            f = open('Virtual_app/virtual_files/ssnfile.txt', 'a+', encoding="utf-8")
            f.write(f"{name},{SSN}" + "\n")

            f.close()
        else: messages.success(request,'ADD Names please')

    return render(request,'SocialSecurity.html')


def Agency(request):
    if request.method == "POST":
   
    
        name = request.POST['name']
        ssn = request.POST['ssn']
        # answer = request.POST['answer']
        print(name)
        # Ask the voter for name

        name = name
        cla = CLA(name)

        # Default condition assumes voter does not have an SSN
        voterValidated = False
        SSN = 0
        validID = 0
            
        # Ask voter for SSN
        print("What is your SSN?")
        SSN = ssn

        # Check if there is a match.
        f = open('Virtual_app/virtual_files/ssnfile.txt', 'r', encoding="utf-8")

        # Check every line in ssnfile.txt
        matchFound = False
        for line in f:
            # Read line
            currentLine = line.split(",")
            storedSSN = currentLine[1].replace('\n', '')
            # If we find a match
        if SSN == storedSSN:
                # Match found, quit the loop
                matchFound = True
                validID = cla.generate_validation_num()
                print(f"{cla.name}, your validation number is: {validID}. Make sure to remember it.")
                messages.success(request,f"{cla.name}, your validation number is: {validID}. Make sure to remember it. ")
                messages.success(request,'Are there any more voters? Or Exit To Home')
        else:
            # Reject voter, ask for SSN again
                print("SSN invalid")
                messages.error(request,"SSN invalid , Try again.")
                

        f.close()


        # Write Name and Validation number on row in .txt file
        f = open('Virtual_app/virtual_files/voterfile.txt', 'a+', encoding="utf-8")
        f.write(f"{cla.name},{SSN},{validID}" + "\n")

      
                  # ***** CTF: Central Tabulating Facility functionality *****
    return render(request,'Virtual.html')





def Code(request):
    if request.method == "POST":
        name = request.POST['name']
        valid_no = request.POST['valid_no']
        vote = request.POST['vote']
    

    # Have a class representing a candidate and their votes
      


        # Ask voter to enter name, valid_no, and vote
        f = open("Virtual_app/virtual_files/votes.txt", "r")
        for line in f:
            currentLine = line.split(",")
            # Store the candidate's name
            nameOfCandidate = currentLine[0]
        f.close()    
        name = name
        valid_no = valid_no
        vote = vote
        vodes_count=1
        # Create a Voter Message
    

        # Check validation number against list received by the CLA
        # Open voterfile.txt
        f = open("Virtual_app/virtual_files/voterfile.txt", "r")

        matchFound = False
        for line in f:
            # Read line
            currentLine = line.split(",")
            storedValidNo = currentLine[2].replace('\n', '')
            # If we find a match
            if valid_no == storedValidNo:
                # Match found, quit the loop
                matchFound = True

                # FIXME: Testing matching functionality
                print(f"Valid_no {storedValidNo} found!")
                print(f"Voter's SSN is {currentLine[1]}")

                break

        # FIXME: Testing matching functionality
        if not matchFound:
          
            messages.error(request,"Could not find a match")
        f.close()

        # If the validation number is present in voterfile.txt, "cross off" that number
        # Add the validation number to usednumbers.txt
        # FIXME: Have the program check if the validation number is present in usednumbers.txt when the user
        #   enters their validation number (i.e., there is a match with voter file)
        if matchFound:
            f = open("usednumbers.txt", "a")
            f.write(f"{valid_no}\n")

        f.close()

        # CTF adds the voter's SSN to the tally of one candidate
        # Create a new file, votes.txt, with the voter's candidate, SSN added as a line
        if matchFound:
            f = open("votes.txt", "a")
            f.write(f"{vote},{valid_no}\n")

        f.close()

        # After all votes have been received, the CTF publishes the outcome
        # Tally up all the votes for each candidate in votes.txt

        # Have an empty list of Candidate objects
        # Each Candidate will have a name and vote_count
        candidates = []
        count=[]
        # Open votes.txt
        f = open("Virtual_app/virtual_files/votes.txt", "r")
        for line in f:
            currentLine = line.split(",")
            # Store the candidate's name
            nameOfCandidate = currentLine[0]
            
            count.append(nameOfCandidate)
            #print(nameOfCandidate)
             
            # If the candidate is in the list, simply increment the vote count
            #    of that candidate
            candidateIsInList = False
            for candidate in candidates:
                if candidate[0] == nameOfCandidate:
                    vodes_count+=1
                    candidateIsInList = True
                    break

            # If the candidate is not in the list, add them with a default vote count of 1
        if not candidateIsInList:
            candidates.append(name)
        x=Counter(count).keys() # equals to list(set(words))
        y=Counter(count).values()
         
        
       #
        list3 = [item for sublist in zip(x, y) for item in sublist]
        def pairwise(it):
            it = iter(it)
            while True:
                try:
                    yield next(it), next(it)
                except StopIteration:
                    # no more elements in the iterator
                    return

        for a, b in pairwise(list3):
            o=(a , b)
            
            messages.success(request,f'{o}')
    # Print out the tally of votes
       
    return render(request,'code.html')




def home(request):
    
    return render(request,'home.html')