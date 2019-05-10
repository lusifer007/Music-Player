import os
from tkinter import*
from pygame import mixer
import tkinter.messagebox as tmsg
from tkinter import filedialog
from pygame import *
import threading
from tinytag import TinyTag
from mutagen.mp3 import MP3
import time
import webbrowser


root = Tk()
mixer.init() #intializing pygame mixer

# getting screen's height in pixels
height = root.winfo_screenheight()
height = height - 100
# getting screen's width in pixels
width = root.winfo_screenwidth()
width = width
#set Screen according to width and height
root.geometry(f"{width}x{height}")
root.wm_iconbitmap("icon.ico")
root.title("XYZ Music Player")
#functions

playlist = []
# def byt_image_converter(f):
#     tag = TinyTag.get(f.name, image=True)
#     image_data = tag.get_image()
#     print(image_data)
#     with open("x.jpg","w") as f:
#         f.write(image_data)
#     f.close()
    # fh = open("x.png", "wb")
    # fh.write(str.decode('base64'))
    # fh.close()


def file_browser():
    global filename
    filename = filedialog.askopenfile()
    add_toplaylist(filename)
def stop_music():
    mixer.music.stop()
def play():
    global paused
    if paused:
        mixer.music.unpause()
        paused = FALSE
        #missing
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlist_content.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            tag = TinyTag.get(play_it.name)
            title['text']= "Title : "+tag.title
            album['text'] =" Album : "+tag.album
            artist['text'] ="Artist : "+tag.artist
            year['text'] = "year : "+tag.year
            composer['text'] = "Composer : "+tag.composer
            genre['text'] = "Genre : "+tag.genre
            show_details()
            # byt_image_converter(play_it)
            #statusbar2['text'] = "Playing Music "+ " "+os.path.basename(filename.name)
        except:
            tmsg.showinfo("Error","There are some problem importing Sound Clip")

        #statusbar2['text'] = "Music Resumed"
