from openweatherapi_connection import OpenWeatherMapConnection
import streamlit as st
import pandas as pd

# Helper functions to format temperature and wind speed units based on user selection
def get_temp_unit_symbol(unit_system_value):
    if unit_system_value == "metric": return "°C"
    if unit_system_value == "imperial": return "°F"
    return " K"

def get_wind_speed_unit(unit_system_value):
    if unit_system_value == "metric": return "m/s"
    if unit_system_value == "imperial": return "mph"
    return "m/s" # Default for standard (Kelvin)


def main():
    st.title("⛅ :orange[Accurate Weather & Forecast]")
    st.subheader("Get real-time weather info and hourly forecast in your area through geo coordinates!")

    try:
        conn = st.connection("openweathermap", type=OpenWeatherMapConnection)
    except Exception as e:
        st.error(f"Fatal Error: Could not initialize OpenWeatherMap connection: {e}")
        st.caption("Ensure API key is in .streamlit/secrets.toml ([connections.openweathermap])")
        st.stop()

    # Input for latitude and longitude
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        lat_input = st.number_input(
            "Enter Latitude:", 
            min_value=-90.0, 
            max_value=90.0, 
            value=40.7128,  # Default to New York City
            step=0.0001,
            format="%.4f"
        )
    with col2:
        lon_input = st.number_input(
            "Enter Longitude:", 
            min_value=-180.0, 
            max_value=180.0, 
            value=-74.0060, # Default to New York City
            step=0.0001,
            format="%.4f"
        )

    units_options = {"Celsius (°C)": "metric", "Fahrenheit (°F)": "imperial"}
    selected_unit_display = st.selectbox("Temperature Unit:", options=list(units_options.keys()), index=0)
        
    units_value = units_options[selected_unit_display]

    if st.button("Get Weather Data 🌍"):
        if lat_input is not None and lon_input is not None:
            with st.spinner(f"Fetching weather for Lat: {lat_input:.4f}, Lon: {lon_input:.4f}..."):
                weather_data = conn.query(lat=lat_input, lon=lon_input, units=units_value)

                if weather_data:
                    location = weather_data["location"]
                    current = weather_data["current_weather"]
                    forecast_df = weather_data["forecast_df"]
                    units_system = weather_data["units_system"]
                    temp_unit_sym = get_temp_unit_symbol(units_system)
                    wind_unit_sym = get_wind_speed_unit(units_system)

                    st.markdown("---")
                    st.subheader(f"📍 Location: {location.get('city', 'N/A')}")
                    loc_details = []
                    if location.get("state"):
                        loc_details.append(f"State: {location['state']}")
                    if location.get("country"):
                        loc_details.append(f"Country: {location['country']}")
                    if loc_details:
                        st.markdown(", ".join(loc_details))

                    st.markdown("---")
                    st.subheader(f"☀️ Current Weather ({current['timestamp_dt'].strftime('%Y-%m-%d %H:%M %Z')})")

                    # Prepare data for Current Weather DataFrame
                    current_weather_details_list = [
                        {"Metric": "Temperature", "Value": f"{current.get('temperature', 'N/A'):.1f}{temp_unit_sym}"},
                        {"Metric": "Condition", "Value": f"{current.get('description', 'N/A')}"},
                        {"Metric": "Feels Like", "Value": f"{current.get('feels_like', 'N/A'):.1f}{temp_unit_sym}"},
                        {"Metric": "Min/Max Temperature", "Value": f"{current.get('temp_min', 'N/A'):.1f}{temp_unit_sym} / {current.get('temp_max', 'N/A'):.1f}{temp_unit_sym}"},
                        {"Metric": "Humidity", "Value": f"{current.get('humidity', 'N/A')}%"},
                        {"Metric": "Wind Speed", "Value": f"{current.get('wind_speed', 'N/A'):.1f} {wind_unit_sym}"},
                    ]
                    if current.get('wind_gust') is not None:
                        current_weather_details_list.append({"Metric": "Wind Gust", "Value": f"{current['wind_gust']:.1f} {wind_unit_sym}"})
                    if current.get('visibility') is not None:
                        current_weather_details_list.append({"Metric": "Visibility", "Value": f"{current['visibility']/1000:.1f} km"})
                    if current.get('cloudiness') is not None:
                        current_weather_details_list.append({"Metric": "Cloudiness", "Value": f"{current['cloudiness']}%"})
                    if current.get('sunrise_dt'):
                        current_weather_details_list.append({"Metric": "Sunrise", "Value": current['sunrise_dt'].strftime('%H:%M %Z')})
                    if current.get('sunset_dt'):
                        current_weather_details_list.append({"Metric": "Sunset", "Value": current['sunset_dt'].strftime('%H:%M %Z')})

                    current_weather_df = pd.DataFrame(current_weather_details_list)
                    st.dataframe(current_weather_df.set_index("Metric"), use_container_width=True)


                    st.markdown("---")
                    st.subheader("🕒 3-Hour Forecast (Next ~24 Hours)")
                    
                    display_forecast_df = forecast_df.copy()
                    if not display_forecast_df.empty:
                        display_forecast_df["Time"] = display_forecast_df["Time"].apply(lambda x: x.strftime('%a %H:%M')) # Format time
                        display_forecast_df["Temp"] = display_forecast_df["Temp"].apply(lambda x: f"{x:.1f}{temp_unit_sym}" if pd.notnull(x) else "N/A")
                        display_forecast_df["Feels Like"] = display_forecast_df["Feels Like"].apply(lambda x: f"{x:.1f}{temp_unit_sym}" if pd.notnull(x) else "N/A")
                        display_forecast_df["Humidity (%)"] = display_forecast_df["Humidity (%)"].apply(lambda x: f"{x:.0f}%" if pd.notnull(x) else "N/A")
                        display_forecast_df["Wind Speed"] = display_forecast_df["Wind Speed"].apply(lambda x: f"{x:.1f} {wind_unit_sym}" if pd.notnull(x) else "N/A")
                        display_forecast_df["Cloudiness (%)"] = display_forecast_df["Cloudiness (%)"].apply(lambda x: f"{x:.0f}%" if pd.notnull(x) else "N/A")
                        display_forecast_df["Rain (3h mm)"] = display_forecast_df["Rain (3h mm)"].apply(lambda x: f"{x:.1f} mm" if pd.notnull(x) else "0.0 mm")
                        display_forecast_df["Snow (3h mm)"] = display_forecast_df["Snow (3h mm)"].apply(lambda x: f"{x:.1f} mm" if pd.notnull(x) else "0.0 mm")
                        
                        # Select and reorder columns for display
                        cols_to_show = [
                            "Time", "Temp", "Feels Like", "Description",
                            "Prob. of Precip. (%)", "Humidity (%)", "Wind Speed",
                            "Cloudiness (%)", "Rain (3h mm)", "Snow (3h mm)"
                        ]

                        st.dataframe(display_forecast_df[cols_to_show].set_index("Time"), use_container_width=True)

        else:
            st.warning("⚠ Please enter valid latitude and longitude values.")
            
    # Attribution for the data source
    st.markdown("---")
    st.markdown("Weather data provided by [OpenWeatherMap](https://openweathermap.org/).")

if __name__ == "__main__":
    main()
