from pathlib import Path

from fastapi import FastAPI
import uvicorn

from roger.dataclasses import Playability, Version, Weather
from roger.inference import run_inference_on_live

app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/infer/live/{version}')
def get_live_prediction(version: Version, weather: Weather):
    model_path = Path(f'./models/{version}/tennis.pkl')
    playability_ = run_inference_on_live(
        model_path=model_path,
        outlook=weather.outlook,
        temperature=weather.temperature,
        humidity=weather.humidity,
        wind=weather.wind,
    )
    play_map: dict[bool, str] = {
        True: 'for playing',
        False: 'not to play',
    }
    Playability(
        outlook=weather.outlook,
        temperature=weather.temperature,
        humidity=weather.humidity,
        wind=weather.wind,
        can_play=playability_,
        description=f"""When
        {weather.outlook.value=} &
        {weather.temperature.value=} &
        {weather.humidity.value=} &
        {weather.wind.value=},
        It is advised {play_map.get(playability_)}""",
    )
    # return Playability


def start():
    """Launched with `poetry run start` at root level."""
    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)
