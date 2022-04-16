#This script involves around adding functionality to the front-end.
#Any technical functions or methods used in the front end is defined here. 

#Library Imports
import tkinter as tk
from tkinter import messagebox as msg
import tkinter.filedialog as fd
import playsound as p
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os as os
from datetime import datetime as dt
import shutil as sh
import textwrap
import sys

#Imports other parts of the program
import sqlInterface as sqlCont
import commonAlgorithms as algs

#Imports a library not supported by pillow
from transformLibrary.transforms import RGBTransform

class backgroundVariables():
    """Contains variables used across the program"""
    
    #
    #Customisation Variables
    #
    #These variables can be changed to edit the appearance of the program

    startupTone = "softwareAssets/startupTone1.mp3"
    FontStyle = ("Segoe UI", 11)
    BiggerFontStyle = ("Segoe UI", 14)
    titleFontStyle = ("Segoe UI", 30)
    flashcardFont = ImageFont.truetype("segoeui.ttf", 24, encoding="unic")

    version = "1.0"
    repoAddress = "https://github.com/TotalDwarf03/FlashcardRevisionSoftware"

    #
    #Technical Variables
    #
    #These variables are used throughout the program and shouldn't be edited

    previousFrame = "none"

    #Flashcard Properties
    previousOperation = None #Defines whether Rename, new set or edit function is being performed
    setInfo = 0

    #Flashcard Creation
    flashcardSet = None

    img = None
    questions = []
    answers = []
    images = []

    flashCardPointer = 0

    imagesPath = "Images/"

    #Settings
    tint = None
    factor = None

def raiseFrame(frame):
    """Raises a given frame"""
    frame.tkraise()

def back(instance):
    """Returns to the previous frame"""
    if backgroundVariables.previousFrame == "main":
        raiseFrame(instance.mainMenu)
    if backgroundVariables.previousFrame == "maker":
        raiseFrame(instance.creationSuite)

def findChildren(instance, parent, mode, colour):
    """Recursively finds all child widets for a given parent and performs an action on them depending on the mode"""
    if parent == None: 
        parent = instance.root #Sets the window to the parent if there is no parent passed in

        if mode == "colour":
            instance.themeDrop.config(fg=colour[2], bg=colour[1])
            instance.themeDrop["menu"].config(fg=colour[2], bg=colour[0])

    try:
        parent.config(bg=colour[0])
    except:
        pass #Ignore the error if the parents colour cannot be changed

    for child in parent.winfo_children(): 
        if child.winfo_children():
            findChildren(instance, child, mode, colour) #Recurse if the child has children
        else:
            if mode == "font":
                try:
                    child.config(font=backgroundVariables.FontStyle)
                except:
                    pass #Ignore error if font cannot be changed

            if mode == "clear":
                if type(child) == tk.Text:
                    child.delete("1.0", tk.END) #Empty any text widgets
            
            if mode == "colour":
                if child == instance.menubar:
                    pass    #Ignore changing the menubar as it cannot be edited
                else:
                    if type(child) == tk.Button:
                        child.config(fg=colour[2], bg=colour[1]) 
                    if type(child) == tk.Label:
                        child.config(fg=colour[2], bg=colour[0])  
                    if type(child) == tk.Scrollbar or type(child) == tk.Frame:
                        pass #Ignore any scrollbars or frames as they cannot be recoloured
 
    if mode == "font":
        instance.nameHolder.config(font=backgroundVariables.titleFontStyle)
        instance.cardCounterLbl.config(font=backgroundVariables.BiggerFontStyle)
        instance.tipsTitle.config(font=backgroundVariables.titleFontStyle)
        instance.abtTitle.config(font=backgroundVariables.titleFontStyle)   #Changes the fonts of specific widget
    if mode == "clear":
        instance.imageFilepreview.config(image="")

