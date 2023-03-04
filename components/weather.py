

def sand_storm():
    pass

def wind_at_your_back():
    pass

def calm_breeze():
    pass

def extreme_sun():
    pass

def spice_clouds():
    pass

def noxious_miasma():
    pass

def rain():
    pass


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
