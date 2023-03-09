from .explorations import skill_check, earn

from .actions import Action, VisitAction

import .locations

class SettlementEncounterResultAction(Action):
    pass


def mercs(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("hr"), deck)
    if i > 0 : return None

    engine.msg("Mercenaries will train you, for a price")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+1 Max Stamina (100 credits)"
        def perform(self):
            if self.entity.credits >= 100:
                self.entity.credits -= 100
                self.entity.max_stamina += 1
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)


    class optionB(SettlementEncounterResultAction):
        FLAVOR = "+1 H (200 credits)"
        def perform(self):
            if self.entity.credits >= 200:
                self.entity.credits -= 200
                self.entity.h += 1
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]


def water_merchants(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("Water Merchants with assorted goods")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+1 Max Water (80 credits)"
        def perform(self):
            if self.entity.credits >= 80:
                self.entity.credits -= 80
                self.entity.max_water += 1
                self.engine.settlement_actions.pop(event.K_6, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Recover all water (10 credits)"
        def perform(self):
            if self.entity.credits >= 10:
                self.entity.credits -= 10
                self.entity.water = self.entity.max_water
                self.engine.settlement_actions.pop(event.K_7, None)

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
        def perform(self):
            if self.entity.credits >= 20:
                self.entity.credits -= 20
                self.entity.quest += 1
        def available(self):
            return self.entity.quest_guild is not None

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Sell 1 quest item (15 credits)"
        def perform(self):
            if self.entity.quest > 0:
                self.entity.credits += 15
                self.entity.quest -= 1
        def available(self):
            return self.entity.quest > 0

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def hire_major(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc.level, entity.skill_test_n("kr"), deck)
    if i > 0 : return None

    engine.msg("Major house agent paying for intel.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Sell intel on guild locations."
        def perform(self):
            self.engine.settlement_actions.pop(event.K_6, None)
            self.engine.settlement_actions.pop(event.K_7, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Sell 1 relic (60 credits)"
        def perform(self):
            if self.entity.relic > 0:
                self.entity.credits += 60
                self.entity.relic -= 1
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
        def available(self):
            return self.entity.relic > 0

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
        def perform(self):
            if self.entity.credits >= 10:
                self.entity.credits -= 10
                self.entity.quest += 1
        def available(self):
            return self.entity.quest_guild is not None

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "equipment"
        def perform(self):
            pass
        # TODO

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
        def perform(self):
            self.entity.credits += 5
            self.entity.stamin -= 1
        def available(self):
            return self.entity.stamina > 0

    oa = optionA(engine, entity)

    return [oa]

def guild_merchants(engine, entity):
    engine.msg("Guild merchants selling high quality equipment surpluses.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "150"
        def perform(self):
            pass
        #TODO

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "300"
        def perform(self):
            pass
        #TODO

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def traveling_mechanic(engine, entity):
    engine.msg("A famous traveling mechanic offering services you won't find anywhere else.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "speed tweaks (75 credits)"
        def perform(self):
            if self.entity.credits >= 75:
                self.entity.speed += 1
                self.entity.credits -= 75
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
                self.engine.settlement_actions.pop(event.K_8, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "fuel tank tweaks (75)"
        def perform(self):
            pass
            if self.entity.credits >= 75:
                self.entity.max_fuel += 1
                self.entity.credits -= 75
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
                self.engine.settlement_actions.pop(event.K_8, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "cargo space tweaks (50)"
        def perform(self):
            pass
            if self.entity.credits >= 50:
                self.entity.credits -= 50
                self.entity.max_cargo += 1
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
                self.engine.settlement_actions.pop(event.K_8, None)

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def informant(engine, entity):
    engine.msg("A cloaked house informant selling information on the region")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "reveal"
        def perform(self):
            if self.entity.credits >= 20:
                pass
                #TODO

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "double scrap for a turn"
        def perform(self):
            if self.entity.credits >= 50:
                self.entity.DOUBLE_SCRAP = getattr(self.entity, "DOUBLE_SCRAP", 0) + 1
                self.entity.credits -= 50

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def fortune_teller(engine, entity):
    engine.msg("a traveling fortune teller who will guide your life in a new direction.")

    roll = engine.deck.top

    mod = {}
    if roll.rank == 'W': mod['h']=1
    if roll.rank == 'K': mod['k']=1
    if roll.rank == 'Q': mod['r']=1
    if roll.rank == 'J': mod['h'], mod['k']=2,-1
    if roll.rank == '0': mod['k'], mod['r']=2,-1
    if roll.rank == '9': mod['r'], mod['h']=2,-1
    if roll.rank == '8': mod['h'], mod['r']=1,-1
    if roll.rank == '7': mod['k'], mod['h']=1,-1
    if roll.rank == '6': mod['r'],mod['k']=1,-1
    if roll.rank == '5': mod['stamina'], mod['h']=1,-1
    if roll.rank == '4': mod['stamina'], mod['k']=1,-1
    if roll.rank == '3': mod['stamina'], mod['r']=1,-1
    if roll.rank == '2': mod['stamina']=1
    if roll.rank == 'A': mod['h']=1

    for k,v in mod.items():
        setattr(self.entity, k, max(1, getattr(self.entity, k, 0) + v))

    return none

def cartographer(engine, entity):
    engine.msg("a local cartographer is selling maps of the region")

    class optiona(visitaction):
        flavor = "reveal (10)"
        limit = 5
        def perform(self):
            if self.entity.credits >= 10:
                self.entity.credits -= 10
                self.limit = self.limit - 1
                pass
                #TODO
            if self.limit == 0:
                self.engine.settlement_actions.pop(event.K_6, None)

    return [oa]

def drifter(engine, entity):
    engine.msg("an old drifer, who has lived many years on Eridoor.")
    import .companions

    class optiona(visitaction):
        flavor = "Hire Host, a seeker"
        def perform(self)
            companion = companion.Host()
            self.engine.msg(f"{companion} joins you")
            companion.join(e)
            self.engine.settlement_actions.pop(event.K_6, None)
            self.engine.settlement_actions.pop(event.K_7, None)
        def available(self):
            if len(self.companion) > 0 : return False
            return companions.Seeker in companions.COMPANION_DECK.values()



    class optionb(visitaction):
        flavor = "Hire Kale, a mystic"
        def perform(self)
            companion = companion.Mystic()
            self.engine.msg(f"{self.companion} joins you")
            companion.join(e)
            self.engine.settlement_actions.pop(event.K_6, None)
            self.engine.settlement_actions.pop(event.K_7, None)
            pass
        def available(self):
            if len(self.companion) > 0 : return False
            return companions.Mystic in companions.COMPANION_DECK.values()

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
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "+1 H (100 credits)"
        def perform(self)
            pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]


def scrap_dealers(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("Scrap dealers offering good deals for those interested.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
            pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def bounty_hunters(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("Bounty hunters looking for intel.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
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
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
            pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def food_vendor(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("A food vendor, cooking up something mouthwatering.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
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
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
            pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def tea(engine, entity):
    engine.msg("enjoy a quiet cup of tea.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
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
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
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
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
            pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def festival(engine, entity):
    engine.msg("The Festival of Merchants is happening. Time to kick back and enjoy the celebration.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
            pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def glider_race_mechanic(engine, entity):
    engine.msg("A glider race mechanic offers to increase your speed or fuel capacity.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
            pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

def spike(engine, entity):
    engine.msg("The legendary smuggler is here, of all places.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+2 cargo (80 credits)"
        def perform(self)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self)
            pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

