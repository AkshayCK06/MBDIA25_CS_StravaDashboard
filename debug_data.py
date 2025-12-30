
import pandas as pd
from src.data_manager import DataManager
from src.data_processing import ActivityProcessor

def debug():
    print("Loading data...")
    dm = DataManager()
    
    # Load raw dataframe
    df_raw = dm.load_activities_as_dataframe()
    
    # Process data
    print("\nProcessing data...")
    processor = ActivityProcessor(df_raw)
    df_proc = processor.df
    
    if 'average_speed_kmh' in df_proc.columns and 'type' in df_proc.columns:
        print("\n--- Average Speed by Type (km/h) ---")
        stats = df_proc.groupby('type')['average_speed_kmh'].describe()
        print(stats)
        
        print("\n--- Sample Rides (First 3) ---")
        print(df_proc[df_proc['type'] == 'Ride'][['name', 'distance_km', 'moving_time_min', 'average_speed_kmh']].head(3))
        
        print("\n--- Sample Walks (First 3) ---")
        print(df_proc[df_proc['type'] == 'Walk'][['name', 'distance_km', 'moving_time_min', 'average_speed_kmh']].head(3))
    else:
        print("Required columns for speed analysis missing.")

if __name__ == "__main__":
    debug()
