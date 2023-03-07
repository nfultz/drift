def reset(engine):
    engine.WEATHER_SPICE_CLOUDS = 0
    engine.WEATHER_EXREME_HEAT  = 0
    engine.WEATHER_SAND_STORM   = 0
    engine.WEATHER_WIND_BACK    = 0

def sand_storm(engine):
    engine.msg("A sand storm is on the horizon, preventing movement for a while.")
    engine.WEATHER_SAND_STORM = 1#TODO

def wind_at_your_back(engine):
    engine.msg("The wind is at your back - take advantage of the opportunity to explore.")
    engine.WEATHER_WIND_BACK = 1#TODO

def calm_breeze(engine):
    engine.msg("Clear skies and a pleasnt breeze across the golden dunes.")
    engine.fatigue = 0

def extreme_sun(engine):
    engine.msg("The sun beats down, making it hard to move.")
    engine.WEATHER_EXREME_HEAT = 1#TODO

def spice_clouds(engine):
    engine.msg("Blue and orange dance together in pockets of brilliant spice.")
    engine.WEATHER_SPICE_CLOUDS = 1#TODO

def noxious_miasma(engine):
    engine.msg("The smell of something rotten blankets your senses and turns your stomach.")
    for e in engine.entities:
        e.stamina = max(0, e.stamina - 3)

def rain(engine):
    engine.msg("Sometimes the impossible becomes reality - rain in the desert.")
    for e in engine.entities:
        e.stamina = e.max_stamina
        e.water = e.max_water


WEATHER_EVENTS = {
  'A': sand_storm,
  '2': wind_at_your_back,
  '3': wind_at_your_back,
  '4': wind_at_your_back,
  '5': wind_at_your_back,
  '6': calm_breeze,
  '7': calm_breeze,
  '8': calm_breeze,
  '9': calm_breeze,
  '0': calm_breeze,
  'J': extreme_sun,
  'Q': spice_clouds,
  'K': noxious_miasma,
  'W': rain
}

def draw(deck):
    return WEATHER_EVENTS[deck.bottom.rank]
