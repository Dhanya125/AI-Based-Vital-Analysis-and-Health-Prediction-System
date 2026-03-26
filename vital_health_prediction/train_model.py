import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

def train_model(dataset_path):
    """
    Train ML model using your dataset
    Replace this with your actual ML code
    """
    
    # Load your dataset
    # Option 1: From local file
    # df = pd.read_csv(dataset_path)
    
    # Option 2: From Google Drive (download first)
    # You can use gdown or manually download
    
    # Example dataset structure (replace with your actual data)
    # Your dataset should have columns: heart_rate, spo2, temperature, condition
    
    # For demonstration, creating synthetic data
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'heart_rate': np.random.randint(50, 130, n_samples),
        'spo2': np.random.randint(85, 100, n_samples),
        'temperature': np.random.uniform(35, 39, n_samples),
        'condition': []
    }
    
    # Generate labels based on rules (replace with your actual labels)
    for i in range(n_samples):
        hr = data['heart_rate'][i]
        sp = data['spo2'][i]
        temp = data['temperature'][i]
        
        if hr > 100:
            data['condition'].append('Tachycardia')
        elif hr < 60:
            data['condition'].append('Bradycardia')
        elif sp < 95:
            data['condition'].append('Hypoxia')
        elif temp > 37.5:
            data['condition'].append('Fever')
        else:
            data['condition'].append('Normal')
    
    df = pd.DataFrame(data)
    
    # Prepare features and target
    X = df[['heart_rate', 'spo2', 'temperature']].values
    y = df['condition'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    accuracy = model.score(X_test_scaled, y_test)
    print(f"Model Accuracy: {accuracy:.2%}")
    
    # Save model and scaler
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/saved_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    print("Model saved to models/saved_model.pkl")
    return model, scaler

if __name__ == '__main__':
    # Replace with your actual dataset path
    dataset_path = 'data/raw/your_dataset.csv'
    
    if os.path.exists(dataset_path):
        train_model(dataset_path)
    else:
        print(f"Dataset not found at {dataset_path}")
        print("Training with synthetic data for demo...")
        train_model(None)