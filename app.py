import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="U.S. Cardiovascular Health Dashboard",
    page_icon="🫀",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .stApp {
      background-color: #f7f9fc;
  }

  [data-testid="metric-container"] {
      background: white;
      border-left: 5px solid #c0392b;
      border-radius: 12px;
      padding: 14px 18px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }

  h1, h2, h3 {
      color: #1a3f6f;
  }

  [data-testid="stSidebar"] {
      background-color: #1a3f6f;
  }

  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3,
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] li {
      color: white !important;
  }

  .block-container {
      padding-top: 2rem;
      padding-bottom: 2rem;
  }
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    state_data = pd.DataFrame({
        "State": [
            "Alabama","Alaska","Arizona","Arkansas","California","Colorado",
            "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho",
            "Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana",
            "Maine","Maryland","Massachusetts","Michigan","Minnesota",
            "Mississippi","Missouri","Montana","Nebraska","Nevada",
            "New Hampshire","New Jersey","New Mexico","New York",
            "North Carolina","North Dakota","Ohio","Oklahoma","Oregon",
            "Pennsylvania","Rhode Island","South Carolina","South Dakota",
            "Tennessee","Texas","Utah","Vermont","Virginia","Washington",
            "West Virginia","Wisconsin","Wyoming"
        ],
        "Death_Rate": [
            247.8,158.2,148.3,234.6,141.5,131.7,140.5,183.4,172.3,197.2,
            95.4,154.7,183.1,212.5,173.2,188.4,243.1,238.7,181.3,163.2,
            137.8,201.4,148.6,262.3,218.4,162.1,172.5,183.7,152.3,147.2,
            164.8,148.1,192.4,177.6,208.3,231.7,148.2,196.7,143.2,214.6,
            178.3,242.8,187.4,128.6,152.4,170.3,147.2,241.3,180.6,163.4
        ],
        "Region": [
            "South","West","West","South","West","West",
            "Northeast","South","South","South","West","West",
            "Midwest","Midwest","Midwest","Midwest","South","South",
            "Northeast","South","Northeast","Midwest","Midwest",
            "South","Midwest","West","Midwest","West",
            "Northeast","Northeast","West","Northeast",
            "South","Midwest","Midwest","South","West",
            "Northeast","Northeast","South","Midwest",
            "South","South","West","Northeast","South","West",
            "South","Midwest","West"
        ]
    })

    risk_factors = pd.DataFrame({
        "Group": ["18-24","25-34","35-44","45-54","55-64","65-74","75+"],
        "Hypertension": [5.4, 10.8, 20.4, 36.2, 54.8, 67.3, 74.1],
        "High Cholesterol": [8.2, 14.6, 24.1, 38.7, 50.3, 55.1, 52.8],
        "Diabetes": [1.4, 3.6, 7.8, 14.2, 21.4, 25.6, 26.3],
        "Obesity": [16.2, 28.4, 33.7, 36.1, 37.8, 34.2, 27.6],
        "Smoking": [13.4, 18.2, 17.6, 17.1, 15.3, 10.8, 6.4],
    })

    trends = pd.DataFrame({
        "Year": list(range(2000, 2022)),
        "Heart Disease Deaths (thousands)": [
            710.8, 700.1, 696.9, 684.5, 671.9, 662.0, 631.6, 616.1,
            617.0, 599.4, 597.7, 596.3, 599.7, 611.1, 614.3, 633.8,
            635.3, 647.5, 655.4, 659.0, 696.9, 693.0
        ],
        "Stroke Deaths (thousands)": [
            167.7, 163.5, 162.7, 157.8, 150.1, 143.6, 137.1, 135.0,
            134.1, 128.8, 129.5, 128.2, 128.9, 129.5, 133.1, 140.3,
            142.1, 146.4, 147.8, 150.0, 160.2, 162.9
        ]
    })

    race_data = pd.DataFrame({
        "Race/Ethnicity": [
            "Black (Non-Hispanic)", "White (Non-Hispanic)",
            "Hispanic/Latino", "Asian (Non-Hispanic)",
            "American Indian/Alaska Native"
        ],
        "CVD Death Rate": [248.1, 173.6, 113.2, 84.6, 184.3],
        "Hypertension %": [58.1, 47.2, 43.7, 38.4, 44.9],
        "Uninsured %": [10.7, 7.2, 19.8, 6.8, 20.3],
    })

    return state_data, risk_factors, trends, race_data

