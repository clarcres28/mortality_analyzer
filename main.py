import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
st.title("Life Expectancy and Mortality Analyzer")
st.write("Explore mortality rates, survival probabilities, and life expectancy across different ages")
df=pd.read_csv("synthetic_mortality_life_table.csv")
st.subheader("Mortality data set")
st.dataframe(df.head(10))
st.subheader("Select Age")
selected_age = st.slider("Choose an Age",min_value=0,max_value=100,value=30)
st.write("Selected Age:", selected_age)
selected_data=df[df["Age"]==selected_age]
st.dataframe(selected_data)
mortality = selected_data["Mortality_Rate_qx"].iloc[0]
survivors = selected_data["Survivors_lx"].iloc[0]
deaths = selected_data["Deaths_dx"].iloc[0]
life_expectancy = selected_data["Life_Expectancy_ex"].iloc[0]
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Mortality Rate",f"{mortality * 100:.3f}%")
with col2:
    st.metric("Survivors",f"{survivors:,.0f}")
with col3:
    st.metric("Expected Deaths",f"{deaths:,.0f}")
with col4:
    st.metric("Remaining Life Expectancy",f"{life_expectancy:.2f} years")
st.subheader("Mortality Rate by Age")
st.line_chart(df, x="Age",y="Mortality_Rate_qx")
st.subheader("Remaining life expectancy")
st.line_chart(df, x="Age", y="Life_Expectancy_ex")
st.subheader("Survival Probability Calculator")

current_age = st.number_input(
    "Current Age",
    min_value=0,
    max_value=99,
    value=30
)

future_age = st.number_input(
    "Future Age",
    min_value=current_age + 1,
    max_value=100,
    value=max(60, current_age + 1)
)

lx = df.loc[
    df["Age"] == current_age,
    "Survivors_lx"
].iloc[0]

lx_future = df.loc[
    df["Age"] == future_age,
    "Survivors_lx"
].iloc[0]

survival_probability = lx_future / lx

st.metric(
    "Survival Probability",
    f"{survival_probability * 100:.2f}%"
)
death_probability = 1 - survival_probability

st.metric(
    "Probability of Death Before Future Age",
    f"{death_probability * 100:.2f}%"
)
def age_category(age):
    if age < 18:
        return "0-17"
    elif age < 40:
        return "18-39"
    elif age < 60:
        return "40-59"
    elif age < 80:
        return "60-79"
    else:
        return "80-100"

df["Age_Group"] = df["Age"].apply(age_category)

group_data = df.groupby("Age_Group")[
    "Mortality_Rate_qx"
].mean()

st.subheader("Average Mortality Rate by Age Group")

st.bar_chart(group_data)
st.subheader("Compare Mortality by Age")

age1 = st.selectbox(
    "Select First Age",
    df["Age"],
    index=30
)

age2 = st.selectbox(
    "Select Second Age",
    df["Age"],
    index=60
)

rate1 = df.loc[
    df["Age"] == age1,
    "Mortality_Rate_qx"
].iloc[0]

rate2 = df.loc[
    df["Age"] == age2,
    "Mortality_Rate_qx"
].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        f"Mortality at Age {age1}",
        f"{rate1 * 100:.3f}%"
    )

with col2:
    st.metric(
        f"Mortality at Age {age2}",
        f"{rate2 * 100:.3f}%"
    )
    st.subheader("Download Mortality Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Mortality Dataset",
    data=csv,
    file_name="mortality_analysis.csv",
    mime="text/csv"
)