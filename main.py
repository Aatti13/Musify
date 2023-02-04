# Imports

from tkinter import *

import requests as requests
from PIL import Image, ImageTk
from pytube import YouTube
from datetime import date
from pathlib import Path
from tkinter import messagebox
import os


# Initialising Class Music Window

class MusicWindow:
    def __init__(self, window):
        """
        :param window:
        1. self.root --> window init
        2. self.bg --> background colour --> :type: <str>
        3. self.font --> Font init --> :type: <str>
        4. self.button_flag = Button Pressed checker --> :type: <bool>
        """
        self.root = window
        self.bg = "#252429"  # Background colour
        self.font = "Leelawadee UI Semilight"  # Font Initialisation
        self.button_flag = True  # Button Pressed Checker
        # --------------------------------------------------------------------------------------------------------------
        # Config
        self.root.config(bg=self.bg)  # Configure bg colour
        # --------------------------------------------------------------------------------------------------------------
        # Functions

        def search():
            """
            :parameter Search
            p --> To access YouTube info --:type <pytube.Stream.streams>
            th --> to get thumbnail data --:type hyperlink: <str>
            rr --> To request info (Query) --:type Query <requests.Response>
            p_at --> Date to isoformat()  --:type <str>
            cc --> converts p_at into a list (splitting at '-')  :type <list>
            published_at --> Release Date :type <date>

            Exceptions
            1. :exception pytube.Error
            2. :exception HTTPNotFOUNError
            3. :exception TypeError

            :returns: [self.thumbnail_label, self.song_title_label, self.song_info_label, self.artist_label,
                        published_at, file_size, self.download_now_label, self.download_button]

            """

            try:
                link = self.text_box.get()  # To get link

                p = YouTube(link)
                th = p.thumbnail_url  # Thumbnail

                rr = requests.get(th)  # Getting thumbnail in accessible format

                with open("Images/thumbnail.png", "wb") as f:  # inserting into png file
                    f.write(rr.content)

                self.thumbnail_img = Image.open("Images/thumbnail.png")
                self.thumbnail_img = self.thumbnail_img.resize((480, 360), Image.Resampling.LANCZOS)
                self.thumbnail_img = ImageTk.PhotoImage(self.thumbnail_img)

                p_at = date.isoformat(p.publish_date)  # Converting date from :type <date> to :type <str>
                cc = p_at.split("-")  # converting date from :type <str> to type: <list>
                published_at = "-".join(cc[::-1])
                size = p.streams.get_by_itag(251)

                dd = size

                file_size = dd.filesize_mb  # Getting File Size

                if 1 <= file_size < 1000:
                    file_size = f"{int(dd.filesize_mb)} MB"  # Shows File size in Megabytes
                elif file_size >= 1000:
                    file_size = f"{int(dd.filesize_gb)} GB"  # Shows File size in Gigabytes
                else:
                    file_size = f"{int(dd.filesize_kb)} KB"  # Shows File size in Kilobytes

                self.thumbnail_label.config(image=self.thumbnail_img)  # Change config: Thumbnail

                # Changing config of song title, info & Uploader/Artist
                self.song_title_label.config(text=p.title)
                self.song_info_label.config(text=f"{p.views} views | Released: {published_at} | Size: {file_size}")
                self.artist_label.config(text=p.author)

                # Show Download Label & Download Button
                self.download_button.config(image=self.download_button_img)
                self.download_button.place(x=833, y=637)
                self.download_now_label.config(text="Download Song:")

            except Exception as e:
                messagebox.showerror("Musify", f"STATUS: {e}")  # Display Error Message


        def download():

            """
            :parameter download (0 parameters)

            1. link --> To get YouTubeLink :type <str>
            2. audio --> to Get Stream for audio via itag :type <pytube.Stream.streams>
            3. downloads_path --> Get Path to Music Folder :type <str>
            4. dir_file_path --> To Create an additional folder 'Downloaded' :type <str>
            5. Download...

            Exceptions
            :exception FileNotFoundError
            :exception HTTPException
            :exception StreamNotFoundError

            :returns: 'STATUS : COMPLETE'
            """
            if self.button_flag is True:
                self.button_flag = False
                link = self.text_box.get()  # To get link
                p = YouTube(link)
                audio = p.streams.get_by_itag(251)  # Searching for Stream by itag
                first_download = audio
                downloads_path = str(Path.home() / "Downloads")  # Getting path to Music Folder of Device
                dir_file_path = fr"{downloads_path}\Music Downloaded"  # Create file path for download
                file_name = first_download.download(dir_file_path)  # To download the YouTube Audio
                new_name = os.path.split(file_name)  # Splitting filename :type: <list>
                ff = os.path.splitext(file_name)  # Splitting filename :type: <list>
                r = ff[0].split("\\")
                os.rename(file_name, fr"{new_name[0]}\{r[-1]}" + '.mp3')  # Converting to .mp3

                self.download_button.place(x=4000, y=2000)  # Remove Button from Screen
                self.download_now_label.config(text="STATUS: COMPLETE")  # Changes Label Configuration after Download is Complete

                self.button_flag = True
            else:
                messagebox.showerror("Musify", "STATUS: ERROR")  # To show Errors

        # --------------------------------------------------------------------------------------------------------------
        # Images

        """
        *Main Images*
        1. :img self.top_img --> Top right Blue ridge
        2. :img self.logo_img --> Logo Image
        3. :img self.search_bar_img --> Search Bar (Image)
        4. :img self.search_button_img --> Search button (Image)
        5. :img self.download_button_img --> Download button (Image)
        6. :img self.musical_note_img --> The Theme Musical Note Credits (At the Top (GitHub))
        
        *Some Important Keywords*
        -  Image.Resampling.LANCZOS --> To Resize the images based of Pixels
        -  ImageTk.PhotoImage() --> To Convert into Readable format for tkinter window
        
        *Folder Name* 
        Images
        
        *Images*
        1. download image.png
        2. logo.png
        3. musical note.jpg
        4. searchbutton.png
        5. search ber.png
        6. top_label.png
        
        """

        self.top_img = Image.open("Images/top_label.png")
        self.top_img = self.top_img.resize((1080, 280), Image.Resampling.LANCZOS)
        self.top_img = ImageTk.PhotoImage(self.top_img)

        self.logo_img = Image.open("Images/logo.png")
        self.logo_img = self.logo_img.resize((100, 100), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img)

        self.search_bar_img = Image.open("Images/search bar.png")
        self.search_bar_img = self.search_bar_img.resize((383, 60), Image.Resampling.LANCZOS)
        self.search_bar_img = ImageTk.PhotoImage(self.search_bar_img)

        self.search_button_img = Image.open("Images/searchbutton.png")
        self.search_button_img = self.search_button_img.resize((45, 45), Image.Resampling.LANCZOS)
        self.search_button_img = ImageTk.PhotoImage(self.search_button_img)

        self.download_button_img = Image.open("Images/download image.png")
        self.download_button_img = self.download_button_img.resize((60, 60), Image.Resampling.LANCZOS)
        self.download_button_img = ImageTk.PhotoImage(self.download_button_img)

        self.musical_note_img = Image.open("Images/musical note.jpg")
        self.musical_note_img = self.musical_note_img.resize((112, 288), Image.Resampling.LANCZOS)
        self.musical_note_img = ImageTk.PhotoImage(self.musical_note_img)

        # --------------------------------------------------------------------------------------------------------------
        # Labels

        """
        **Labels**
        1. :var top_label --> Top Blue Ridge Label
        2. :var logo_label --> To Display Logo
        3. :var logo_text --> To display Musify
        4. :var search_bar_label --> To Display Searchbar
        5. :var thumbnail_label --> To display Thumbnail of Song (Activated After pressing search button)
        6. :var song_title_label --> To Display Song Title
        7. :var song_info_label --> To Show Additional Info --> [views, Release Date, File Size]
        8. :var artist_label --> To display Artist/Uploader
        9. :var download_now_label --> To Show 'Download Now' next to the Download Button
        10. :var musical_note_label --> To display Theme musical note
        
        *NOTE*
        Labels (5-9): Initialised/config changed after pressing search button
         
         *Exception(s)*
         :exception FileNotFoundError
         :exception DirectoryNotFoundError
         :exception HTTPSError
         
        """

        self.top_label = Label(self.root, image=self.top_img, bg=self.bg)
        self.top_label.place(x=-100, y=-200)

        self.logo_label = Label(self.root, image=self.logo_img, bg=self.bg)
        self.logo_label.place(x=40, y=10)

        self.logo_text = Label(self.root, text="Musify", font=(self.font, 20), bg=self.bg, fg="#00a8f3")
        self.logo_text.place(x=55, y=111)

        self.search_bar_label = Label(self.root, image=self.search_bar_img, bd=0, bg=self.bg)
        self.search_bar_label.place(x=543, y=100)

        self.thumbnail_label = Label(self.root, bd=0, bg=self.bg)
        self.thumbnail_label.place(x=60, y=240-30)

        self.song_title_label = Label(self.root, font=(self.font, 12, "bold"), bd=0, bg=self.bg, fg="white")
        self.song_title_label.place(x=60, y=610-30)

        self.song_info_label = Label(self.root, font=(self.font, 10), bd=0, bg=self.bg, fg="white")
        self.song_info_label.place(x=60, y=642-20)

        self.artist_label = Label(self.root, font=(self.font, 14), bg=self.bg, fg="blue")
        self.artist_label.place(x=60, y=667-20)

        self.download_now_label = Label(self.root, font=(self.font, 18), bd=0, bg=self.bg, fg="white")
        self.download_now_label.place(x=653, y=647)

        self.musical_note = Label(self.root, image=self.musical_note_img, bg=self.bg, bd=0)
        self.musical_note.place(x=690, y=240)

        # --------------------------------------------------------------------------------------------------------------
        # Buttons
        """
        *Buttons*
        1. search_button --> To Search entered Link 
        2. download_button --> To Download the Music
        
        *Exceptions*
        :exception HTTPSError
        :exception pytube.cli.Error
        :exception tkinter.ttk._tclError
        
        """

        self.search_button = Button(self.root, image=self.search_button_img, command=search, bd=0, bg="white")
        self.search_button.place(x=861, y=107)

        self.download_button = Button(self.root, bd=0, bg=self.bg, command=download)

        # --------------------------------------------------------------------------------------------------------------
        # Text Entry
        """
        *Text Box*
        :var text_box --> To enter your YouTube link --> :type <str>
        
        *Exceptions*
        :exception HTTPSError
        :exception FileNotFoundError
        :exception EmptyArgumentError
        :exception NilSearchResultError
        :exception tkinter.ttk,_tclError
        """
        self.text_box = Entry(self.root, font=(self.font, 16), width=19, bd=0, bg="white")
        self.text_box.place(x=640, y=114)



if __name__ == "__main__":
    window = Tk()  # Initialising Tkinter Window
    window.geometry("980x720")  # Defining Geometry
    window.title("Music-Made-Easy")  # MusicWindow Title
    window.iconbitmap("Images/logo.ico")  # App Icon
    window.resizable(False, False)
    x = MusicWindow(window)
    window.mainloop()

