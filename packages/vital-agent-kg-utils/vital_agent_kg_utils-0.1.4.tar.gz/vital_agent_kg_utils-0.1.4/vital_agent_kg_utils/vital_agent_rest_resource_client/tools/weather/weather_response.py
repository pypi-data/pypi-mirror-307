from typing import List, Optional
from typing_extensions import TypedDict

from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_data import ToolData
from vital_agent_kg_utils.vital_agent_rest_resource_client.tools.tool_results import ToolResults


class WeatherPrediction(TypedDict):
    """
    Represents a daily weather prediction.

    Attributes:
        date (str): The date of the prediction in ISO8601 format.
        weather_code (int): The weather condition code.
        weather_code_description (str): The weather condition description.
        temperature_max (float): The maximum temperature for the day.
        temperature_min (float): The minimum temperature for the day.
        apparent_temperature_max (float): The maximum apparent temperature for the day.
        apparent_temperature_min (float): The minimum apparent temperature for the day.
        sunrise (str): The time of sunrise in ISO8601 format.
        sunset (str): The time of sunset in ISO8601 format.
        precipitation_sum (float): The precipitation sum for the day.
        precipitation_hours (float): The precipitation hours for the day.
        precipitation_probability_max (float): The precipitation probability for the day.
        precipitation_probability_min (float): The precipitation probability for the day.
        precipitation_probability_mean (float): The precipitation probability for the day.
        daylight_duration (float): The daylight duration for the day.
        uv_index_max (float): The maximum uv index for the day.
        wind_gusts_10m_max (float): The maximum wind gusts for the day.
    """
    date: str
    weather_code: int

    weather_code_description: Optional[str]

    temperature_max: float
    temperature_min: float
    apparent_temperature_max: float
    apparent_temperature_min: float
    sunrise: str
    sunset: str
    precipitation_sum: float
    precipitation_hours: float
    precipitation_probability_max: float
    precipitation_probability_min: float
    precipitation_probability_mean: float
    daylight_duration: float
    uv_index_max: float
    wind_gusts_10m_max: float


class WeatherData(ToolData):
    """
    Represents the weather data including current conditions and daily predictions.

    Attributes:
        place_label (str): The place label of the weather prediction.
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        timezone (str): The timezone of the location.

        temperature (float): The current temperature at the location.
        humidity (int): The current relative humidity at the location.
        wind_speed (float): The current wind speed at the location.

        weather_code (int): The weather condition code.
        weather_code_description (str): The weather condition description.
        apparent_temperature (float): The apparent temperature at the location.
        is_day (int): When 1, is daytime
        precipitation (float): The current precipitation at the location.
        precipitation_probability (float): The current precipitation probability at the location.
        cloud_cover (float): The current cloud cover at the location.
        wind_direction_10m (float): The wind direction at the location.
        wind_gusts_10m (float): The wind gusts at the location.

        daily_predictions (List[WeatherPrediction]): A list of daily weather predictions.
    """
    place_label: str
    latitude: float
    longitude: float
    timezone: str

    temperature: Optional[float]
    humidity: Optional[int]
    wind_speed: Optional[float]

    weather_code: Optional[int]

    weather_code_description: Optional[str]

    apparent_temperature: Optional[float]
    is_day: Optional[int]
    precipitation: Optional[float]
    precipitation_probability: Optional[float]
    cloud_cover: Optional[float]
    wind_direction_10m: Optional[float]
    wind_gusts_10m: Optional[float]

    daily_predictions: List[WeatherPrediction]


class WeatherResponse(ToolResults):
    weather_data: WeatherData
