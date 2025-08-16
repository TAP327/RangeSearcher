# RangeSearcher

## Introduction
---
This program was built to help AidData, a research team under the Global Reasearch Institute at the College of William & Mary search CSVs and save the output in a new CSV.  AidData is a group that works to compile a database of Chinese foreign aid projects to other nations that fall under the Belt and Road Initiative.  

This program can be used to refine a CSV by rows that contain two key words within a certain user-specified range of each other.  The range can be defined in words or characters.  After searching, the program provides the user with a sample of the rows with matches in the form of a Pandas DataFrame.  The user can choose for the output to be converted to a CSV and saved to the user's computer.  

## Built With
---
- CSS
- Flask
- HTML
- OS
- Pandas
- Pathlib
- Platform
- PyInstaller
- Python
- RegEx
- Tempfile

## Getting Started
---
This is a python flask program that is run as a locally-hosted webpage.  To run this program, download the Windows executbale or run the source code in a terminal such as PowerShell or Visual Studio Code as a module.
### Prerequisites
If you are running the program in your terminal, the prerequisites for running the program can be downloaded using the terminal command "pip install .".  Otherwise, just download and run the executable.
### Installation
The program can be downloaded off of GitHub as an executable.  If you download the source code, use the "pip install ." command to run it.
## Usage
---
This program is fairly straightforward to use, and provides tips and error messages for if you get stuck.  Below is a step-by-step rundown on the program with any specifications on if an answer should follow any formatting rules.  
At any point, the program may show error messages in a new page.  These are left out of this description, but will explain to you how the program errored if they are thrown.  You can go to the previous page and the information you entered will still be there for you to edit.  If the program errors out, the user will be asked if they would like to search again.  Searching again brings the user to a blank forum/home page while returning to the previous page maintains the user's input in the forum.
- First, double click on the executable file or run the program in your terminal as a module ("python -m RangeSearcher").  The command is case sensitive.
- The program will ask for you for the CSV file you would like to search.  Make sure to enter the full path of the file, not just the name.  You can go into the file explorer, right click on the file you want to search, and copy the path.  
- The program will ask if you would like to search the file by a range measured in characters or words.  For example, you could 'characters' for if you'd like to search for projects where the word 'subsidiary' is within 100 characters of 'bank' or 'words'for if you'd like to search for projects where 'subsidiary' is within 5 words of 'bank'
- The program will ask how many words/characters long you would like the range it searches by to be.  In the previous step, the first example would enter the number 100 and the second would enter the number 5. Lag time shouldn't be a problem if you search by characters, but in long files, you may notice some lag time for longer, word-based ranges. It's not recommended to search by a range longer than 10 words unless the file is short.  If you are experiencing too much lag time, either keep waiting or exit the program, reenter, and try again with a character-based or shorter range.
- The program will ask what number column you would like to search by. To know what number to enter, look at the CSV file you fed the program and start counting from the far left starting at the number 1 (not 0).  
- The program will then show you a sample of the projects it found in the format of a table generated from a Pandas DataFrame.  If the DataFrame is empty, it didn't find any matches.  There is no reason to save this data.  If no DataFrame appears, it is still processing the data.  The DataFrame will cut off after 10 rows automatically since this is just a preview.  The program will ask you if you would like to save the data as a CSV or search again.
- If you save the CSV, the program will tell you whether the data saved correctly or not.  The data is saved as a CSV in folder named 'Output' inside of the folder your original CSV file is saved.  If the folder does not already exist, the program will create it before saving the data. The file contains a suffix that starts with '_processed'.  The suffix includes the column number that the user searched under (i.e. '_col14'), the range (i.e. '_char100' for a range of 100 characters or '_word5' for a range of five words), and if that file had already been searched with that range and column combination, a number at the end to make the name a unique filename (i.e. '(1)'). 
- Finally, the program asks the user if they would like to search another file.  At this point, you can either search again or quit the program.  If you search again, the previously detailed steps will repeat with whatever file you give it. 
## Roadmap
---
No updates are planned for RangeSearcher at this time.  Feel free to let me know if you have any suggestions!
## Contributing
---
Any and all contributions are welcome!  If you have a suggestion for an improvement, feel free to fork the repository and make a pull request.  You could also open an issue with the tag "enhancement".  Thank you for helping to make RangeSeearcher.py even better!

## License
---
Distributed under the Unlicense License. See LICENSE.txt for more information.
