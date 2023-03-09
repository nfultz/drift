from .explorations import skill_check, earn

from .actions import Action, VisitAction

class SettlementEncounterResultAction(Action):
    def available(self): return True
    pass


def mercs(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("hr"), deck)
    if i > 0 : return None

    engine.msg("Mercenaries will train you, for a price")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+1 Max Stamina (100 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "+1 H (100 credits)"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]


def water_merchants(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("Water Merchants with assorted goods")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+1 Max Water (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Recover all water (10 credits)"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def hire_minor(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return None

    engine.msg("Hire a minor house agent to establish an exchange.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+1 quest item (20 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Sell 1 quest item (15 credits)"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def hire_major(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return None

    engine.msg("Major house agent paying for intel.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Sell intel."
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Sell 1 relic (60 credits)"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]



def market_day(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("hk"), deck)
    if i > 0 : return None

    engine.msg("Market day in the settlement.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Buy 1 quest item (10 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "equipment"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def work_trader(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("hr"), deck)
    if i > 0 : return None

    engine.msg("Sign up to work for a trader and make some extra credits.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Work for 5 credits (! stamina)"
        pass

    oa = optionA(engine, entity)

    return [oa]

def guild_merchants(engine, entity):
    engine.msg("Guild merchants selling high quality equipment surpluses.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "150"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "300"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def traveling_mechanic(engine, entity):
    engine.msg("A famous traveling mechanic offering services you won't find anywhere else.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "speed"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "fuel"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "cargo"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def informant(engine, entity):
    engine.msg("A cloaked house informant selling information on the region")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "reveal"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "double scrap"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def fortune_teller(engine, entity):
    engine.msg("a traveling fortune teller who will guide your life in a new direction.")

    class optiona(visitaction):
        flavor = "reveal"
        pass

    class optionb(visitaction):
        flavor = "double scrap"
        pass

    oa = optiona(engine, entity)
    ob = optionb(engine, entity)

    return [oa, ob]

def cartographer(engine, entity):
    engine.msg("a local cartographer is selling maps of the region")

    class optiona(visitaction):
        flavor = "reveal"
        pass

    oa = optiona(engine, entity)

    return [oa, ob]

def drifter(engine, entity):
    engine.msg("an old drifer, who has lived many years on Eridoor.")

    class optiona(visitaction):
        flavor = "Host"
        pass

    class optionb(visitaction):
        flavor = "Kale"
        pass

    oa = optiona(engine, entity)
    ob = optionb(engine, entity)

    return [oa, ob]


###

def scouts(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return None

    engine.msg("Sand scouts selling information")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+1 Max Stamina (100 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "+1 H (100 credits)"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]


def scrap_dealers(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("Scrap dealers offering good deals for those interested.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def bounty_hunters(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("Bounty hunters looking for intel.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def raided(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("hk"), deck)
    if i > 0 : return None

    engine.msg("Water has been raided, and people are paying for any you can spare.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def food_vendor(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("A food vendor, cooking up something mouthwatering.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def trader_used(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return None

    engine.msg("a trader selling a large collection of 'gently' used equipment")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def tea(engine, entity):
    engine.msg("enjoy a quiet cup of tea.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def red_mercs(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return None

    engine.msg("Mercenaries offering Credits for job leads.")
    engine.msg("enjoy a quiet cup of tea.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def smugglers(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return None

    engine.msg("Smugglers looking to purchase relics and scrap at a good price.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def festival(engine, entity):
    engine.msg("The Festival of Merchants is happening. Time to kick back and enjoy the celebration.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def glider_race_mechanic(engine, entity):
    engine.msg("A glider race mechanic offers to increase your speed or fuel capacity.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def spike(engine, entity):
    engine.msg("The legendary smuggler is here, of all places.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

