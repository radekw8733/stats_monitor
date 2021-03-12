import colorama
from datetime import datetime
import enum

# author: radke
# my private library for logging stuff etc..
class Logger():
    _printToTerminal = False
    _writeToFile = False
    _FileName = None
    _loggingLevel = 0
    def __init__(self,terminalWrite = True, fileNameToWrite = "",loggingLevel = 2) -> None:
        """Logger init

        Args:
            terminalWrite (bool, optional): Toggle logger to write output to terminal. Defaults to True.
            fileNameToWrite (str, optional): If not empty, logger will write logs to filename provided by this argument. Defaults to be empty.
            loggingLevel (int, optional): Terminal output logging level. 
            Levels: 1 - ERROR, 2 - INFO, 3 - DEGUG. Defaults to 2 - INFO.
        """
        self._loggingLevel = loggingLevel
        if terminalWrite == False:
            self._printToTerminal = False
        else:
            self._printToTerminal = True
        if fileNameToWrite != "":
            self._writeToFile = True
            self._FileName = open(fileNameToWrite, "a")
    def error(self,string):
        if self._printToTerminal == True and self._loggingLevel >= 1:
            print(datetime.now().strftime("[%H:%M:%S]") + colorama.Fore.RED + "[ERROR] " + string + colorama.Style.RESET_ALL)
        if self._writeToFile == True:
            self._FileName.write(datetime.now().strftime("[%H:%M:%S]") + "[ERROR] " + string)
    def info(self,string):
        if self._printToTerminal == True and self._loggingLevel >= 2:
            print(datetime.now().strftime("[%H:%M:%S]") + colorama.Fore.GREEN + "[INFO] " + string + colorama.Style.RESET_ALL)
        if self._writeToFile == True:
            self._FileName.write(datetime.now().strftime("[%H:%M:%S]") + "[INFO] " + string)
    def debug(self,string):
        if self._printToTerminal == True and self._loggingLevel >= 3:
            print(datetime.now().strftime("[%H:%M:%S]") + colorama.Fore.BLUE + "[DEBUG] " + string + colorama.Style.RESET_ALL)
        if self._writeToFile == True:
            self._FileName.write(datetime.now().strftime("[%H:%M:%S]") + "[DEBUG] " + string)

class loggingLevel(enum.Enum):
    ERROR = 1
    INFO = 2
    DEBUG = 3