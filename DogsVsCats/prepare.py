
from os import listdir,path,makedirs
import zipfile
import shutil
import numpy as np

def initializeFolders(baseFolder,sampleFolder,trainingFolder,validationFolder):
    if path.exists(f'{baseFolder}/train'):
        shutil.rmtree(f'{baseFolder}/train')
    if path.exists(sampleFolder):
        shutil.rmtree(sampleFolder)
    if path.exists(trainingFolder):
        shutil.rmtree(trainingFolder)
    if path.exists(validationFolder):
        shutil.rmtree(validationFolder)
    archive = zipfile.ZipFile(f'{baseFolder}/train.zip', 'r')
    archive.extractall(baseFolder)
    archive.close()
    shutil.move(f'{baseFolder}/train',sampleFolder)

def getDogAndCatsSampleFiles(sampleFolder):
    sampleFiles= [f for f in listdir(sampleFolder) if path.isfile(path.join(sampleFolder, f))]
    dogSampleFiles=[{'Name':f,'IsValidation':False} for f in sampleFiles if f.startswith('dog') ]
    catSampleFiles=[{'Name':f,'IsValidation':False} for f in sampleFiles if f.startswith('cat') ]
    return dogSampleFiles,catSampleFiles

def getdValidationFileCount(sampleFiles):
    validationToTrainingRatio=0.1
    categoryFileCount=len(sampleFiles)
    return int(categoryFileCount*validationToTrainingRatio)

def getRandomlyChosenFileIndex(totalFile,requiredCount):
    deck = list(range(0, totalFile-1))
    np.random.shuffle(deck)
    return deck[0:requiredCount]    

def splitSampleToTrainingAndValidationFileCount(sampleFiles):
    validationFileCount=getdValidationFileCount(sampleFiles)
    chosenValidationFileIndex=getRandomlyChosenFileIndex(len(sampleFiles), validationFileCount)
    for i in chosenValidationFileIndex:
        sampleFiles[i]["IsValidation"] = True
    return [f['Name'] for f in sampleFiles if not f['IsValidation']],[f['Name'] for f in sampleFiles if f['IsValidation']]

def moveFiles(files, srcFolder,destinationFolder, initializeDestFolder=True):
    
    if initializeDestFolder:
        if path.exists(destinationFolder):
            shutil.rmtree(destinationFolder)
        makedirs(destinationFolder)        

    for file in files :
        shutil.move(f'{srcFolder}/{file}', destinationFolder)

def main():
    baseFolder=f'{path.dirname(path.abspath(__file__))}/data'
    sampleFolder=f'{baseFolder}/sample'
    trainingFolder=f'{baseFolder}/training'
    validationFolder=f'{baseFolder}/validation'
    
    initializeFolders( baseFolder, sampleFolder, trainingFolder, validationFolder )
    dogSampleFiles,catSampleFiles=getDogAndCatsSampleFiles(sampleFolder)
    
    dogTrainingFiles,dogValidationFiles=splitSampleToTrainingAndValidationFileCount(dogSampleFiles)
    catTrainingFiles,catValidationFiles=splitSampleToTrainingAndValidationFileCount(catSampleFiles)
    
    moveFiles( dogTrainingFiles, sampleFolder, f'{trainingFolder}/dogs' )
    moveFiles( dogValidationFiles, sampleFolder, f'{validationFolder}/dogs' )
    moveFiles( catTrainingFiles, sampleFolder, f'{trainingFolder}/cats' )
    moveFiles( catValidationFiles, sampleFolder, f'{validationFolder}/cats' )

    shutil.rmtree(sampleFolder)

main()