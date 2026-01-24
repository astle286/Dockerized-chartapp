# 📊 ChartApp

ChartApp is a sleek Flask web app for uploading CSV files, generating interactive charts with Plotly, and previewing your dataset with style. Built for clarity, speed, and delight.

![ChartApp UI](https://raw.githubusercontent.com/astle286/chartapp/main/assets/chartapp-ui.png)

---

## 🚀 Features

- 📁 Upload CSV files (only once per session)
- 🎨 Choose between light and dark chart themes
- 📈 Configure two charts independently (Chart A & Chart B)
- 📊 Select chart types: Line, Bar, Scatter, Pie
- 🧠 Multi-series plotting with dynamic dropdowns
- 🔍 Toggle between limited and full data preview
- 💡 Smooth transitions and animated theme switcher

---

## 🖼 Interface Preview

### Chart Configuration

![Chart Settings](https://raw.githubusercontent.com/astle286/chartapp/main/assets/chart-settings.png)

### Generated Charts

![Chart A & B](https://raw.githubusercontent.com/astle286/chartapp/main/assets/chart-output.png)

### Data Preview Toggle

![Data Preview](https://raw.githubusercontent.com/astle286/chartapp/main/assets/data-preview.png)

---

## 🛠 Tech Stack

- **Flask** — backend framework
- **Plotly Express** — chart rendering
- **Bootstrap 5** — responsive UI
- **Jinja2** — templating
- **JavaScript** — theme and preview toggles

---

## 📦 Setup

```bash
git clone https://github.com/astle286/chartapp.git
cd chartapp
pip install -r requirements.txt
flask run

🧠 Future Ideas
Export charts as PNG or PDF

DataTables integration for full preview

CSV download of filtered data

Chart sharing via link

📸 Screenshots
All screenshots are stored in /assets and used to showcase the app’s features.

🧑‍💻 Author
Built with joy by Astle  
Modular, maintainable, and made to delight.

📄 License
MIT License — feel free to fork, remix, and build on it.