def getFlashcardSet(instance):
    """Gets a selected flashcard from the tree view"""

    cursorItem = instance.tree.focus()

    if cursorItem == "":
        msg.showerror(title="Error!", message="Please select a set of flashcards first!")   #Error if no set selected
        return "error"
    else:
        selectedSetDict = instance.tree.item(cursorItem)
        selectedSetInfo = selectedSetDict["values"]
        selectedSetID = selectedSetInfo[0]  #Get id of selected set

        backgroundVariables.flashcardSet = sqlCont.getRow(selectedSetID) #Gets the data of the selected set from the database

        questions = backgroundVariables.flashcardSet[4]
        answers = backgroundVariables.flashcardSet[5]
        images = backgroundVariables.flashcardSet[6]

        backgroundVariables.questions = creator.stringToList(questions)
        backgroundVariables.answers = creator.stringToList(answers)
        backgroundVariables.images = creator.stringToList(images)   #Converts the information from the database to a list

#
#Menubar Functions
#

class menubar():
    """Contains all menubar functions"""

    def exit():
        """Displays a confirmation message then closes the application"""
        confirmation = msg.askokcancel(title="Confirmation", message="This will close the application. Are you sure you want to proceed?")
        if confirmation:
            sys.exit()

    def loadRevisionTips(instance):
        """Loads the revision tips screen"""
        raiseFrame(instance.tips)

    def loadAbout(instance):
        """Loads the about screen"""
        raiseFrame(instance.about)

#
#Splash Screen Functions
#

class splashScrn():
    """Contains all Splash Screen functions"""
    def __init__(self, instance):
        """Loads the splashscreen and plays the startup tone"""
        raiseFrame(instance.splashScrn)
        p.playsound(backgroundVariables.startupTone, False)

#
#Main Menu Fuctions
#

