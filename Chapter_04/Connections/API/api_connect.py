from connection import EdamamConnectionProvider
import streamlit as st

def main():
    api_connection = EdamamConnectionProvider(connection_name='nutritionProvider')

    st.title(":orange[Edamam API: Nutrition Analysis]")
    st.subheader("Write the ingredients of any recipe and we'll analyze their nutritional info for you! :)")

    ingredients_input = st.text_area("Enter your ingredients (one per line) 👇")

    if st.button("Analyze Ingredients 🍡"):
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split("\n") if ingredient]
        nutritional_info = api_connection.query(ingredients)
        if nutritional_info:
            st.success("Nutritional information fetched successfully!")
            display_nutritional_info(nutritional_info)
        else:
            st.error("No nutritional information found for the given ingredients.")


def display_nutritional_info(nutritional_info):
    for info in nutritional_info:
        st.markdown(f"### Ingredient: {info['ingredient']}")

        with st.expander("See Nutritional Information"):
            st.markdown(f"#### Calories: {info['calories']}")
            st.markdown(f"**Total Weight**: {info['totalWeight']} grams")
            st.markdown(f"**Diet Labels**: {', '.join(info['dietLabels'])}")
            st.markdown(f"**Health Labels**: {', '.join(info['healthLabels'])}")
            for nutrient, details in info['totalNutrients'].items():
                st.markdown(f"#### {nutrient}: {details['quantity']} {details['unit']}")

# Edamam API Attribution
def footer():
    st.write("")
    st.write("")
    st.markdown('[More from Edamam](https://www.edamam.com/)')
    st.write("")
    st.image('badge.png')


if __name__ == "__main__":
    main()
    footer()
