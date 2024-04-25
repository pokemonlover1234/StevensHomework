#do not change any function names
def findAlphabeticallyFirstWord(string):
    if " " in string:
        sep = " "
    else:
        sep = ","
    words = [word.lower() for word in string.split(sep) if not (word == "" or word == " ")]
    res = words[0]
    for word in words[1:]:
        n = 0
        while(True):
            # If new word is equal to current result up to 
            # its own length, then it is alphabetically break the result
            # I.e. Apple coming before Applesauce
            if n >= len(word):
                res = word
                break
            # In the same vein, if the current result is equal to 
            # the new word, but is shorter than the new word, then 
            # res is kept
            if n >= len(res):
                break
            # If the current letter is before the letter in res
            # then the current considered word comes before res and
            # should be the new res
            if ord(word[n]) < ord(res[n]):
                res = word
                break
            # If the current letter comes after the same letter in res
            # then the current cannot can never be alphabetically before res
            if ord(word[n]) > ord(res[n]):
                break
            # If the current letter is the same, consider the next letter
            if ord(word[n]) == ord(res[n]):
                n += 1
    return res


#Ask the user for the input string, separated by a space or comma
string = input("Input a list of words, seperated by space or comma: ")

# Find the first word in alphabetical order
first_word = findAlphabeticallyFirstWord(string)

# Print the result

print(first_word)