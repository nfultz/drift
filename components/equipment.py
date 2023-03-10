
items = []
def draw(card):
    return items.pop(card.value % len(items)) if len(items) >0 else None

def _equip(name='', cost=0, glider=False):
    def wrap(f):
        f.name = name
        f.cost = cost
        f.glider_upgrade = glider
        items.append(f)
        return f
    return wrap

@_equip("Snack Containers",25)
def snack(entity):
    entity.SNACK = 1

@_equip("Scavengers' Modular Storage", 25)
def scav_storage(entity):
    entity.max_cargo += 2

@_equip("Desert Campsite Toolkit", 50)
def desert_campsite_toolkit(entity):
    entity.DESERT_CAMPSITE_TOOLKIT = 1


@_equip("Weather Monitor", 60)
def weather_monitor(entity):
    entity.WEATHER_MONITOR = 1

#TODO
@_equip("Explorer Sling", 75)
def f(entity):
    pass

@_equip("Heat Regulator", 80)
def heat_regulator(entity):
    entity.HEAT_REGULATOR = 1

@_equip("Medical Pack", 90)
def medical_pack(entity):
    entity.MEDICAL_PACK = 1

@_equip("Air Purifier Mask", 95)
def air_purifier(entity):
    entity.AIR_PURIFIER = 1

@_equip("Improved Hot Weather Clothing", 100)
def hot_weather_clothes(entity):
    entity.max_stamina += 1

@_equip("Wayfinding Binoculars", 130)
def wayfinding_binoculars(entity):
    entity.WAYFINDING = 1

@_equip("Data Decryption Algo", 140)
def data_decrypt(entity):
    entity.k += 1

@_equip("Sand Drummer System", 140)
def drummer(entity):
    entity.r += 1

@_equip("Magnetic Grapple Gloves", 140)
def grapple(entity):
    entity.h += 1

@_equip("Scrap Detection Unit", 160)
def scrap_detector(entity):
    entity.SCRAP_DETECTOR = 1
    pass

@_equip("Pathfinder Tools", 175)
def pathfinder_toosl(entity):
    entity.PATHFINDER_TOOLS = 1

@_equip("Environment Scanner Unit", 180)
def environment_scanner(entity):
    entity.ENV_SCANNER = 1

@_equip("Information Visor", 200)
def info_visor(entity):
    entity.k += 1
    entity.r -= 1

@_equip("Enhanced Strength Suit Switches", 200)
def strength_suit(entity):
    entity.h += 1
    entity.k -= 1

@_equip("Technicians' Tookit", 200)
def tech_toolkit(entity):
    entity.r += 1
    entity.h -= 1

@_equip("Credit Duplication Program", 250)
def credit_duplicator(entity):
    entity.CREDIT_DUPLICATOR = 5

@_equip("Piezo Moisture Capture", 300)
def piezo_capture(entity):
    entity.PIEZO_CAPTURE = 1
    pass

#TODO
@_equip("Thermal Cooling Underwear", 360)
def f(entity):
    pass


### Glider Upgrades

#TODO
@_equip("Optical Navigation Glasses", 80,True)
def f(entity):
    pass

@_equip("Stabilized Relic Storage", 90,True)
def stabilized_relics(entity):
    entity.max_cargo -= 2
    entity.max_relic += 1

@_equip("Anti-Gravity Towing Unit", 120,True)
def antigrav_towing(entity):
    entity.max_cargo += 6
    entity.speed -= 1

@_equip("Reserve Fuel Canisters", 145,True)
def reserve_fuel(entity):
    entity.max_fuel += 2
    entity.max_cargo -= 4

@_equip("Fuel Drip Injection Systems", 180,True)
def fuel_drip(entity):
    entity.max_fuel += 2
    entity.speed += 1

#TODO
@_equip("Long Range Communications", 200,True)
def f(entity):
    pass

#TODO
@_equip("Scavenger Arm", 260,True)
def f(entity):
    pass

#TODO
@_equip("Onboard Scanner", 260,True)
def f(entity):
    pass

#TODO
@_equip("Hacking Module", 260,True)
def f(entity):
    pass

@_equip("Portable Repair Kit", 300,True)
def portable_repait(entity):
    entity.PORTABLE_REPAIR = 1

@_equip("Fuel Recycle Kit", 400,True)
def fuel_recycler(entity):
    entity.FUEL_RECYCLE = 1
    pass

## Cargo upgrades

@_equip("Cargo Upgrade X", 90,True)
def cargo_x(entity):
    entity.max_cargo += 2
    entity.cargo_upgrade += 1
    if entity.cargo_upgrade == 3: entity.fame += 1

@_equip("Cargo Upgrade Y", 145,True)
def cargo_y(entity):
    entity.max_cargo += 2
    entity.cargo_upgrade += 1
    if entity.cargo_upgrade == 3: entity.fame += 1

@_equip("Cargo Upgrade Z", 215,True)
def cargo_z(entity):
    entity.max_cargo += 3
    entity.cargo_upgrade += 1
    if entity.cargo_upgrade == 3: entity.fame += 1

## Fuel upgrades

@_equip("Fuel Capacity Upgrade X", 110,True)
def fuel_x(entity):
    entity.max_fuel += 1
    entity.fuel_upgrade += 1
    if entity.fuel_upgrade == 3: entity.fame += 1

@_equip("Fuel Capacity Upgrade Y", 140,True)
def fuel_y(entity):
    entity.max_fuel += 1
    entity.fuel_upgrade += 1
    if entity.fuel_upgrade == 3: entity.fame += 1

@_equip("Fuel Capacity Upgrade Z", 180,True)
def fuel_z(entity):
    entity.max_fuel += 1
    entity.fuel_upgrade += 1
    if entity.fuel_upgrade == 3: entity.fame += 1


## Relic upgrades

@_equip("Relic Capacity Upgrade X", 100,True)
def relic_x(entity):
    entity.max_relic += 1
    entity.relic_upgrade += 1
    if entity.relic_upgrade == 3: entity.fame += 1

@_equip("Relic Capacity Upgrade Y", 200,True)
def relic_y(entity):
    entity.max_relic += 1
    entity.relic_upgrade += 1
    if entity.relic_upgrade == 3: entity.fame += 1

@_equip("Relic Capacity Upgrade Z", 300,True)
def relic_z(entity):
    entity.max_relic += 1
    entity.relic_upgrade += 1
    if entity.relic_upgrade == 3: entity.fame += 1


## Speed upgrades

@_equip("Top Speed Upgrade X", 120,True)
def speed_x(entity):
    entity.speed += 1
    entity.speed_upgrade += 1
    if entity.speed_upgrade == 3: entity.fame += 1

@_equip("Top Speed Upgrade Y", 240,True)
def speed_y(entity):
    entity.speed += 1
    entity.speed_upgrade += 1
    if entity.speed_upgrade == 3: entity.fame += 1

@_equip("Top Speed Upgrade Z", 420,True)
def speed_z(entity):
    entity.speed += 1
    entity.speed_upgrade += 1
    if entity.speed_upgrade == 3: entity.fame += 1
