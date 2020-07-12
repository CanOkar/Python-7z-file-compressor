import datetime
import glob
import hashlib
import os


class Logging:
    def create(self):
        open("log.txt", "a")  # creates a file named "log.txt" if it does not exist

    def today(self):
        logFile = open("log.txt", "a")
        logFile.write("----------------------------------------" + str(datetime.date.today())+
                      "----------------------------------------\n")
        logFile.close()

    def started(self):
        logFile.write("Compression process has started on " + str(datetime.datetime.now()) + "\n")
        logFile.close()

    def finished(self):
        logFile = open("log.txt", "a")
        logFile.write("Compression process has finished on " + str(datetime.datetime.now()) + "\n")
        logFile.write(str(datetime.date.today()) + ".7z file has been successfully created \n")
        logFile.write("--------------------------------------------------------------"
                      "---------------------------\n")
        logFile.close()


def calculateHash(fileName):  # purpose of calculateHash is obvious as its name :)
    opnToReadHash = open(fileName, 'rb')
    hashValue = hashlib.sha256()  # creates a pre-described sha256 variable
    while bytesOfFile := opnToReadHash.read(8192):  # chops big files into parts
        hashValue.update(bytesOfFile)
    return hashValue.hexdigest()


createLogFile = Logging()
createLogFile.create()

logDateofToday = Logging()
logDateofToday.today()

FDBfiles = glob.glob('*.FDB')  # reads file names from disk
collectionOfHashes = {}

for FDBfile in FDBfiles:  # fills dictionary with calculated hash and corresponding file name
    collectionOfHashes[FDBfile] = calculateHash(FDBfile)

logFile = open("log.txt", "a")
logFile.write("Calculated hashes: \n")
for keyName, value in collectionOfHashes.items():
    logFile.write(keyName + ": " + value + "\n")
logFile.close()

willBeDeleted = []
x = 1
y = 1

for dbName, calculatedHash in collectionOfHashes.items():

    for i in range(x, len(collectionOfHashes)):
        hsh = tuple(collectionOfHashes.items())[i][y]
        if calculatedHash == hsh:
            y = y - 1
            dbNameDel = tuple(collectionOfHashes.items())[i][y]
            willBeDeleted.append(dbNameDel)
            y = 1
    x += 1

willBeDeleted = list(set(willBeDeleted))

logFile = open("log.txt", "a")
logFile.write("Deleted files because of being same : \n")
for yx in willBeDeleted:
    os.remove(yx)
    logFile.write(yx + " Deleted \n")


compressionStarted = Logging()
compressionStarted.started()

os.system("start /wait cmd /c 7z.exe a -t7z -m0=lzma2 -mx=9 -sdel compressed.7z *.FDB")

os.rename("compressed.7z", str(datetime.date.today()) + ".7z")

compressionFinished = Logging()
compressionFinished.finished()
