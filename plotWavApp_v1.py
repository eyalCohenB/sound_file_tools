'''
This script creates a tkinter app to analyse all channels of a '*.wav' file.
Written By: Eyal Cohen
'''
import matplotlib.pyplot as plt
from scipy.io import wavfile
import tkinter as tk
from tkinter import filedialog
import warnings
warnings.filterwarnings('ignore')

# Global vars
selected_file = None

def specgramView(fig, sampRate, dataToView, num, channel_cnt):
    ax = fig.add_subplot(channel_cnt, 2, num * 2 - 1)  # Specgram on the left
    if num ==1 :
        ax.set_title( "Specgram", pad = 8)
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("ch" + str(num))
    ax.specgram(dataToView, Fs=sampRate)

def plotView(fig, dataToView, num, channel_cnt):
    ax = fig.add_subplot(channel_cnt, 2, num * 2)  # Plot on the right
    if num ==1 :
        ax.set_title("Plot", pad = 8)
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("ch" + str(num))
    ax.plot(dataToView)

def viewData(data):
    plot_flag = 0
    try:
        # print(len(data[1][0]), "channels on this .wav file")
        if len(data[1][0]):
            fig = plt.figure(figsize=(15, 8))
            plt.subplots_adjust(wspace=0.4, hspace=0.4)
        for i in range(len(data[1][0])):
            plot_flag = 1
            specgramView(fig, data[0], data[1][:, i],  i + 1, len(data[1][0]))
            plotView(fig, data[1][:, i], i + 1, len(data[1][0]))
    except:
        plot_flag = 1
        # print("1 channel on this .wav file")
        fig = plt.figure(figsize=(15, 4))
        specgramView(fig, data[0], data[1], 1, 1)
        plotView(fig, data[1], 1, 1)
    finally:
        if plot_flag == 1:
            plt.show()
        pass
    
def UploadBtnAction(selected_file_label,event = None):
    global selected_file
    selected_file = filedialog.askopenfilename()
    selected_file_name = selected_file.split("/")[len(selected_file.split("/")) - 1]
    selected_file_label.config(text = "Selected:    " + str(selected_file_name))
    # print('Selected File Path: ', selected_file)

def ViewBtnAction(event=None):
    global selected_file
    data = wavfile.read(selected_file)
    viewData(data)

def createAndRunApp():
    global selected_file

    # Main app
    root = tk.Tk()
    root.title('Sound Viewer ANL')
    root.geometry("400x200")

    # explenation label
    exp_label = tk.Label(master= root , text="Choose a file using the 'Upload' button \n Then click 'View Data'" ,font='Consolas 12' )
    exp_label.place(x = 5 , y = 5 )

    # Logo png
    # logo = tk.PhotoImage(file = "./anlLogo.png")
    # logo_label = tk.Label(master = root , image = logo)
    # logo_label.place(x = 70 , y = 0)

    # quit button
    quit_button = tk.Button(master = root , text = 'Quit' , width = 10 , font='Consolas 12', command = root.destroy)
    quit_button.place(x = 5 , y = 162 )

    # Selected file name lable
    selected_file_label = tk.Label(master = root, text= '' )
    selected_file_label.place(x =20 , y = 100 )

    # upload button
    upload_button = tk.Button(master = root, text='Upload', command= lambda : UploadBtnAction(selected_file_label))
    upload_button.place(x = 5 , y = 50 )
    
    # view data  button
    view_button = tk.Button(master = root , text = 'View Data' , command= ViewBtnAction)
    view_button.place( x = 300, y = 100 )

    # Creator label
    creator_label = tk.Label(master = root , text = 'Created by: Eyal Cohen')
    creator_label.place(x = 260 , y = 177)

    # pack widgets
    # exp_label.pack()
    # quit_button.pack()
    
    # Run app
    root.mainloop()

def main():
    createAndRunApp()
    
if __name__ == "__main__":
    main()
