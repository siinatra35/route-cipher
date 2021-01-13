import math
import sys
import re

# Current path position:
g_posR = 0  # row position
g_posC = 0  # column position

# Current path direction:
g_dirR = 0  # row direction
g_dirC = 0  # column direction

# Current path borders:
g_borderL = 0  # left column
g_borderT = 0  # top row
g_borderR = 0  # right column
g_borderB = 0  # bottom row

grid = []  # holds matrix


def fillTableForEncrypt(letters, totalRows, totalCols):
    """ creates an array to hold the plaintext and appends extra character """
    # creates a matrix using the text length divided by the total columns
    for number_of_rows in range(math.ceil(len(letters) / totalCols)):
        rows = []  # holds cipher text
        for index in range(totalCols): 
            if number_of_rows * totalCols + index < len(letters):
                rows.append(letters[number_of_rows * totalCols + index])
            else:
                # appends a - character if the matrix has empty spaces
                rows.append('-')
        grid.append(rows)  # appends newly formed matrix to grid
    return grid  # returns newly formed grid


def fillTableForDecrypt(letters, totalRows, totalCols, pathtype):
    """creates decryption matrix using the ciphertext"""
    global g_posR, g_posC  # current row position and and current column position
    newGrid = []  # holds decrypted grid

    # creates a matrix using the ciphertext length and total columns
    for number_of_rows in range(math.ceil(len(letters) / totalCols)):
        rows = []  # holds a decrypted text
        for index in range(totalCols):
            if number_of_rows * totalCols + index < len(letters):
                rows.append(letters[number_of_rows * totalCols + index])
            else:
                # appends a - character if the matrix has empty spaces
                rows.append('-')
        newGrid.append(rows)  # appends newly formed matrix to grid

    initPathParameters(pathtype, totalRows, totalCols)  # sets the position of the row and column
    pos = 0  # position in the grid
    while pos < totalRows * totalCols:  # writes newly formed grid
        # using row position and grid position we create the new matrix
        newGrid[g_posR][g_posC] = letters[pos]
        # this function allow use to read the matrix based on the chosen path
        makeOneStep(pathtype)
        pos += 1  # increments by to add letters
    return newGrid  # returns newly formed grid holding the decrypted text


def readCipherText(grid, totalRows, totalCols, pathtype):
    """reads the newly created cipher text"""
    initPathParameters(
        pathtype, totalRows, totalCols)  # sets the starting, direction, and path for the grid
    global g_posR, g_posC  # row position and column position
    cipher_text = ""  # holds created cipher text
    # appends the cipher text from the grid
    while len(cipher_text) < totalRows * totalCols:
        cipher_text += grid[g_posR][g_posC]
        makeOneStep(pathtype)  # moves position in the grid
    return cipher_text  # returns new created encrypted text


def readPlainText(matrix, totalRows, totalCols):
    plain_text = "" 
    for rows in range(totalRows):
        for columns in range(totalCols):
            plain_text += str(matrix[rows][columns])
    return plain_text


def initPathParameters(pathtype, totalRows, totalCols):
    global g_posR, g_posC, g_borderL, g_borderT, g_borderR, g_borderB, g_dirR, g_dirC
    g_posR = 0  # current row position
    g_posC = totalCols - 1  # current column position

    g_borderL = 0  # left side of the grid
    g_borderT = 0  # top side of the grid
    g_borderR = totalCols - 1  # right side of the grid
    g_borderB = totalRows - 1  # bottom side of the grid

    if pathtype == "clockwise":
        g_dirR = 1  # sets starting direction for the row
        g_dirC = 0  # sets starting direction for the column
    elif pathtype == "anticlockwise":
        g_dirR = 0
        g_dirC = -1


def makeOneStep(pathtype):
    """moves position in grid"""
    global g_posR, g_posC, g_borderL, g_borderT, g_borderR, g_borderB, g_dirR, g_dirC

    if g_posR + g_dirR >= g_borderT and g_posR + g_dirR <= g_borderB:
        g_posR += g_dirR  # row position
    else:
        if g_dirR == 1:
            if pathtype == "clockwise":  # moves down the grid
                g_dirR = 0
                g_dirC = -1
                g_borderR -= 1
            elif pathtype == "anticlockwise":
                g_dirR = 0
                g_dirC = 1
                g_borderL += 1
        elif g_dirR == -1:
            if pathtype == "clockwise":
                g_dirR = 0
                g_dirC = 1
                g_borderL += 1
            elif pathtype == "anticlockwise":
                g_dirR = 0
                g_dirC = -1
                g_borderR -= 1

    if g_posC + g_dirC >= g_borderL and g_posC + g_dirC <= g_borderR:
        g_posC += g_dirC  # column position
    else:
        if g_dirC == 1:
            if pathtype == "clockwise":  # moves up in the grid
                g_dirR = 1
                g_dirC = 0
                g_borderT += 1
            elif pathtype == "anticlockwise":
                g_dirR = -1
                g_dirC = 0
                g_borderB -= 1
        else:
            if pathtype == "clockwise":
                g_dirR = -1
                g_dirC = 0
                g_borderB -= 1
            elif pathtype == "anticlockwise":
                g_dirR = 1
                g_dirC = 0
                g_borderT += 1

        g_posR += g_dirR


