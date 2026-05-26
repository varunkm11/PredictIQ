# 🚀 Streamlit Cloud Deployment Guide

## Quick Start

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Your code pushed to a GitHub repository

---

## Deployment Steps

### 1. **Prepare Your GitHub Repository**

Ensure your repository has this structure:
```
PredictIQ/
├── app.py                    # Entry point (at root)
├── requirements.txt          # All dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml.example # Secrets template (for reference)
├── model/
│   ├── auto_trainer.py
│   ├── train_data.csv
│   └── model_metadata.json
├── api/
│   ├── main.py
│   └── schemas.py
├── .gitignore
└── README.md
```

**✅ Your project is ready!** The root `app.py` is the entry point.

---

### 2. **Push to GitHub**

```bash
git init
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/PredictIQ.git
git push -u origin main
```

---

### 3. **Deploy on Streamlit Cloud**

1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Click **"New app"**
3. Select:
   - **Repository**: `YOUR-USERNAME/PredictIQ`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **"Deploy"** and wait 2-3 minutes

---

### 4. **App URL**

Your app will be live at:
```
https://predictiq.streamlit.app
```
(Actual URL depends on repo name and Streamlit's subdomain)

---

## Configuration Files Explained

### `.streamlit/config.toml`
- **Theme**: Dark theme with gradient colors matching your app
- **Client Settings**: Shows error details for debugging
- **Server Settings**: Standard Streamlit Cloud settings

### `requirements.txt`
All Python dependencies are already included:
- `streamlit==1.40.0` - Frontend framework
- `fastapi==0.115.0` - API (optional for Cloud)
- `xgboost==2.1.1` - ML model
- `scikit-learn==1.5.2` - ML preprocessing
- And other dependencies

---

## Secrets Management (Optional)

If you need API keys or database credentials:

1. On Streamlit Cloud dashboard, go to your app
2. Click **"Settings"** → **"Secrets"**
3. Add your secrets in TOML format:
   ```toml
   API_URL = "https://api.example.com"
   API_KEY = "your-secret-key"
   ```

4. Access in your code:
   ```python
   import streamlit as st
   api_key = st.secrets["API_KEY"]
   ```

---

## Troubleshooting

### ❌ "Module not found" errors
- **Solution**: Check `requirements.txt` has all imports

### ❌ "app.py not found"
- **Solution**: Ensure `app.py` is at the repository root

### ❌ App takes too long to load
- **Solution**: Consider optimizing imports or caching:
  ```python
  @st.cache_resource
  def load_model():
      return joblib.load("model/model.pkl")
  ```

### ❌ Memory/Storage issues
- **Solution**: Streamlit Cloud has limits:
  - Max 1 GB RAM per app
  - 1 GB storage
  - Consider removing large cached files from git

---

## Post-Deployment

### Monitor Your App
- **Logs**: Click app → **"Logs"** tab
- **Usage**: Dashboard shows active users, visits
- **Settings**: Rerun policy, secrets, environment

### Update Your App
Just push new changes to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```
Streamlit Cloud auto-redeploys within seconds!

---

## Advanced: Custom Domain

To use your own domain (e.g., `predictiq.yourcompany.com`):

1. Go to app **Settings** → **Custom Domain**
2. Configure DNS records as shown
3. Update your domain registrar

---

## Performance Tips

1. **Cache expensive operations**:
   ```python
   @st.cache_data
   def train_model(df):
       return train_on_dataset(df)
   ```

2. **Lazy load data**:
   ```python
   if uploaded_file:
       df = pd.read_csv(uploaded_file)
   ```

3. **Use `.streamlit/config.toml` for optimization**:
   ```toml
   [client]
   toolbarMode = "minimal"
   
   [logger]
   level = "warning"
   ```

---

## Resources

- 📚 [Streamlit Docs](https://docs.streamlit.io/)
- 🚀 [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- 💬 [Community Forum](https://discuss.streamlit.io/)
- 🐛 [GitHub Issues](https://github.com/streamlit/streamlit/issues)

---

## Summary Checklist

- ✅ `app.py` at root level
- ✅ `requirements.txt` with all dependencies
- ✅ `.streamlit/config.toml` configured
- ✅ `.gitignore` prevents secrets from being committed
- ✅ Code pushed to GitHub (`main` branch)
- ✅ GitHub repository linked to Streamlit Cloud
- ✅ App deployed and running!

Happy deploying! 🎉