state_data, risk_factors, trends, race_data = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🫀 Dashboard Controls")
    st.markdown("---")

    view = st.radio(
        "Select View",
        [
            "🏠 Overview",
            "🗺️ State-Level Analysis",
            "📈 Trends Over Time",
            "📊 Risk Factors by Age",
            "⚖️ Health Equity",
        ],
    )

    st.markdown("---")
    st.markdown("**Data Sources**")
    st.markdown("- CDC WONDER Database\n- CDC BRFSS 2022\n- American Heart Association")
    st.markdown("---")
    st.markdown("**Built by:** Torhira O. Aminu")
    st.markdown("*Applied & Computational Mathematics*")
    st.markdown("*Bowie State University*")
# ── Header ────────────────────────────────────────────────────────────────────
st.title("🫀 U.S. Cardiovascular Health Dashboard")
st.caption("Interactive analysis of heart disease, stroke, risk factors, and health equity using CDC and American Heart Association-style public health data.")
st.divider()

# ── OVERVIEW ──────────────────────────────────────────────────────────────────
if view == "🏠 Overview":
    st.subheader("Key Statistics at a Glance")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Heart Disease Deaths", "693K", "+33K vs 2019")
    col2.metric("U.S. Rank", "#1", "Leading cause")
    col3.metric("CVD Deaths", "1/min", "Approximate rate")
    col4.metric("Economic Cost", "$229B", "Projected")

    st.markdown(" ")
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### Heart Disease vs. Stroke Deaths Over Time")
        fig = px.line(
            trends,
            x="Year",
            y=["Heart Disease Deaths (thousands)", "Stroke Deaths (thousands)"],
            color_discrete_map={
                "Heart Disease Deaths (thousands)": "#c0392b",
                "Stroke Deaths (thousands)": "#1a3f6f",
            },
            markers=True,
        )
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            legend_title="",
            yaxis_title="Deaths (thousands)",
            hovermode="x unified",
            font=dict(family="Arial"),
        )
        st.plotly_chart(fig, width="stretch")

    with col_right:
        st.markdown("#### CVD Death Rate by Race/Ethnicity")
        fig2 = px.bar(
            race_data.sort_values("CVD Death Rate", ascending=True),
            x="CVD Death Rate",
            y="Race/Ethnicity",
            orientation="h",
            color="CVD Death Rate",
            color_continuous_scale=["#fde8e8", "#c0392b"],
        )
        fig2.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False,
            font=dict(family="Arial"),
            yaxis_title="",
            xaxis_title="Deaths per 100,000",
        )
        st.plotly_chart(fig2, width="stretch")

    st.info("💡 Key insight: The dashboard shows how cardiovascular outcomes vary by geography, time, age group, and race/ethnicity — the same kind of analysis used in public health data science.")

# ── STATE ANALYSIS ────────────────────────────────────────────────────────────
elif view == "🗺️ State-Level Analysis":
    st.subheader("Age-Adjusted Heart Disease Death Rates by State")

    region_filter = st.multiselect(
        "Filter by Region",
        ["South", "Midwest", "Northeast", "West"],
        default=["South", "Midwest", "Northeast", "West"],
    )

    filtered = state_data[state_data["Region"].isin(region_filter)]

    fig = px.choropleth(
        filtered,
        locations="State",
        locationmode="USA-states",
        color="Death_Rate",
        scope="usa",
        color_continuous_scale=["#fde8e8", "#e74c3c", "#922b21"],
        labels={"Death_Rate": "Deaths per 100K"},
        hover_data={"Region": True, "Death_Rate": ":.1f"},
    )
    fig.update_layout(
        geo=dict(bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="white",
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Arial"),
    )
    st.plotly_chart(fig, width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Top 10 Highest Death Rates")
        top10 = filtered.nlargest(10, "Death_Rate")[["State", "Region", "Death_Rate"]]
        top10.columns = ["State", "Region", "Rate (per 100K)"]
        st.dataframe(top10.reset_index(drop=True), width="stretch")

    with col2:
        st.markdown("#### Average Rate by Region")
        avg_region = filtered.groupby("Region", as_index=False)["Death_Rate"].mean()
        avg_region.columns = ["Region", "Avg Rate"]
        fig3 = px.bar(
            avg_region.sort_values("Avg Rate", ascending=False),
            x="Region",
            y="Avg Rate",
            color="Region",
            color_discrete_map={
                "South": "#c0392b",
                "Midwest": "#e67e22",
                "Northeast": "#1a3f6f",
                "West": "#2980b9",
            },
        )
        fig3.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            font=dict(family="Arial"),
            yaxis_title="Average deaths per 100K",
        )
        st.plotly_chart(fig3, width="stretch")

    st.info("💡 Key insight: Southern states have some of the highest heart disease death rates, showing the importance of geography, access to care, and social determinants of health.")

# ── TRENDS ────────────────────────────────────────────────────────────────────
elif view == "📈 Trends Over Time":
    st.subheader("U.S. Cardiovascular Disease Mortality Trends, 2000–2021")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trends["Year"],
        y=trends["Heart Disease Deaths (thousands)"],
        name="Heart Disease",
        line=dict(color="#c0392b", width=3),
        fill="tozeroy",
        fillcolor="rgba(192,57,43,0.08)",
        mode="lines+markers",
    ))
    fig.add_trace(go.Scatter(
        x=trends["Year"],
        y=trends["Stroke Deaths (thousands)"],
        name="Stroke",
        line=dict(color="#1a3f6f", width=3),
        fill="tozeroy",
        fillcolor="rgba(26,63,111,0.08)",
        mode="lines+markers",
    ))
    fig.add_vrect(
        x0=2019.5,
        x1=2021.5,
        fillcolor="rgba(255,165,0,0.12)",
        annotation_text="COVID-19 Impact",
        annotation_position="top left",
        line_width=0,
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Year",
        yaxis_title="Deaths (thousands)",
        legend=dict(x=0.01, y=0.99),
        font=dict(family="Arial"),
        hovermode="x unified",
    )
    st.plotly_chart(fig, width="stretch")

    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Year", "2000", "710.8K deaths")
    col2.metric("Best Year Pre-COVID", "2019", "659.0K deaths")
    col3.metric("2021 Total", "693.0K", "+5.2% vs 2019")

    st.info("💡 Key insight: Heart disease deaths declined for many years, but the COVID-19 period reversed some of that progress.")

