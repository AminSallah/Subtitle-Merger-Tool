import sys
import tkinter as tk
from tkinter import filedialog
import os
import re
import aeidon
from tkinter import ttk, messagebox
import tkinter.font as tkfont


############################################
class Ass2srt:
    def __init__(self, filename):
        self.filename = filename
        self.load()

    def output_name(self, tag=None):
        outputfile = self.filename[0:-4]
        if tag:
            outputfile = outputfile+"."+tag
        return outputfile+".srt"

    def load(self, filename=None):
        if filename is None:
            filename = self.filename
        try:
            with open(file=filename, mode="r", encoding="utf-8") as f:
                data = f.readlines()
        except UnicodeDecodeError:
            with open(file=filename, mode="r", encoding="windows-1256") as f:
                data = f.readlines()

        self.nodes = []
        for line in data:
            if line.startswith("Dialogue"):
                line = line.lstrip("Dialogue:")
                node = line.split(",")
                node[1] = timefmt(node[1])
                node[2] = timefmt(node[2])
                node[9] = re.sub(r'{.*}', "", node[9]).strip()
                node[9] = re.sub(r'\\N', "\n", node[9])
                self.nodes.append(node)
                # print(f"{node[1]}-->{node[2]}:{node[9]}\n")

    def to_srt(self,console_text, name=None, line=0, tag=None,):
        if name is None:
            name = self.output_name(tag=tag)
        with open(file=name, mode="w", encoding="utf-8") as f:
            index = 1
            for node in self.nodes:
                f.writelines(f"{index}\n")
                f.writelines(f"0{node[1]} --> 0{node[2]}\n")
                if line == 1:
                    text = node[9].split("\n")[0]
                elif line == 2:
                    tmp = node[9].split("\n")
                    if len(tmp) > 1:
                        text = tmp[1]
                else:
                    text = node[9]
                f.writelines(f"{text}\n\n")
                index += 1
            print_to_console(console_text,f"Converting -->{name}")

    def __str__(self):
        return f"文件名:{self.filename}\n合计{len(self.nodes)}条字幕\n"


def timefmt(strt):
    strt = strt.replace(".", ",")
    return f"{strt}0"


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help=".ass file to convert")
    parser.add_argument("-s", "--suffix", default="zh", choices=["zh", "en", "fr", "de"],
                        help="add suffix to subtitles name")
    parser.add_argument("-l", "--line", type=int,
                        choices=[0, 1, 2], default=0, help="keep double subtitles")
    parser.add_argument("-i", "--info", action="store_true",
                        help="display subtitles infomation")
    parser.add_argument("-o", "--out", help="output file name")

    args = parser.parse_args()

    if args.file is None:
        parser.print_help()

    app = Ass2srt(args.file)
    if args.info:
        print(app)
        sys.exit()

    line = 0
    if args.line:
        line = args.line

    app.to_srt(name=args.out, line=line, tag=args.suffix)




##############################################
def print_to_console(console_text, message):
    # Function to print a message to the console area
    console_text.configure(state=tk.NORMAL)  # Enable editing
    console_text.insert(tk.END, message + '\n')
    console_text.configure(state=tk.DISABLED)  # Disable editing
    console_text.see(tk.END)  # Scroll to the end of the console

# Function to retrieve the list of installed fonts
def get_installed_fonts():
    try:
        return list(tkfont.families())
    except:
        return []
    
# Function to select font for Top Style
def select_font_top(font_name_top_label, font_name_top_menu):
    selected_font = font_name_top_menu.get()
    if selected_font:
        font_name_top_label.configure(text=selected_font)

# Function to select font for Bottom Style
def select_font_bot(font_name_bot_label, font_name_bot_menu):
    selected_font = font_name_bot_menu.get()
    if selected_font:
        font_name_bot_label.configure(text=selected_font)

def normalize_episode_format(episode):
    return episode.zfill(2)

def get_unique_identifier(pattern, season_number, episode_number):
    # Format the unique identifier using the specified pattern
    # if pattern == r's(\d+)\s*e(\d+)' or r'S(\d+)\s*E(\d+)':
    #     return patterns_and_formats[pattern].format(int(season_number), int(episode_number))
    # elif pattern == r'(\d+)x(\d+)' or r'(\d+)\s+x\s+(\d+)':
    #     return patterns_and_formats[pattern].format(int(season_number), episode_number)
    # else:
    return patterns_and_formats[pattern].format(int(season_number), int(episode_number))


def read_patterns_from_file(filename):
    patterns_and_formats = {}
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line = line.split("#")[0]  # Remove comments
            pattern, format_str = line.split("|")
            patterns_and_formats[pattern.strip()] = format_str.strip()
    return patterns_and_formats

# Read patterns from file
patterns_and_formats = read_patterns_from_file("patterns.txt")



