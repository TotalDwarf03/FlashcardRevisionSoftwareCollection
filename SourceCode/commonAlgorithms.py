#This script contains a series of commonly used algorithms.
#These include any validation, sorts or searches.

def quickSort(dataset, mode):
    """Sorts the given dataset in ascending or descending order"""

    lowerList = []
    equalList = []
    upperList = []

    if len(dataset) > 1:
        pivot = dataset[0] #Assign a pivot

        #For each element in the dataset,
        #If its lower than the pivot, put it in the lower list,
        #If its higher than the pivot, put it in the upper list,
        #If its equal to the pivot, put it in the equal list
        for value in dataset: 
            if value < pivot:
                lowerList.append(value)
            if value == pivot:
                equalList.append(value)
            if value > pivot:
                upperList.append(value)

        #Will recursively sort upper and lower lists until whole list is sorted
        if mode == "asc":
            return quickSort(lowerList, mode) + equalList + quickSort(upperList, mode)
        if mode == "desc":
            return quickSort(upperList, mode) + equalList + quickSort(lowerList, mode)
    else:
        return dataset

def binarySearch(dataset, searchedVal):
    """Searches a given dataset for a value (must be sorted first)"""

    leftPointer = 0
    rightPointer = len(dataset)
    
    #While the pointers haven't crossed,
    #If the midpoint is the searched value, return it (if value found)
    #If the midpoint is greater than the searched value, discard the upper half of the list
    #If the midpoint is less than the searched value, discard the lower half of the list
    while leftPointer <= rightPointer:
        midPoint = (leftPointer + rightPointer) //2

        if dataset[midPoint] == searchedVal:
            return midPoint

        if dataset[midPoint] > searchedVal:
            rightPointer = midPoint - 1

        if dataset[midPoint] < searchedVal:
            leftPointer = midPoint + 1
    return -1

def lengthCheck(value, characters):
    """Returns True if the length of value is less than characters"""
    
    if len(value) > characters:
        return False
    else:
        return True

def presenceCheck(value):
    """Returns True if value isn't empty"""

    if len(value.replace(" ", "")) == 0:
        return False
    else:
        return True