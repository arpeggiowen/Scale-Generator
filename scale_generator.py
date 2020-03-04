# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:51:33 2020

@author: Owen
"""
import tkinter as tk
from sys import platform


# full chromatic scale
notes = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
sharps = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
flats = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']

# major scale modes
modes = ['Ionian','Dorian','Phrygian','Lydian','Mixolyidian','Aeolian','Locrian']

def gen_scale(key, mode,accidentals):
    # Generate scale notes based on given key and mode
    # 'key' is a note name, e.g. 'Eb'
    # 'mode' is an integer between 0 (Ionian) and 6 (Locrian)

    # check if user prefers to use sharp accidentals, otherwise default to flats
    if accidentals.lower() in ['sharp','sharps','#','s']:
        notes = sharps

        if len(key) > 2:
            key = key[:2]

    else:
        notes = flats

        if len(key) > 2:
            key = key[3:]


    # major scale step intervals (2 = whole tone, 1 = half tone)
    steps = [2,2,1,2,2,2,1]

    # rotate intervals to match selected mode, then remove last step
    steps = steps[mode:] + steps[:mode]
    steps.pop(-1)
    
    # find position of selected note within chromatic list
    idx = notes.index(key)
    
    # rotate 'notes' list to begin at selected key
    notes_shifted = notes[idx:] + notes[:idx]
    
    # iterate through notes and add to scale
    i = 0
    scale = [notes_shifted[0]]    # initialise scale to be returned with tonic
    for s in steps:
        i += s
        scale.append(notes_shifted[i])
        
    return scale

# function to set same colours for multiple widgets. Argument 'widget_type' must be string.
def widget_colours(widget_name,widget_type):
    # Buttons
    if widget_type.lower() == 'button':
        widget_name.config(bg='SystemButtonHighlight',
                           activebackground='SystemButtonHighlight',
                           fg='SystemButtonText',
                           highlightbackground='SystemButtonHighlight')
    # OptionMenus
    elif widget_type.lower() == 'optionmenu':
        widget_name.config(bg='SystemWindow',
                           fg='SystemMenuText',
                           activebackground='SystemButtonHighlight',
                           relief='ridge',
                           highlightbackground='SystemButtonHighlight')
        widget_name["menu"].config(bg='SystemWindow')
    # Labels
    elif widget_type.lower() == 'label':
        widget_name.config(bg='SystemWindow')
    # Radiobuttons
    elif widget_type.lower() == 'radiobutton':
        widget_name.config(bg='SystemWindow')

#-----------------------Interface-----------------------#

class Window(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()
        
    # create main window
    def init_window(self):
        
        self.master.title("Scale Tool")
        
        self.pack(fill=tk.BOTH, expand=1)

        # set colours to system defaults
        self.configure(bg="SystemWindow")

        # set accidentals to display
        acc = tk.StringVar()
        acc.set('#')
        
        # set notes display variable
        keyVar = tk.StringVar()
        keyVar.set('C')
        
        # add notes menu
        keys = tk.OptionMenu(self,keyVar,*notes)
        keys.config(width=len(max(notes,key=len)))
        widget_colours(keys,'optionmenu')
        keys.grid(row=1,column=0,padx=2,sticky='ew')
        
        # add modes variable
        modeVar = tk.StringVar()
        modeVar.set(modes[0])
        
        # add modes menu
        mode = tk.OptionMenu(self,modeVar,*modes)
        mode.config(width=len(max(modes,key=len)))
        widget_colours(mode,'OptionMenu')
        mode.grid(row=1,column=3,padx=2,pady=2,sticky='ew')
        
        # add button to generate scale
        scaleGen = tk.Button(self, text="Generate scale",
                             command= lambda : self.tk_gen_scale(keyVar.get(),modes.index(modeVar.get()),acc.get()))
        widget_colours(scaleGen,'button')
        scaleGen.grid(row=3,column=1,rowspan=2,columnspan=2,pady=2)
        
        self.scale_notes = tk.StringVar()
        self.scale_notes.set(gen_scale('C',0,acc.get()))
        
        disp_notes = tk.Label(self,textvariable=self.scale_notes,width=sum(len(i) for i in notes))
        widget_colours(disp_notes,'label')
        disp_notes.grid(row=5,column=1,rowspan=2,columnspan=2)

        # Radio buttons to select type of accidentals displayed
        sharpsRad = tk.Radiobutton(self, variable=acc,text='#',value='#')
        widget_colours(sharpsRad,'radiobutton')
        sharpsRad.grid(row=8,column=1,rowspan=2,columnspan=2)

        flatsRad = tk.Radiobutton(self,variable=acc,text='b',value='b')
        widget_colours(flatsRad, 'radiobutton')
        flatsRad.grid(row=10,column=1,rowspan=2,columnspan=2)
        
        # add quit button
        quitButton = tk.Button(self, text="Quit", command=self.app_exit)
        widget_colours(quitButton,'button')
        quitButton.grid(row=14,column=1,columnspan=2)

    def tk_gen_scale(self,key,mode,accidentals):
        scale = gen_scale(key,mode,accidentals)
        self.scale_notes.set(scale)
    
    # quit command
    def app_exit(self):
        self.master.destroy()
        
root = tk.Tk()

root.geometry("450x200")
#root.resizable(0,0)

app = Window(root)

root.mainloop()