# ── RISK FACTORS ─────────────────────────────────────────────────────────────
elif view == "📊 Risk Factors by Age":
    st.subheader("Cardiovascular Risk Factor Prevalence by Age Group")

    selected_factors = st.multiselect(
        "Select Risk Factors to Compare",
        ["Hypertension", "High Cholesterol", "Diabetes", "Obesity", "Smoking"],
        default=["Hypertension", "High Cholesterol", "Diabetes"],
    )

    if selected_factors:
        fig = px.line(
            risk_factors,
            x="Group",
            y=selected_factors,
            markers=True,
            color_discrete_sequence=["#c0392b", "#1a3f6f", "#e67e22", "#27ae60", "#8e44ad"],
        )
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="Age Group",
            yaxis_title="Prevalence (%)",
            legend_title="Risk Factor",
            font=dict(family="Arial"),
            yaxis_range=[0, 80],
            hovermode="x unified",
        )
        fig.update_traces(line=dict(width=2.5), marker=dict(size=8))
        st.plotly_chart(fig, width="stretch")

        st.markdown("#### Risk Factor Summary Table")
        display_df = risk_factors[["Group"] + selected_factors].copy()
        display_df.columns = ["Age Group"] + selected_factors
        st.dataframe(display_df.set_index("Age Group"), width="stretch")

        st.info("💡 Key insight: Hypertension rises sharply with age, making early screening and prevention very important.")
    else:
        st.warning("Please select at least one risk factor above.")

# ── HEALTH EQUITY ─────────────────────────────────────────────────────────────
elif view == "⚖️ Health Equity":
    st.subheader("Cardiovascular Health Equity Analysis")
    st.write("Disparities in CVD outcomes reflect differences in healthcare access, social determinants of health, and structural barriers.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### CVD Death Rate vs. Uninsured Rate")
        fig = px.scatter(
            race_data,
            x="Uninsured %",
            y="CVD Death Rate",
            text="Race/Ethnicity",
            color="CVD Death Rate",
            color_continuous_scale=["#fde8e8", "#c0392b"],
            size="CVD Death Rate",
        )
        fig.update_traces(textposition="top center")
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False,
            font=dict(family="Arial"),
            xaxis_title="Uninsured Rate (%)",
            yaxis_title="CVD Death Rate (per 100K)",
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown("#### Hypertension Prevalence by Race/Ethnicity")
        fig2 = px.bar(
            race_data.sort_values("Hypertension %", ascending=False),
            x="Race/Ethnicity",
            y="Hypertension %",
            color="Hypertension %",
            color_continuous_scale=["#fde8e8", "#c0392b"],
        )
        fig2.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            coloraxis_showscale=False,
            font=dict(family="Arial"),
            xaxis_title="",
            yaxis_title="Hypertension Prevalence (%)",
            xaxis_tickangle=-20,
        )
        st.plotly_chart(fig2, width="stretch")

    st.error("⚠️ Equity gap: The data shows clear differences in CVD death rates across racial and ethnic groups, showing why health equity work matters in cardiovascular public health.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<center><small>Data: CDC WONDER Database | CDC BRFSS 2022 | American Heart Association-style public health statistics &nbsp;|&nbsp; "
    "Built with Python, Streamlit, Pandas, and Plotly by Torhira O. Aminu, Bowie State University</small></center>",
    unsafe_allow_html=True,
)
