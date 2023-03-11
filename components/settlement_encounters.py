from .explorations import skill_check, earn

from .actions import Action, VisitAction, RevealAction

from  . import locations

from tcod import event # :(event

class SettlementEncounterResultAction(Action):
    pass

items = {}
def draw(card):
    return items[card]

def _add(*cards):
    def wrap(f):
        for card in cards:
            items[card] = f
        return f
    return wrap

@_add("AC", "AS")
def mercs(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc, entity, "hr", engine.deck)
    if i > 0 : return None

    engine.msg("Mercenaries will train you, for a price")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+1 Max Stamina (100 credits)"
        def perform(self):
            if self.entity.credits >= 100:
                self.entity.credits -= 100
                self.entity.max_stamina += 1
                self.engine.settlement_actions.pop(event.K_6, None)

                if not hasattr(entity, "MARJORIE_BONUS"):
                    self.engine.settlement_actions.pop(event.K_7, None)


    class optionB(SettlementEncounterResultAction):
        FLAVOR = "+1 H (200 credits)"
        def perform(self):
            if self.entity.credits >= 200:
                self.entity.credits -= 200
                self.entity.h += 1
                if not hasattr(entity, "MARJORIE_BONUS"):
                    self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]


@_add("2C", "2S")
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

@_add("3C", "3S")
def hire_minor(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc, entity, "kr", engine.deck)
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

