import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Define the CTAR locations and corresponding histogram data (sample data for histograms)
towns_info = {
    7: ("Ambatondrazaka", (-17.8324, 48.4086), [10, 20, 30, 40, 50]),
    30: ("Ambositra", (-20.5300, 47.2441), [15, 25, 35, 45, 55]),
    100: ("Ambatomainty", (-17.1884, 44.5947), [5, 10, 15, 20, 25]),
    # Add the rest of your CTARs here...
    103: ("Ambovombe", (-25.1744, 46.0876), [12, 22, 32, 42, 52])
}

# Extracting data for the map
city_names = [info[0] for info in towns_info.values()]
latitudes = [info[1][0] for info in towns_info.values()]
longitudes = [info[1][1] for info in towns_info.values()]
histogram_data = [info[2] for info in towns_info.values()]

# Create a scatter mapbox plot with histograms as popups
fig = go.Figure()

for i, city in enumerate(city_names):
    # Add CTAR location as a marker
    fig.add_trace(go.Scattermapbox(
        lat=[latitudes[i]],
        lon=[longitudes[i]],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=12,
            color='darkorange',
        ),
        name=city,
        customdata=[histogram_data[i]],  # Pass the histogram data
        hoverinfo='text',
        hovertext=f"{city}",
        showlegend=False
    ))

# Update layout with the map settings
fig.update_layout(
    width=1200,  # Set the desired width
    height=900,  # Set the desired height
    mapbox=dict(
        style="open-street-map",
        center=dict(lat=-19, lon=47),
        zoom=5
    ),
    title="CTAR les plus fréquentés de Madagascar",
    showlegend=False
)

# Display the map in Streamlit
st.plotly_chart(fig)

# Logic to display the histogram when a marker is clicked
if 'last_click' in st.session_state:
    last_click = st.session_state['last_click']
    city_index = city_names.index(last_click['hovertext'])
    st.write(f"Histogram for {city_names[city_index]}")
    hist_fig = px.histogram(histogram_data[city_index], nbins=5, title=f"Histogram for {city_names[city_index]}")
    st.plotly_chart(hist_fig)

# Set up a click callback to capture click events
def click_callback(trace, points, state):
    st.session_state['last_click'] = points[0]

# Attach the callback to each marker
for trace in fig.data:
    trace.on_click(click_callback)

# Display the map with clickable markers
st.plotly_chart(fig)