class mainMenu():
    """Contains all main menu functions"""

    #Searching and Sorting Tree Functions

    def sortTree(tree, col, reverse):
        """Sorts the data within a tree based on the column and redisplays it in its sorted form"""

        #get the data from the tree and sort it
        data = []
        for child in tree.get_children(""): 
            elem = (tree.set(child, col), child) 
            data.append(elem) #Puts the data in the selected column into a list to be manipulated

        data.sort(reverse=reverse)

        #rearrange items in sorted positions
        for index, (value, child) in enumerate(data): #for every element with the data array
            tree.move(child, "", index) #move the data to a given index

        #reverse sort function when a column is clicked (from ascending to decending or vice versa)
        tree.heading(col, command=lambda: mainMenu.sortTree(tree, col, not reverse))

    def search(instance):
        """Searches the Treeview's Set Name column for the required set"""
        data = []

        searchedValue = instance.searchEnt.get() #Get the user's input

        for child in instance.tree.get_children():
            elem = instance.tree.set(child, "setName")
            data.append(elem.strip())   #Adds all set names to a list

        data = algs.quickSort(data, "asc") #Sorts the data
        searchLocation = algs.binarySearch(data, searchedValue) #Searches for the input in the list of sets

        if searchLocation != -1:    #If set is found
            for child in instance.tree.get_children():
                elem = instance.tree.set(child, "setName")
                elem = elem.strip()

                if elem == data[searchLocation]: #if set is the searched for set, leave it in the treeview
                    pass
                else:
                    instance.tree.delete(child) #if set is not the searched for set, remove it from the tree
            
        else:
            msg.showerror(title="Error!", message="Searched Value Not Found!") #Error if set not found
    
    def clear(instance):
        """Clears the current search"""
        mainMenu.updateTree(instance)   #Resets the tree
        instance.searchEnt.delete(0, tk.END)    #Empties searchbar

    #Navigation Button Functions
    def newSet(instance):
        """Goes to the card creation suite"""
        backgroundVariables.previousFrame = "main"
        backgroundVariables.previousOperation = "new"
        instance.creatorExitBtn["state"] = "active"
        raiseFrame(instance.creationSuite)
        freshCreator = creator(instance, False) #Sets up the creator with no loaded values
    
    def edit(instance):
        """Goes to the card creation suite with the selected set loaded"""
        backgroundVariables.previousFrame = "main"
        backgroundVariables.previousOperation = "edit"
        instance.creatorExitBtn["state"] = "disabled"
        freshCreator = creator(instance, True) #Sets up the creator with the selected set loaded

    def loadProps(instance, previousFrame):
        """Loads the Card Properties Menu and Adds its Contents"""
        backgroundVariables.previousFrame = previousFrame

        #Empties previous data input
        instance.nameEnt.delete(0, tk.END)
        instance.subjectEnt.delete(0, tk.END)

        if backgroundVariables.previousOperation == "new" and backgroundVariables.previousFrame == "maker": 
            raiseFrame(instance.cardConfigMenu) #Load empty properties screen if new set
        else:
            cursorItem = instance.tree.focus()

            if cursorItem == "":
                msg.showerror(title="Error!", message="Please select a set of flashcards first!")
            else:
                selectedSetDict = instance.tree.item(cursorItem)
                selectedSetInfo = selectedSetDict["values"]
                backgroundVariables.setInfo = selectedSetInfo

                instance.nameEnt.insert(0, str(selectedSetInfo[1]).lstrip())
                instance.subjectEnt.insert(0, str(selectedSetInfo[2]).lstrip()) #load set information into properties screen if existing set

                raiseFrame(instance.cardConfigMenu)

    def delete(instance):
        """Deletes a flashcard set and all related assets"""

        cursorItem = instance.tree.focus()

        if cursorItem == "":
            msg.showerror(title="Error!", message="Please select a set of flashcards first!") #Error if no set selected
        else:
            selectedSetDict = instance.tree.item(cursorItem)
            selectedSetInfo = selectedSetDict["values"]
            selectedSetID = selectedSetInfo[0]

            #Confirms deletion
            confirmation = msg.askokcancel(title="Confirmation", message="This will permanently delete the Flashcard Set. Are you sure you want to proceed?")
            if confirmation:
                sqlCont.deleteSet(selectedSetID) #Deletes the set from the database
                sh.rmtree(f"Images/{selectedSetID}") #Deletes any images stored regarding the set
                sqlCont.fixIncrement()  #Updates database so there are no gaps in the setID
                mainMenu.updateTree(instance)

                dirList = os.listdir("Images/") #Get all set images 

                #For every file in the Images folder with an ID bigger than the deleted one,
                #Reduce the ID by 1 to match the database
                for i in range(0, len(dirList)):
                    if os.path.isdir(f"Images/{dirList[i]}"): #Checks if object at the path is a folder
                        if int(dirList[i]) > selectedSetID:
                            newName = str(int(dirList[i]) -1) 

                            os.rename(f"Images/{dirList[i]}", f"Images/{newName}")                

    def updateTree(instance):
        """Updates the TreeView on the main menu from the database"""

        for child in instance.tree.get_children():
            instance.tree.delete(child) #Empty current treeview

        instance.storedSets = sqlCont.getAllData()  #Get all sets from the database
        
        if instance.storedSets != None:
            instance.charsToRemove = "('"

            #Format each set from the database appropritely
            #and turn them into lists
            for item in instance.storedSets:
                params = str(item).split(",")
                for i in range(0, 4):
                    for char in instance.charsToRemove:
                        params[i] = (params[i].replace(char, ""))

                #Add specific set info to the treeview
                instance.tree.insert("", tk.END, values=(params[0], params[1], params[2], params[3]))

    def revise(instance):
        """Goes to revision Screen and loads the selected set for use"""

        if getFlashcardSet(instance) == "error": 
            pass #If no set selected, dont do anything
        else:
            if len(backgroundVariables.questions) == 1:
                backgroundVariables.flashCardPointer = 0
                instance.backBtnRev["state"] = "disabled"
                instance.nextBtnRev["state"] = "disabled"
            else:
                backgroundVariables.flashCardPointer = 0
                instance.backBtnRev["state"] = "disabled"
                instance.nextBtnRev["state"] = "active"
            
            revision(instance)  #Setup Revision suite with Selected set
            raiseFrame(instance.revisionFrame)

