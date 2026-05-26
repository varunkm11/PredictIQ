import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import os
import sys

# Add root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from model.auto_trainer import (
    train_on_dataset,
    load_metadata,
    predict_single,
    detect_column_types
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PredictIQ",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0a0e1a; color: #e0e0e0; }
    .main  { background-color: #0a0e1a; }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #7c83fd, #ff6b9d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-sub {
        color: #8892b0;
        font-size: 1.1rem;
        margin-top: 4px;
    }
    .card {
        background: linear-gradient(135deg, #131929, #1a2035);
        border: 1px solid #2a3050;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .step-badge {
        background: linear-gradient(135deg, #00d4ff22, #7c83fd22);
        border: 1px solid #7c83fd55;
        border-radius: 50%;
        width: 32px; height: 32px;
        display: inline-flex;
        align-items: center; justify-content: center;
        font-weight: bold; color: #7c83fd;
        margin-right: 10px;
    }
    .metric-box {
        background: #131929;
        border: 1px solid #2a3050;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00d4ff;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8892b0;
        margin-top: 4px;
    }
    .tag {
        display: inline-block;
        background: #1a2035;
        border: 1px solid #2a3050;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.8rem;
        color: #7c83fd;
        margin: 3px;
    }
    .success-box {
        background: #0d2818;
        border: 1px solid #21c45d55;
        border-radius: 12px;
        padding: 16px 20px;
        color: #21c45d;
    }
    .warning-box {
        background: #2a1a00;
        border: 1px solid #ff990055;
        border-radius: 12px;
        padding: 16px 20px;
        color: #ffaa00;
    }
    .danger-box {
        background: #2a0a0a;
        border: 1px solid #ff4b4b55;
        border-radius: 12px;
        padding: 16px 20px;
        color: #ff4b4b;
    }
    div[data-testid="stMetricValue"] { color: #00d4ff !important; }
    .stProgress > div > div { background: linear-gradient(90deg, #00d4ff, #7c83fd); }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="hero-title" style="font-size:1.8rem">🔮 PredictIQ</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">AutoML Inference Platform</p>', unsafe_allow_html=True)
    st.divider()

    page = st.radio(
        "Navigate",
        ["🏠 Home", "📂 Train Model", "🔮 Predict", "📊 Monitoring", "ℹ️ About"],
        index=0
    )

    st.divider()

    # Model status
    metadata = load_metadata()
    if metadata:
        st.markdown("**✅ Model Trained**")
        st.caption(f"Target: `{metadata['target_column']}`")
        st.caption(f"Accuracy: `{metadata['accuracy']*100:.1f}%`")
        st.caption(f"Rows: `{metadata['total_rows']:,}`")
        st.caption(f"Version: `{metadata['model_version']}`")
    else:
        st.markdown("**⚠️ No Model Trained**")
        st.caption("Go to Train Model to get started.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":
    st.markdown('<h1 class="hero-title">PredictIQ</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Upload any dataset. Pick your target. Get predictions instantly.</p>', unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>📂 Step 1</h3>
            <p>Upload any CSV dataset — churn, fraud, loan default, disease, returns.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>🎯 Step 2</h3>
            <p>Pick your target column. PredictIQ auto-detects features and trains XGBoost.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <h3>🔮 Step 3</h3>
            <p>Predict on single customers or batch upload thousands of rows instantly.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🗂️ Datasets You Can Use")

    datasets = [
        ("🏦", "Credit Card Fraud",     "fraud detection",       "Kaggle: Credit Card Fraud Detection"),
        ("📱", "Customer Churn",         "churn prediction",      "Kaggle: Telco Customer Churn"),
        ("💰", "Loan Default",           "risk assessment",       "Kaggle: Home Credit Default Risk"),
        ("🏥", "Patient Readmission",    "healthcare ML",         "Kaggle: Diabetes 130 Hospitals"),
        ("🛒", "Product Returns",        "e-commerce ML",         "Kaggle: E-Commerce Returns"),
        ("✈️", "Flight Delay",           "delay prediction",      "Kaggle: Flight Delay Prediction"),
    ]

    c1, c2 = st.columns(2)
    for i, (icon, name, tag, source) in enumerate(datasets):
        col = c1 if i % 2 == 0 else c2
        with col:
            st.markdown(f"""
            <div class="card">
                <b>{icon} {name}</b>
                <span class="tag">{tag}</span>
                <p style="color:#8892b0;font-size:0.85rem;margin-top:6px">📥 {source}</p>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — TRAIN MODEL
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📂 Train Model":
    st.title("📂 Train on Your Dataset")
    st.markdown("Upload any CSV — PredictIQ handles the rest automatically.")
    st.divider()

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"],
        help="Any classification dataset with a 0/1 or Yes/No target column"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded: **{uploaded_file.name}** — {len(df):,} rows × {len(df.columns)} columns")

            # Dataset preview
            with st.expander("👀 Preview Dataset", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)

            st.divider()

            # Column info
            col1, col2 = st.columns(2)
            numeric_cols, categorical_cols = detect_column_types(df)

            with col1:
                st.markdown("**🔢 Numeric Columns**")
                for c in numeric_cols:
                    st.markdown(f'<span class="tag">{c}</span>', unsafe_allow_html=True)

            with col2:
                st.markdown("**🔤 Categorical Columns**")
                if categorical_cols:
                    for c in categorical_cols:
                        st.markdown(f'<span class="tag">{c}</span>', unsafe_allow_html=True)
                else:
                    st.caption("None detected")

            st.divider()

            # Target column selection
            st.subheader("🎯 Select Target Column")
            st.caption("This is the column you want to predict (must be 0/1 or Yes/No or similar binary values)")

            # Smart suggestion — find likely target columns
            likely_targets = []
            for col in df.columns:
                unique_vals = df[col].nunique()
                col_lower = col.lower()
                if unique_vals == 2:
                    likely_targets.append(col)
                elif any(word in col_lower for word in ["churn","fraud","default","return","delay","target","label","outcome","result","status"]):
                    likely_targets.append(col)

            if likely_targets:
                st.info(f"💡 Suggested target columns: {', '.join([f'`{c}`' for c in likely_targets[:3]])}")

            target_col = st.selectbox(
                "Choose Target Column",
                options=df.columns.tolist(),
                index=df.columns.tolist().index(likely_targets[0]) if likely_targets else 0
            )

            # Show target distribution
            if target_col:
                st.markdown(f"**Target Distribution for `{target_col}`:**")
                value_counts = df[target_col].value_counts()
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    st.dataframe(value_counts.reset_index(), use_container_width=True)
                with col_b:
                    st.bar_chart(value_counts)

            st.divider()

            # Train button
            if st.button("🚀 Train Model Now", type="primary", use_container_width=True):
                with st.spinner("Training model... this takes 10-30 seconds"):
                    try:
                        accuracy, report, feature_names, target_classes, metadata = train_on_dataset(
                            df, target_col
                        )

                        st.balloons()

                        st.markdown(f"""
                        <div class="success-box">
                            ✅ <b>Model trained successfully!</b><br>
                            Accuracy: <b>{accuracy*100:.2f}%</b> on test set
                        </div>
                        """, unsafe_allow_html=True)

                        st.divider()

                        # Results
                        r1, r2, r3, r4 = st.columns(4)
                        r1.metric("Accuracy",  f"{accuracy*100:.1f}%")
                        r2.metric("Features",  len(feature_names))
                        r3.metric("Classes",   len(target_classes))
                        r4.metric("Train Rows", f"{int(len(df)*0.8):,}")

                        st.subheader("📊 Classification Report")
                        report_df = pd.DataFrame(report).transpose().round(3)
                        st.dataframe(report_df, use_container_width=True)

                        st.subheader("✅ Features Used")
                        for f in feature_names:
                            st.markdown(f'<span class="tag">{f}</span>', unsafe_allow_html=True)

                        st.info("👉 Now go to **🔮 Predict** to make predictions!")

                    except Exception as e:
                        st.error(f"Training failed: {str(e)}")
                        st.caption("Common issues: target column has >2 unique values, too many nulls, or non-numeric data.")

        except Exception as e:
            st.error(f"Could not read CSV: {str(e)}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — PREDICT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔮 Predict":
    st.title("🔮 Make Predictions")

    metadata = load_metadata()

    if metadata is None:
        st.warning("⚠️ No model trained yet. Go to **📂 Train Model** first.")
        st.stop()

    st.success(f"✅ Using model trained on `{metadata['target_column']}` — Accuracy: {metadata['accuracy']*100:.1f}%")
    st.divider()

    predict_mode = st.tabs(["👤 Single Prediction", "📁 Batch Prediction"])

    # ── Single Prediction ──────────────────────────────────────────────────────
    with predict_mode[0]:
        st.subheader("Enter Feature Values")
        st.caption("Fill in values for each feature the model was trained on.")

        feature_names  = metadata["feature_names"]
        numeric_cols   = metadata["numeric_cols"]
        categorical_cols = metadata["categorical_cols"]

        # Load training data for reference ranges
        train_df = None
        if os.path.exists("model/train_data.csv"):
            try:
                train_df = pd.read_csv("model/train_data.csv")
            except:
                pass

        input_values = {}
        cols = st.columns(2)

        for i, feature in enumerate(feature_names):
            col = cols[i % 2]
            with col:
                if feature in categorical_cols and train_df is not None and feature in train_df.columns:
                    unique_vals = train_df[feature].dropna().unique().tolist()
                    input_values[feature] = st.selectbox(f"{feature}", unique_vals, key=f"feat_{feature}")

                elif feature in numeric_cols and train_df is not None and feature in train_df.columns:
                    col_data  = train_df[feature].dropna()
                    min_val   = float(col_data.min())
                    max_val   = float(col_data.max())
                    mean_val  = float(col_data.mean())
                    input_values[feature] = st.number_input(
                        f"{feature}",
                        min_value=min_val,
                        max_value=max_val,
                        value=mean_val,
                        key=f"feat_{feature}"
                    )
                else:
                    input_values[feature] = st.text_input(f"{feature}", value="0", key=f"feat_{feature}")

        st.divider()

        if st.button("🔮 Predict", type="primary", use_container_width=True):
            with st.spinner("Running prediction..."):
                try:
                    result = predict_single(input_values)

                    st.divider()
                    st.subheader("📊 Result")

                    target_classes = metadata.get("target_classes", ["0","1"])
                    probs = result["probabilities"]

                    # Show metrics
                    mc = st.columns(len(probs) + 1)
                    mc[0].metric("Prediction", result["prediction_label"])
                    for j, (cls, prob) in enumerate(probs.items()):
                        mc[j+1].metric(f"P({cls})", f"{prob*100:.1f}%")

                    # Confidence bar
                    st.markdown("**Confidence:**")
                    st.progress(result["confidence"])

                    # Verdict
                    confidence = result["confidence"]
                    if confidence >= 0.8:
                        st.markdown(f'<div class="success-box">🎯 High Confidence Prediction — {confidence*100:.1f}%</div>', unsafe_allow_html=True)
                    elif confidence >= 0.6:
                        st.markdown(f'<div class="warning-box">⚠️ Medium Confidence — {confidence*100:.1f}% — review manually</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="danger-box">❗ Low Confidence — {confidence*100:.1f}% — uncertain prediction</div>', unsafe_allow_html=True)

                    with st.expander("🔧 Raw Output"):
                        st.json(result)

                except Exception as e:
                    st.error(f"Prediction failed: {str(e)}")

    # ── Batch Prediction ───────────────────────────────────────────────────────
    with predict_mode[1]:
        st.subheader("📁 Batch Prediction")
        st.caption(f"Upload a CSV with these columns: `{', '.join(metadata['feature_names'])}`")

        batch_file = st.file_uploader("Upload CSV for batch prediction", type=["csv"], key="batch_upload")

        if batch_file:
            batch_df = pd.read_csv(batch_file)
            st.dataframe(batch_df.head(), use_container_width=True)
            st.caption(f"{len(batch_df):,} rows detected")

            if st.button("🚀 Run Batch Predictions", type="primary"):
                results = []
                progress = st.progress(0)
                status   = st.empty()

                for i, row in batch_df.iterrows():
                    try:
                        result = predict_single(row.to_dict())
                        row_result = row.to_dict()
                        row_result["Prediction"]  = result["prediction_label"]
                        row_result["Confidence"]  = f"{result['confidence']*100:.1f}%"
                        for cls, prob in result["probabilities"].items():
                            row_result[f"P({cls})"] = f"{prob*100:.1f}%"
                        results.append(row_result)
                    except:
                        pass

                    progress.progress((i + 1) / len(batch_df))
                    status.caption(f"Processing {i+1}/{len(batch_df)}...")

                status.empty()

                if results:
                    result_df = pd.DataFrame(results)
                    st.success(f"✅ Done! {len(results):,} predictions made.")
                    st.dataframe(result_df, use_container_width=True)

                    # Stats
                    pred_counts = result_df["Prediction"].value_counts()
                    st.bar_chart(pred_counts)

                    # Download
                    csv = result_df.to_csv(index=False)
                    st.download_button(
                        "⬇️ Download Results CSV",
                        data=csv,
                        file_name="batch_predictions.csv",
                        mime="text/csv",
                        type="primary"
                    )

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — MONITORING
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Monitoring":
    st.title("📊 Model Monitoring")

    metadata = load_metadata()
    if metadata is None:
        st.warning("No model trained yet.")
        st.stop()

    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Model Accuracy",  f"{metadata['accuracy']*100:.1f}%")
    c2.metric("Total Features",  len(metadata["feature_names"]))
    c3.metric("Training Rows",   f"{metadata['total_rows']:,}")
    c4.metric("Target Classes",  len(metadata["target_classes"]))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Features Used")
        for f in metadata["feature_names"]:
            st.markdown(f'<span class="tag">{f}</span>', unsafe_allow_html=True)

    with col2:
        st.subheader("📌 Model Info")
        st.json({
            "target_column":  metadata["target_column"],
            "target_classes": metadata["target_classes"],
            "model_version":  metadata["model_version"],
            "trained_at":     metadata["trained_at"],
            "accuracy":       metadata["accuracy"]
        })

    # Training data distribution
    if os.path.exists("model/train_data.csv"):
        st.divider()
        st.subheader("📈 Training Data Distribution")
        train_df = pd.read_csv("model/train_data.csv")
        target   = metadata["target_column"]

        if target in train_df.columns:
            st.bar_chart(train_df[target].value_counts())

        st.subheader("📊 Feature Statistics")
        numeric_cols = metadata["numeric_cols"]
        available    = [c for c in numeric_cols if c in train_df.columns]
        if available:
            st.dataframe(train_df[available].describe().round(2), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "ℹ️ About":
    st.title("ℹ️ About PredictIQ")
    st.divider()

    st.markdown("""
    ## PredictIQ — AutoML Inference Platform

    Upload **any binary classification dataset**, pick your target column,
    and get a production-ready prediction API instantly.
    """)

    st.subheader("🛠️ Tech Stack")
    st.markdown("""
    | Component | Technology |
    |-----------|-----------|
    | ML Model  | XGBoost + Scikit-learn Pipeline |
    | AutoML    | Auto feature detection + preprocessing |
    | API Server | FastAPI |
    | Frontend  | Streamlit |
    | Containerization | Docker |
    | CI/CD     | GitHub Actions |
    """)

    st.subheader("✅ Supported Datasets")
    st.code("""
Any CSV with:
- Binary target column (0/1, Yes/No, True/False)
- Any mix of numeric and categorical features
- Missing values handled automatically
- No preprocessing needed
    """)

    st.subheader("📚 Learn More")
    st.markdown("""
    - **Source Code**: [GitHub](https://github.com/)
    - **Documentation**: Full docs coming soon
    - **API Docs**: Check `/docs` endpoint
    """)
