from flask import Flask, render_template, redirect, url_for, request
from pathlib import *
import os
import pandas as pd
import platform
import regex as re
import tempfile

app = Flask(__name__)

def _handleException(e):
    errorMSG = f'An unexpected error occurred: {str(e)}'
    return render_template('rs_error.html', error_msg = errorMSG)

def _getDF(filename: str): 
    data = pd.DataFrame()
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError("The file provided does not exist.")
    if path.suffix != '.csv':
        raise ValueError("The file provided is not a .csv file.")
    
    data = pd.read_csv(filepath_or_buffer = filename)
    return data

def _makeRegex(userData: dict, df: pd.DataFrame) -> pd.DataFrame:
    term1 = userData['term1']
    term2 = userData['term2']
    rangenum = str(userData['rangenum'])
    cwradio = userData['cwradio']
    adjcolnum = int(userData['colnum']) - 1

    basePattern1 = re.compile(re.escape(term1), re.IGNORECASE)
    basePattern2 = re.compile(re.escape(term2), re.IGNORECASE)

    if cwradio == 'char':
        rePattern = re.compile(r"((" + re.escape(term1) + r").{0," + re.escape(rangenum) + r"}(" + re.escape(term2) + r"))|(" + re.escape(term2) + r".{0," + re.escape(rangenum) + r'}(' + re.escape(term1) + r'))', re.IGNORECASE)
    else:
        rePattern = re.compile(r"((" + re.escape(term1) + r")(\W){0,}((\w){0,}(\W){0,}){0," + re.escape(rangenum) + r"}(" + re.escape(term2) + r"))|(" + re.escape(term2) + r"(\W){0,}((\w){0,}(\W){0,}){0," + re.escape(rangenum) + r"}(" + re.escape(term1) + r"))", re.IGNORECASE)

    searchSeries = df.iloc[:,adjcolnum]
    i = 0
    resultList = []
    for each in searchSeries:
        if pd.notna(each) and type(each) == str and re.search(basePattern1, each) != None and re.search(basePattern2, each) != None and re.search(rePattern, each) != None:
            resultList.append(df.iloc[i])
        i = i + 1

    resultDF = pd.DataFrame(resultList)
    return resultDF

def _getOutputFolder(filename: str) -> list:
    #cwdPath = Path(os.getcwd())
    cwdPath = Path(filename).resolve().parent
    if platform.system() == 'Windows':
        processedFolder = str(cwdPath) + '\\Output'
    else: 
        processedFolder = str(cwdPath) + '/Output'

    folderPath = Path(processedFolder)
    folderInfo = [processedFolder, folderPath]
    return folderInfo

def _getOutputFile(userData: dict, df: pd.DataFrame) -> None:
    csvname = userData['csvname']
    rangenum = str(userData['rangenum'])
    cwradio = userData['cwradio']
    colnum = int(userData['colnum'])
    processedFolder = userData['processedFolder']

    filename = Path(csvname).stem

    if platform.system() == "Windows":
        nameSuggestion = str(processedFolder) + '\\' + filename + '_processed_col' + str(colnum) + '_' + cwradio + rangenum
    else:
        nameSuggestion = str(processedFolder) + '/' + filename + '_processed_col' + str(colnum) + '_' + cwradio + rangenum

    processedPath = Path(nameSuggestion)
    if not processedPath.exists():
        processedPath = Path(nameSuggestion + '.csv')
    else:
        i = 0
        while processedPath.exists():
            newNameSuggestion = nameSuggestion + '(' + str(i) + ').csv'
            processedPath = Path(newNameSuggestion)
            i = i + 1
    
    userData['processedPath'] = processedPath
    
@app.route('/error/')
def error():
    return render_template('rs_error.html')

@app.route('/noresults/')
def no_results():
    return render_template('rs_noresults.html')