def merge_subtitles(file_list, output_dir, font_name_top, font_size_top, font_name_bot, font_size_bot, outline_value_top, outline_value_bot, show_name_suffix,console_text):
    # Use "Arial" as default if font_name_bot is empty
    font_name_bot_value = font_name_bot.strip() if font_name_bot.strip() else "Arial"
    font_name_top_value = font_name_top.strip() if font_name_top.strip() else "Arial"
    # Create the header dynamically with the user-entered values

    custom_header = f"""[Script Info]
ScriptType: v4.00+
Collisions: Normal
[V4+ Styles]
Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,WenQuanYi Micro Hei,16,&H00ffffff,&H00000000,&H00000000,0,0,2,1,1,0,20,20,20
Style: Alternate,WenQuanYi Micro Hei,9,&H00ffffff,&H00000000,&H00000000,0,0,2,1,1,0,20,20,20
Style: Top,{font_name_top_value},{font_size_top},&H00FFFFFF,&H00000000,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,0,{outline_value_top},0,8,10,10,10,0
Style: Mid,Arial,14,&H0000FFFF,&H00FFFFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,5,10,10,10,0
Style: Bot,{font_name_bot_value},{font_size_bot},&H00FFFFFF,&H00000000,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,0,{outline_value_bot},0,2,10,10,10,0
"""
    subtitle_dict = {}

    patterns = [
        r's(\d+)e(\d+)',  # s01e02
        r'Season\s*(\d+)\s*Episode\s*(\d+)',  # Season 1 Episode 02
        r'Season(\d+)Episode(\d+)',  # Season1Episode02
        r'S(\d+)\s*Part(\d+)',  # S1 Part2
        r'S(\d+)E(\d+)',  # S01E02
        r'(\d+)\s+x\s+(\d+)',  # 1 x 3
        r's(\d+)e(\d+)',  # s1e02
        r'season\s*(\d+)e(\d+)',  # season 1e02
        r'(\d+)x(\d+)',  # 1x3
        r'Season_(\d+)_Episode_(\d+)'  # Season_1_Episode_9
        
    ]
    # Loop through the selected files
    for in_filename in file_list:
        if in_filename.endswith('.ass'):
            srt = Ass2srt(in_filename)
            srt.to_srt(console_text)
            in_filename= in_filename.replace(".ass", ".srt")
            print(in_filename)

        # Extract episode number from the filename (assuming format "s01e01" or similar)
        for pattern in patterns_and_formats:
            episode_match = re.search(pattern, os.path.basename(in_filename), re.IGNORECASE)
            if episode_match:
                season_number = normalize_episode_format(episode_match.group(1))
                episode_number = normalize_episode_format(episode_match.group(2))
            # else:
            #     season_number = '00'
            #     episode_number = '00'
        
        
        
     

        

        # Initialize unique_identifier and match
        unique_identifier = None
        match = None
        
        # Try each pattern
        for pattern in patterns_and_formats:
            sequence_match = re.search(pattern, show_name_suffix)
            if sequence_match:
                unique_identifier = get_unique_identifier(pattern, season_number, episode_number)
                match = sequence_match
                break
                            

                

                match = sequence_match
                break  # Exit the loop once a match is found

            # elif not sequence_match:
            #     match = None
            #     unique_identifier = f"S{season_number}E{episode_number}"
            #     break
                

        # Store the subtitle file in the dictionary using the unique identifier
        if not unique_identifier:
            
            unique_identifier = ""
            match = None
            subtitle_dict.setdefault(unique_identifier, []).append(in_filename)
        else:
            subtitle_dict.setdefault(unique_identifier, []).append(in_filename)
        
        

    try:
        for unique_identifier, file_group in subtitle_dict.items():
            # Check if there are multiple versions (siblings) of the same episode
            if len(file_group) == 2:
                in_filename1, in_filename2 = file_group

                # Try different encodings until we successfully open the files
                encodings_to_try = ['utf-8', 'windows-1256']
                for encoding in encodings_to_try:
                    try:
                        # Create aeidon projects
                        project1 = aeidon.Project()
                        project1.open_main(in_filename1, encoding)

                        project2 = aeidon.Project()
                        project2.open_main(in_filename2, encoding)

                        # Modify event entries
                        for subtitle in project1.subtitles:
                            subtitle.ssa.style = 'Top'
                        for subtitle in project2.subtitles:
                            subtitle.ssa.style = 'Bot'

                        # # Extract sequence from show_name_suffix
                        # unique_identifier = f"S{season_number}E{episode_number}"
                        # sequence_match = re.search(r's(\d+)e(\d+)', show_name_suffix, re.IGNORECASE)
                        # if sequence_match:
                        #     # Replace sequence in show_name_suffix with episode identifier
                        #     show_name = show_name_suffix[:sequence_match.start()] + unique_identifier + show_name_suffix[sequence_match.end():]
                        # else:
                        #     show_name = show_name_suffix

                        # Extract sequence from show_name_suffix
                        # match = sequence_match
                        # sequence_match = re.search(r's(\d+)e(\d+)', show_name_suffix, re.IGNORECASE)
                        if match:
                            show_name = show_name_suffix[:sequence_match.start()] + unique_identifier + show_name_suffix[sequence_match.end():]
                        else:
                            show_name = show_name_suffix
                        
                        

                        # Set up output filename
                        show_name = show_name.strip()  # Trim spaces
                        if show_name:
                            out_filename = os.path.join(output_dir, f"{show_name}.ass")
                        else:
                            out_filename = os.path.join(output_dir, f"{unique_identifier}.ass")
                        # Set up output format
                        out_format = aeidon.files.new(aeidon.formats.ASS, out_filename, 'utf_8')
                        out_format.header = custom_header

                        # Merge subtitle events from project2 into project1
                        project1.subtitles.extend(project2.subtitles)

                        # Save the merged project
                        print_to_console(console_text, f"Subtitles merged for: {show_name}")
                        # messagebox.showinfo(title='proccessing', message=f"Subtitles merged for: {show_name}")
                        project1.save_main(out_format)

                        break  # Successfully processed the files, no need to try other encodings
                    except UnicodeDecodeError:
                        pass  # Try the next encoding
            else:
                # print(f"Warning: Missing sibling for {file_group[0]}. Skipping this sequence.")
                print_to_console(console_text, f"Warning: Missing sibling for {file_group[0]}. Skipping this sequence.")
                # messagebox.showinfo(title= "Error" ,message= f"Warning: Missing sibling for {file_group[0]}. Skipping this sequence.")

    except Exception as e:
        print_to_console(console_text, f"Error processing subtitles: {str(e)}")


