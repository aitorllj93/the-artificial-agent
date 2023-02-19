from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config

from config import get_value

config_dict = get_default_config()
config_dict['language'] = get_value('providers.openweathermap.language', 'en')


owm = OWM(get_value('providers.openweathermap.apiKey'), config_dict)
mgr = owm.weather_manager()


def get_observation(
    location: str = get_value(
        'providers.openweathermap.location', 'London,GB')
):
    observation = mgr.weather_at_place(location)
    return observation
