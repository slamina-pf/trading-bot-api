
def clean_data(df):
    # Drop rows with NaN values
    df.dropna(inplace=True)
    
    # Drop duplicate rows
    df.drop_duplicates(inplace=True)
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    return df