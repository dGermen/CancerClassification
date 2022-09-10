# -*- coding: utf-8 -*-
"""
Earlier version on Fri May 29 10:04:04 2020
Created on Tue Jun 16 19:10:57 2020

Project No: ???

@author: Deniz Germen
"""

import random
from random import randrange
# Assumptions from the developer

# File names will be set according to initial files names
# User will format excel files according to initial file format (Which sheet is used, which cell data is written etc.)
# All data will come with patient ids and ids will ONLY consist of numbers
# Number of data per patient is consistent
# No missing data
# M and B is written at the END of the row

# =============================================================================
# Notes from developer
# Add unpacking, packing sites at the start, end of the functions?
# =============================================================================

#Here we set global defaults

# Changes some viewing options nothing more no/yes
exactModeOff = "yes"

trainingFileName = "cancerTrainingData.csv" 
testFileName = 'cancerTestingData.csv'


# This is where program will initiate, it takes an input but doesn't do anything with it since you have no say in this
def isThisCancerMain(userWishes):
    
    trainingData = excelReader(trainingFileName)
    
    classifierData = classifierDataCreator(trainingData)
    
    classifierPrinter(classifierData);
    
    testData = excelReader(testFileName)
    
    idealMajorityPoint = classifierTesterOptimizer(classifierData, testData)
    
    loop(classifierData, testData, idealMajorityPoint)
    
    createNewRecord(classifierData, idealMajorityPoint)
    
    createdData = newDataCreator(classifierData, 250, 0.5, idealMajorityPoint)
    
    # classifierDataCreated = classifierDataCreator(createdData)
    
    # classifierPrinter(classifierDataCreated)

    # wherethisallgoes(classifierData)
def wherethisallgoes(classifierData):
    for i in range(0,10):
        createdData = newDataCreator(classifierData, 250, 0.5, 0)
        
        classifierData = classifierDataCreator(createdData)
        
        classifierPrinter(classifierData)
# Input: Classifier data, patient data, chosen majority point 
# Output: Noting, just prints
# User can read data from the data base
def loop(classifierData, testData, MajorityPoint):
    
    while(1 == 1):
        pID = input("Type an ID to check a patient ('quit' to stop):")
        
        if pID == "quit":
            break
        
        try:         
            # So it crashes before printing
            testData['attributes'][pID]
                
            print("Checking ID:{}'s classification".format(pID))
            
            # Accesses dictionary according to input, pID, classifies with classifier
            identifiedClass = classifier(classifierData, testData['attributes'][pID], MajorityPoint, "on")
            
            if identifiedClass == "M":
                identifiedClass = "Malignant"
                
            else:
                identifiedClass = "Benign"
            
            # Reports back the result
            print("Overall Diagnosis for patient {}: {}".format(pID,identifiedClass))
            
        except KeyError:
            print("Please enter a valid patient ID")
            pass
        
    print("Program finished. \n")
    
# Input: fileName or full location
# Output: excelData formatted for classifierDataCreator, classifier
# Reads data from excel file, returns a dictionary that is usable by classifierDataCreator
def excelReader(fileName = 'cancerTrainingData.csv'):
      
    # Informs user that data is being read
    print("Reading in file {}...".format(fileName))
    
    # Creates the output dictionary. Carrying attributes, classification dictionaries that can be accesed with ids and attributeNames list
    dataDictionary = {
        "attributes": {}, 
        "classification": {},
        "dataProperties": {
            'attributeNames': [],
            'attributeLength': [],
            'numberOfPatients': 0
            },
        }
    
    records = open(fileName, 'r')
    
    # Goes thourgh the "records" created from excel file, assigns values to respective places
    for indx, line in enumerate(records):
        lineList = line.split(',')
        
        # Checking if id is numeric
        if lineList[0].isnumeric():
            
            # Records attributes according to id
            dataDictionary['attributes'][lineList[0]] = lineList[1:-1]

            # Records classification according to id
            dataDictionary['classification'][lineList[0]] = lineList[-1][0]
            
            # Counting number of patients
            dataDictionary['dataProperties']['numberOfPatients'] += 1
        
        # Checking if there is a "#" to find attribute names, this part essantially designed to make program adaptable
        elif lineList[0][0] == "#":
            
            # Bad formatted input data makes everything harder, remember that name ID is stored but generally NOT used as name so start from index 1
            dataDictionary['dataProperties']['attributeNames'].append(lineList[0].split(" ")[1].split("_")[0].replace("\n",""))
            
    # Setting the data properties
    dataDictionary['dataProperties']['attributeLength'] = len(list(dataDictionary['attributes'].values())[0])
    
    # Informs user that data has been read
    print("Done reading file {}.\n".format(fileName))
    
    return dataDictionary        