#
#Flashcard Creation Functions
#

class creator():
    """Contains all card creation functions"""
    def __init__(self, instance, loadVariables):
        """Sets up the creator"""
        creator.emptyCreator(instance) #Clear any already filled fields 

        if loadVariables == True:
            if getFlashcardSet(instance) == "error":
                pass #If no set selected, do nothing
            else:
                setId = backgroundVariables.flashcardSet[0]

                for i in range(0, len(backgroundVariables.images)):
                    try:
                        #Move saved set images into Images folder to be used
                        pilImg = Image.open(f"Images/{setId}/{i}.png")
                        pilImg.save(f"Images/{i}.png", )
                        os.remove(f"Images/{setId}/{i}.png")
                    except FileNotFoundError:
                        pass #ignore error if image doesn't exist
                
                sh.rmtree(f"Images/{setId}") #Delete storage folder

                raiseFrame(instance.creationSuite)
                creator.loadCard(instance)  #Put information into creator

    def stringToList(string):
        """Converts a given string to a list (typically, string from database)"""
        charstoRemove = ("[]'")

        for char in charstoRemove:
            string = string.replace(char, "") #Remove old list formatting
        
        array = string.split(",")

        for i in range(0, len(array)):
            try:
                if array[i][0] == " ":
                    array[i] = array[i].replace(" ", "", 1) #Remove first to character from the element if it's a space
            except IndexError:
                pass

        return array

    def emptyCreator(instance):
        """Empties the flashcard creator"""

        backgroundVariables.questions = []
        backgroundVariables.answers = []
        backgroundVariables.images = []
        backgroundVariables.flashCardPointer = 0

        findChildren(instance, instance.creationSuite, "clear", None) #Empty any widgets in the creator frame
        try:
            os.remove("Images/tempImg.png") #Removes any residue cache image
        except:
            pass    #if no cache image, ignore error
        instance.creatorPreviousBtn["state"] = "disabled" 
        #disable previous button as the next card displayed will always be the first one in the set

    def generatePreviewImage(pilImg):
        """Downsizes a given image to be displayed"""

        width, height = pilImg.size
        pilImg.close()

        increment = 2
        originalWidth = width
        originalHeight = height

        #while the width or height is over 200 pixels, continue to shrink the image by an increment of 1
        while width > 200 or height > 200:
            width = originalWidth / increment
            height = originalHeight / increment
            increment += 1

        img = tk.PhotoImage(file=r"Images/tempImg.png") #Open the selected image
        img = img.subsample(increment, increment) #Downscale the image
        backgroundVariables.img = img 

    def saveCard(q, a, fileName):
        """Saves the inputted flashcard"""

        #If inputted question and answer follow validation routines,
        #Add the card to the set's data ready to be pushed to the database
        if algs.lengthCheck(q, 60) == True and algs.lengthCheck(a, 120) == True:
            if algs.presenceCheck(q) == True and algs.presenceCheck(a) == True:

                #If new card, append it
                if backgroundVariables.flashCardPointer == len(backgroundVariables.questions):
                    backgroundVariables.questions.append(q)
                    backgroundVariables.answers.append(a)
                    backgroundVariables.images.append(fileName)

                #If existing card, overwrite it
                if backgroundVariables.flashCardPointer < len(backgroundVariables.questions):
                    backgroundVariables.questions[backgroundVariables.flashCardPointer] = q
                    backgroundVariables.answers[backgroundVariables.flashCardPointer] = a
                    backgroundVariables.images[backgroundVariables.flashCardPointer] = fileName

                try:
                    #Try to save the image on the card in the appropriate folder
                    pilImg = Image.open("Images/tempImg.png")
                    pilImg.save(f"Images/{backgroundVariables.flashCardPointer}.png", )
                    pilImg.close()
                    os.remove("Images/tempImg.png")
                except:
                    pass #If no image selected, ignore
            else:
                msg.showerror(title="Error!", message="Question and Answer field must be filled!") 
                return "Error" #Error if presence check failed
        else:
            msg.showerror(title="Error!", message="Question or Answer is too long! (maximum of 60 characters)") 
            return "Error" #Error if length check failed

    def loadCard(instance, afterDelete=False):
        """Loads a Flashcard into the creator"""

        #If the pointer is inside the list or a card has been deleted,
        #replace data in inputs with current card
        if backgroundVariables.flashCardPointer < len(backgroundVariables.questions) or afterDelete == True: 
            instance.questionTxt.delete("1.0", tk.END)
            instance.answerTxt.delete("1.0", tk.END)

            instance.questionTxt.insert("0.0", backgroundVariables.questions[backgroundVariables.flashCardPointer])
            instance.answerTxt.insert("0.0", backgroundVariables.answers[backgroundVariables.flashCardPointer])

            try:
                pilImg = Image.open(f"Images/{backgroundVariables.flashCardPointer}.png")
                pilImg.save("Images/tempImg.png")
                creator.generatePreviewImage(pilImg)
                instance.imageFilepreview.config(image=backgroundVariables.img)
                pilImg.close()
                os.remove("Images/tempImg.png")
            except:
                pass #Ignore if image doesn't exist
    
    def browseFiles(instance):
        """Opens a file browser window to select an image to be added to a card"""

        creator.removePreviewImg(instance) #Removes image already on card

        file = fd.askopenfile(parent=instance.root,mode='rb',title='Choose a file') #Open file browser

        #If a file is selected, open it and save it as a cache image.
        #Then, display it in the editor
        if file: 
            splitFile = str(file).split("'")
            fileDir = str(splitFile[1])
            pilImg = Image.open(fileDir)
            pilImg.save("Images/tempImg.png")
            pilImg.close()

            pilImg = Image.open("Images/tempImg.png")
            creator.generatePreviewImage(pilImg)
            instance.imageFilepreview.config(image=backgroundVariables.img)
            file.close()
    
    def removePreviewImg(instance):
        """Removes the current image in the creator"""

        instance.imageFilepreview.config(image="") #Remove image from widget
        try:
            os.remove(f"Images/{backgroundVariables.flashCardPointer}.png") #Delete image from storage
        except FileNotFoundError:
            pass #ignore error if image doesn't exist

    def deleteCard(instance):
        """Deletes the current flashcard"""

        confirmation = msg.askokcancel(title="Confirmation", message="This card will be completely discarded. Are you sure you want to proceed?")
        if confirmation:
            #Remove question, answer and image from the set's data
            try:
                backgroundVariables.questions.pop(backgroundVariables.flashCardPointer)
            except IndexError:
                findChildren(instance, None, "clear", None)
            else:
                backgroundVariables.answers.pop(backgroundVariables.flashCardPointer)
                backgroundVariables.images.pop(-1)

                creator.removePreviewImg(instance) #Remove the image

                files = os.listdir("Images/") #Get every file in the Images folder
                files2 = []

                #For each .png file (image) that is after the current card's image,
                #Decrease the image's ID by 1 so it matches with the question and answer
                for count, file in enumerate(files):
                    if ".png" in file:
                        if file != "tempImg.png":
                            files[count] = file[:-4]
                            files2.append(files[count])

                files = files2

                for count, file in enumerate(files): #Second for loop because files have been removed
                    if int(files[count]) > backgroundVariables.flashCardPointer:
                        try:
                            os.rename(f"Images/{file}.png", f"Images/{int(file)-1}.png")
                        except FileNotFoundError: #If card doesnt have an image, Ignore bug
                            pass

                if backgroundVariables.flashCardPointer != 0:
                    backgroundVariables.flashCardPointer -= 1
                
                if backgroundVariables.flashCardPointer == 0:
                    instance.creatorPreviousBtn["state"] = "disabled"
                
                try:
                    creator.loadCard(instance, True) #Try to load the card before the deleted one
                except IndexError:
                    pass #if no file to load, dont load it      
            
    def exit(instance):
        """Displays a confirmation message then goes back to main menu"""
        confirmation = msg.askokcancel(title="Confirmation", message="All progress will be discarded. Are you sure you want to proceed?")
        if confirmation:

            #Delete any image files stored
            for i in range(0, len(backgroundVariables.images)):
                try:
                    os.remove(f"Images/{backgroundVariables.images[i]}.png")
                except:
                    pass
            backgroundVariables.previousFrame = "main"
            backgroundVariables.previousOperation = None
            back(instance) #Return to previous screen
    
    def next(instance):  
        """Loads the next Flashcard""" 

        #Get inputted data
        q = instance.questionTxt.get("1.0", tk.END).rstrip()
        a = instance.answerTxt.get("1.0", tk.END).rstrip()

        fileName = backgroundVariables.flashCardPointer
        
        #If inputs follow validation routines, save the card,
        #Empty the creator and load the next card
        if creator.saveCard(q, a, fileName) != "Error":
            findChildren(instance, instance.creationSuite, "clear", None)
            backgroundVariables.flashCardPointer += 1

            if backgroundVariables.flashCardPointer == 1:
                instance.creatorPreviousBtn["state"] = "active"

            creator.loadCard(instance)
        
    def previous(instance):
        """Loads the previous flashcard"""

        #Get inputted data
        q = instance.questionTxt.get("1.0", tk.END).rstrip()
        a = instance.answerTxt.get("1.0", tk.END).rstrip()

        fileName = backgroundVariables.flashCardPointer

        #If inputs follow validation routines, save the card,
        #Empty the creator and load the previous card
        if creator.saveCard(q, a, fileName) != "Error":
            findChildren(instance, instance.creationSuite, "clear", None)
            backgroundVariables.flashCardPointer -= 1

            if backgroundVariables.flashCardPointer == 0:
                instance.creatorPreviousBtn["state"] = "disabled"

            creator.loadCard(instance)

    def finish(instance):
        """Finalises the set and goes to card properties screen"""

        #Get inputted data
        q = instance.questionTxt.get("1.0", tk.END).rstrip()
        a = instance.answerTxt.get("1.0", tk.END).rstrip()

        fileName = backgroundVariables.flashCardPointer
        
        #If data follows validation routines,
        #Go to flashcard properties screen
        if creator.saveCard(q, a, fileName) != "Error":
            mainMenu.loadProps(instance, "maker")