def show_details():
    audio = MP3(filename.name)
    global total_length
    total_length = audio.info.length
    mins, secs = divmod(total_length,60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    Total_duration['text'] ="Total Duration : "+timeformat

    t1 = threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    x = 0
    while x<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(x,60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins,secs)
            current_duration['text'] ="Current Duration : "+timeformat
            percentage = (x/t)*100
            song_status_bar.set(int(percentage))
            time.sleep(1)
            x += 1

paused = FALSE
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    #statusbar2['text'] = "Stopped"
def add_toplaylist(f):
    index = 0
    x = os.path.basename(f.name)
    playlist_content.insert(index,x)
    playlist.insert(index,filename)
    index+=1
def del_song():
    selected_song = playlist_content.curselection()
    selected_song = int(selected_song[0])
    playlist_content.delete(selected_song)
    playlist.pop(selected_song)
def restart_music():
    mixer.music.load(filename.name)
    mixer.music.play()
def exit():
    root.destroy()
def mute_music():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        volume_btn.configure(image=music_Photo)
        volume_btn.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        volume_btn.configure(image=volume_photo)
        volume_btn.set(0)
        muted = TRUE
def volume_change(event):
    v = int(event)/1000
    mixer.music.set_volume(v)
    # x = int(event)
    # print(x)
    # if x == 0:
    #     speaker1 = PhotoImage(file="icon/speaker1.png")
    #     volume_btn.configure(image=speaker1)
    # elif x >=1 and x <= 60:
    #     speaker2 = PhotoImage(file="icon/speaker2.png")
    #     volume_btn.configure(image=speaker2)
    # elif x>=61 and x<=100:
    #     speaker3 = PhotoImage(file="icon/speaker3.png")
    #     volume_btn.configure(image=speaker3)
    # else:
    #     volume_photo = PhotoImage(file="icon/speaker.png")
    #     volume_btn.configure(image=volume_photo)
def save_project():
    with open('data_file.txt', 'w') as filehandle:
        for listitem in playlist:
            filehandle.write('%s\n' % listitem)
    tmsg.showinfo("Check in the root folder for all data")
def load_project():
    tmsg.showinfo("We are very sorrry","This function is not Developed properly , follow the source code .you can contribute to the project")
    # places = []
    # with open('data_file.txt', 'r') as filehandle:
    #     for line in filehandle:
    #         # remove linebreak which is the last character of the string
    #         currentPlace = line[:-1]
    #         places.append(currentPlace)
    # length = len(places)
    # print(places[0])
    # a = os.path.split(places[0])
    # print(a['name'])
    # for i in range(0,length):
    #     index = 0
    #     x = os.path.basename(places[i])
    #     playlist_content.insert(index,x)
    #     playlist.insert(index,filename)
    #     index+=1
def help():
    webbrowser.open('https://github.com/lusifer007/Music-Player')
def credit():
    webbrowser.open('https://www.facebook.com/milan.hembram.31')
    webbrowser.open('https://www.facebook.com/abhimanyu.das3')
    webbrowser.open('https://www.facebook.com/mrinal.pahan.9')
    webbrowser.open('https://www.facebook.com/waseemuddin.wani.3')
    webbrowser.open('https://www.facebook.com/UstadExpo/photos/a.2155736404503329/2351314314945536/?type=3&theater')
def p():
    pass
#main menu
topmenu = Menu(root)
m1 = Menu(topmenu)
m1.add_command(label="Open File",command=file_browser)
m1.add_command(label="Save",command=save_project)
m1.add_command(label="Load Project",command=load_project)
m1.add_cascade(label="Exit",command=exit)
topmenu.add_cascade(label="File",menu=m1)
m3 = Menu(topmenu)
m3.add_command(label="Developers",command=credit)
topmenu.add_cascade(label="About US",menu=m3)
m2 = Menu(topmenu)
m2.add_command(label="Help",command=help)
topmenu.add_cascade(label="Get Help",menu=m2)
root.config(menu=topmenu)
#Last Status Bar
status_end = Label(root,text="MilanExpo Copyright",bg="#ed662c",fg="white")
status_end.pack(fill=X,side=BOTTOM)
#Frame 1
f1_width = width *0.03
f1_width = int(f1_width)
l_height = height * 0.05
l_height = int(l_height)
f1 = Frame(root,bg="#42f4e8",width=f1_width)
l1 = Label(f1,text="Playlist",font="Arial 25",bg="black",fg="white")
l1.pack(fill=X)
playlist_content = Listbox(f1,height=l_height,width=f1_width,bg="#d62675",fg="white")
playlist_content.pack()
add_btn = Button(f1,text="+Add",command=file_browser)
add_btn.pack(side=LEFT)
remove_btn = Button(f1,text="-Remove",command=del_song)
remove_btn.pack(side=LEFT)
f1.pack(side=LEFT,fill=Y)


#Frame 2
f2 = Frame(root,bg="black")
song_name = Label(f2,text="Beta Version 1.0",height=2,font="airstrike 20 bold",bg="black",fg="white")
song_name.pack()
f2.pack(side=TOP,fill=X)

#frame 3
f3 = Frame(root,bg="white")
song_status_bar = Scale(f3,from_=0,to=100,orient=HORIZONTAL,command=file_browser,
                          length=600,bg="#28d626",fg="white",highlightbackground="white",)
song_status_bar.pack(side=BOTTOM,)
sample_photo = PhotoImage(file="sample.png")
l_test = Label(f3,image=sample_photo,bg="#41c7f4")
l_test.pack()
# previous_photo = PhotoImage(file="icon/previous.png")
# previous_btn = Button(f3,image=previous_photo,command=file_browser,fg="white",bg="white",justify=LEFT)
# previous_btn.pack(side=LEFT,anchor=S)
playphoto = PhotoImage(file="icon/play.png")
playbtn = Button(f3,image=playphoto,command=play,fg="white",bg="white")
playbtn.pack(side=LEFT,anchor=S)
pausephoto = PhotoImage(file="icon/pause.png")
pausebtn = Button(f3,image=pausephoto,command=pause_music,fg="white",bg="white")
pausebtn.pack(side=LEFT,anchor=S)
# next_photo = PhotoImage(file="icon/next.png")
# next_btn = Button(f3,image=next_photo,command=file_browser,fg="white",bg="white")
# next_btn.pack(side=LEFT,anchor=S)
replay_photo = PhotoImage(file="icon/restart.png")
replay_btn = Button(f3,image=replay_photo,command=restart_music,fg="white",bg="white")
replay_btn.pack(side=LEFT,anchor=S)
volume_photo = PhotoImage(file="icon/stop.png")
volume_btn = Button(f3,image=volume_photo,command=stop_music,fg="white",bg="white")
volume_btn.pack(side=LEFT,anchor=S)
music_photo = PhotoImage(file="icon/speaker3.png")

current_duration = Label(f3,text="Current Duration 00:00")
current_duration.pack(side=BOTTOM,anchor=SW)
Total_duration = Label(f3,text="Total Duration 00:00")
Total_duration.pack(side=BOTTOM,anchor=SW)

music_volume = Scale(f3,from_=0,to=100,command=volume_change)
music_volume.set(50)
mixer.music.set_volume(50/1000)
music_volume.pack(side=RIGHT)


f3.pack(side=LEFT,fill=Y)

#frame 4
f4 = Frame(root,bg="#42f4e8",width=500)
all_details = Label(f4,text="Songs Details",bg="#ed662c",fg="white",width=100)
all_details.pack(side=TOP,fill=X)
title = Label(f4,text="Title :",font="Courier 11",bg="#42f4e8")
title.pack(side=TOP)
album = Label(f4,text="Ablum :",font="Courier 11",bg="#42f4e8")
album.pack(side=TOP)
artist = Label(f4,text="Artist :",font="Courier 11",bg="#42f4e8")
artist.pack(side=TOP)
year = Label(f4,text="Year : ",font="Courier 11",bg="#42f4e8")
year.pack(side=TOP)
composer = Label(f4,text="Composer : ",font="Courier 11",bg="#42f4e8")
composer.pack(side=TOP)
genre = Label(f4,text="Genre : ",font="Courier 11",bg="#42f4e8")
genre.pack(side=TOP)
f4.pack(side=LEFT,fill=BOTH,)
def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
