# Converts Udemy Subtitles in human readable ones
import re
import sys
from os.path import abspath, join, exists, basename, dirname, isdir


# ---------------------------- UTILS -------------------------------------
def __get_path__(relative_path):
    """
    Converts the relative path into an absolute path
    :param relative_path: string, relative path of the file
    :return: string
        absolute path: base path + relative path
    """
    try:
        # NOTE:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")
    return join(base_path, relative_path)

def remove_time_range(text):
    #removes the time range and the possible number of the block
    regex = r"(\n?[\d]*?)?\n?\d{1,2}:\d{2}(:\d{2})?(.|,)\d{1,3}((.|,)\d{1,3})?(( )?-->( )?|(,))\d{1,2}:\d{2}(:\d{2})?(.|,)\d{1,3}((.|,)\d{1,3})?( line:[\d]*% )?\n"
    return re.sub(regex, "", text)

def remove_webvtt(text):
    regex = r"WEBVTT -: |WEBVTT |WEBVTT\n"
    return re.sub(regex, "", text)

def remove_new_line(text):
    return text.replace("\n", " ")

def add_new_line(text):
    text = text.replace(" .", ".")
    return text.replace(". ", ".\n")

def remove_tag(text):
    regex1 = r"<v ->"
    regex2 = r"</v>"
    return re.sub(regex2, "", re.sub(regex1, "", text))

if __name__ == '__main__':
    print("\nWELCOME TO UdemySubs\n")
    close_program = False

    while not close_program:
        exit = False
        while not exit:
            #TODO input extension validation (.vtt, .srt, .txt)
            file_path = input("\nInsert the subtitles path file+name:\t")

            file_path = __get_path__(file_path)
            if not exists(file_path):
                exit = False
                print("\nFile not Found. Please Retry.\n")
            else:
                base_name = basename(file_path)

                exit = True
                try:
                    with open(file_path, 'r', encoding="UTF-8") as f:
                        print("\nProcessing ", base_name)
                        text = f.read()
                    text = remove_webvtt(remove_tag(add_new_line(remove_new_line(remove_time_range(text)))))
                    print("\n\n\n--------\tOUTPUT\t--------\n\n", text)
                except Exception:
                    print("\nFile not Found. Extension of the file not valid. Try with .vtt, .srt or .txt\n") #FIXME

        save = input("\n\nDo you want to save the output? Yes/y to continue:\t")
        if save.lower() == "y" or save.lower() == "yes":
            exists = False
            while not exists:
                file_path = input("Insert the output path file+name:\t")

                file_path = __get_path__(file_path)
                dir_name = dirname(file_path)
                if not isdir(dir_name):
                    print("\nPath not valid. Please Retry.\n")
                    exists = False
                else:
                    base_name = basename(file_path)
                    print("\nSaving ", base_name)
                    exists = True
                    with open(file_path, 'w', encoding="UTF-8") as f:
                        f.write(text)

        close = input("\nDo you want to perform another computation? Yes/y to continue:\t")
        if close.lower() == "y" or close.lower() == "yes":
            close_program = False
        else:
            close_program = True
            print("\nBye!\n")
