# NeuroNexus - B2Twin Digital Twin System

## 🎯 Overview
NeuroNexus is an AI-powered digital twin system for Biosphere 2, developed during the B2Twin Hackathon (March 22-23, 2025). The system provides real-time monitoring and analysis of environmental data using Streamlit and the Gemma 2B AI model.

## 🚀 Features
- Real-time environmental data visualization
- AI-powered trend analysis and insights
- Multi-parameter correlation analysis
- Interactive data exploration
- Historical data analysis
- Anomaly detection

## 🛠️ Tech Stack
- Python 3.9+
- Streamlit
- Pandas
- Plotly
- NumPy
- Ollama (Gemma 2B model)

## 📊 Data Format
The application expects CSV files with the following formats:

### Temperature Data
```csv
timestamp,temperature,humidity
2025-03-22 10:00:00,25.6,82.3
```

### CO₂ Data
```csv
timestamp,co2_level,pressure
2025-03-22 10:00:00,412.5,1013.2
```

### Radiation Data
```csv
timestamp,solar_radiation,par_level
2025-03-22 10:00:00,856.3,385.3
```

## 🏃‍♂️ Running the App

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start Ollama with Gemma 2B:
   ```bash
   ollama run gemma:2b
   ```

3. Launch the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure
```
neuronexus/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
└── data/              # Sample data directory
```

## 🤝 Contributing
This project was created during the B2Twin Hackathon 2025. Feel free to fork and extend!

## 📜 License
MIT License