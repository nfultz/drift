
class Background():
    def __init__(self, h=2, k=2, r=2):
        self.h=h
        self.k=k
        self.r=r

    def bonus(self, player):
        pass

    def goal(self, player):
        return False

    def reward(self, player):
        pass

class Unskilled(Background):
    pass

class Soldier(Background):
    from .settlement_encounters import SettlementEncounterResultAction
    def __init__(self):
        super().__init__(3,1,2)

    def bonus(self, player):
        player.max_stamina += 1

    def goal(self, player):
        n = 0
        for i in player.moves:
            if isinstance(i, self.SettlementEncounterResultAction):
                n = n + 1
            if n == 3:
                return True
        return False

    def reward(self, player):
        player.max_stamina += 1
        player.h += 1


class Merchant(Background):
    def __init__(self):
        super().__init__(2,3,1)

    def bonus(self, player):
        player.HAGGLER = 1

    from .actions import SellScrap
    def goal(self, player):
        n = 0
        for i in player.moves:
            if isinstance(i, self.SellScrap):
                n = n + i.amount
            if n >= 10:
                return True
        return False

    def reward(self, player):
        player.HARD_BARGIN = 5

class Explorer(Background):
    def __init__(self):
        super().__init__(2,1,3)

    def bonus(self, player):
        player.DELVER = 1

    from .actions import CampingAction
    def goal(self, player):
        n = set()
        for i in player.moves:
            if isinstance(i, self.CampingAction):
                n.add(i.loc)
            if len(n) == 5:
                return True
        return False

    def reward(self, player):
        player.SURVIVAL_KNOWLEDGE = 5


class Scoundrel(Background):
    def __init__(self):
        super().__init__(1,2,3)

    def bonus(self, player):
        player.OFFWORLD_CONTACTS = 25


    from .actions import SellRelic
    def goal(self, player):
        n = 0
        for i in player.moves:
            if isinstance(i, self.SellRelic):
                n = n + i.amount
            if n >= 3:
                return True
        return False

    def reward(self, player):
        player.r += 1
        player.HIGHEST_BIDDERS = 25

class Navigator(Background):
    def __init__(self):
        super().__init__(1,3,2)

    def bonus(self, player):
        player.WAYFINDING = 1

    from .actions import RevealAction
    def goal(self, player):
        n = 0
        for i in player.moves:
            if isinstance(i, self.RevealAction):
                n = n + 1
            if n >= 30:
                return True
        return False

    def reward(self, player):
        player.PATHFINDER = 1


class Freelancer(Background):
    def __init__(self):
        super().__init__(3,2,1)


    def bonus(self, player):
        player.WORK_FOR_HIRE = 1


    def goal(self, player):
        n = 0
        from .guilds import ALL_GUILDS
        for g in ALL_GUILDS:
            n += int(g.level)
            if n >= 6:
                return True
        return False

    def reward(self, player):
        #x = choose_stat() #TODO
        player.r += 1
        player.k += 1


def rebuilding_the_past(player):
    player.restoration = 0

def hard_times(player):
    #x = choose_stat() #TODO
    #player[x] += 1
    player.h += 1
    player.max_stamina -= 1

def no_intro_needed(player):
    player.credits += 100
    player.GLIDER_DISCOUNT = 4

def returning_home(player):
    player.credits += 50
    player.MOONDEW_REST_DISCOUNT = 1
    player.MOONDEW_REST_WATER = 1

def familiar_face(player):
    player.MOONDEW_REST_DISCOUNT = 1
    player.EQUIP_DISCOUNT = 4

def place_to_hide(player):
    player.secrecy = 0

def quiet_wanderer(player):
    #x = choose_stat() #TODO
    #player[x] += 1
    player.r += 1
    player.max_stamina += 1
    player.fame_per_companion = 99

def friendly_face(player):
    player.GUILD_QUEST_DIFFICULTY = 1 #TODO
    player.COMPANION_DISCOUNT = 50

def skilled_laborer(player):
    player.MOONDEW_LABORER = 1

def random_background(deck):
    choices = [Unskilled, Soldier, Merchant, Explorer, Scoundrel, Navigator, Freelancer]
    return choices[deck.bottom.value % len(choices)]

def introduction(deck):
    card = deck.bottom

    if card.major:
        if card.rank == 'W':
            return rebuilding_the_past
        elif card.value > 10:
            return hard_times
        elif card.value > 7 :
            return no_intro_needed
        elif card.value > 4 :
            return returning_home
        else :
            return familiar_face
    elif not card.major:
        if card.rank == 'W':
            return place_to_hide
        elif card.value > 10:
            return quiet_wanderer
        elif card.value > 5 :
            return friendly_face
        else:
            return skilled_laborer

