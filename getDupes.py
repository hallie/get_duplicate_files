import os.path, sys
MAX_RECURSION_LIMIT = 5000
sys.setrecursionlimit(MAX_RECURSION_LIMIT) # Necessary...

###
# @function getAllFilesOfEqualSize
# @param {string} mypath - The relative path to the root directory.
# @param {opt={}} equal_sizes - The dictionary holding all of the sizes.
#   The key is the size, and the value is an array with all of the paths
#   to files of that size.
# @param {opt=[]} potential_dupes - List of all keys where there is more
#   than one value, indicating that it could be a duplicate.
# @return {dictionary} equal_sizes
# @return {array} potential_dupe
###
def getAllFilesOfEqualSize(mypath, equal_sizes = {}, potential_dupe = []):
    # Creates a list of every item in given directory.
    directory = os.listdir(mypath)
    # Iterates through the direcory.
    for item in directory:
        # Joins the current item to the directory's path, sets to current_path.
        current_path = os.path.join(mypath, item)
        # Checks to see if the current path points to a file.
        if (os.path.isfile(current_path)):
            # Gets the extension of the current file.
            #ext = os.path.splitext(current_path)[1].lower()
            # Checks if the file is a bitmap file.
            #if (ext == ".bmp"):
            # Stringifies the file size.
            size = str(os.path.getsize(current_path))
            # Adds the file to the list located at that size key.
            if (size in equal_sizes):
                equal_sizes[size].append(current_path)
                # If the length of this list at this value is two, add the
                #  key to the potential_dupe list.
                if (len(equal_sizes[size]) == 2):
                    potential_dupe.append(size)
            else:
                equal_sizes[size] = [current_path]
        # If the path points to a directory, run getAllFilesOfEqualSize on it.
        else:
            equal_sizes, potential_dupe = getAllFilesOfEqualSize(current_path,
                                                                equal_sizes,
                                                                potential_dupe
                                                               )
    # Return the equal_sizes directory and the potential_dupe list.
    return equal_sizes, potential_dupe


###
# @function compareImages
# @param {array} img_list - The list of image paths being compared.
# @param {int} img_size - The size of the images being looked at.
# @param {opt=0} k - The depth of the recursive call.
# @return {array} img_list
###
def compareImages(img_list, img_size, k=0):
    # Sets n to be the square root of the image size.
    n = int(img_size**(.5))
    # If k is greater than or equal to n, the process is done.
    if (k >= n):
        return img_list
    # Sets start to n*k
    start = n*k
    # Sets end to n * (k+1)
    end = n*(k+1)
    # If end's index is out of range, set it to the end of the list.
    if (end >= img_size):
        end = -1
    # Creates a dictionary to hold the bit strings.
    kn_elements = {}
    # Creates a list of strings that might have duplicates.
    might_has_dupe = []
    # Iterates through the images.
    for img in img_list:
        # Opens the file at that image path.
        f = open(img, 'rb')
        # Sets img_kn to the chunk of bits from the start to end points.
        img_kn = f.read()[start:end]
        # Closes the file.
        f.close()
        # Puts the path in the value list associated with that string.
        if not(img_kn in kn_elements):
            kn_elements[img_kn] = [img]
        else:
            kn_elements[img_kn].append(img)
            # Adds to list of potential dupes if length equal to 2.
            if (len(kn_elements[img_kn]) == 2):
                might_has_dupe.append(img_kn)
    # Initializes a list of known duplicates.
    actual_dupes = []
    # Iterates through the might_has_dupe list.
    for mhd in might_has_dupe:
        # Extends what was returned by recursice comparison.
        actual_dupes.extend(compareImages(kn_elements[mhd], img_size, k+1))
    # Returns the actual dupes.
    return actual_dupes

###
# @function getDupes
# @param {string} mypath - The relative path to the root directory.
# @return {array} all_dupes - A list of all of the duplicates lists.
###
def getDupes(mypath):
    # Gets the equal_sizes dictionary and the potential_dupe list.
    equal_sizes, potential_dupe = getAllFilesOfEqualSize(mypath)
    # Initializes a list of all duplicates.
    all_dupes = []
    # Iterates through the potential_dupe list.
    for pd in potential_dupe:
        # Runs compareImages on the list at that key.
        duplicates = compareImages(equal_sizes[pd], int(pd))
        # Appends it to the list of duplicates if something is returned.
        if (len(duplicates) > 0):
            all_dupes.append(duplicates)
    # Donezo
    return all_dupes