#
#Card Properties Functions
#

class cardConfig():
    """Contains all card properties functions"""

    def save(instance):
        """Saves a flashcard set"""

        data = None
        rename = None

        #Get inputted data
        setName = instance.nameEnt.get()
        setSubject = instance.subjectEnt.get()

        #Get time and date of save
        now = dt.now()
        dateModified = now.strftime("%d-%m-%Y %H:%M")

        #If from the creation suite, load the data from it
        if backgroundVariables.previousFrame == "maker":
            if algs.presenceCheck(setName) == True and algs.presenceCheck(setSubject) == True:
                data = [setName, setSubject, dateModified, str(backgroundVariables.questions), str(backgroundVariables.answers), str(backgroundVariables.images)]
        
        else:
            #If not from the creation suite, rename the set
            if algs.presenceCheck(setName) == True and algs.presenceCheck(setSubject) == True:
                setId = backgroundVariables.setInfo[0] 
                sqlCont.renameSet(setId, setName, setSubject) #Renames the set with the inputted setname and subject
                rename = True

        if data != None: 
            #If the set is new, Add new set to the database and get its ID
            if backgroundVariables.previousOperation == "new":
                sqlCont.insertData(data)
                setId = sqlCont.getLastSetId()

            #If set isn't new, update the data which has been changed
            else:
                setId = str(backgroundVariables.flashcardSet[0])
                sqlCont.editSet(setId, data)
                rename = True

            #Save Images in a reuseable folder
            path = os.path.join(backgroundVariables.imagesPath, setId) #Makes a path for the new folder
            os.mkdir(path) #Makes the directory at the path

            #For every image to be saved, Put it in the new folder for storage
            for i in range(0, len(backgroundVariables.images)):
                try:
                    pilImg = Image.open(f"Images/{i}.png")
                    pilImg.save(f"Images/{setId}/{i}.png", )
                    os.remove(f"Images/{i}.png")
                except FileNotFoundError:
                    pass #ignore error if image doesn't exist
        
        if data != None or rename == True:
            msg.showinfo(title="Save Successful", message="Flashcard set saved successfully!")
            backgroundVariables.previousFrame = "main"
            mainMenu.updateTree(instance)
            back(instance)
        else:
            msg.showerror(title="Error!", message="All fields must be filled!")

