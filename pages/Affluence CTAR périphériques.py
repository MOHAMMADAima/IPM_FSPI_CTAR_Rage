import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Define the updated dictionary for town names and GPS coordinates
towns_info = {
    7: ("Ambatondrazaka", (-17.8324, 48.4086)),
    30: ("Ambositra", (-20.5300, 47.2441)),
    100: ("Ambatomainty", (-17.1884, 44.5947)),
    13: ("Antsirabe", (-19.8659, 47.0333)),
    10: ("Antsiranana", (-12.2795, 49.2913)),
    14: ("Antsohihy", (-14.8667, 47.9833)),
    12: ("Bekily", (-24.2333, 45.3833)),
    1: ("Soanierana Ivongo", (-16.9167, 49.5833)),
    2: ("Fianarantsoa", (-21.4545, 47.0833)),
    16: ("Ihosy", (-22.4021, 46.1253)),
    17: ("Maevatanana", (-16.9333, 46.8333)),
    18: ("Mahajanga", (-15.7167, 46.3167)),
    19: ("Maintirano", (-18.0566, 44.0297)),
    31: ("Manakara", (-22.1451, 48.0115)),
    15: ("Mandritsara", (-15.8333, 48.8333)),
    23: ("Manja", (-21.4167, 44.8667)),
    4: ("Maroantsetra", (-15.4333, 49.7500)),
    21: ("Miarinarivo", (-19.0010, 46.7334)),
    8: ("Moramanga", (-18.9333, 48.2000)),
    22: ("Morondava", (-20.2833, 44.2833)),
    9: ("Nosy Be", (-13.3333, 48.2667)),
    24: ("Sambava", (-14.2667, 50.1667)),
    101: ("Sainte Marie", (-17.0000, 49.8500)),
    25: ("Taolagnaro", (-25.0314, 46.9821)),
    28: ("Toamasina", (-18.1492, 49.4023)),
    26: ("Toliara", (-23.3568, 43.6917)),
    27: ("Tsiroanomandidy", (-18.7713, 46.0520)),
    3: ("Vangaindrano", (-23.3479, 47.5972)),
    97: ("Mananjary", (-21.2300, 48.3439)),
    102: ("Fort Dauphin", (-25.0347, 46.9883)),
    103: ("Ambovombe", (-25.1744, 46.0876))
}

# Streamlit page
st.title("CTAR Patient Visits Map")

# Check if dataframes are available in session state
if 'dataframes' in st.session_state:
    dataframes = st.session_state['dataframes']
    
    # Select a file to analyze from the uploaded files
    selected_file = st.selectbox("Sélectionnez un fichier pour l'analyse", options=list(dataframes.keys()))

    # Load the selected dataframe
    if selected_file:
        ctar = dataframes[selected_file]
        
        # Preprocess the data
        ctar['date_de_consultation'] = pd.to_datetime(ctar['date_de_consultation'])
        ctar['year'] = ctar['date_de_consultation'].dt.year
        ctar['year']=ctar['year'].astype(int)
        
        # Group by 'id_ctar' and 'year', then count the occurrences
        yearly_recurrence = ctar.groupby(['id_ctar', 'year']).size().reset_index(name='nombre de visite patients')
        
        # Convert the column values to integers
        yearly_recurrence['id_ctar'] = yearly_recurrence['id_ctar'].astype(int)
        
        # Replace integer values with corresponding dictionary values
        yearly_recurrence['town_name'] = yearly_recurrence['id_ctar'].map(lambda x: towns_info.get(x, ("Unknown", (0, 0)))[0])
        yearly_recurrence['gps_coordinates'] = yearly_recurrence['id_ctar'].map(lambda x: towns_info.get(x, ("Unknown", (0, 0)))[1])
        
        # Select the year to visualize
        selected_year = st.selectbox("Select Year", options=yearly_recurrence['year'].unique())
        
        # Filter data for the selected year
        filtered_data = yearly_recurrence[yearly_recurrence['year'] == selected_year]
        
        # Extract the data for the map
        town_names = filtered_data['town_name'].tolist()
        latitudes = [coord[0] for coord in filtered_data['gps_coordinates']]
        longitudes = [coord[1] for coord in filtered_data['gps_coordinates']]
        populations = filtered_data['nombre de visite patients'].tolist()
        
        # Create a scatter mapbox plot
        fig = go.Figure(go.Scattermapbox(
            lat=latitudes,
            lon=longitudes,
            mode='markers+text',
            marker=go.scattermapbox.Marker(
                size=[10 + (pop / 500) for pop in populations],  # Adjust size based on town values
                color='darkorange',
            ),
            text=[f"CTAR {name}: {value} patients" for name, value in zip(town_names, populations)],
            textposition='top center',
        ))
        
        fig.update_layout(
            width=1200,  # Set the desired width
            height=900,  # Set the desired height
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=-19, lon=47),
                zoom=5
            ),
            title=f"Nombre de visite patients dans les CTARs en {selected_year}",
            showlegend=True
        )
        
        # Show the map
        st.plotly_chart(fig)