@app.route('/saved/', methods = ['POST'])
def saved():
    pickleDF = request.form.get('df_file')
    path = request.form.get('path')

    if not pickleDF or not path:
        errorMSG = "Required data is missing, and as a result, the CSV could not be saved."
        return render_template('rs_error.html', error_msg = errorMSG)
    
    try:
        df = pd.read_pickle(pickleDF)
    except (FileNotFoundError, ValueError) as e:
        errorMSG = 'The following error occured while trying to read in the provided data: ' + str(e)
        return render_template('rs_error.html', error_msg = errorMSG)
    except PermissionError:
        errorMSG = 'A permission error occureed while trying to access the data.'
        return render_template('rs_error.html', error_msg = errorMSG)
    
    try:
        os.remove(pickleDF)
    except (FileNotFoundError, ValueError) as e:
        errorMSG = 'The following error occured while trying to read in the provided data: ' + str(e)
        return render_template('rs_error.html', error_msg = errorMSG)
    
    path = request.form.get('path')

    try:
        df.to_csv(path_or_buf = path, encoding = 'utf-8', index = False, header = True)
    except (FileNotFoundError, ValueError) as e:
        errorMSG = 'The following error occured while trying to read in the provided data as a CSV: ' + str(e)
        return render_template('rs_error.html', error_msg = errorMSG)
    except PermissionError:
        errorMSG = 'A permission error occureed while trying to access the data.'
        return render_template('rs_error.html', error_msg = errorMSG)    
    
    if Path(path).exists():
        return render_template('rs_saved.html', path_msg = path)
    else:
        errorMSG = 'Your CSV could not be saved for an unknown reason.'
        return render_template('rs_error.html', error_msg = errorMSG)

@app.route('/results/')
def results():
    csvname = request.args.get('csvname')
    term1 = request.args.get('term1')
    term2 = request.args.get('term2')
    rangenum = request.args.get('rangenum')
    cwradio = request.args.get('cwradio')
    colnum = request.args.get('colnum')
    processedFolder = ''
    processedPath = ''

    try:
        df = _getDF(csvname)
    except FileNotFoundError:
        msg = 'The filepath you provided was not found.  \
                Please check to make sure that you typed it in correctly.  You can click on the file name \
                in you can double click on the file in your File Explorer and copy the path there.'
        return render_template('rs_error.html', error_msg = msg)
    except ValueError:
        msg = 'The file path you provided was not a CSV file. Please check to make sure that the \
                file your working with is a CSV and that you typed it in correctly.  You can click \
                on the file name in you can double click on the file in your File Explorer and copy the path there.'
        return render_template('rs_error.html', error_msg = msg)
    
    inputDict = {
        'csvname': csvname,
        'term1': term1,
        'term2': term2,
        'rangenum': rangenum,
        'cwradio': cwradio,
        'colnum': colnum,
        'processedFolder': processedFolder,
        'pickle': ''
    }
    resultDF = _makeRegex(inputDict, df)
    pickleDF = tempfile.NamedTemporaryFile(delete = False, suffix = '.pkl')
    resultDF.to_pickle(pickleDF.name)
    if pickleDF:
        print('pickleDF exists')
    else:
        print('pickleDF does not exist')
    inputDict['pickle'] = pickleDF.name
    print(inputDict.get('pickle'))
    ltdDF = resultDF.iloc[:10,:10]

    if len(resultDF) != 0:
        folderInfo = _getOutputFolder(csvname)
        try:
            folderInfo[1].mkdir()
            saveMSG = f"Directory '{folderInfo[0]}' created successfully."
        except FileExistsError:
            saveMSG = f"Directory '{folderInfo[0]}' already exists."
        except PermissionError:
            saveMSG = f"Permission denied: Unable to create '{folderInfo[0]}'."
            return render_template('rs_error.html', error_msg = saveMSG)
        except Exception as e:
            saveMSG = f"An error occurred: {e}"
            return render_template('rs_error.html', error_msg = saveMSG)

        inputDict['processedFolder'] = folderInfo[0]
        _getOutputFile(inputDict, resultDF)
        print(inputDict.get('processedPath'))
        return render_template('rs_results.html', df = ltdDF, userData = inputDict)
    else: 
        return render_template('rs_noresults.html')

@app.route('/')
def home():
   return render_template('rs_forum.html')

def main():
    app.run()