# Input: excelData formatted by excelReader
# Output: classiferData formatted for classifier
# Finds attributes for classifier(essantially classsifier itself)
def classifierDataCreator(trainingDataDictionary):
       
    # Creating values that will be used inside the function
    totalValuesMalignant = [0]*trainingDataDictionary['dataProperties']['attributeLength']
    totalValuesBenign = [0]*trainingDataDictionary['dataProperties']['attributeLength']
    
    numberOfMalignantPatient = 0
    numberOfBenignPatient = 0
    
    averageValuesMalignant = []
    averageValuesBenign = []
    cutOffs = []
    
    # Finding total of each attribute and number of people for each classification
    for pID,patientAttributes in trainingDataDictionary['attributes'].items():
        
        # Finding total patient nubmer for each class
        if trainingDataDictionary['classification'][pID] == "M":
            numberOfMalignantPatient += 1
            
        elif trainingDataDictionary['classification'][pID] == "B":
            numberOfBenignPatient += 1
            
        # Summing up attributes for different classes
        for atrIndx,attributeValue in enumerate(patientAttributes):
            
            if trainingDataDictionary['classification'][pID] == "M":
                totalValuesMalignant[atrIndx] += float(attributeValue)
                
            elif trainingDataDictionary['classification'][pID] == "B":
                totalValuesBenign[atrIndx] += float(attributeValue)
                
    
    # Finding average for each classification and cut off
    for atrIndx, (totalValueMalignant, totalValueBenign) in enumerate(zip(totalValuesMalignant,totalValuesBenign)):
    
        averageValuesMalignant.append(totalValueMalignant/numberOfMalignantPatient) 
        averageValuesBenign.append(totalValueBenign/numberOfBenignPatient)
        cutOffs.append((averageValuesMalignant[atrIndx] +averageValuesBenign[atrIndx] ) / 2)

    # Conveying some properties from input dictionary, adds found information
    classifierDictionary ={
        'averageValuesMalignant' : averageValuesMalignant,
        'averageValuesBenign' : averageValuesBenign,
        'cutOffs' : cutOffs,
        'dataProperties' : trainingDataDictionary['dataProperties']
        }
    
    return classifierDictionary

# Input: classifier data to print
# Output: noting
#  Prints the classifier data according to guide lines
def classifierPrinter(classifierData):
    
    # Printing classic formatting
    print("Classifier, benign and malignant stats")
    print("=====================================================================")
    print("{:>28} {:>12} {:>12} {:>12}".format("Key","Malignant","Classifier","Benign"))
    print("{:>28} {:>12} {:>12} {:>12}".format("","Average","Midpoint","Average"))
    
    # Priting data from "classifierData"
    for attributeName,averageValueMalignant,cutOff,averageValuesBenign in\
    zip(classifierData['dataProperties']['attributeNames'][1::],classifierData['averageValuesMalignant'],
        classifierData['cutOffs'],classifierData['averageValuesBenign']):
        
        print("{:>28} {:>12.3f} {:>12.3f} {:>12.3f}".format(attributeName,averageValueMalignant,cutOff,averageValuesBenign))

    # Giving spaceee
    print("\n")
