# Subtitle Merger Tool




**1. Prerequisites**

- Python 3.x
- aeidon
- Tkinter (usually included with Python)
- CustomTkinter

**2. Installation**

1. Clone this repository to your local machine:

```bash
git clone https://github.com/AminSallah/SubtitleMerge
```

2. Navigate to the cloned repository's directory:

```bash
cd your-repo
```

3. Run the tool:

```bash
python main.py
```

**3. Usage**

- Click the "Browse" button under "Select Subtitle Files" to choose the subtitle files you want to merge.
  
  You can choose multiple files for different languages, and the Smart Merge feature will analyze and merge only sibling subtitles.

    1. Press the "Browse" button to select the subtitles you want to treat as the top subtitles, then click "OK".
    2. Press the "Browse" button ***again*** to select the subtitles you want to merge with the top subtitles, then click "OK".
  
- Click the "Select Directory" button to choose the output directory for the merged subtitle file.
- Customize the font styles, sizes, and outlines for the top and bottom subtitles using the respective sections.
- Enter a prefix for the merged subtitle filename in the "Show Name" field.
   This will be helpful for TV shows and merging a large number of subtitles at once. </br>
   </br>
**Example**:</br>
   srtInput > Friends.S01E01.English.srt, Friends.S01E02.English.srt, Friends.S01E03.English.srt</br>
   srtInput > Friends.Season 01 Episode 01.English.srt, Friends.Season 01 Episode 02.English.srt, Friends.Season 03 Episode 01.English.srt </br>
   Show name prefix = Friends.s01e01.720p</br>
   Output files > Friends.s01e01.720p.ass, Friends.s01e02.720p.ass, Friends.s01e03.720p.ass</br>
- Click the "Merge Subtitles" button to start the merging process.
- The console will display messages about the progress of the merging process.

**4. Options**

- **Select Subtitle Files**: Use this option to choose the subtitle files you want to merge. You can select multiple files by holding down the Ctrl key while selecting.
- **Output Directory**: Choose the directory where the merged subtitle file will be saved.
- **Top Style Font**: Select the font style for the top subtitle.
- **Top Style Font Size**: Set the font size for the top subtitle.
- **Outline for Top Style**: Set the outline thickness for the top subtitle.
- **Bottom Style Font**: Select the font style for the bottom subtitle.
- **Bottom Style Font Size**: Set the font size for the bottom subtitle.
- **Outline for Bottom Style**: Set the outline thickness for the bottom subtitle.
- **Show Name**: Enter a prefix for the merged subtitle filename.
- **Merge Subtitles**: Click this button to initiate the merging process.

**5. Notes**

1. The tool currently supports `.srt` and `.ass` subtitle formats. (.ass converted to srt automatically and saved into srt directory)
2. Make sure to provide correct and consistent episode numbers in the subtitle filenames for accurate merging.
3. You can choose different font styles, sizes, and outlines for the top and bottom subtitles.
4. The merged subtitles will be saved with the specified prefix and the appropriate extension.


I'm actively working on expanding the customization options, and in the future, you can look forward to more features being added.
If you have any specific feature requests or suggestions, feel free to reach out on my Patreon page:

<a href="https://ko-fi.com/amin_salah" rel="nofollow"><img height="36" style="height: 36px; max-width: 100%;" src="https://camo.githubusercontent.com/6d394442bad846f705d9f455fa612cc5c8878c1837338da05b713de22a4f2cda/68747470733a2f2f63646e2e6b6f2d66692e636f6d2f63646e2f6b6f6669312e706e673f763d32" border="0" alt="Buy Me a Coffee at ko-fi.com" data-canonical-src="https://cdn.ko-fi.com/cdn/kofi1.png?v=2"></a>

Your support and feedback are greatly appreciated and will help shape the future development of this tool.





---
