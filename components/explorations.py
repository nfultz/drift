def skill_check(loc, entity, skill, deck, level=None):

    from .locations import Desert

    level = level or loc.level

    bonus = {'h':0, 'k':0, 'r':0}

    # TODO LONG-RANGE_COMS
    # for e in engine.entities:
    #     if e is entity: continue
    #     if hasattr(e, "LONG_RANGE_COMS"):
    #         bonus['h'] += 1
    #         bonus['k'] += 1
    #         bonus['r'] += 1

    if isinstance(loc, Desert):
        if hasattr(entity, "SCAVENGER_ARM"):   bonus["h"] += 1
        if hasattr(entity, "ONBOARD_SCANNER"): bonus["r"] += 1
        if hasattr(entity, "HACKING_MODULE"):  bonus["k"] += 1


    stat = entity.skill_test_n(skill, bonus)

    retry = 0
    retry += getattr(entity, "EXPLORER_SLING", 0)
    retry += getattr(entity, "BETA_REROLL", 0)
    retry += getattr(entity, "DELVER", 0)

    # Duncan bonus
    if 'h' in skill and entity.h + bonus['h'] == stat:
        retry += getattr(entity, "DUNCAN_REROLL", 0)

    stat = {1:2, 2:4, 3:7, 4:9, 5:11, 6:14}[stat]

    for i in range(level,0, -1):
        if deck.top.value > stat:
            while retry > 0:
                  retry -= 1
                  if deck.top.value <= stat:
                      break
            else:
                return i
    return 0

def earn(entity, level=1, **kwargs):

    if hasattr(entity, "WORK_FOR_HIRE"):
        if entity.quest_guild is not None:
            kwargs['quest'] = kwargs.get('quest', 0) + 1

    for k,v in list(kwargs.items()): #NB: need list() bc of quest.pop below
        if v == 0:
            kwargs.pop(k)
            continue
        if k == 'stamina':
            entity.stamina = min(entity.stamina + v, entity.max_stamina)
        if k == 'cargo':
            if entity.cargo >= entity.max_cargo:
                if hasattr(entity, "ENV_SCANNER") and entity.quest_guild is not None:
                    entity.quest += 1
                    kwargs.pop('cargo')
                    kwargs['quest'] = kwargs.get('quest', 0) + 1
                continue
            m = getattr(entity,"DOUBLE_SCRAP",0)
            if m > 0:
                m = min(informant, v)
                v -= m
                entity.DOUBLE_SCRAP -= m
                kwargs['cargo'] += m
            entity.cargo = min(entity.cargo + m + v*level+getattr(entity, "SCRAP_DETECTOR", 0), entity.max_cargo)
        if k == 'relic':
            entity.relic = min(entity.relic + v, entity.max_relic)
        if k == 'credits':
            entity.credits += v*level
        if k == 'quest':
            if entity.quest_guild is not None:
                entity.quest += v*level + getattr(entity, "BETA_REROLL", 0)/2
            else:
                kwargs.pop("quest")
        if k == 'water':
            entity.water = min(entity.water + v, entity.max_water)
        if k == 'fame':
            entity.fame += 1
    return kwargs



####### DESERT EXPLORATIONS


def crashed_drone(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=2, quest=1)

def old_solar_arrays(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=3)

def hidden_military_gear(loc, entity, deck):
    i = skill_check(loc, entity, "hr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=3, quest=1, credits=25)


def communications_tower(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=3, quest=1)

def hibernation_pods(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=3, quest=1, stamina=entity.max_stamina)

def explorer_campground_pods(loc, entity, deck):
    entity.stamina = entity.max_stamina
    i = skill_check(loc, entity, "hr", deck)
    if i > 0 : return i
    return earn(entity, loc.level, credits=5, quest=1)
    #TODO choose

def buried_storage_crates(loc, entity, deck):
    entity.cargo += 2
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity, level=loc.level, credits=10, quest=1, cargo=2)

def hidden_landing_pad(loc, entity, deck):
    return earn(entity,level=loc.level, cargo=2)
    #TODO choose