# Input: classifier Data and test Data
# Output: Optimized majority point
# Optimizes majority point according to testData 
def classifierTesterOptimizer(classifierData,testData):
    
    # Informing user
    print("Classifying records...")
    
    maxMajorityPointAccuracy = 0    
    
    # "+1 is for real life, python indexing difference
    for majorityPoint in range(1,classifierData['dataProperties']['attributeLength']+1):
    
        falseClassification = 0
        
        # Comparing real and found classifications
        for pID, patientAttributes in testData['attributes'].items():
            if classifier(classifierData,patientAttributes, majorityPoint) != testData['classification'][pID]:
                falseClassification += 1
        
        # Finding accuracy for respective point chosen
        majorityPointAccuracy = (testData['dataProperties']['numberOfPatients'] - falseClassification)/testData['dataProperties']['numberOfPatients']
        
        # Made by developer to view the process, disabled in default
        if exactModeOff == "no":
            print("\nFor majority point of {}:".format(majorityPoint))
            print("The classifier correctly predicted the class (malignant/benign) of {} records out of {} records."\
                  .format(testData['dataProperties']['numberOfPatients'] - falseClassification, testData['dataProperties']['numberOfPatients']))
            print("The classifier achieved an accuracy of {:.4} percent.".format(majorityPointAccuracy*100)) 
        
        # Checking if new point is performed better than earlier tests, if yes changes it as the new best
        if majorityPointAccuracy > maxMajorityPointAccuracy:
            maxMajorityPointAccuracy = majorityPointAccuracy
            idealMajorityPoint = majorityPoint
            idealFalseClassification = falseClassification
    
    print("Done classifying.\n")
    
    # Made by developer to view the process, disabled in default
    if exactModeOff == "no":
        print("Best results have been obtained for majority point of {}:".format(idealMajorityPoint))
        
    print("The classifier correctly predicted the class (malignant/benign) of {} records out of {}"\
              .format(testData['dataProperties']['numberOfPatients'] - idealFalseClassification, testData['dataProperties']['numberOfPatients']))
    print("The classifier achieved an accuracy of {:.4} percent.".format(maxMajorityPointAccuracy*100)) 
    
    return idealMajorityPoint

# Input: classifierData and singePatientData
# Output: result of the classfying
# Compares data from the single patient and classifier, arrives at a conclusion and reports back
def classifier(classifierData, singlePatientData, majorityPoint, printer = "off"):
    
    point = [0]*classifierData['dataProperties']['attributeLength']
    
    # According function caller's wish prints out the header
    if printer == "on":
        print("{:>28} {:>12} {:>12} {:>12}".format("Key","Patient","Classifier","Class"))
        print("{:>28} {:>12} {:>12} {:>12}".format("","Value","Cutoff",""))
        
    # Made according to example output, nubmers resebmle the indexes of attribute names
    userDefinedPrinting = [3, 9, 4, 8, 2, 7, 1, 6, 10, 5]     
    
    # Comparing cut off and respective attribute making up over all point of maliganity
    for atrNameIndx in userDefinedPrinting:
        
        # Because of the attribute name list starting with ID and ID not being used this is necessary
        atrIndx = atrNameIndx-1
                
        if classifierData['cutOffs'][atrIndx] < float(singlePatientData[atrIndx]):
            point[atrIndx] = 1
            
        # According to function caller's wish prints the outcome and data for both patient and classifier
        if printer == "on":
            Class = "Benign"
            if point[atrIndx] == 1:
                Class = "Malignant"
            
            # Printing out key, patient value, classifier cutoff, class
            print("{:>28} {:>12.3f} {:>12.3f} {:>12}".format(classifierData['dataProperties']['attributeNames'][atrNameIndx],
            float(singlePatientData[atrIndx]),classifierData['cutOffs'][atrIndx],Class)) #!!! float, should have changed in reader?

    if printer == "on": # With this 2 spaces without 1 how is this possible?
        print("")
        
    # Returns back the final conclusion for all total of all attributes  
    if sum(point) < majorityPoint:

        return "B"
    
    return "M"

# Input: classifier data, ideal majority point
# Output: Nothing
# Takes attribute input from user and diagnoses
def createNewRecord(classifierData, idealMajorityPoint):
    
    singlePatientData =[0]*classifierData['dataProperties']['attributeLength']
    
    print("Welcome to auto-diagnose!")
    
    while(1):
        
        for atrIndx in range(0,classifierData['dataProperties']['attributeLength']):
            
            # Due to ID....
            atrNameIndx = atrIndx + 1
            
            while(1):
            
                try:
                    # Asking for data for respective attribute
                    data = input("Please enter {}: ".format(classifierData['dataProperties']['attributeNames'][atrNameIndx]))
                    singlePatientData[atrIndx] = float(data)
                    break
                    
                except ValueError:
                    print("Please enter a number")
                    pass
        # Calling classifier and recording outcome
        identifiedClass = classifier(classifierData, singlePatientData, idealMajorityPoint, "on")        
        
        if identifiedClass == "M": #!!! Used this combo more than once may be make it into a function???
            identifiedClass = "Malignant"
                
        else:
                identifiedClass = "Benign"
        
        # Reporting the outcome
        print("Overall Diagnosis for the patient: {}".format(identifiedClass))
        
        while(1):
        
            stay = input("Do you want to auto-diagnose new patient? [y/n]:")
            
            if (stay == "n") or (stay == "y"):
                break
          
            else:
                print("Please enter a valid answer!")
        
        if (stay == "n"):
            print("Thank you for using auto-diagnose!\n")
            break

