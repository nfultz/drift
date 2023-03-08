def skill_check(level, stat, deck):
    stat = {1:2, 2:4, 3:7, 4:9, 5:11, 6:14}[stat]

    for i in range(level,0, -1):
        if deck.top.value >= stat: return i
    return 0

def earn(entity, level=1, **kwargs):
    for k,v in kwargs.items():
        if k == 'stamina':
            entity.stamina = min(entity.stamina + v, entity.max_stamina)
        if k == 'cargo':
            entity.cargo = min(entity.cargo + v*level, entity.max_cargo)
        if k == 'relic':
            entity.relic = min(entity.relic + v, entity.max_relic)
        if k == 'credits':
            entity.credits += v*level
        if k == 'quest':
            entity.quest += v*level
        if k == 'water':
            entity.water = min(entity.water + v, entity.max_water)
    return kwargs



####### DESERT EXPLORATIONS


def crashed_drone(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hkr"), deck)
    if i > 0 : return i
    return earn(entity, cargo=2, quest=1)

def old_solar_arrays(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return i
    return earn(entity, cargo=3)

def hidden_military_gear(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hr"), deck)
    if i > 0 : return i
    return earn(entity, cargo=3, quest=1, credits=25)


def communications_tower(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return i
    return earn(entity, cargo=3, quest=1)

def hibernation pods(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hkr"), deck)
    if i > 0 : return i
    return earn(entity, cargo=3, quest=1, stamina=entity.max_stamina)

def explorer_campground_pods(loc, entity, deck):
    entity.stamina = entity.max_stamina
    i = skill_check(loc.level, entity.skill_test_n("hr"), deck)
    if i > 0 : return i
    return earn(entity, level, credits=5, quest=1)
    #TODO choose

def buried_storage_crates(loc, entity, deck):
    entity.cargo += 2
    i = skill_check(loc.level, entity.skill_test_n("hkr"), deck)
    if i > 0 : return i
    return earn(entity, level, credits=10, quest=1, cargo=2)

def hidden_landing_pad(loc, entity, deck):
    entity.cargo += 2
    return earn(entity, cargo=2)
    #TODO choose


def hidden_atomics_storage(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return i
    return earn(entity, relic=2)

def small_hidden_safe_house(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hk"), deck)
    if i > 0 : return i
    return earn(entity, relic=1, credits=20, quest=1)

def small_harvester_wrecks(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hkr"), deck)
    if i > 0 : return i
    return earn(entity, quest=1)
    #TODO choose

def pilgrims_path_and_temple(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hr"), deck)
    if i > 0 : return i
    return earn(entity, relic=1, quest=2)

def locked_scavenger_tools(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return i
    return earn(entity, cargo=1, quest=1)

def hidden_water_storage(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return i
    return earn(entity, water=entity.max_water, cargo=1, quest=1)

def dried_well_and_ladder(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hkr"), deck)
    if i > 0 : return i
    return earn(entity, relic=1, credits=10)

def lone_trader(loc, entity, deck):
    #TODO
    pass

def suspicious_small_wind_traps(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("k"), deck)
    if i > 0 : return i
    j = skill_check(loc.level, entity.skill_test_n("r"), deck)
    return earn(entity, relic=1, credits=20 if j == 0 else 0)

def machine_scrap_pile(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hkr"), deck)
    if i > 0 : return i
    #TODO CHOOSE
    return earn(entity, cargo=1)

def old_major_house_outpost(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hk"), deck)
    if i > 0 : return i
    return earn(entity, credits=10, quest=1) #TODO typo in book table

def maintenance_shaft(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hr"), deck)
    if i > 0 : return i
    return earn(entity, credits=5, cargo=1)

def spaceship_graveyard(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hkr"), deck)
    if i > 0 : return i
    return earn(entity, cargo=2, quest=1)

def mechanics_workshop(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return i
    #TODO glider upgrade
    j = skill_check(loc.level, entity.skill_test_n("hkr"), deck)
    return earn(entity, cargo=3 if j ==0 else 0)


def forgotten_shuttle(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hr"), deck)
    if i > 0 : return i
    return earn(entity, cargo=2, relic=1)
    #TODO choose

def chemical_research_lab(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return i
    return earn(entity, relic=1, quest=1, water=2)

def scrap_stockpile(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("hkr"), deck)
    if i > 0 : return i
    return earn(entity, cargo=3, quest=1)

def mirror_to_another_world(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return i
    #todo teleport
    return earn(entity, relics=2)

def crater_with_glowing_crate_and_goo(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("h"), deck)
    if i > 0 : return i
    return earn(entity, relics=1)

def small_otherworldly_spaceship(loc, entity, deck):
    i = skill_check(loc.level, entity.skill_test_n("k"), deck)
    if i > 0 : return i
    #todo teleport
    return earn(entity, cargo=5, relic=1)



DESERT_EXPLORATIONS = {
    True: {
      'A': crashed_drone,
      '2': hidden_military_gear,
      '3': hibernation_pods,
      '4': buried_storage_crates,
      '5': hidden_atomics_storage,
      '6': small_harvester_wrecks,
      '7': locked_scavenger_tools,
      '8': dried_well_and_ladder,
      '9': suspicious_small_wind_traps,
      '0': old_major_house_outpost,
      'J': spaceship_graveyard,
      'Q': forgotten_shuttle,
      'K': scrap_stockpile,
      'W': crater_with_glowing_crate_and_goo
      }
    False: {
      'A': old_solar_arrays,
      '2': communications_tower,
      '3': explorer_campground_pods,
      '4': hidden_landing_pad,
      '5': small_hidden_safe_house,
      '6': pilgrims_path_and_temple,
      '7': hidden_water_storage,
      '8': lone_trader,
      '9': machine_scrap_pile,
      '0': maintenance_shaft,
      'J': mechanics_workshop,
      'Q': chemical_research_lab,
      'K': mirror_to_another_world,
      'W': small_otherworldly_spaceship,
      }
    }
