# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 16:51:33 2020

@author: Owen
"""
import tkinter as tk


# full chromatic scale
notes = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
modes = ['Ionian','Dorian','Phrygian','Lydian','Mixolyidian','Aeolian','Locrian']

def gen_scale(key, mode):
    # Generate scale notes based on given key and mode
    # 'key' is a note name, e.g. 'Eb'
    # 'mode' is an integer between 0 (Ionian) and 6 (Locrian)
    
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

#print(gen_scale('D#/Eb',3))

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
        
        # set notes display variable
        keyVar = tk.StringVar()
        keyVar.set(notes[0])
        
        # add notes menu
        keys = tk.OptionMenu(self,keyVar,*notes)
        keys.config(width=len(max(notes,key=len)))
        keys.grid(row=1,column=0,padx=2,sticky='ew')
        
        # add modes variable
        modeVar = tk.StringVar()
        modeVar.set(modes[0])
        
        # add modes menu
        mode = tk.OptionMenu(self,modeVar,*modes)
        mode.config(width=len(max(modes,key=len)))
        mode.grid(row=1,column=3,padx=2,pady=2,sticky='ew')
        
        # add button to generate scale
        scaleGen = tk.Button(self, text="Generate scale", 
                             command= lambda : self.tk_gen_scale(keyVar.get(),modes.index(modeVar.get())))
        scaleGen.grid(row=3,column=1,rowspan=2,columnspan=2,pady=2)
        
        self.scale_notes = tk.StringVar()
        self.scale_notes.set(gen_scale('C',0))
        
        disp_notes = tk.Label(self,textvariable=self.scale_notes,width=sum(len(i) for i in notes))
        disp_notes.grid(row=5,column=1,rowspan=2,columnspan=2)
        
        # add quit button
        quitButton = tk.Button(self, text="Quit", command=self.app_exit)
        quitButton.grid(row=7,column=1)
        
    def tk_gen_scale(self,key,mode):
        scale = gen_scale(key,mode)
        self.scale_notes.set(scale)
    
    # quit command
    def app_exit(self):
        self.master.destroy()
        
root = tk.Tk()

root.geometry("450x200")
#root.resizable(0,0)

app = Window(root)

root.mainloop()