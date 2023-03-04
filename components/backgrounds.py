
class Background():
    def __init__(self, h, k, r):
        self.h=h
        self.k=k
        self.r=r

    def bonus(self):
        pass

    def goal(self):
        pass

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
        player.SURVIVAL_KNOWLEDGE = 5 #TODO


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
        player.inventory += "WAYFINDING" #TODO

    def goal(self, player):
        n = 0
        for i in player.moves:
            if i.type == 'reveal':
                n = n + 1
            if n >= 30:
                return True
        return False

    def reward(self, player):
        player.PATHFINDER = 1 #TODO


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

    @static
    def choose_stat(): #TODO
        pass

    def reward(self, player):
        x = choose_stat() #TODO
        player[x] += 1
        y = choose_stat(x!='h', x!='k', x!='r')
        player[y] += 1

