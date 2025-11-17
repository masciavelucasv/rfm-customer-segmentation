# 📊 RFM Customer Segmentation using Online Retail Dataset

This project performs **RFM (Recency, Frequency, Monetary)** customer segmentation using the **Online Retail** dataset from Kaggle.  
It groups customers into meaningful segments such as **Champions**, **Loyal Customers**, **At Risk**, **Lost**, and more—helping businesses understand customer value and retention patterns.

---

## 📁 Dataset Source

This project uses the **Online Retail Dataset**, originally from the  
**UCI Machine Learning Repository**, mirrored on Kaggle:

🔗 Dataset link:  
https://www.kaggle.com/datasets/tunguz/online-retail

⚠️ *The dataset is NOT included in this repository due to size and licensing restrictions.*

---

## 🛠️ Technologies Used

- Python  
- Pandas  
- NumPy  
- Matplotlib  
- Seaborn  
- Jupyter Notebook / VSCode  
- GitHub  

---

## 🧮 RFM Methodology

For each customer:

- **Recency** → Days since last purchase  
- **Frequency** → Number of transactions  
- **Monetary** → Total money spent  

Each metric is divided into 4 quantile-based scores (1–4), then combined:

