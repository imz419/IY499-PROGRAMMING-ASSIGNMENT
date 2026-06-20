================================================================================
GROUPED DATA STATISTICS APPLICATION - README
================================================================================

Identifying Information:
------------------------
Name:        [Imran Mohammed]
P-Number:    [P433238]
Course Code: IY499 Introduction to Programming
Date:        June 2026



Declaration of Own Work:
------------------------
I confirm that this assignment is my own work.

Program Description:
------------------------------------
This Grouped Data Statistics Application is a command line Python program designed 
to collect, process, and visualize numerical data. The program allows users to 
input numerical data points, which are then saved to a CSV file for persistent 
storage. Users can then load this data and compute various statistical measures 
including mean, median, mode, variance, and standard deviation. 

A key feature is the ability to group data into classes with a user-specified 
class width, and then display a histogram using Matplotlib for data visualization. 
The program demonstrates several core programming concepts: file handling (CSV 
read/write using pandas), data validation and error checking, complex data 
structures (dictionaries for grouped data), sorting algorithms, and a robust 
menu-driven user interface. The application is designed to be robust against 
invalid user inputs and includes comprehensive error recovery mechanisms.


Packages/Libraries Used:
------------------------
- pandas        : For CSV file reading and writing (DataFrame operations)
- numpy         : For numerical computations (ceil function for class calculation)
- matplotlib    : For data visualization (histogram plotting)
- statistics    : For statistical calculations (mean, median, mode, variance, stdev)
- os            : For file existence checking (built-in)
- csv           : For CSV file handling (built-in)


Installation Instructions:
--------------------------
1. Ensure Python 3.8 or higher is installed on your system.

2. Install the required packages using pip. Open a terminal and run:

   pip install pandas numpy matplotlib

   (The 'statistics' module is built into Python 3.4+ and does not need installation)

3. Verify installations:

   python -c "import pandas; import numpy; import matplotlib; print('All packages installed!')"


How to Run the Program:
-----------------------
1. Save the program file as 'dataProject.py' in your desired folder.

2. Open a terminal (Command Prompt, PowerShell, or Terminal).

3. Navigate to the folder containing the file:

   cd path/to/your/folder

4. Run the program with:

   python dataProject.py

5. Follow the on-screen menu to:
   - Option 1: Enter data and save to CSV
   - Option 2: View statistics (mean, median, mode, etc.)
   - Option 3: Draw a histogram with grouped data
   - Option 4: View current data in memory
   - Option 5: Exit the program


File Structure:
---------------
dataProject.py    - Main program file
README.txt        - This documentation file
data.csv          - Data file created automatically by the program (stores user data)


Features Demonstrated:
----------------------
- Functions to break up code into manageable pieces
- Complex data structures (dictionaries, lists, tuples)
- File access (reading from and writing to CSV files)
- Sorting algorithm (data sorting for grouping)
- Robust user interface (menu-driven CLI)
- Data visualization (histogram using Matplotlib)
- Comprehensive error checking and error recovery
- Input validation with range checking

================================================================================