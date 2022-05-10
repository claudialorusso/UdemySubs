# Converts Udemy Subtitles in human readable ones
import re
import sys
from os import path

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
        # It's a runtime computation. don't worry about the inline warning.
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")
    return path.join(base_path, relative_path)

def remove_time_range(text):
    #removes the time range and the possible number of the block
    regex = r"\n?[\d]*?\n\d{2}:\d{2}:\d{2}(.|,)\d{3} --> \d{2}:\d{2}:\d{2}(.|,)\d{3}( line:[\d]*% )?\n|\n?[\d]*?\n\d{2}:\d{2}(.|,)\d{3} --> \d{2}:\d{2}(.|,)\d{3}( line:[\d]*% )?"
    return re.sub(regex, "", text)

def remove_webvtt(text):
    regex = r"WEBVTT -: |WEBVTT "
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
    #TODO Input validation
    file_path = input("Insert the subtitles path file:\t")
    file_path = __get_path__(file_path)
    #file_name = path.basename(file_path)
    #file_output_name = file_name + "_readable.txt"
    #file_output_path = input("Where do you want to save the output?:\t")
    #file_output_path = __get_path__(file_output_path)
    with open(file_path, 'r', encoding="UTF-8") as f:
        text = f.read()
    text = remove_webvtt(remove_tag(add_new_line(remove_new_line(remove_time_range(text)))))

    print("\n\n\n--------\tOUTPUT\t--------\n\n", text)