@_add("4C", "4S")
def hire_major(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc, entity, "kr", engine.deck)
    if i > 0 : return None

    engine.msg("Major house agent paying for intel.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Sell intel on guild locations."
        def perform(self):
            self.engine.settlement_actions.pop(event.K_6, None)
            if not hasattr(entity, "MARJORIE_BONUS"):
                self.engine.settlement_actions.pop(event.K_7, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Sell 1 relic (60 credits)"
        def perform(self):
            if self.entity.relic > 0:
                self.entity.credits += 60
                self.entity.relic -= 1
                if not hasattr(entity, "MARJORIE_BONUS"):
                    self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
        def available(self):
            return self.entity.relic > 0

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]



@_add("5C", "5S")
def market_day(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc, entity, "hk", engine.deck)
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
        from .equipment import items

        def perform(self):
            if self.entity.credits > self.cost:
                self.entity.credits -= self.cost
                self.item(self.entity)
                items.pop(self.idx)
                return

        def available(self):
            if not any(not i.glider for i in items.values()): return False
            n = 1
            for i, item in enumerate(items):
                if item.glider:continue
                if self.engine.deck.bottom.value % n == 0:
                    n = n+1
                    self.idx = i
                    self.item = item
            self.cost = self.item.cost // 10 * 5
            self.FLAVOR = f"Purchase {self.item.name} at {self.cost} credits (normally {self.item.cost})"
            return True

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

@_add("6C", "6S")
def work_trader(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc, entity, "hr", engine.deck)
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

@_add("7C", "7S")
def guild_merchants(engine, entity): #TODO choose
    engine.msg("Guild merchants selling high quality equipment surpluses.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Two for 150"
        def perform(self):
            n = 2
            total = 100
            if self.entity.credits >= 150:
                self.entity.credits -= 150
                from .equipment import items
                for idx, i in enumerate(list(items)):
                    if i.cost < total and not i.glider:
                        items.pop(idx)
                        i(self.entity)
                        total -= i.cost
                        n = n - 1
                        self.engine.settlement_actions.pop(event.K_6, None)
                        self.engine.settlement_actions.pop(event.K_7, None)
                        if n == 0: return

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Two for 300"
        def perform(self):
            n = 2
            total = 200
            if self.entity.credits >= 300:
                self.entity.credits -= 300
                from .equipment import items
                for idx, i in enumerate(list(items)):
                    if i.cost < total and not i.glider:
                        items.pop(idx)
                        i(self.entity)
                        total -= i.cost
                        n = n - 1
                        self.engine.settlement_actions.pop(event.K_6, None)
                        self.engine.settlement_actions.pop(event.K_7, None)
                        if n == 0: return

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

@_add("8C", "8S")
def traveling_mechanic(engine, entity):
    engine.msg("A famous traveling mechanic offering services you won't find anywhere else.")

    picked = [0]

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "speed tweaks (75 credits)"
        def perform(self):
            if self.entity.credits >= 75:
                picked[0] += 1
                self.entity.speed += 1
                self.entity.credits -= 75
                self.engine.settlement_actions.pop(event.K_6, None)
                if not hasattr(entity, "MARJORIE_BONUS") or picked >= 2:
                    self.engine.settlement_actions.pop(event.K_7, None)
                    self.engine.settlement_actions.pop(event.K_8, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "fuel tank tweaks (75)"
        def perform(self):
            if self.entity.credits >= 75:
                picked[0] += 1
                self.entity.max_fuel += 1
                self.entity.credits -= 75
                self.engine.settlement_actions.pop(event.K_7, None)
                if not hasattr(entity, "MARJORIE_BONUS") or picked >= 2:
                    self.engine.settlement_actions.pop(event.K_6, None)
                    self.engine.settlement_actions.pop(event.K_8, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "cargo space tweaks (50)"
        def perform(self):
            if self.entity.credits >= 50:
                picked[0] += 1
                self.entity.credits -= 50
                self.entity.max_cargo += 1
                self.engine.settlement_actions.pop(event.K_8, None)
                if not hasattr(entity, "MARJORIE_BONUS") or picked >= 2:
                    self.engine.settlement_actions.pop(event.K_6, None)
                    self.engine.settlement_actions.pop(event.K_7, None)

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

@_add("9C", "9S")
def informant(engine, entity):
    engine.msg("A cloaked house informant selling information on the region")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "reveal"
        def perform(self):
            rev = RevealAction(self.engine, self.entity)
            rev.COST = 0
            rev.radius = 10
            rev.min_dist=3
            rev.available()
            if self.entity.credits >= 20:
                self.entity.credits -=20
                rev.perform()

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "double scrap for a turn"
        def perform(self):
            if self.entity.credits >= 50:
                self.entity.DOUBLE_SCRAP = getattr(self.entity, "DOUBLE_SCRAP", 0) + 1
                self.entity.credits -= 50

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

@_add("0C", "0S")
def fortune_teller(engine, entity):
    engine.msg("a traveling fortune teller who will guide your life in a new direction.")

    roll = engine.deck.top

    mod = {}
    # TODO Lookup table
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
        setattr(entity, k, max(1, getattr(entity, k, 0) + v))

    return None

@_add("JC", "JS")
@_add("QC", "QS")
@_add("KC", "KS")
def cartographer(engine, entity):
    engine.msg("a local cartographer is selling maps of the region")

    class optiona(VisitAction):
        FLAVOR = "reveal (10)"
        limit = 5
        def perform(self):
            rev = RevealAction(self.engine, self.entity)
            rev.COST = 0
            rev.radius = 10
            rev.min_dist=3
            rev.available()
            if self.entity.credits >= 10:
                self.entity.credits -= 10
                self.limit = self.limit - 1
                rev.perform()
            if self.limit == 0:
                self.engine.settlement_actions.pop(event.K_6, None)

    return [optiona(engine, entity)]

@_add("WC", "WS")
def drifter(engine, entity):
    engine.msg("an old drifer, who has lived many years on Eridoor.")
    from . import companions

    class optiona(VisitAction):
        FLAVOR = "Hire Host, a seeker"
        def perform(self):
            companion = companion.Host()
            self.engine.msg(f"{companion} joins you")
            companion.join(e)
            self.engine.settlement_actions.pop(event.K_6, None)
            self.engine.settlement_actions.pop(event.K_7, None)
        def available(self):
            if len(self.entity.companions) > 0 : return False
            return companions.Seeker in companions.COMPANION_DECK.values()



    class optionb(VisitAction):
        FLAVOR = "Hire Kale, a mystic"
        def perform(self):
            companion = companion.Mystic()
            self.engine.msg(f"{self.companion} joins you")
            companion.join(e)
            self.engine.settlement_actions.pop(event.K_6, None)
            self.engine.settlement_actions.pop(event.K_7, None)
            pass
        def available(self):
            if len(self.entity.companions) > 0 : return False
            return companions.Mystic in companions.COMPANION_DECK.values()

    oa = optiona(engine, entity)
    ob = optionb(engine, entity)

    return [oa, ob]


###

@_add("AD", "AH")
def scouts(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc, entity, "kr", engine.deck)
    if i > 0 : return None

    engine.msg("Sand scouts selling information")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "reveal(20 credits)"
        limit = 2
        def perform(self):
            rev = RevealAction(self.engine, self.entity)
            rev.COST = 0
            rev.radius = 5
            rev.min_dist=2
            rev.available()
            rev2 = RevealAction(self.engine, self.entity)
            rev2.COST = 0
            rev2.radius = 5
            rev2.min_dist=2
            rev2.available()
            if self.entity.credits >= 20:
                self.entity.credits -= 20
                self.limit = self.limit - 1
                rev.perform()
                rev2.perform()
            if self.limit == 0:
                self.engine.settlement_actions.pop(event.K_6, None)

    oa = optionA(engine, entity)

    return [oa]


@_add("2D", "2H")
def scrap_dealers(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("Scrap dealers offering good deals for those interested.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "2 cargo (5 credits)"
        def perform(self):
            if self.entity.credits >= 5:
                self.entity.credits -= 5
                self.entity.cargo += 2
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self):
            if self.entity.credits >= 10:
                self.entity.credits -= 10
                self.entity.quest += 1
        def available(self):
            return self.entity.quest_guild is not None

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

@_add("3D", "3H")
def bounty_hunters(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("Bounty hunters looking for intel.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Sell intel."
        def perform(self):

            amt = 0
            for y in self.engine.game_map.locations.values():
                for loc in y.values():
                    if isinstance(loc, locations.Settlement):
                        amt += 1

            self.entity.credits += 10 *amt
            self.engine.settlement_actions.pop(event.K_6, None)

    oa = optionA(engine, entity)

    return [oa]

@_add("4D", "4H")
def raided(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc, entity, "hk", engine.deck)
    if i > 0 : return None

    engine.msg("Water has been raided, and people are paying for any you can spare.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Sell 1 water"
        def perform(self):
            if self.entity.water >= 1:
                self.entity.water -= 1
                self.entity.credits += 30
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
                self.engine.settlement_actions.pop(event.K_8, None)
            pass

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Sell 2 water"
        def perform(self):
            if self.entity.water >= 1:
                self.entity.water -= 1
                self.entity.credits += 30
                self.entity.quest += 1
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
                self.engine.settlement_actions.pop(event.K_8, None)
            pass
        def available(self):
            return self.entity.quest_guild is not None

    class optionC(SettlementEncounterResultAction):
        FLAVOR = "Sell 3 water"
        def perform(self):
            if self.entity.water >= 3:
                self.entity.water -= 3
                self.entity.credits += 50
                self.entity.quest += 2
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
                self.engine.settlement_actions.pop(event.K_8, None)
            pass
        def available(self):
            return self.entity.quest_guild is not None

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)
    oc = optionC(engine, entity)

    return [oa, ob, oc]

@_add("5D", "5H")
def food_vendor(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)

    engine.msg("A food vendor, cooking up something mouthwatering.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+1 to h"
        def perform(self):
            if self.entity.credits >= 25:
                self.entity.credits -= 25
                self.entity.h += 1 #TODO choose
                self.engine.settlement_actions.pop(event.K_6, None)
                if not hasattr(entity, "MARJORIE_BONUS"):
                    self.engine.settlement_actions.pop(event.K_7, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "quest item"
        def perform(self):
            if self.entity.credits >= 10:
                self.entity.credits -= 10
                self.entity.stamina = self.entity.max_stamina + 2
                if not hasattr(entity, "MARJORIE_BONUS"):
                    self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
            pass

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

@_add("6D", "6H")
def trader_used(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc, entity, "kr", engine.deck)
    if i > 0 : return None

    engine.msg("a trader selling a large collection of 'gently' used equipment")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Old Equipment (50)"
        def perform(self):
            if self.entity.credits >= 50:
                from .equipment import items
                for idx, i in enumerate(list(items)):
                    if i.cost < 100 and not i.glider:
                        items.pop(idx)
                        i(self.entity)
                        self.entity.credits -= 50
                        self.engine.settlement_actions.pop(event.K_6, None)
                        self.engine.settlement_actions.pop(event.K_7, None)
                        return

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Nice Equipment (150)"
        def perform(self):
            if self.entity.credits >= 150:
                from .equipment import items
                for idx, i in enumerate(list(items)):
                    if i.cost < 200 and not i.glider:
                        items.pop(idx)
                        i(self.entity)
                        self.entity.credits -= 150
                        self.engine.settlement_actions.pop(event.K_6, None)
                        self.engine.settlement_actions.pop(event.K_7, None)
                        return

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

@_add("7D", "7H")
def tea(engine, entity):
    engine.msg("enjoy a quiet cup of tea.")

    picked = [0]

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "h"
        def perform(self):
            picked[0] += 1
            self.entity.h += 1
            self.engine.settlement_actions.pop(event.K_6, None)
            if not hasattr(entity, "MARJORIE_BONUS") or picked[0] >= 2:
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
                self.engine.settlement_actions.pop(event.K_8, None)
                self.engine.settlement_actions.pop(event.K_9, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "k"
        def perform(self):
            picked[0] += 1
            self.entity.k += 1
            self.engine.settlement_actions.pop(event.K_7, None)
            if not hasattr(entity, "MARJORIE_BONUS") or picked[0] >= 2:
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_8, None)
                self.engine.settlement_actions.pop(event.K_9, None)

    class optionC(SettlementEncounterResultAction):
        FLAVOR = "r"
        def perform(self):
            picked[0] += 1
            self.entity.r += 1
            self.engine.settlement_actions.pop(event.K_8, None)
            if not hasattr(entity, "MARJORIE_BONUS") or picked[0] >= 2:
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
                self.engine.settlement_actions.pop(event.K_9, None)

    class optionD(SettlementEncounterResultAction):
        FLAVOR = "max stamina"
        def perform(self):
            picked[0] += 1
            self.entity.max_stamina += 1
            self.engine.settlement_actions.pop(event.K_9, None)
            if not hasattr(entity, "MARJORIE_BONUS") or picked[0] >= 2:
                self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)
                self.engine.settlement_actions.pop(event.K_8, None)


    oa = optionA(engine, entity)
    ob = optionB(engine, entity)
    oc = optionC(engine, entity)
    od = optionD(engine, entity)

    return [oa, ob, oc, od]

@_add("8D", "8H")
def red_mercs(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc, entity, "kr", engine.deck)
    if i > 0 : return None

    engine.msg("Mercenaries offering Credits for job leads.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Sell intel to mercenaries."
        def perform(self):

            amt = 0
            for y in self.engine.game_map.locations.values():
                for loc in y.values():
                    if isinstance(loc, locations.Settlement):
                        amt += 1

            self.entity.credits += 20 *amt
            self.engine.settlement_actions.pop(event.K_6, None)

            pass

    oa = optionA(engine, entity)

    return [oa]

@_add("9D", "9H")
def smugglers(engine, entity):
    loc = engine.game_map.get_loc(entity.x, entity.y)
    i = skill_check(loc, entity, "kr", engine.deck)
    if i > 0 : return None

    engine.msg("Smugglers looking to purchase relics and scrap at a good price.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Sell a relic (70 credits)"
        def perform(self):
            if self.entity.relic >= 1:
                self.entity.relic -=1
                self.entity.credits +=70
                if not hasattr(entity, "MARJORIE_BONUS"):
                    self.engine.settlement_actions.pop(event.K_7, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Sell 2 cargo (20)"
        def perform(self):
            if self.entity.cargo >= 2:
                self.entity.relic -=2
                self.entity.credits +=20
                if not hasattr(entity, "MARJORIE_BONUS"):
                    self.engine.settlement_actions.pop(event.K_6, None)

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

@_add("0D", "0H")
def festival(engine, entity):
    engine.msg("The Festival of Merchants is happening.")
    engine.msg("Time to kick back and enjoy the celebration.")
    entity.water = entity.max_water
    entity.stamina = entity.max_stamina + 3 #Temp!
    from . import weather
    weather.reset(engine)

    return None

@_add("JD", "JH")
@_add("QD", "QH")
@_add("KD", "KH")
def glider_race_mechanic(engine, entity):
    engine.msg("A glider race mechanic offers to increase your speed or fuel capacity.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "+1 Speed (65)"
        def perform(self):
            if self.entity.credits >= 65:
                self.entity.credits -=65
                self.entity.speed += 1
                self.engine.settlement_actions.pop(event.K_6, None)
                if not hasattr(entity, "MARJORIE_BONUS"):
                    self.engine.settlement_actions.pop(event.K_7, None)

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "+1 max fuel (65)"
        def perform(self):
            if self.entity.credits >= 65:
                self.entity.credits -=65
                self.entity.max_fuel += 1
                if not hasattr(entity, "MARJORIE_BONUS"):
                    self.engine.settlement_actions.pop(event.K_6, None)
                self.engine.settlement_actions.pop(event.K_7, None)

    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

@_add("WD", "WH")
def spike(engine, entity):
    engine.msg("The legendary smuggler is here, of all places.")

    class optionA(SettlementEncounterResultAction):
        FLAVOR = "Sell a relic (200 credits)"
        def perform(self):
            if self.entity.relic >= 1:
                self.entity.relic -=1
                self.entity.credits +=200

    class optionB(SettlementEncounterResultAction):
        FLAVOR = "Buy quest item (10)"
        def perform(self):
            if self.entity.credits >= 10:
                self.entity.credits -= 10
                self.entity.quest += 1
        def available(self):
            return self.entity.quest_guild is not None

    class optionC(SettlementEncounterResultAction):
        FLAVOR = "Equipment (100)" #TODO choose
        def perform(self):
            if self.entity.credits >= 100:
                from .equipment import items
                for idx, i in enumerate(list(items)):
                    items.pop(idx)
                    i(self.entity)
                    self.entity.credits -= 100
                    self.engine.settlement_actions.pop(event.K_8, None)
                    return


    oa = optionA(engine, entity)
    ob = optionB(engine, entity)

    return [oa, ob]

