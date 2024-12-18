import folium.features
import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static

# Streamlit page configuration
st.set_page_config(page_title="Cultural Map of India", layout="wide")

# Add title
st.title("INDIA'S CULTURAL MAP")

# Load the data
file_path = "india_censusa.csv"
df = pd.read_csv(file_path)

# Preprocessing
# Clean the Density column
df["Density_cleaned"] = df["Density[a]"].str.extract(r"(\d+)").astype(float)
# Map Culture to numeric values
df["Culture_numeric"] = pd.factorize(df["Culture"])[0]

# Define the GeoJSON file
json1 = "states_india.geojson"

# Create the map
m = folium.Map(location=[20, 77], zoom_start=4)

# Dropdown options
choice = ['Density_cleaned', 'Culture_numeric']
choice_selected = st.selectbox("Select Choice", choice)

# Add choropleth layer
folium.Choropleth(
    geo_data=json1,
    name="choropleth",
    data=df,
    columns=["State or union territory", choice_selected],
    key_on="feature.properties.st_nm",
    fill_color="YlOrBr",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=choice_selected
).add_to(m)

# Function to generate the state-specific page URL
def get_state_page_url(state_name):
    """
    Returns the relative path to the state-specific page URL in the React app.
    """
    # Ensure the state name matches the format used in React routing
    state_slug = state_name.replace(" ", "_").lower()
    # Return full URL to React app with state route
    return f"http://localhost:3000/state/{state_slug}"  # React dev server URL

# Add GeoJSON layer with tooltips and clickable features
style_function = lambda x: {'fillColor': '#ffffff', 'color': '#000000', 'fillOpacity': 0.1, 'weight': 0.5}
highlight_function = lambda x: {'fillColor': '#000000', 'color': '#000000', 'fillOpacity': 0.50, 'weight': 0.5}

# Create GeoJSON layer with click events
geojson = folium.GeoJson(
    json1,
    name='states',
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['st_nm'],
        aliases=['State:'],
        style="""
            background-color: white;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """
    )
)

# Add click events to each state
for feature in geojson.data['features']:
    state_name = feature['properties']['st_nm']
    # Find cultural information for this state
    state_culture = df.loc[df['State or union territory'] == state_name, 'Culture'].iloc[0] if len(df.loc[df['State or union territory'] == state_name]) > 0 else "Cultural information not available"
    state_page_url = get_state_page_url(state_name)
    
    # Create popup with cultural information and link to React app
    popup_html = f"""
        <div onclick="window.location.href='{state_page_url}'" style="cursor: pointer;">
            <h4>{state_name}</h4>
            <p><b>Culture:</b> {state_culture}</p>
            <p>Click to view more details</p>
        </div>
    """
    
    # Add popup to the feature
    feature['properties']['info'] = popup_html

# Add the click handler to show popups
geojson.add_child(folium.features.GeoJsonPopup(['info'], parse_html=True))
geojson.add_to(m)

# Hide all countries except India by setting bounds explicitly
m.fit_bounds([[6, 68], [36, 98]])

# Render the map
folium_static(m, width=900, height=600)
