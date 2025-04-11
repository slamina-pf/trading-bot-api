
def computing_outliers(df):
    numeric_columns = df.select_dtypes(include=['number']).columns
    
    if len(numeric_columns) == 0:
        print("No numeric columns available for outlier handling.")
        return df
    
    for column in numeric_columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
        
        mean_value = df[column].mean()
        df[column] = df[column].where(~outliers, mean_value)
    
    return df

def clean_data(df):
    # Drop rows with NaN values
    df.dropna(inplace=True)
    
    # Drop duplicate rows
    df.drop_duplicates(inplace=True)
    
    # Handling outliers
    df = computing_outliers(df)
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    return df