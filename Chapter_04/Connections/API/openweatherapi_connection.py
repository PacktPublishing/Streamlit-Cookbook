from streamlit.connections import BaseConnection # For newer Streamlit versions>=1.28.0
from typing import Optional, Dict, Any
import streamlit as st
import requests
import pandas as pd
import datetime as dt
import time # For the retry delay


class OpenWeatherMapConnection(BaseConnection[requests.Session]):
    """
    A connection class to fetch current weather and forecast data
    from the OpenWeatherMap API using latitude and longitude.
    It also performs reverse geocoding to get city/state/country names.
    """
    def __init__(self, connection_name: str = "openweathermap", **kwargs):
        super().__init__(connection_name, **kwargs)
        self._session: Optional[requests.Session] = None
        self._api_key: Optional[str] = None
        self._geocoding_url = "http://api.openweathermap.org/geo/1.0/reverse"
        self._current_weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self._forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    def _connect(self, **kwargs) -> requests.Session:
        # This method is called by _get_session() when self._session is None
        if "api_key" in kwargs: # Allow explicit API key passing
            self._api_key = kwargs.pop("api_key")
        else:
            self._api_key = self._secrets.get("api_key")

        if not self._api_key:
            # This error will be caught by st.connection's initialization
            raise ValueError("OpenWeatherMap API key not found in secrets or arguments.")
        
        session = requests.Session()
        session.headers.update({"Accept": "application/json"})
        return session

    def _get_session(self) -> requests.Session:
        # Ensures _connect (and thus API key loading) happens before session is used
        if self._session is None:
            self._session = self._connect()
        if self._api_key is None and self._session is not None: # Safeguard
             # This implies _connect ran but didn't set _api_key, or _api_key was reset
             # Try to re-initialize API key part of _connect logic
             if "api_key" in self._kwargs: # Check if it was passed in original st.connection call
                 self._api_key = self._kwargs["api_key"]
             else:
                 self._api_key = self._secrets.get("api_key")
             if not self._api_key:
                 raise ValueError("API Key became unset after session initialization.")
        return self._session

    def _handle_api_error(self, e: requests.exceptions.HTTPError, api_name: str) -> str:
        """
        Helper to format API error messages.
        """
        error_message = f"{api_name} HTTP error: {e.response.status_code} {e.response.reason}"
        try:
            error_details = e.response.json()
            if "message" in error_details:
                error_message = f"{api_name} API Error ({error_details.get('cod', e.response.status_code)}): {error_details['message']}"
        except Exception: pass
        return error_message
    
    def _make_api_request(self, url: str, params: Dict[str, Any], api_name: str) -> Dict[str, Any]:
        """
        Generic helper to make an API request and handle common errors.
        """
        session = self._get_session() # Ensures session and API key are loaded
        if not self._api_key: # Critical check before making request
            raise ValueError(f"{api_name} failed: API key is not set.")
        
        # Add appid to params if not already there (should be there from calling methods)
        if 'appid' not in params:
            params['appid'] = self._api_key

        try:
            response = session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if "cod" in data and str(data["cod"]) != "200" and not (api_name == "Reverse Geocoding" and isinstance(data, list)): # Geocoding returns list on success
                raise Exception(f"{api_name} API Error ({data['cod']}): {data.get('message', 'Unknown error')}")
            return data
        except requests.exceptions.HTTPError as e:
            raise Exception(self._handle_api_error(e, api_name))
        except requests.exceptions.RequestException as e:
            raise Exception(f"{api_name} request failed: {e}")
        except Exception as e:
            raise Exception(str(e))

    def _reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Handles the call to the Geocoding API and returns the location details
        through reverse geocoding method.
        """
        # Ensures that the API key is ready before forming params for the first crucial call.
        self._get_session() # This will call _connect() if needed and set self._api_key
        if not self._api_key:
            raise ValueError("API key not available for reverse geocoding.")

        params = {"lat": lat, "lon": lon, "limit": 1, "appid": self._api_key}
        
        try:
            data = self._make_api_request(self._geocoding_url, params, "Reverse Geocoding")
        except Exception as e:
            # If it's a 401 on the first try for geocoding, try one more time after a tiny delay.
            # This is a targeted fix for the "first call 401" issue.
            if "401" in str(e):
                time.sleep(0.2) # Very short delay
                # Force re-check/re-load of API key just in case (belt-and-suspenders)
                if not self._api_key: self._api_key = self._secrets.get("api_key")
                if not self._api_key: raise ValueError("API Key missing on retry attempt for geocoding.")
                params['appid'] = self._api_key # Ensure it's in params for retry
                
                data = self._make_api_request(self._geocoding_url, params, "Reverse Geocoding (Retry)")
            else:
                raise # Re-raise other errors immediately

        if not data or not isinstance(data, list): # Geocoding API returns a list
            raise Exception(f"No location details found or unexpected format for lat={lat}, lon={lon}. Data: {data}")
        
        location_info = data[0]
        return {
            "city": location_info.get("name"),
            "state": location_info.get("state"),
            "country": location_info.get("country"),
        }

    # _fetch_current_weather_data and _fetch_forecast_data remain largely the same,
    # just ensure they call self._get_session() or self._make_api_request which handles it.

    def _fetch_current_weather_data(self, lat: float, lon: float, units: str) -> Dict[str, Any]:
        """
        Fetches and returns weather conditions data from the Current Weather API.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self._api_key,
            "units": units,
        }
        
        data = self._make_api_request(self._current_weather_url, params, "Current Weather")
        main = data.get("main", {})
        wind = data.get("wind", {})
        weather_desc = data.get("weather", [{}])[0]
        sys_info = data.get("sys", {})
        clouds_info = data.get("clouds", {})
        timezone_offset = data.get("timezone", 0)

        return {
            "timestamp_dt": dt.datetime.fromtimestamp(data["dt"] + timezone_offset, tz=dt.timezone.utc),
            "temperature": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "temp_min": main.get("temp_min"),
            "temp_max": main.get("temp_max"),
            "pressure": main.get("pressure"),
            "humidity": main.get("humidity"),
            "description": weather_desc.get("description", "").capitalize(),
            "wind_speed": wind.get("speed"),
            "wind_gust": wind.get("gust"),
            "visibility": data.get("visibility"),
            "cloudiness": clouds_info.get("all"),
            "sunrise_dt": dt.datetime.fromtimestamp(sys_info["sunrise"] + timezone_offset, tz=dt.timezone.utc) if "sunrise" in sys_info else None,
            "sunset_dt": dt.datetime.fromtimestamp(sys_info["sunset"] + timezone_offset, tz=dt.timezone.utc) if "sunset" in sys_info else None,
        }

    def _fetch_forecast_data(self, lat: float, lon: float, units: str) -> pd.DataFrame:
        """
        Retrieves and returns the 3-hour forecast data via their Forecast API endpoint.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self._api_key,
            "units": units,
            "cnt": 8,  # Request 8 * 3-hour = 24 hours forecast
        }
        
        data = self._make_api_request(self._forecast_url, params, "Weather Forecast")
        
        forecast_list = []
        city_info = data.get("city", {})
        timezone_offset = city_info.get("timezone", 0)

        for entry in data.get("list", []):
            main = entry.get("main", {})
            weather_desc = entry.get("weather", [{}])[0]
            wind = entry.get("wind", {})
            
            forecast_list.append({
                "Time": dt.datetime.fromtimestamp(entry["dt"] + timezone_offset, tz=dt.timezone.utc),
                "Temp": main.get("temp"),
                "Feels Like": main.get("feels_like"),
                "Description": weather_desc.get("description", "").capitalize(),
                "Humidity (%)": main.get("humidity"),
                "Wind Speed": wind.get("speed"),
                "Cloudiness (%)": entry.get("clouds", {}).get("all"),
                "Prob. of Precip. (%)": int(entry.get("pop", 0) * 100),
                "Rain (3h mm)": entry.get("rain", {}).get("3h"),
                "Snow (3h mm)": entry.get("snow", {}).get("3h"),
            })
        return pd.DataFrame(forecast_list)


    def query(self, lat, lon, units):
        """
        Returns fetched location (reverse geocoded), current weather, and 3-hour forecast data.
        """
        @st.cache_data(ttl=600) # Cache combined result for 10 minutes
        def _query(lat: float, lon: float, units: str = "metric") -> Dict[str, Any]:
            try:
                # Ensure session and API key are ready. _get_session() handles this.
                self._get_session()
                if not self._api_key: # This should ideally never be true if _get_session worked
                    st.error("API Key could not be loaded for the query.")
                    return None

                location_data = self._reverse_geocode(lat, lon) # Retry logic is now inside here
                current_weather_data = self._fetch_current_weather_data(lat, lon, units)
                forecast_df = self._fetch_forecast_data(lat, lon, units)
                
                if not location_data.get("city") and current_weather_data.get("city_name_api"):
                    location_data["city"] = current_weather_data["city_name_api"]

                return {
                    "location": location_data,
                    "current_weather": current_weather_data,
                    "forecast_df": forecast_df,
                    "units_system": units
                }
            except Exception as e:
                st.error(f"Failed to fetch weather data: {str(e)[:500]}") # Show truncated error
                return None # Return None on failure, app checks for this
        return _query(lat, lon, units)