def browse_files(entry):
    # Specify the allowed subtitle file extensions
    file_types = [
        ("Subtitle Files", "*.txt;*.srt;*.ass;*.ssa"),
        ("All Files", "*.*")
    ]
    file_paths = filedialog.askopenfilenames(filetypes=file_types)

    # Get the current content of the entry field
    current_paths = entry.get()
    # Add the newly selected paths to the existing ones
    updated_paths = ';'.join(filter(None, [current_paths, ';'.join(file_paths)]))
    # Update the entry field with the combined paths
    entry.delete(0, tk.END)
    entry.insert(0, updated_paths)

def select_output_dir(entry):
    output_dir = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, output_dir)

import customtkinter
from tkinter import messagebox


def main():
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    app = customtkinter.CTk()
    app.title("Subtitle Merger")
    app.resizable(False, True)

    # frame = ttk.Frame(app)
    frame = customtkinter.CTkFrame(master=app)
    frame.grid(row=0, column=0, padx=20, pady=33, sticky="nsew")

    for i in range(4):
        frame.grid_rowconfigure(i, weight=1)
    for i in range(6):
        frame.grid_columnconfigure(i, weight=1)

    title_label = customtkinter.CTkLabel(master=app, text="Subtitle Tools", font=('Arial', 16, 'bold'))
    title_label.grid(row=0, column=0, columnspan=6, pady= 5,  sticky='n')

    label1 = customtkinter.CTkLabel(frame, text="Select Subtitle Files:")
    label1.grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=5)

    entry1 = customtkinter.CTkEntry(frame, width=80)
    entry1.grid(row=1, column=2, columnspan=2, sticky='ew', padx=5, pady=5)

    browse_button1 = customtkinter.CTkButton(frame, text="       Browse        ", command=lambda: browse_files(entry1))
    browse_button1.grid(row=1, column=4, columnspan=2, sticky='e', padx=5, pady=5)

    label2 = customtkinter.CTkLabel(frame, text="Output Directory:")
    label2.grid(row=2, column=0, columnspan=2, sticky='w', padx=5, pady=5)

    entry2 = customtkinter.CTkEntry(frame, width=180)
    entry2.grid(row=2, column=2, columnspan=2, sticky='ew', padx=5, pady=5)

    browse_button2 = customtkinter.CTkButton(frame, text="Select Directory", command=lambda: select_output_dir(entry2))
    browse_button2.grid(row=2, column=4, columnspan=2, sticky='e', padx=5, pady=5)

    


    font_size_top = tk.StringVar(value="13")
    font_size_bot = tk.StringVar(value="13")
    outline_value_top = tk.StringVar(value="0.5")
    outline_value_bot = tk.StringVar(value="0.5")
    show_name = tk.StringVar(value="MergedSubtitle_")
   
    font_frame = customtkinter.CTkFrame(master=app)
    font_frame.grid(row=3, column=0, columnspan=6, padx=20, pady=0, sticky='nsew')
    for i in range(1):
        font_frame.grid_rowconfigure(i, weight=1)
    for i in range(1):
        font_frame.grid_columnconfigure(i, weight=1)

    Top=str('Top Subtitle')
    Bottom=str('Bottom Subtitle')
    tabview = customtkinter.CTkTabview(font_frame,width=250)
    tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    tabview.add(Top)
    tabview.add(Bottom)
    
    
    
    
    font_name_top_label = customtkinter.CTkLabel(tabview.tab(Top), text="Top Style Font:")
    font_name_top_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

    font_name_top_menu = customtkinter.CTkComboBox(tabview.tab(Top), values=get_installed_fonts(), state='readonly', width=150)
    font_name_top_menu.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    font_name_top_button = customtkinter.CTkButton(tabview.tab(Top), text="Select", command=lambda: select_font_top(font_name_top_label, font_name_top_menu))
    font_name_top_button.grid(row=0, column=2, padx=5, pady=1, sticky='w')

    font_size_top_label = customtkinter.CTkLabel(tabview.tab(Top), text="Top Style Font Size:")
    font_size_top_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)

    font_size_top_entry = customtkinter.CTkEntry(tabview.tab(Top), textvariable=font_size_top, width=10)
    font_size_top_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    outline_value_top_label = customtkinter.CTkLabel(tabview.tab(Top), text="Outline for Top Style:")
    outline_value_top_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)

    outline_value_top_entry = customtkinter.CTkEntry(tabview.tab(Top), textvariable=outline_value_top, width=10)
    outline_value_top_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

    font_name_bot_label = customtkinter.CTkLabel(tabview.tab(Bottom), text="Bottom Style Font:")
    font_name_bot_label.grid(row=0, column=3, sticky='w', padx=5, pady=5)

    font_name_bot_menu = customtkinter.CTkComboBox(tabview.tab(Bottom), values=get_installed_fonts(), state='readonly', width=150)
    font_name_bot_menu.grid(row=0, column=4, padx=5, pady=5, sticky='ew')

    font_name_bot_button = customtkinter.CTkButton(tabview.tab(Bottom), text="Select", command=lambda: select_font_bot(font_name_bot_label, font_name_bot_menu))
    font_name_bot_button.grid(row=0, column=5, padx=5, pady=5, sticky='w')

    font_size_bot_label = customtkinter.CTkLabel(tabview.tab(Bottom), text="Bottom Style Font Size:", width=10)
    font_size_bot_label.grid(row=1, column=3, sticky='ew', padx=5, pady=5)

    font_size_bot_entry = customtkinter.CTkEntry(tabview.tab(Bottom), textvariable=font_size_bot, width=10)
    font_size_bot_entry.grid(row=1, column=4, padx=5, pady=5, sticky='ew')

    outline_value_bot_label = customtkinter.CTkLabel(tabview.tab(Bottom), text="Outline for Bottom Style:")
    outline_value_bot_label.grid(row=2, column=3, sticky='w', padx=5, pady=5)

    outline_value_bot_entry = customtkinter.CTkEntry(tabview.tab(Bottom), textvariable=outline_value_bot, width=10)
    outline_value_bot_entry.grid(row=2, column=4, padx=5, pady=5, sticky='ew')

    settings_frame = customtkinter.CTkFrame(master=app)
    settings_frame.grid(row=4, column=0, columnspan=6, padx=20, pady=25, sticky='nsew')
    for i in range(4):
        settings_frame.grid_rowconfigure(i, weight=1)
    for i in range(1):
        settings_frame.grid_columnconfigure(i, weight=1)

    show_name_label = customtkinter.CTkLabel(settings_frame, text="Show Name:" )
    show_name_label.grid(row=0, column=0,columnspan=2, sticky='w', padx=5, pady=5)

    show_name_entry = customtkinter.CTkEntry(settings_frame, textvariable=show_name)
    show_name_entry.grid(row=0, column=0, columnspan=2,padx=80 , sticky='ew')

    merge_button = customtkinter.CTkButton(settings_frame, text="Merge Subtitles", command=lambda: merge_subtitles(
        entry1.get().split(';'),
        entry2.get(),
        font_name_top_menu.get(),
        font_size_top_entry.get(),
        font_name_bot_menu.get(),
        font_size_bot_entry.get(),
        outline_value_top_entry.get(),
        outline_value_bot_entry.get(),
        show_name_entry.get(),
        console_text
    ))
    merge_button.grid(row=5, column=0, pady=5, sticky='n')
    
    console_text = customtkinter.CTkTextbox(settings_frame, height=40, wrap=tk.WORD, state=tk.DISABLED)
    console_text.grid(row=6, column=0, columnspan=6, sticky='nsew', padx=5, pady=5)


    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    app.mainloop()

if __name__ == '__main__':
    main()



