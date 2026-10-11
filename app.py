import pandas as pd
import plotly.express as px
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="F1 Performance Dashboard", page_icon="🏎️", layout="wide"
)

st.title("🏎️ Formula 1 Analytics Dashboard")
st.markdown(
    "Explore driver performances, podium finishes, and team statistics across F1 history."
)


# Load and Cache Data
@st.cache_data
def load_data():
    races = pd.read_csv("data/races.csv")
    results = pd.read_csv("data/results.csv")
    drivers = pd.read_csv("data/drivers.csv")
    constructors = pd.read_csv("data/constructors.csv")

    # Merge into a single flat DataFrame
    df = (
        results.merge(races[["raceId", "year", "name"]], on="raceId")
        .merge(
            drivers[["driverId", "forename", "surname", "nationality"]],
            on="driverId",
        )
        .merge(
            constructors[["constructorId", "name"]],
            on="constructorId",
            suffixes=("_race", "_team"),
        )
    )

    df["driver_name"] = df["forename"] + " " + df["surname"]
    # Convert position to numeric (replacing non-finishers '\\N' with NaN)
    df["positionOrder"] = pd.to_numeric(df["positionOrder"], errors="coerce")
    df["points"] = pd.to_numeric(df["points"], errors="coerce")

    return df


# Load data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading files from data folder: {e}")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")
selected_year = st.sidebar.selectbox(
    "Select Season", sorted(df["year"].unique(), reverse=True)
)

filtered_df = df[df["year"] == selected_year]

# Top Metrics
top_driver = (
    filtered_df.groupby("driver_name")["points"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)
top_team = (
    filtered_df.groupby("name_team")["points"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

col1, col2, col3 = st.columns(3)
col1.metric("Selected Season", selected_year)
col2.metric("Championship Leader / Winner", top_driver)
col3.metric("Top Team", top_team)

st.markdown("---")

# --- Visualizations ---
tab1, tab2 = st.tabs(["Driver Standings", "Team Comparison"])

with tab1:
    st.subheader(f"Driver Points Standing ({selected_year})")
    driver_points = (
        filtered_df.groupby("driver_name")["points"]
        .sum()
        .reset_index()
        .sort_values(by="points", ascending=False)
        .head(10)
    )

    fig_drivers = px.bar(
        driver_points,
        x="points",
        y="driver_name",
        orientation="h",
        color="points",
        color_continuous_scale="Reds",
        title=f"Top 10 Drivers by Points in {selected_year}",
    )
    fig_drivers.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_drivers, use_container_width=True)

with tab2:
    st.subheader(f"Constructor Points ({selected_year})")
    team_points = (
        filtered_df.groupby("name_team")["points"]
        .sum()
        .reset_index()
        .sort_values(by="points", ascending=False)
    )

    fig_teams = px.pie(
        team_points,
        values="points",
        names="name_team",
        title="Constructor Points Distribution",
        hole=0.4,
    )
    st.plotly_chart(fig_teams, use_container_width=True)