# Input: Classifier data, howmany patients will be created, what fraction will be malignant, majority point
# Output: Fresh, new new new patient dictionary
# Creates data according to average points of the patients and assuming given majority point is a right diagnose
def newDataCreator(classifierData, numberOfPatient, malignantToTotalRatio, majorityPoint):
    
    # Creates the dictionary that will be send back, conveying info from classifier
    createdDataDictionary = {
        "attributes": {}, 
        "classification": {},
        "dataProperties": classifierData['dataProperties'],
        }
    
    createdDataDictionary['dataProperties']['numberOfPatient'] = numberOfPatient
    
    atrIndxList = list(range(0,classifierData['dataProperties']['attributeLength']))
    atrRangeMalignant = []
    atrRangeBenign = []
    
    # Creating the range for randomizing attribute points
    for atrIndx in atrIndxList:
        
        rangeMalignant = classifierData['averageValuesMalignant'][atrIndx] - classifierData['cutOffs'][atrIndx]
        atrRangeMalignant.append([classifierData['averageValuesMalignant'][atrIndx] - rangeMalignant,
                                     classifierData['averageValuesMalignant'][atrIndx] + rangeMalignant])
                                     
        rangeBenign = min(classifierData['averageValuesBenign'][atrIndx], 
                          classifierData['cutOffs'][atrIndx] -classifierData['averageValuesBenign'][atrIndx])
        atrRangeBenign.append([classifierData['averageValuesBenign'][atrIndx] - rangeBenign,
                                  classifierData['averageValuesBenign'][atrIndx] + rangeBenign])
        
    numberOfMalignant = int(round(numberOfPatient*malignantToTotalRatio))
    numberOfBenign = numberOfPatient-numberOfMalignant
    numberOfClass = numberOfMalignant
    
    Class = "M"

    i = 0
    # All of the patients will be created under this
    while( i < 2):
        
        i2 = 0
        # Randomzing the number of malignant points with in a patient but with wished classification taht is determined by majority point
        if (Class == "M"):
            
            lowerLimit = majorityPoint
            # This is 11 due to randrange not providing the upper limit
            upperLimit = 11
                
        elif (Class == "B"):
            
            lowerLimit = 0
            # This is NOT "majorityPoint - 1" due to randrange not providing the upper limit
            upperLimit = majorityPoint
        
        # Patients will be created by class order this is controlled by how many malignant points they have
        while( i2 < numberOfClass):
    
            # Set how many malignant point will patient have
            numberOfMalignantPoint = randrange(lowerLimit,upperLimit)
            currentMalignantPoint = 0         
            
            # Not to overwrite old created patient
            while(1):
                pID = randrange(1,numberOfPatient*10)
                if pID in createdDataDictionary.keys():
                    pass
                else:
                    break
            
            # Setting patient classification
            createdDataDictionary['classification'][pID] = Class
            
            # Shuffling the attribute index list order, so not always same parameters are malignant/benign
            random.shuffle(atrIndxList)
            
            # Creating the key in dictionary, -100 so it is obvious developer is not over written the value
            createdDataDictionary['attributes'][pID] = [-100]*classifierData['dataProperties']['attributeLength']

            # Setting the attributes one by one
            for atrIndx in atrIndxList:
                
                if currentMalignantPoint <= numberOfMalignantPoint: #!!! for loop can be used here for this if/elif think about it
                
                    atrRangeInUse = atrRangeMalignant
        
                elif currentMalignantPoint > numberOfMalignantPoint:

                    atrRangeInUse =  atrRangeBenign

                createdDataDictionary['attributes'][pID][atrIndx] = random.uniform(atrRangeInUse[atrIndx][0],atrRangeInUse[atrIndx][1])
                currentMalignantPoint +=1
                
            i2 += 1
            
        numberOfClass = numberOfBenign
        Class = "B"
        
        i += 1

    print("Created the new {} patients out of thin air!(Actually from classifier data) Their malingnant to total ratio is  {}%".format(numberOfPatient, malignantToTotalRatio*100))
    return createdDataDictionary

# As everything is, starts at the end...
isThisCancerMain("PLEASE NO")






