#
#Flashcard Revision
#

class revision():
    """Contains all revision functions"""

    def __init__(self, instance):
        """Sets up the revision suite"""
        revision.loadQuestion(instance)
    
    def loadQuestion(instance):
        """Loads a question onto the flashcard to be displayed to the user"""

        #Update card counter
        instance.cardCounterLbl.config(text=f"{backgroundVariables.flashCardPointer+1}/{len(backgroundVariables.questions)}")

        question = backgroundVariables.questions[backgroundVariables.flashCardPointer] #get question
        revision.displayCard(instance, question, "q") #Put question on the card

        #Update button to show the answer
        instance.showAnsBtn.config(text="Show Answer", command=lambda: revision.loadAnswer(instance))

    def loadAnswer(instance):
        """Loads an answer onto the flashcard to be displayed to the user"""

        answer = backgroundVariables.answers[backgroundVariables.flashCardPointer] #get answer
        revision.displayCard(instance, answer, "a") #Put answer on the card

        #Update button to show the question
        instance.showAnsBtn.config(text="Show Question", command=lambda: revision.loadQuestion(instance))

    def displayCard(instance, text, mode):
        """Puts the given text onto the flashcard"""

        flashcardbg = Image.open("softwareAssets/Notecard.png") #open flashcard resource image
        flashcardbg = flashcardbg.convert("RGB") #convert its colour codes to rgb (255, 255, 255)

        tintedCard = settings.flashcardImg(instance, flashcardbg, backgroundVariables.factor, backgroundVariables.tint) #tint the card to match the theme

        editableImg = ImageDraw.Draw(tintedCard) #convert flashcard to a drawing so it can be edited

        imgWidth, imgHeight = tintedCard.size #get the size of the flashcard in pixels

        paragraph = textwrap.wrap(text, width=20) #turn the questions into lines of 20
        textYpos, padding = 20, 10

        #For each line in the paragraph, Get the width of the line,
        #Position the text in the middle of the flashcard and Increment the height for the next line
        for line in paragraph: 
            textWidth, textHeight = editableImg.textsize(line, font=backgroundVariables.flashcardFont) 
            editableImg.text(((imgWidth - textWidth)/2, textYpos), line, font=backgroundVariables.flashcardFont, fill=(0,0,0)) 
            textYpos += textHeight + padding 

        if mode == "q": #If loading a question
            try:
                cardImg = Image.open(f"Images/{backgroundVariables.flashcardSet[0]}/{backgroundVariables.flashCardPointer}.png")
            except FileNotFoundError:
                cardWithImg = tintedCard #If card has no image, don't load one
            else:
                #If card has an image, Load it onto the tinted card

                cardWithImg = tintedCard.copy() #creates a copy of the image to be edited

                origCardImgWidth, origCardImgHeight = cardImg.size

                #Scale the image down so that its at most 200x200 pixels
                if origCardImgWidth > origCardImgHeight:
                    newCardImgWidth = 200
                    rescalePercent = newCardImgWidth/origCardImgWidth
                    newCardImgHeight = int(origCardImgHeight * rescalePercent)
                else:
                    newCardImgHeight = 100
                    rescalePercent = newCardImgHeight/origCardImgHeight
                    newCardImgWidth = int(origCardImgWidth * rescalePercent)

                cardImg = cardImg.resize((newCardImgWidth, newCardImgHeight))

                #Put the image on the card
                cardWithImg.paste(cardImg, (int((imgWidth - newCardImgWidth)/2), int(imgHeight - newCardImgHeight - padding)))
        else:
            cardWithImg = tintedCard

        tkimg = ImageTk.PhotoImage(cardWithImg) #convert edited image to a tkinter image so it can be displayed
        instance.flashcardLbl.config(image=tkimg) #put image into placeholder label
        instance.flashcardLbl.image = tkimg #link them so it shows up

    def nextCard(instance):
        """Goes to next Flashcard"""
        if backgroundVariables.flashCardPointer == 0:
            instance.backBtnRev["state"] = "active" #If on the first card, enable the previous button

        backgroundVariables.flashCardPointer += 1
        revision.loadQuestion(instance) #Load next card

        if backgroundVariables.flashCardPointer == len(backgroundVariables.questions)-1:
            instance.nextBtnRev["state"] = "disabled" #If last card, disable next button
    
    def previousCard(instance):
        """Goes to previous card"""
        if backgroundVariables.flashCardPointer == len(backgroundVariables.questions)-1:
            instance.nextBtnRev["state"] = "active" #If on the last card, enable the next button

        backgroundVariables.flashCardPointer -= 1
        revision.loadQuestion(instance) #Load previous card

        if backgroundVariables.flashCardPointer == 0:
            instance.backBtnRev["state"] = "disabled" #If first card, disable previous button
    
    def exit(instance):
        """Exits the revision suite"""
        confirmation = msg.askokcancel(title="Confirmation", message="This will take you back to the Main Menu. Are you sure you want to proceed?")
        if confirmation:
            raiseFrame(instance.mainMenu) #Go to main menu
