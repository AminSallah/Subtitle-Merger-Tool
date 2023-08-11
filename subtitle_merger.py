import sys
import tkinter as tk
from tkinter import filedialog
import os
import re
import aeidon
from tkinter import ttk
import tkinter.font as tkfont


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
        font_name_top_label.config(text=selected_font)

# Function to select font for Bottom Style
def select_font_bot(font_name_bot_label, font_name_bot_menu):
    selected_font = font_name_bot_menu.get()
    if selected_font:
        font_name_bot_label.config(text=selected_font)

def normalize_episode_format(episode):
    return episode.zfill(2)



def merge_subtitles(file_list, output_dir, font_name_top, font_size_top, font_name_bot, font_size_bot, outline_value_top, outline_value_bot, show_name_suffix):
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
    # Loop through the selected files
    for in_filename in file_list:
        # Extract episode number from the filename (assuming format "s01e01" or similar)
        episode_match = re.search(r's(\d+)e(\d+)', os.path.basename(in_filename), re.IGNORECASE)
        if episode_match:
            season_number = normalize_episode_format(episode_match.group(1))
            episode_number = normalize_episode_format(episode_match.group(2))
        else:
            season_number = '00'
            episode_number = '00'
        
        # Create a unique identifier for the merged file
        unique_identifier = f"S{season_number}E{episode_number}"

        # Store the subtitle file in the dictionary using the unique identifier
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

                        # Extract sequence from show_name_suffix
                        sequence_match = re.search(r's(\d+)e(\d+)', show_name_suffix, re.IGNORECASE)
                        if sequence_match:
                            # Replace sequence in show_name_suffix with episode identifier
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
                        project1.save_main(out_format)

                        break  # Successfully processed the files, no need to try other encodings
                    except UnicodeDecodeError:
                        pass  # Try the next encoding
            else:
                print(f"Warning: Missing sibling for {file_group[0]}. Skipping this sequence.")

    except Exception as e:
        print(f"Error processing subtitles: {str(e)}")


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


def main():
    app = tk.Tk()
    app.title("Subtitle Merger")

    label1 = tk.Label(app, text="Select Subtitle Files:", width=30)
    label1.pack()

    entry1 = tk.Entry(app, width=50)
    entry1.pack()

    browse_button1 = tk.Button(app, text="Browse", command=lambda: browse_files(entry1))
    browse_button1.pack()

    label2 = tk.Label(app, text="Output Directory:", width=30)
    label2.pack()

    entry2 = tk.Entry(app, width=50)
    entry2.pack()

    browse_button2 = tk.Button(app, text="Select Directory", command=lambda: select_output_dir(entry2))
    browse_button2.pack()

    font_size_top = tk.StringVar(value="13")
    font_size_bot = tk.StringVar(value="13")
    outline_value_top = tk.StringVar(value="0.5")
    outline_value_bot = tk.StringVar(value="0.5")
    show_name = tk.StringVar(value="MergedSubtitle_")

    font_size_top_label = tk.Label(app, text="Font Size for Top Style:", width=30)
    font_size_top_label.pack()

    font_size_top_entry = tk.Entry(app, textvariable=font_size_top, width=50)
    font_size_top_entry.pack()

    font_size_bot_label = tk.Label(app, text="Font Size for Bottom Style:", width=30)
    font_size_bot_label.pack()

    font_size_bot_entry = tk.Entry(app, textvariable=font_size_bot, width=50)
    font_size_bot_entry.pack()

    outline_value_top_label = tk.Label(app, text="Outline for Top Style:", width=30)
    outline_value_top_label.pack()

    outline_value_top_entry = tk.Entry(app, textvariable=outline_value_top, width=50)
    outline_value_top_entry.pack()

    outline_value_bot_label = tk.Label(app, text="Outline for Bottom Style:", width=30)
    outline_value_bot_label.pack()

    outline_value_bot_entry = tk.Entry(app, textvariable=outline_value_bot, width=50)
    outline_value_bot_entry.pack()

    show_name_label = tk.Label(app, text="Name:", width=30)
    show_name_label.pack()

    show_name_entry = tk.Entry(app, textvariable=show_name, width=50)
    show_name_entry.pack()

    font_name_top_label = tk.Label(app, text="Arial", width=30)
    font_name_top_label.pack()

    font_name_top_menu = ttk.Combobox(app, values=get_installed_fonts())
    font_name_top_menu.pack()

    font_name_top_button = tk.Button(app, text="Select Top Font", command=lambda: select_font_top(font_name_top_label, font_name_top_menu))
    font_name_top_button.pack()

    font_name_bot_label = tk.Label(app, text="Arial", width=30)
    font_name_bot_label.pack()

    font_name_bot_menu = ttk.Combobox(app, values=get_installed_fonts())
    font_name_bot_menu.pack()

    font_name_bot_button = tk.Button(app, text="Select Bottom Font", command=lambda: select_font_bot(font_name_bot_label, font_name_bot_menu))
    font_name_bot_button.pack()

    merge_button = tk.Button(app, text="Merge Subtitles", command=lambda: merge_subtitles(
        entry1.get().split(';'),
        entry2.get(),
        font_name_top_menu.get(),  # Get the selected font for Top Style
        font_size_top_entry.get(),
        font_name_bot_menu.get(),  # Get the selected font for Bottom Style
        font_size_bot_entry.get(),
        outline_value_top_entry.get(),
        outline_value_bot_entry.get(),
        show_name_entry.get()
    ))
    merge_button.pack()

    app.mainloop()

if __name__ == '__main__':
    main()