def menu_check(questions):
    """checks input on user and repeats questions if a error is encountered"""
    values = ""  # holds user input
    while True:
        user_input = input(questions)
        user_input = user_input.replace(" ", "")  # removes spaces
        if len(user_input) == 0:  # checks for no input
            print("Error! No input detected. ")
        # if only letters are entered or special characters
        elif re.match("^[A-Za-z0-9_-]*$", user_input):
            values = user_input  # assigns text from user input
            break  # stops question loop
    return values  # returns user input


def grouping(plain_text, totalCols):
    """creates matrix from the plaintext that is used to encrypt and decrypt"""
    if len(plain_text) % totalCols == 0:  # checks if there are extra spaces
        return [plain_text[rows*totalCols:rows*totalCols+totalCols] for rows in range(len(plain_text)//totalCols)]
    else:  # adds a column if there is a remainder
        return [plain_text[rows*totalCols:rows*totalCols+totalCols] for rows in range(len(plain_text)//totalCols+1)]


def topToBottom(plaintext, route_size, decrypt=False):
    """Encrypts/Decrypts from top to bottom"""
    while len(plaintext) % route_size != 0: # appends a - charater of there is extra spaces 
        plaintext += "-"

    if decrypt == False:
        grid = grouping(plaintext, route_size) # receives newly formed grid
        encrypted_text = "" # holds encrypted text
        pos = 0 # position in grid
        while pos < route_size: # repeats the step through of the grid based on the route size
            rows = []
            for i in grid:
                rows.append(i[pos])
            if pos % 2 == 1:
                rows.reverse()
            encrypted_text += "".join(rows)
            pos += 1
        return encrypted_text

    if decrypt == True:
        size = len(plaintext) // route_size
        G = grouping(plaintext, size)
        out = ""
        for passthru in range(size):
            for pos, lets in enumerate(G):
                if pos % 2 == 0:
                    a = lets[0]
                    G[pos] = lets[1:]
                if pos % 2 == 1:
                    a = lets[-1]
                    G[pos] = lets[:-1]
                out += a

        return out


def main():
    additional_Path = ""
    # questions to user
    path_options = """Please select the desired route path.\n[1]. clockwise\n[2]. anticlockwise\n[3]. Spiraling inside out\n[4]. Top-to-Bottom\n\n>>> """
    route_size_choice = "\nPlease enter a route size above 2: "
    get_plaintext = "Please enter the desired text for encryption/decryption: "

    while True:
        choice = input(path_options) # getting users choice for pathtype 
        if choice == "1": # clockwise path 
            pathtype = "clockwise"
            break
        elif choice == "2": # counter clockwise path 
            pathtype = "anticlockwise" 
            break
        elif choice == "3": # inside out path 
            pathtype = "clockwise" 
            additional_Path = "spiraling"
            break
        elif choice == "4": # top to bottom path
            pathtype = "Top-to-Bottom"
            break
        else:
            print('Invalid input: Please enter one of the choices listed above.\n')

    try:
        # checks input 
        route_size = menu_check(route_size_choice)
        plain_text = menu_check(get_plaintext)
        totalCols = int(route_size) # assigns total columns 
        totalRows = len(plain_text) / totalCols # assigns rows based on text length and route size
    except Exception as e: # checks for errors for value assignment
        print("A errors has occurred: ",e)
        print("Rerunning program.........")
        main() # reruns program

    if totalRows != math.floor(totalRows): # adds a extra row 
        totalRows = math.floor(totalRows) + 1 
    elif type(totalRows) is float:  # if rows is a decimal value
        # rounds to the nearest whole number 
        totalRows = len(plain_text) // totalCols

    # prints the selected pathtype 
    if choice == "3": 
        print("Selected path type:", additional_Path)
    else:
        print("Selected path type:", pathtype)

    # prints column and row values to user
    print("Total Columns: ", totalCols)
    print("Total Rows: ", totalRows)


    # grid = fillTableForEncrypt(plain_text, totalRows, totalCols)
    # encryptedText = readCipherText(grid, totalRows, totalCols, pathtype)
    

    new_grid = []
    if totalRows != math.floor(totalRows):
        print("The length does not match the table dimensions.")
        sys.exit(0)
    elif choice == "1" or choice == "2" or choice == "3":
        grid = fillTableForEncrypt(plain_text, totalRows, totalCols)
        encryptedText = readCipherText(grid, totalRows, totalCols, pathtype)
        new_grid = fillTableForDecrypt(encryptedText, totalRows, totalCols, pathtype)
        decryptedText = readPlainText(new_grid, totalRows, totalCols)
    elif choice == "4":
        encryptedText = topToBottom(plain_text, totalCols)
        decryptedText = topToBottom(encryptedText, totalCols, decrypt=True)

  
    if choice == "1" or choice == "2" or choice == "4":
        print("Encrypted Text: ", encryptedText)
        print("Decrypted Text: ", decryptedText)
    else:
        print("Encrypted Text: ", encryptedText[::-1])
        print("Decrypted Text: ", decryptedText[::1])


if __name__ == "__main__":
    main()
