import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import json
from typing import List, Dict

class StationReading:
    """Manages metadata and validates PM2.5 readings for a specific air quality station. (CO3)"""
    
    def __init__(self, station_id: str, location: str):
        self.station_id = station_id
        self.location = location
        self.readings: List[float] = []
        self.dates: List[str] = []

    def add_reading(self, date: str, pm25: float):
        """Validates and appends a PM2.5 reading. Rejects negative values. (CO1)"""
        if pm25 < 0:
            raise ValueError(f"Invalid reading {pm25} at {self.station_id}. PM2.5 cannot be negative.")
        self.readings.append(pm25)
        self.dates.append(date)

    def __len__(self) -> int:
        """Special method returning the total number of valid readings collected."""
        return len(self.readings)

def generate_simulated_data(filename: str):
    """Generates a reproducible, simulated CSV dataset. (CO2)"""
    dates = pd.date_range(start='2026-10-01', periods=30, freq='D')
    np.random.seed(42)
    
    data = []
    for station in ['ST-01', 'ST-02']:
        # Generate base PM2.5 data with a normal distribution
        base_pm25 = np.random.normal(loc=35.0, scale=10.0, size=30)
        
        # Inject realistic failure cases and anomalies (BL4)
        base_pm25[5] = 120.0  # Spike (e.g., local fire or sensor glitch)
        base_pm25[15] = -5.0  # Invalid negative reading to test validation
        
        for date, reading in zip(dates, base_pm25):
            data.append({'date': date.strftime('%Y-%m-%d'), 'station_id': station, 'pm25': round(reading, 2)})
            
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def analyze_and_plot(filename: str):
    # 1. File I/O & Class Implementation (CO2, CO3)
    stations: Dict[str, StationReading] = {
        'ST-01': StationReading('ST-01', 'North Campus'),
        'ST-02': StationReading('ST-02', 'South Campus')
    }
    
    valid_data = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                val = float(row['pm25'])
                # Passes data through the class validation method
                stations[row['station_id']].add_reading(row['date'], val)
                valid_data.append({'date': row['date'], 'station_id': row['station_id'], 'pm25': val})
            except ValueError as e:
                print(f"Validation Flag: {e}")

    # 2. NumPy Array Operations (CO4)
    df = pd.DataFrame(valid_data)
    pm25_array = df['pm25'].to_numpy()
    
    mean_pm25 = np.mean(pm25_array)
    std_pm25 = np.std(pm25_array)
    
    # Anomaly Rule: 2 Standard Deviations above the mean (BL5)
    threshold = mean_pm25 + (2 * std_pm25)
    anomalies = pm25_array[pm25_array > threshold]
    
    print(f"\n[NumPy Analysis] System Mean: {mean_pm25:.2f}, Anomaly Threshold: {threshold:.2f}")
    print(f"[NumPy Analysis] Anomalies detected: {anomalies}")

    # 3. Pandas Series/DataFrames and JSON Export (CO5)
    monthly_summary = df.groupby('station_id')['pm25'].agg(['mean', 'max', 'count']).reset_index()
    monthly_summary.to_json('monthly_summary.json', orient='records', indent=4)
    print("\n[Pandas] Station Summary Exported to JSON:")
    print(monthly_summary)

    # 4. Matplotlib Plots (CO6)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Time Series Trend
    for station_id in stations:
        station_data = df[df['station_id'] == station_id]
        ax1.plot(station_data['date'], station_data['pm25'], marker='o', label=station_id)
    
    ax1.axhline(y=threshold, color='red', linestyle='--', label=f'Anomaly Threshold ({threshold:.1f})')
    ax1.set_title('Daily PM2.5 Trends by Station')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('PM2.5 Concentration (µg/m³)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Histogram Distribution
    ax2.hist(df['pm25'], bins=12, color='steelblue', edgecolor='black', alpha=0.7)
    ax2.set_title('Distribution of Valid PM2.5 Readings')
    ax2.set_xlabel('PM2.5 Concentration (µg/m³)')
    ax2.set_ylabel('Frequency (Days)')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('air_quality_analysis.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    dataset_file = 'simulated_air_quality.csv'
    print("Generating simulated dataset...")
    generate_simulated_data(dataset_file)
    print("Running analysis pipeline...\n")
    analyze_and_plot(dataset_file)