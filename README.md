# 🛠️ MaintWatch

**MaintWatch** is a modular Streamlit dashboard for visualizing aircraft maintenance data, detecting anomalies, and analyzing technician and pilot performance. Built for aviation safety professionals, it supports relational data exploration across ATA chapters, components, and personnel.

---

## 🚀 Features

- Upload or use sample maintenance logs
- Detect anomalies using z-score thresholds
- Filter by aircraft, component, technician, pilot, and ATA chapter
- Visualize trends and outliers with Altair charts
- Summarize performance by technician, pilot, and ATA chapter
- Download flagged anomalies as CSV

---

## 📁 Folder Structure

MaintWatch/
├── .streamlit/
│   └── config.toml               # Theme and server settings
├── pages/
│   ├── Anomalies.py              # Filtered view + chart
│   ├── Technicians.py            # Technician performance
│   ├── Pilots.py                 # Pilot performance
│   └── ATA_Summary.py           # ATA chapter insights
├── data/
│   ├── sample_maintenance.csv   # Sample log
│   ├── components.csv            # Component metadata
│   ├── ames.csv                  # Technician data (renamed)
│   └── pilots.csv                # Pilot data
├── utils/
│   └── data_loader.py           # Shared load/merge/anomaly logic
├── Home.py                       # Landing page
├── requirements.txt              # Dependencies
└── README.md                     # This file



---

## 🧪 Sample Data

Sample files are provided in the `data/` folder. These include:
- Realistic DO-228 components with ATA chapters
- Technicians (`ames.csv`) and pilots with experience and base info
- Maintenance records with varied `hours_since_last` for anomaly detection

---

## 🧰 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/MaintWatch.git
cd MaintWatch

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run Home.py
