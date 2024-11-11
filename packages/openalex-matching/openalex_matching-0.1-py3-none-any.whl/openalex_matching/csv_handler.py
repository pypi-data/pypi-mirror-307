import pandas as pd

def name_csv_reader(inputFileName):
    try:
        if not inputFileName.lower().endswith(".csv"):
            raise ValueError("Invalid input file format, only csv files are acceptable")
        
        df = pd.read_csv(inputFileName)

        # Check if 'Names' column exists
        if 'Names' in df.columns:
            namesArray = df['Names'].to_numpy()
        else:
            raise ValueError("'Names' column not found in input CSV file")
        
        return namesArray
    
    except FileNotFoundError:
        print("No file found")

def name_csv_writer(outputFileName, dataToWrite):

    if not isinstance(dataToWrite, dict):
        raise TypeError("Invalid Input, only can write from dictionary inputs")
    
    if not outputFileName.lower().endswith(".csv"):
        raise ValueError("Invalid output file format, only csv files are acceptable")
    
    df = pd.DataFrame.from_dict(dataToWrite)
    df.to_csv(outputFileName, index=False)
    print("data appended to csv")


       