#
#Application settings
#

class settings():
    """Contains all setting functions"""

    def gotoSettings(instance):
        """Goes to Settings"""
        backgroundVariables.previousFrame = "main"
        raiseFrame(instance.settings)

    def apply(instance):
        """Applies a theme"""
        theme = instance.themeVar.get() #Get chosen theme

        #Sets colour palette to appropriate theme
        if theme == "Light":
            colours = ["#E4E7EB", "#9AABB3", "#000000"]
            backgroundVariables.tint = (0,0,0)
            backgroundVariables.factor = 0
        if theme == "Dark":
            colours = ["#242526", "#3A3B3C", "#B0B3B8"]
            backgroundVariables.tint = (33,46,82)
            backgroundVariables.factor = .60
        if theme == "Hello Kitty":
            colours = ["#FEDCDB", "#FEB1B7", "#FD788B"]
            backgroundVariables.tint = (207,87,138)
            backgroundVariables.factor = .60

        #Updates widgets with the theme
        findChildren(instance, None, "colour", colours)

        #Store current theme
        with open("DataStorage/theme.txt", "w") as f:
            f.write(str(theme))
        
    def flashcardImg(instance, img, fact=None, tint=None, mode=None):
        """Tints the Flashcard Template to match the theme"""

        #If card needs tinting, tint it
        if tint != None:
            tintedbg = RGBTransform().mix_with(tint, factor=fact).applied_to(img)
        #If card doesnt need tinting, dont tint it
        else:
            tintedbg = img

        if mode != "start":
            return tintedbg