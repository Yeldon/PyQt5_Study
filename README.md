

# PyQt5\_Study

Learn to write some simple GUIs.


# FUNWAVE\_input

generate or edit the FUNWAVE input file with a GUI.


## Two ways of generating input

-   use pre-defined dictionaty (without existing data file)

-   read from input file (with existing data file)
    by editing the pre-defined dictionary key and value lists in `parameter_dictionary`,


## layout

for input number \(n\)

-   if \(n<10\), 1 column
-   if \(10<=n<30\), 2 column
-   if \(30<=n<60\), 3 column
-   if \(60<=n<100\), 4 column
-   if \(n>100\), 5 column


## Data types:

Five data types are supported.

-   integer
-   float
-   string
    If none of the rest of the four types is satisfied, then it would be
    recognized as string
-   logical
    Either `T` or `F`
-   unknown

For existing `'input.txt'` file, if the input is empty, the data type will be
`unknown`. 


## Notes:

-   The `input.txt` file should be place under the same directory with the python file.
-   If there is comments on the original input file, they will all be eliminated in the new file.
-   The program can tell if you input the value with correct type. Except:

(1) Integer like *100* for a variable should be float.

(2) Numbers such as *95.* is also fine for the float. 

-   If reading from the existing `input.txt` file, make sure all values in the
    existing `input.txt` file are correct, the program chooses will use the data
    type used in the existing file.

-   If the existing `input.txt` was destroyed by the program by mistaken, find
    `input_backup.txt` to get recovery.


## Future work<code>[/]</code>

-   [ ] error message dialog
-   [ ] Re-organize the layout by groups
-   [ ] Compile as executable file