def hidden_atomics_storage(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    return earn(entity, relic=2)

def small_hidden_safe_house(loc, entity, deck):
    i = skill_check(loc, entity, "hk", deck)
    if i > 0 : return i
    return earn(entity,level=loc.level, relic=1, credits=20, quest=1)

def small_harvester_wrecks(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, quest=1)
    #TODO choose

def pilgrims_path_and_temple(loc, entity, deck):
    i = skill_check(loc, entity, "hr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, relic=1, quest=2)

def locked_scavenger_tools(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=1, quest=1)

def hidden_water_storage(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, water=entity.max_water, cargo=1, quest=1)

def dried_well_and_ladder(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, relic=1, credits=10)

def lone_trader(loc, entity, deck): #TODO
    return 0

def suspicious_small_wind_traps(loc, entity, deck):
    i = skill_check(loc, entity, "k", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "r", deck)
    return earn(entity,loc.level, relic=1, credits=20 if j == 0 else 0)

def machine_scrap_pile(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    #TODO CHOOSE
    return earn(entity,loc.level, cargo=1)

def old_major_house_outpost(loc, entity, deck):
    i = skill_check(loc, entity, "hk", deck)
    if i > 0 : return i
    return earn(entity,loc.level, credits=10, quest=1) #TODO typo in book table

def maintenance_shaft(loc, entity, deck):
    i = skill_check(loc, entity, "hr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, credits=5, cargo=1)

def spaceship_graveyard(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=2, quest=1)

def mechanics_workshop(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    #TODO glider upgrade
    j = skill_check(loc, entity, "hkr", deck)
    return earn(entity,loc.level, cargo=3 if j ==0 else 0)


def forgotten_shuttle(loc, entity, deck):
    i = skill_check(loc, entity, "hr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=2, relic=1)
    #TODO choose

def chemical_research_lab(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, relic=1, quest=1, water=2)

def scrap_stockpile(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=3, quest=1)

def mirror_to_another_world(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    #todo teleport
    return earn(entity,loc.level, relics=2)

def crater_with_glowing_crate_and_goo(loc, entity, deck):
    i = skill_check(loc, entity, "h", deck)
    if i > 0 : return i
    return earn(entity,loc.level, relics=1)

def small_otherworldly_spaceship(loc, entity, deck):
    i = skill_check(loc, entity, "k", deck)
    if i > 0 : return i
    #todo teleport
    return earn(entity,loc.level, cargo=5, relic=1)



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
      },
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


#### Location explorations

@staticmethod
def spices_once_flowed(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=2, quest=1)

@staticmethod
def gone_with_the_desert_winds(loc, entity, deck):
    i = skill_check(loc, entity, "rk", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=1, quest=1)

@staticmethod
def a_friendly_keeper(loc, entity, deck):
    e = earn(entity,loc.level, stamina=entity.max_stamina)
    # TODO Reveal
    return e

@staticmethod
def a_long_and_quiet_view(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, water=1, credits=5, quest=1)

@staticmethod
def cracked_shell(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=2, quest=2, relic=1)

@staticmethod
def encrypted_security(loc, entity, deck):
    i = skill_check(loc, entity, "k", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=3, quest=3, relic=3)

@staticmethod
def captains_log(loc, entity, deck):
    i = skill_check(loc, entity, "h", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=1, quest=1)

@staticmethod
def engineers_log(loc, entity, deck):
    i = skill_check(loc, entity, "rk", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=3)

@staticmethod
def warehouse_wonders(loc, entity, deck):
    i = skill_check(loc, entity, "hr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "hkr", deck)
    return earn(entity,loc.level, cargo=4 if j ==0 else 1, quest=2 if j == 0 else 1)

@staticmethod
def rusted_robotics_workshop(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "k", deck)
    return earn(entity,loc.level, cargo=1, quest=1, relics=2 if j == 0 else 0)

@staticmethod
def guiding_light_keeper(loc, entity, deck): #TODO
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "k", deck)
    return earn(entity,loc.level, cargo=1, quest=1, relics=2 if j == 0 else 0)

@staticmethod
def lost_ways(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "kr", deck)
    return earn(entity,loc.level, cargo=1,  credits=20 if j == 0 else 0, relics=1 if j == 0 else 0, stamina=entity.max_stamina if j ==0 else 0)

@staticmethod
def empty_escape_pods(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "hkr", deck)
    return earn(entity,loc.level, cargo=3 if j == 0 else 2,  credits=5, relics=1 if j == 0 else 0)

@staticmethod
def sealed_for_your_protection(loc, entity, deck):
    i = skill_check(loc, entity, "hk", deck)
    if i > 0 : return i
    return earn(entity,loc.level, relic=2, cargo=1, credits=100)

@staticmethod
def the_sound_of_eridoor(loc, entity, deck): #TODO flavor text
    i = skill_check(loc, entity, "h", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "hr", deck)
    return earn(entity,loc.level, relic=1, fame=3)

@staticmethod
def the_light_of_eridoor(loc, entity, deck): #TODO flavor text
    i = skill_check(loc, entity, "hr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "h", deck)
    return earn(entity,loc.level, relic=1, fame=3)


@staticmethod
def untouched_relics_of_the_past(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "k", deck)
    return earn(entity,loc.level, relic=1, credtis=50, quest = 2 if j ==0 else 0, cargo=3 if j ==0 else 0)

@staticmethod
def abandoned_and_worn_to_time(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "kr", deck)
    return earn(entity,loc.level, cargo=3 if j ==0 else 2, quest=1, relic=1 if j ==0 else 0, credits = 30 if j == 0 else 0)

@staticmethod
def jaws_of_razors(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, relic=1, quest=2)

@staticmethod
def belly_of_the_beast(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity,loc.level, cargo=3, quest=1)

@staticmethod
def bottom_of_the_tank(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "kr", deck)
    return earn(entity,loc.level, fuel=entity.max_fuel, cargo=2 if j ==0 else 0, quest=1 if j ==0 else 0)
    #TODO choose

@staticmethod
def glider_mods_galore(loc, entity, deck):
    i = skill_check(loc, entity, "hr", deck)
    if i > 0 : return i
    #TODO earn upgrade
    j = skill_check(loc, entity, "hk", deck)
    #TODO earn upgrade

    return earn(entity, loc.level)

    #TODO choose


@staticmethod
def a_long_way_down(loc, entity, deck):
    return earn(entity,loc.level, cargo=1)

@staticmethod
def an_even_longer_way(loc, entity, deck):
    return earn(entity,loc.level,  quest=1)

@staticmethod
def the_heart_of_eridoor(loc, entity, deck):
    return earn(entity,loc.level,  stamina=entity.max_stamina, fame=1)

@staticmethod
def the_vision_of_eridoor(loc, entity, deck):
    #TODO reveal
    return earn(entity,loc.level,  fame=1)

@staticmethod
def a_big_hole(loc, entity, deck):
    return earn(entity,loc.level,  quest=1)

@staticmethod
def an_even_bigger_hole(loc, entity, deck):
    return earn(entity,loc.level,  cargo=1)

@staticmethod
def miners_bounty(loc, entity, deck):
    i = skill_check(loc, entity, "hr", deck)
    if i > 0 : return i
    #TODO teleport
    return earn(entity,loc.level,  cargo=2, quest=1)

@staticmethod
def credit_payment_machine(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    #TODO teleport
    return earn(entity,loc.level,  credits=20, quest=1)

@staticmethod
def battlefield_spoils(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    #TODO choose
    return earn(entity,loc.level,  cargo=1, relic=1)

@staticmethod
def buried_memories(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "hr", deck)
    #TODO choose
    return earn(entity,loc.level,  cargo=1, quest=1 if j == 0 else 0)

@staticmethod
def researchers_score(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "k", deck)
    return earn(entity,loc.level,  cargo=1, credits=5, quest=2 if j ==0 else 0 )

@staticmethod
def scientists_working(loc, entity, deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "k", deck)
    #TODO choose
    return earn(entity,loc.level,  cargo=2,  quest=3 if j ==0 else 1 )

@staticmethod
def sanded_down_over_time(loc, entity, deck):
    return earn(entity,loc.level,  quest=1)

@staticmethod
def never_ending_height(loc, entity, deck):
    return earn(entity,loc.level,  cargo=1)

@staticmethod
def that_sinking_feeling(loc, entity, deck):
    return earn(entity,loc.level, credits=5)

@staticmethod
def down_the_drain(loc, entity, deck):
    return earn(entity,loc.level,  cargo=1, quest=1)

@staticmethod
def scattered_ruins(loc, entity, deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    return earn(entity, loc.level, cargo=1, quest=1, stamina=2)

@staticmethod
def barely_standing_structures(loc, entity, deck):
    i = skill_check(loc, entity, "hr", deck)
    if i > 0 : return i
    return earn(entity,loc.level,  cargo=2, quest=1)

@staticmethod
def tip_of_the_sunken_tower(loc, entity, deck):
    return earn(entity,loc.level, cargo=5)

@staticmethod
def safe_haven(loc, entity, deck):
    return earn(entity,loc.level,  cargo=2, quest=1, stamina=3, water=1)

@staticmethod
def operation_restore_eridoor(loc,entity,deck):
    i = skill_check(loc, entity, "k", deck)
    if i > 0 : return i
    j = skill_check(loc, entity, "kr", deck)
    return earn(entity,loc.level,  cargo=1 if j==0 else 0,  relic=2 if j ==0 else 1 )

@staticmethod
def tour_the_facility(loc,entity,deck):
    #water stat any stat #TODO
    pass

@staticmethod
def credits_unpaid(loc,entity,deck):
    i = skill_check(loc, entity, "kr", deck)
    if i > 0 : return i
    return earn(entity,loc.level,  credits=60,quest=1 )

@staticmethod
def glider_transports(loc,entity,deck):
    i = skill_check(loc, entity, "r", deck)
    #TODO glider upgrade
    if i > 0 : return i
    return earn(entity,loc.level,  fuel=1)

@staticmethod
def recording_weather_data(loc,entity,deck):
    i = skill_check(loc, entity, "hk", deck)
    if i > 0 : return i
    # TODO ignore weather
    # TODO reveal
    return earn(entity,loc.level,  cargo=1)

@staticmethod
def damaged_relay(loc,entity,deck):
    i = skill_check(loc, entity, "hkr", deck)
    if i > 0 : return i
    # TODO ignore weather
    # TODO reveal
    return earn(entity,loc.level,  cargo=2)
