from curses.ascii import DEL
from itunes_artwork_finder import search_artwork
import json
import requests
from PIL import Image
from io import BytesIO
import music_tag
from tkinter import Tk, filedialog
import os
import tkinter as tk
from tkinter import ttk

def search_album_artwork(album_name, artist_name=None, hi_res=False):
    results = search_artwork(query=(album_name + " " + (artist_name if artist_name else "")), entity="album", limit=1)
    if results:
        first = results[0]
        print("="*60)
        print(f"🎵 Album Found: {first['title']}")
        print(f"  Artist: {first.get('artist', 'Unknown')}")
        print(f"  Artwork URL: {first.get('uncompressed', first['url'])}")
        print("="*60)
        if hi_res:
            url = first.get('uncompressed', first['url'])
        else:
            url = first['url']
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    else:
        print("No results found.")
        print("="*60)

def find_music_files(folder):
    music_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(('.mp3', '.flac', '.m4a', '.wav')):
                music_files.append(os.path.join(root, file))
    return music_files

DELETE_ALBUM_ART_JPGS = False  # Set to True to delete all existing album art
HI_RES = False  # Set to True to search for high-resolution album art

folder_selected = None
while not folder_selected:
    def start_processing():
        global DELETE_ALBUM_ART_JPGS, HI_RES, folder_selected
        DELETE_ALBUM_ART_JPGS = delete_var.get()
        HI_RES = hires_var.get()
        folder_selected = folder_var.get()
        root.destroy()

    root = Tk()
    root.title("iTunes Artwork Finder")

    mainframe = ttk.Frame(root, padding="10")
    mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    folder_var = tk.StringVar()
    delete_var = tk.BooleanVar(value=False)
    hires_var = tk.BooleanVar(value=False)

    def select_folder():
        folder = filedialog.askdirectory(title="Select Folder Containing Music Files")
        if folder:
            folder_var.set(folder)

    ttk.Label(mainframe, text="Music Folder:").grid(row=0, column=0, sticky=tk.W)
    ttk.Entry(mainframe, textvariable=folder_var, width=40).grid(row=0, column=1, sticky=(tk.W, tk.E))
    ttk.Button(mainframe, text="Browse...", command=select_folder).grid(row=0, column=2, sticky=tk.W)

    ttk.Checkbutton(mainframe, text="Delete existing albumart.jpg", variable=delete_var).grid(row=1, column=0, columnspan=3, sticky=tk.W)
    ttk.Checkbutton(mainframe, text="Search for high-res artwork", variable=hires_var).grid(row=2, column=0, columnspan=3, sticky=tk.W)

    ttk.Button(mainframe, text="Start", command=start_processing).grid(row=3, column=0, columnspan=3, pady=10)

    root.mainloop()

if DELETE_ALBUM_ART_JPGS:
    for root, dirs, files in os.walk(folder_selected):
        for file in files:
            if file.lower() == 'albumart.jpg':
                os.remove(os.path.join(root, file))
                print(f"Deleted: {os.path.join(root, file)}")

for file in find_music_files(folder_selected):
    print("\n" + "-"*60)
    print(f"🎶 File: {file}")
    try:
        tags = music_tag.load_file(file)
        albumname = str(tags['album'])
        artist = str(tags['artist'])
        print(f"   Album: {albumname}")
        print(f"   Artist: {tags.get('artist', 'Unknown')}")
    except Exception as e:
        print(f"   ⚠️ Error reading tags: {e}")
        albumname = None

    albumart_path = os.path.join(os.path.dirname(file), 'albumart.jpg')
    if os.path.exists(albumart_path):
        print(f"   ✅ Found album art at: {albumart_path}")
    else:
        print(f"   ❌ No album art found. Searching online...")
        if albumname:
            img = search_album_artwork(albumname, artist)
            if img:
                img.save(albumart_path)
                print(f"   💾 Saved album art at: {albumart_path}")
            else:
                print(f"   ⚠️ Could not find album art online.")
                if 'missing_albums' not in locals(): missing_albums = []
                missing_albums.append(f"{albumname} - {artist}")
        else:
            print(f"   ⚠️ Skipping search due to missing album name.")

    try:
        if os.path.exists(albumart_path):
            with open(albumart_path, 'rb') as img_in:
                tags['artwork'] = img_in.read()
                tags.save()
                print(f"   🖼️ Embedded album art into file.")
    except Exception as e:
        print(f"   ⚠️ Error embedding album art: {e}")
    print("-"*60)
    
    if 'missing_albums' in locals():
        print("\n" + "="*60)
        print("❗ The following albums were not found online:")
        for album in missing_albums:
            print(f"   - {album}")
        print("="*60)
        
    
    
