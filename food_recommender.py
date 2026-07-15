import pandas as pd
import streamlit as st
import ast

# Load dataset
recipes = pd.read_csv("RAW_recipes.csv")

# Rename columns
recipes.columns = recipes.columns.str.strip().str.lower()

# Convert nutrition column from string to list
recipes["nutrition"] = recipes["nutrition"].apply(ast.literal_eval)

# Split nutrition into separate columns
nutrition_df = pd.DataFrame(
    recipes["nutrition"].tolist(),
    columns=[
        "calories_kcal",
        "total_fat_percent",
        "sugar_percent",
        "sodium_percent",
        "protein_percent",
        "saturated_fat_percent",
        "carbohydrates_percent"
    ]
)

# Combine with original dataset
data = pd.concat([recipes, nutrition_df], axis=1)

# Convert numeric columns
numeric_cols = [
    "calories_kcal",
    "protein_percent",
    "carbohydrates_percent",
    "total_fat_percent",
    "sodium_percent"
]

for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors="coerce")

st.title("Food Recommendation System")
st.write("Get food suggestions based on your nutritional preferences.")

# User sliders
calories = st.slider("Maximum Calories", 50, 1000, 300)
protein = st.slider("Minimum Protein (%)", 0, 100, 10)
carbs = st.slider("Maximum Carbohydrates (%)", 0, 100, 50)
fat = st.slider("Maximum Fat (%)", 0, 100, 20)
sodium = st.slider("Maximum Sodium (%)", 0, 100, 30)

# Filter recipes
filtered = data[
    (data["calories_kcal"] <= calories) &
    (data["protein_percent"] >= protein) &
    (data["carbohydrates_percent"] <= carbs) &
    (data["total_fat_percent"] <= fat) &
    (data["sodium_percent"] <= sodium)
]

st.subheader("Recommended Recipes")

if not filtered.empty:
    st.dataframe(
        filtered[
            [
                "name",
                "calories_kcal",
                "protein_percent",
                "carbohydrates_percent",
                "total_fat_percent",
                "sodium_percent"
            ]
        ]
    )
else:
    st.warning("No recipes match your criteria.")