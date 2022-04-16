#This script revolves around creating the front-end of the program.
#Any UI assets are created here. 

#Library Imports
import backEnd as back
import tkinter as tk
from tkinter import ttk
import sqlInterface as sqlCont
import webbrowser

def callback(url):
    """Opens a web browser window with the given URL"""
    webbrowser.open_new(url)

class ui:
    def __init__(self):
        """Creates all the GUI for the application"""

        #
        #Creates a window for all the widget to reside in
        #

        self.root = tk.Tk()
        self.root.title('Flashcard Revision Software')
        self.root.resizable(False, False)

        #
        #Menubar
        #
        #This Section Creates a Menubar which resides at the top of the window

        self.menubar = tk.Menu(self.root)

        self.optionsMenu = tk.Menu(self.menubar, tearoff=0) 
        self.optionsMenu.add_command(label="Settings", command= lambda: back.settings.gotoSettings(self))
        self.optionsMenu.add_separator()
        self.optionsMenu.add_command(label="Quit", command=back.menubar.exit)

        self.menubar.add_cascade(label="Options", menu=self.optionsMenu) 

        self.helpMenu = tk.Menu(self.menubar, tearoff=0) 
        self.helpMenu.add_command(label="Revision Tips", command= lambda: back.menubar.loadRevisionTips(self))
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label="About", command= lambda: back.menubar.loadAbout(self))

        self.menubar.add_cascade(label="Help", menu=self.helpMenu) 

        self.root.config(menu=self.menubar)

        #
        #Splash Screen
        #
        #This section creates the GUI for the Splash Screen

        self.splashScrn = tk.Frame(self.root)
        self.splashScrn.grid(row=0, column=0, sticky="nsew")
        self.splashScrn.columnconfigure(0, weight=1)

        self.logo = tk.PhotoImage(file=r"softwareAssets/progLogo.png") #Loads Logo from directory
        self.logo = self.logo.subsample(2, 2)  #Scales Image down
        self.logoHolder = tk.Button(self.splashScrn, image=self.logo, command= lambda: back.raiseFrame(self.mainMenu), relief="flat")
        self.logoHolder.grid(row=0, column=0, columnspan=2)

        self.nameHolder = tk.Label(self.splashScrn, text="Flashcard Creation \n"
        "and Examination Suite") 
        self.nameHolder.grid(row=1, column=0, columnspan=2)

        self.subtext = tk.Label(self.splashScrn, text="*Click the logo to begin*")
        self.subtext.grid(row=2, column=0, columnspan=2)

        #
        #Main Menu
        #
        #This section create the GUI for the main menu

        self.mainMenu = tk.Frame(self.root)
        self.mainMenu.grid(row=0, column=0, sticky="nsew")
        self.mainMenu.rowconfigure(1, weight=1)

        #Main Menu Search Bar
        self.searchbarHolder = tk.Frame(self.mainMenu)
        self.searchbarHolder.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 5))

        self.searchEnt = tk.Entry(self.searchbarHolder) 
        self.searchEnt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.searchEnt.insert(tk.END, "Search")

        self.searchIcon = tk.PhotoImage(file=r"softwareAssets/searchlogo.png")
        self.searchIcon = self.searchIcon.subsample(40, 40)
        self.searchBtn = tk.Button(self.searchbarHolder, text="Search", image=self.searchIcon, command=lambda: back.mainMenu.search(self))
        self.searchBtn.pack(side=tk.LEFT, fill=tk.BOTH)

        self.clearIcon = tk.PhotoImage(file=r"softwareAssets/clearLogo.png")
        self.clearIcon = self.clearIcon.subsample(8, 8)
        self.clearBtn = tk.Button(self.searchbarHolder, text = "Clr", image=self.clearIcon, command=lambda: back.mainMenu.clear(instance))
        self.clearBtn.pack(side=tk.LEFT, fill=tk.BOTH)

        #Main Menu Treeview
        self.listboxHolder = tk.Frame(self.mainMenu)
        self.listboxHolder.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=20, pady=(0, 20))

        self.columnHeadings = ("setId", "setName", "subject", "dateModified") #Defines the column headings for the tree widget
        self.tree = ttk.Treeview(self.listboxHolder, columns=self.columnHeadings, show="headings") 

        #define headings for Tree
        self.tree.heading("setId", text="ID:", command=lambda: back.mainMenu.sortTree(self.tree, self.columnHeadings[0], False))
        self.tree.heading("setName", text="Name:", command=lambda: back.mainMenu.sortTree(self.tree, self.columnHeadings[1], False))
        self.tree.heading("subject", text="Subject:", command=lambda: back.mainMenu.sortTree(self.tree, self.columnHeadings[2], False))
        self.tree.heading("dateModified", text="Date Modified:", command=lambda: back.mainMenu.sortTree(self.tree, self.columnHeadings[3], False))

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbarY = tk.Scrollbar(self.listboxHolder)
        self.tree.configure(yscroll=self.scrollbarY.set) #Links scrollbar to treeview
        self.scrollbarY.pack(side=tk.RIGHT, fill=tk.Y)

        #Main Menu Button Pannel
        self.btnHolder = tk.Frame(self.mainMenu)
        self.btnHolder.grid(row=0, column=1, rowspan=3, padx=10)

        self.newSetBtn = tk.Button(self.btnHolder, text="New Set", command= lambda: back.mainMenu.newSet(self))
        self.newSetBtn.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="ew")

        self.editBtn = tk.Button(self.btnHolder, text="Edit", command=lambda: back.mainMenu.edit(self))
        self.editBtn.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        self.propsBtn = tk.Button(self.btnHolder, text="Properties", command=lambda: back.mainMenu.loadProps(self, "main"))
        self.propsBtn.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        self.deleteBtn = tk.Button(self.btnHolder, text="Delete", command=lambda: back.mainMenu.delete(self))
        self.deleteBtn.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        self.reviseBtn = tk.Button(self.btnHolder, text="Revise", command=lambda: back.mainMenu.revise(self))
        self.reviseBtn.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        #
        #Flashcard Creation Suite
        #
        #This section creates the GUI for the Flashcard Maker

        self.creationSuite = tk.Frame(self.root)
        self.creationSuite.grid(row=0, column=0, sticky="nsew")
        self.creationSuite.columnconfigure(0, weight=1)

        self.inputHolders = tk.Frame(self.creationSuite)
        self.inputHolders.grid(row=0, column=0, pady=5)

        self.questionLbl = tk.Label(self.inputHolders, text="Question:")
        self.questionLbl.grid(row=0, column=0, pady=(0, 5))
        self.questionTxt = tk.Text(self.inputHolders, width=60, height=6) 
        self.questionTxt.grid(row=0, column=1, columnspan=2, pady=(0, 5))

        self.binIcon = tk.PhotoImage(file=r"softwareAssets/binIcon.png")
        self.binIcon = self.binIcon.subsample(30, 30)
        self.deleteCardBtn = tk.Button(self.inputHolders, text="Delete Card", image=self.binIcon, command=lambda: back.creator.deleteCard(self))
        self.deleteCardBtn.grid(row=0, column=3, padx=(30, 5), sticky="n")

        self.answerLbl = tk.Label(self.inputHolders, text="Answer:")
        self.answerLbl.grid(row=2, column=0, pady=5)
        self.answerTxt = tk.Text(self.inputHolders, width=60, height=6)
        self.answerTxt.grid(row=2, column=1, columnspan=2, pady=5)

        self.imageLbl = tk.Label(self.inputHolders, text="Image:")
        self.imageLbl.grid(row=4, column=0, pady=5)
        self.imageFilepreview = tk.Label(self.inputHolders, text="")
        self.imageFilepreview.grid(row=4, column=1, pady=5)
        self.imageBrowseBtn = tk.Button(self.inputHolders, text="Browse", command=lambda: back.creator.browseFiles(self), width=10)
        self.imageBrowseBtn.grid(row=4, column=2, sticky="w", pady=5)

        self.creatorNavHolder = tk.Frame(self.creationSuite)
        self.creatorNavHolder.grid(row=1, column=0, pady=(40, 5))

        self.creatorPreviousBtn = tk.Button(self.creatorNavHolder, text="Previous", command=lambda: back.creator.previous(self), width=10)
        self.creatorPreviousBtn.grid(row=0, column=1, padx=5)

        self.creatorNextBtn = tk.Button(self.creatorNavHolder, text="Next", command=lambda: back.creator.next(self), width=10)
        self.creatorNextBtn.grid(row=0, column=2, padx=5)

        self.creatorExitBtn = tk.Button(self.creatorNavHolder, text="Exit", command=lambda: back.creator.exit(self), width=10)
        self.creatorExitBtn.grid(row=0, column=0, padx=(5, 80))

        self.finishBtn = tk.Button(self.creatorNavHolder, text="Finish", command=lambda: back.creator.finish(self), width=10)
        self.finishBtn.grid(row=0, column=3, padx=(80, 5))

        #
        #Flashcard Properties Screen
        #
        #This section creates the GUI for the flashcard properties screen

        self.cardConfigMenu = tk.Frame(self.root)
        self.cardConfigMenu.grid(row=0, column=0, sticky="nsew")
        self.cardConfigMenu.columnconfigure(0, weight=1)

        #Entry boxes
        self.entryHolder = tk.Frame(self.cardConfigMenu)
        self.entryHolder.grid(row=0, column=0, pady=5)

        self.nameLbl = tk.Label(self.entryHolder, text="Name of Set:")
        self.nameLbl.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        self.nameEnt = tk.Entry(self.entryHolder)
        self.nameEnt.grid(row=0, column=1, sticky="ew", pady=(0, 5))

        self.subjectLbl = tk.Label(self.entryHolder, text="Subject:")
        self.subjectLbl.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        self.subjectEnt = tk.Entry(self.entryHolder, width=40)
        self.subjectEnt.grid(row=1, column=1, sticky="ew", pady=(0, 5))

        #Navigation Buttons
        self.propsNavHolder = tk.Frame(self.cardConfigMenu)
        self.propsNavHolder.grid(row=1, column=0)

        self.backBtnProp = tk.Button(self.propsNavHolder, text="Back", command=lambda: back.back(self), width=10)
        self.backBtnProp.grid(row=0, column=0, padx=(0, 5))

        self.saveBtn = tk.Button(self.propsNavHolder, text="Save", command=lambda: back.cardConfig.save(self), width=10)
        self.saveBtn.grid(row=0, column=1, padx=(5, 0))

        #
        #Flashcard Revision
        #
        #This section creates the GUI for the Revision Suite

        self.revisionFrame = tk.Frame(self.root)
        self.revisionFrame.grid(row=0, column=0, sticky="nsew")
        self.revisionFrame.columnconfigure(0, weight=1)

        self.flashcardHolder = tk.Frame(self.revisionFrame)
        self.flashcardHolder.grid(row=0, column=0)

        self.cardCounterLbl = tk.Label(self.flashcardHolder, text="1/12", width=8)
        self.cardCounterLbl.grid(row=0, column=0, columnspan=2)

        self.flashcardLbl = tk.Label(self.flashcardHolder, text="flashcard")
        self.flashcardLbl.grid(row=1, column=0, columnspan=2)

        self.revisionNavHolder = tk.Frame(self.revisionFrame)
        self.revisionNavHolder.grid(row=1, column=0, columnspan=2)

        self.showAnsBtn = tk.Button(self.revisionNavHolder, text="Show Answer", command=lambda: back.revision.loadAnswer(self), width=20)
        self.showAnsBtn.grid(row=0, column=0, columnspan=2, pady=5, padx=5)

        self.backBtnRev = tk.Button(self.revisionNavHolder, text="Back", command=lambda: back.revision.previousCard(self), width=10)
        self.backBtnRev.grid(row=1, column=0, pady=5, padx=5)

        self.nextBtnRev = tk.Button(self.revisionNavHolder, text="Next", command=lambda: back.revision.nextCard(self), width=10)
        self.nextBtnRev.grid(row=1, column=1, pady=5, padx=5)

        self.exitBtnRev = tk.Button(self.revisionNavHolder, text="Exit", command=lambda: back.revision.exit(self), width=10)
        self.exitBtnRev.grid(row=2, column=0, columnspan=2, pady=5, padx=5)

        #
        #Settings Screen
        #
        #This section creates the GUI for the settings screen

        self.settings = tk.Frame(self.root)
        self.settings.grid(row=0, column=0, sticky="nsew")
        self.settings.columnconfigure(0, weight=1)

        self.colourSchemeHolder = tk.Frame(self.settings)
        self.colourSchemeHolder.grid(row=0, column=0)

        with open("DataStorage/theme.txt", "r") as f: #Gets the current theme from the textfile
            theme = f.readline() 

        self.themeOpts = ["Light", "Dark", "Hello Kitty"]
        self.themeVar = tk.StringVar(self.colourSchemeHolder)
        self.themeVar.set(theme) 
        self.themeDrop = tk.OptionMenu(self.colourSchemeHolder, self.themeVar, *self.themeOpts) 
        self.themeDrop.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.themeDrop.config(width=20)

        self.applyBtn = tk.Button(self.colourSchemeHolder, text="Apply", command=lambda: back.settings.apply(self), width=10)
        self.applyBtn.grid(row=0, column=2)

        self.backBtnSet = tk.Button(self.settings, text="Back", command=lambda: back.back(self), width=10)
        self.backBtnSet.grid(row=1, column=0)

        #
        #Revision Tips Screen
        #
        #This section creates the GUI for the revision tips screen

        self.whyUseCards = " • They help you to ‘recall’ information - \n this creates stronger connections for \n your memory. \n • They promote self-reflection which \n ingrains knowledge into your memory. \n • They help you to memorise facts \n quickly. \n • Drilling - flashcards help you to \n practise the same information over and \n over again \n"
        self.makingCards = " • Make sure the questions are correct on \n the card. \n • Keep the Information as \n short as possible \n • Make sure the questions are relevant. \n (Use commonly asked questions from your \n exam board). \n"
        self.usingCards = " • Complete full sets in one sitting. \n • Use Spaced Repetition (use the \n cards at spaced intervals, for example, \n Day1, 2, 4, 8...) \n • Don't skip cards if you get it right. \n the more repetition, the better!"
        self.tipsBoarderHeight = "\n\n\n\n\n\n\n\n\n\n"

        self.tips = tk.Frame(self.root)
        self.tips.grid(row=0, column=0, sticky="nsew")
        self.tips.columnconfigure(0, weight=1)
        self.tips.columnconfigure(2, weight=1)
        self.tips.columnconfigure(4, weight=1)

        self.tipsTitle = tk.Label(self.tips, text="Revision Tips")
        self.tipsTitle.grid(row=0, column=0, columnspan=5)

        self.usingFlashcardsTitleLbl = tk.Label(self.tips, text="Why use Flashcards?")
        self.usingFlashcardsTitleLbl.grid(row=1, column=0)
        self.usingFlashcardsBodyLbl = tk.Label(self.tips, text=self.whyUseCards, justify=tk.LEFT)
        self.usingFlashcardsBodyLbl.grid(row=2, column=0, sticky="n")

        self.boarder1 = tk.Label(self.tips, text=self.tipsBoarderHeight, relief=tk.SUNKEN, borderwidth=1, bg="black")
        self.boarder1.grid(row=1, column=1, rowspan=2)

        self.makingCardsTitleLbl = tk.Label(self.tips, text="How to make Flashcards:")
        self.makingCardsTitleLbl.grid(row=1, column=2)
        self.makingCardsBodyLbl = tk.Label(self.tips, text=self.makingCards, justify=tk.LEFT)
        self.makingCardsBodyLbl.grid(row=2, column=2, sticky="n")

        self.boarder2 = tk.Label(self.tips, text=self.tipsBoarderHeight, relief=tk.SUNKEN, borderwidth=1, bg="black")
        self.boarder2.grid(row=1, column=3, rowspan=2)

        self.makingCardsTitleLbl = tk.Label(self.tips, text="How to use Flashcards:")
        self.makingCardsTitleLbl.grid(row=1, column=4)
        self.makingCardsBodyLbl = tk.Label(self.tips, text=self.usingCards, justify=tk.LEFT)
        self.makingCardsBodyLbl.grid(row=2, column=4, sticky="n")

        self.tipsExitBtn = tk.Button(self.tips, text="Exit", command= lambda: back.raiseFrame(self.mainMenu), width=10)
        self.tipsExitBtn.grid(row=3, column=2, pady=5)

        #
        #About Screen
        #
        #This section creates the GUI for the about screen

        self.aboutProgram = f" This program was designed to offer a digital solution to paperbased flashcards. \n The program has been created by Kieran Pritchard. \n\n Github Address: {back.backgroundVariables.repoAddress} \n *Click to be redirected*"
        self.abtBoarderHeight = "\n\n\n\n\n\n\n"

        self.about = tk.Frame(self.root)
        self.about.grid(row=0, column=0, sticky="nsew")
        self.about.columnconfigure(0, weight=1)

        self.abtTitle = tk.Label(self.about, text="About")
        self.abtTitle.grid(row=0, column=0)

        self.aboutAssets = tk.Frame(self.about)
        self.aboutAssets.grid(row=1, column=0)

        self.logoabt = tk.PhotoImage(file=r"softwareAssets/progLogo.png")
        self.logoabt = self.logo.subsample(2, 2)
        self.logoabtHolder = tk.Label(self.aboutAssets, image=self.logoabt)
        self.logoabtHolder.grid(row=0, column=0, sticky="w")

        self.softInfo = tk.Label(self.aboutAssets, text=f" Flashcard Creation \n and Examination Suite \n Ver: {back.backgroundVariables.version}")
        self.softInfo.grid(row=1, column=0, sticky="w")

        self.boarder3 = tk.Label(self.aboutAssets, text=self.abtBoarderHeight, relief=tk.SUNKEN, borderwidth=1, bg="black")
        self.boarder3.grid(row=0, column=1, rowspan=2, sticky="w")

        self.abtBody = tk.Label(self.aboutAssets, text=self.aboutProgram)
        self.abtBody.grid(row=0, column=2, rowspan=2, sticky="w")
        self.abtBody.bind("<Button-1>", lambda e: callback(back.backgroundVariables.repoAddress)) #If widet is clicked, redirect to the given URL

        self.abtExitBtn = tk.Button(self.about, text="Exit", command= lambda: back.raiseFrame(self.mainMenu), width=10)
        self.abtExitBtn.grid(row=2, column=0, pady=5)

        back.settings.apply(self)

if __name__ == "__main__":
    instance = ui() #Creates all the GUI
    back.findChildren(instance, None, "font", None) #Applies the font to all widets
    back.splashScrn(instance) #Loads the splash screen
    
    sqlCont.setupTable() #Sets up database
    back.mainMenu.updateTree(instance) #Puts all flashcard sets from database into treeview

    instance.root.mainloop() #Waits for input