## Installation

```sh
pip install snakifit
```

## Usage

```python

from snakifit.http_client import *

@http_host(base_url="http://localhost:5049")
class MyHttpApiHost:
    
    @http_get('/WeatherForecast/{city}')
    def get_weather_by_city(self, city: str, days:int) -> dict:
        pass
    
    @http_get('/WeatherForecast/all')
    def get_all_weather_forecast(self, city: str, days:int) -> dict:
        pass
    
    @http_post('/WeatherForecast/{city}')
    def create_weather_forecast(self, city: str, days:int) -> dict:
        pass

api = MyHttpApiHost()
print(api.get_weather_by_city("shanghai", 3))
```
