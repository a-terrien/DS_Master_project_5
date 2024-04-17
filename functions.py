import numpy as np
import pandas as pd

# Création d'une liste de colonnes catégorique à partir d'un dataframe
def separate_feat_by_dtype(df):
    # Identify categorical, float, integer, time-related, and binary columns
    null_ft = list(df.columns[df.isnull().all()])
    binary_ft = [ft for ft in df.columns if df[ft].nunique() == 2]
    constant_ft = [ft for ft in df.columns if df[ft].nunique() == 1]
    # Get list of columns with low variance
    low_var_ft = binary_cols + constant_cols + null_columns
    # Drop low variance columns from temporary dataframe
    temp_df = df.copy()
    temp_df.drop(columns=low_var_cols, inplace=True)
    categorical_ft =  list(temp_df.select_dtypes(include=['object', 'category']).columns)
    float_ft =  list(temp_df.select_dtypes(include=['float']).columns)
    integer_ft =  list(temp_df.select_dtypes(include=['int']).columns)
    time_ft =  list(temp_df.select_dtypes(include=['datetime64[ns]', 'timedelta64[ns]']).columns)

    # Generate summary message
    print("The table contains:")
    print(f"- {len(categorical_ft)} categorical columns")
    print(f"- {len(float_ft)} float columns")
    print(f"- {len(integer_ft)} integer columns")
    print(f"- {len(time_ft)} time-related columns")
    print(f"- {len(binary_ft)} binary columns")
    print(f"- {len(constant_ft)} constant columns")
    print(f"- {len(null_ft)} columns with only NAs.")
    display(df.head(4))
    return categorical_ft, float_ft, integer_ft, time_ft, binary_ft, constant_ft, null_ft
  
def reduce_memory_usage(df):
    # Get initial memory usage of the dataframe
    start_mem = df.memory_usage().sum() / 1024 ** 2
    
    # Loop through each column
    for col in df.columns:
        col_type = df[col].dtype
        
        # Convert object to category if less than 50% unique values
        if col_type == 'object':
            if len(df[col].unique()) / len(df[col]) < 0.5:
                df[col] = df[col].astype('category')
                continue
                
        # Convert int64 to int32 or int16 if it can fit
        if col_type == 'int64':
            col_min = df[col].min()
            col_max = df[col].max()
            if col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                df[col] = df[col].astype(np.int32)
            elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                df[col] = df[col].astype(np.int16)
                
        # Convert float64 to float32 or float16 if it can fit
        if col_type == 'float64':
            col_min = df[col].min()
            col_max = df[col].max()
            if col_min >= np.finfo(np.float32).min and col_max <= np.finfo(np.float32).max:
                df[col] = df[col].astype(np.float32)
            elif col_min >= np.finfo(np.float16).min and col_max <= np.finfo(np.float16).max:
                df[col] = df[col].astype(np.float16)
    
    # Get final memory usage of the dataframe
    end_mem = df.memory_usage().sum() / 1024 ** 2
    print(f"Memory usage reduced from {start_mem:.2f} MB to {end_mem:.2f} MB")
    return df