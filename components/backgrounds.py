
class Background():
    def __init__(self, h=2, k=2, r=2):
        self.h=h
        self.k=k
        self.r=r

    def bonus(self):
        pass

    def goal(self):
        return False

    def reward(self):
        pass

class Soldier(Background):
    def __init__(self):
        super().__init__(3,1,2)

    def bonus(self, player):
        player.max_stamina += 1

    def goal(self, player):
        n = 0
        for i in player.moves:
            if i.type == 'settlement':
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
        player.HAGGLER = 1 #TODO

    def goal(self, player):
        n = 0
        for i in player.moves:
            if i.type == 'trade-scrap' :
                n = n + i.amount
            if n >= 10:
                return True
        return False

    def reward(self, player):
        player.HARD_BARGIN = 5 #TODO

class Explorer(Background):
    def __init__(self):
        super().__init__(2,1,3)

    def bonus(self, player):
        player.DELVER = 1 #TODO

    def goal(self, player):
        n = 0
        for i in player.moves:
            if i.type == 'camp':
                n = n + 1
            if n == 5:
                return True
        return False

    def reward(self, player):
        player.SURVIVAL_KNOWLEDGE = 5


class Scoundrel(Background):
    def __init__(self):
        super().__init__(1,2,3)

    def bonus(self, player):
        player.OFFWORLD_CONTACTS = 1 #TODO

    def goal(self, player):
        n = 0
        for i in player.events:
            if i.type == 'trade-relic':
                n = n + i.amount
            if n >= 3:
                return True
        return False

    def reward(self, player):
        player.r += 1
        player.HIGHEST_BIDDERS = 25 #TODO

class Navigator(Background):
    def __init__(self):
        super().__init__(1,3,2)

    def bonus(self, player):
        player.WAYFINDING = 1

    def goal(self, player):
        n = 0
        for i in player.moves:
            if i.type == 'reveal':
                n = n + 1
            if n >= 30:
                return True
        return False

    def reward(self, player):
        player.PATHFINDER = 1 #DONE


class Freelancer(Background):
    def __init__(self):
        super().__init__(3,2,1)


    def bonus(self, player):
        player.WORK_FOR_HIRE = 1 #TODO

    def goal(self, player):
        n = 0
        for i in player.moves:
            if i.type == 'finish-quest':
                n = n + 1
            if n == 6:
                return True
        return False

    @staticmethod
    def choose_stat(): #TODO
        pass

    def reward(self, player):
        x = choose_stat() #TODO
        player[x] += 1
        y = choose_stat(x!='h', x!='k', x!='r')
        player[y] += 1


def rebuilding_the_past(player):
    player.restoration = 0

def hard_times(player):
    x = choose_stat() #TODO
    player[x] += 1
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
    x = choose_stat() #TODO
    player[x] += 1
    player.max_stamina += 1
    player.fame_per_companion = 99

def friendly_face(player):
    player.GUILD_QUEST_DIFFICULTY = 1
    player.COMPANION_DISCOUNT = 50

def skilled_laborer(player):
    player.MOONDEW_LABORER = 1 #TODO ADD ACTION


def introduction(deck, player):
    card = deck.bottom

    if card.major:
        if card.rank == 'W':
            rebuilding_the_past(player)
        elif card.value > 10:
            hard_times(player)
        elif card.value > 7 :
            no_intro_needed(player)
        elif card.value > 4 :
            returning_home(player)
        else :
            familiar_face(player)
    elif not card.major:
        if card.rank == 'W':
            place_to_hide(player)
        elif card.value > 10:
            quiet_wanderer(player)
        elif card.value > 5 :
            friendly_face(player)
        else:
            skilled_laborer(player)

