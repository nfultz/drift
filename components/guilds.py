from .actions import Action, ExploreAction, MovementAction, RevealAction, RetryAction
from . import locations
from .explorations import skill_check, earn

class Guild():
    level = 0
    message = ""
    def advance(self, engine, entity):
        if entity.quest_guild is None:
            entity.quest_guild = self
        elif entity.quest_guild is not self:
            return
        self._advance(engine, entity)

    def guild_action(self, engine, entity):
        return None

    def _advance(self,engine, entity):
        pass


class EcologyGuild(Guild):
    label = "Guild of Ecology"

    class moisture_collector(locations.GuildUnique):
        level = 1
        @staticmethod
        def encounter(loc,entity,deck):
            if entity.quest >= 3 and entity.cargo >= 3:
                entity.quest = 0
                entity.cargo -= 3
                entity.MC_QUEST = 1

    class wind_trap(locations.GuildUnique):
        level = 2
        @staticmethod
        def encounter(loc,entity,deck):
            if entity.relic >= 1 and entity.cargo >= 2:
                entity.relic -= 1
                entity.cargo -= 2
                entity.WT_QUEST = 1

    class secret_garden(locations.GuildUnique):
        level = 1
        from .tile_types import hidden as tile

        @staticmethod
        def encounter(loc,entity,deck):
            if loc.quest_level == 5.5:
                if entity.quest >= 1:
                    entity.quest = 0
                    entity.SG_QUEST1 = 1
                    entity.stamina = entity.max_stamina

            elif loc.quest_level == 6.5:
                if entity.relic >= 1 and entity.quest >= 6:
                    entity.relic -= 1
                    entity.quest -= 6
                    entity.SG_QUEST2 = 1

    def _advance(self, engine, entity):
        if self.level == 0:
            self.message = "Recover 3 desert herbs"
            entity.quest = 0

            engine.msg(self.message)
            self.level = .5

        elif self.level == 0.5:
            if entity.quest >= 3:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.credits += 50
                entity.fame += 1

                self.level = 1
                return
            engine.msg(self.message)

        elif self.level == 1:
            self.message = "Recover 3 hydroponic storage units and return them to the moisture collector."
            engine.msg(self.message)
            self.level = 1.5

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=5)
            mc = self.moisture_collector(x,y,self)
            engine.game_map.add_location(mc)


        elif self.level == 1.5:
            if hasattr(entity, "MC_QUEST"):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.water = entity.max_water
                entity.credits += 50
                entity.fame +=1

                self.level = 2
                return
            engine.msg(self.message)


        elif self.level == 2:
            self.message = "Recover 1 Relic and 2 Cargo, and transport to wind trap"
            engine.msg(self.message)
            self.level = 2.5

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=5)
            mc = wind_trap(x,y,self)
            engine.game_map.add_location(mc)

        elif self.level == 2.5:
            if hasattr(entity, "WT_QUEST"):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.credits += 25
                #TODO equip upgrade

                self.level = 3

                return
            engine.msg(self.message)

        elif self.level == 3:
            self.message = "Recover 5 plant samples"
            engine.msg(self.message)
            self.level = 3.5

        elif self.level == 3.5:
            if entity.quest >= 5:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.max_water += 1
                entity.fame += 1

                self.level = 4

                return
            engine.msg(self.message)

        elif self.level == 4:
            self.message = "Recover 3 plant samples from desert locations"
            engine.msg(self.message)
            self.level = 4.5

        elif self.level == 4.5:
            if entity.quest >= 3:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.credits += 75
                entity.fame += 1

                self.level = 5

                return
            engine.msg(self.message)

        elif self.level == 5:
            self.message = "Transport Secret Growth Algorithm to Secret Garden"
            engine.msg(self.message)
            entity.quest = 1

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=5)
            self.SG = secret_garden(x,y,self)
            engine.game_map.add_location(self.SG)



            self.level = 5.5

        elif self.level == 5.5:
            if hasattr(entity, "SG_QUEST1"):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.credits += 50

                self.level = 6

                return
            engine.msg(self.message)

        elif self.level == 6:
            self.message = "Transport 6 cargo and 1 relic to to Secret Garden"
            engine.msg(self.message)
            self.level = 6.5
            self.SG.quest_level = 6.5

        elif self.level == 6.5:
            if hasattr(entity, "SG_QUEST2"):
                engine.msg("Guild Maxed!")
                entity.quest = 0
                entity.quest_guild = None

                entity.max_stamina += 1
                entity.fame += 1

                self.level = 7

                return
            engine.msg(self.message)







class RelicsGuild(Guild):
    label = "Guild of Relics"
    relics_recovered = 0

    class relic_museum(locations.GuildUnique):
        level = 2
        @staticmethod
        def encounter(loc,entity,deck):
            if loc.quest_level == .5:
                if entity.relic >= 1:
                    entity.relic = 0
                    entity.RM_QUEST1 = 1
            if loc.quest_level == 3.5:
                if entity.relic >= 3:
                    entity.relic -= 3
                    entity.RM_QUEST2 = 1
            if loc.quest_level == 5.5:
                if entity.relic >= 4:
                    entity.relic -= 4
                    entity.RM_QUEST3 = 1
            if loc.quest_level == 6.5:
                if entity.quest >= 6:
                    entity.quest -= 6
                    entity.RM_QUEST4 = 1

    class guild_of_relics_settlment(locations.Settlement):
        def __init__(self,x,y,guild):
            super().__init__(x,y)
            self.guild = guild

    class stasis_system(locations.GuildUnique):
        level = 3
        @staticmethod
        def encounter(loc,entity,deck):
            if entity.cargo >= 8:
                entity.cargo -= 8
                entity.SS_QUEST = 1

    class lost_great_house(locations.GuildUnique):
        level = 3
        xp = 99
        from .tile_types import hidden as tile
        @staticmethod
        def encounter(loc,entity,deck):
            pass

    def guild_action(self, engine, entity):
        this = self
        class A(Action):
            FLAVOR = "Return relics to the guild."
            def perform(self):
                old = this.relics_recovered
                new = this.relics_recovered + self.entity.relic
                self.entity.relic = 0
                this.relics_recovered = new

                if old < 2 and new >= 2:
                    self.entity.credits += 50
                if old < 3 and new >= 3:
                    self.entity.credits += 25
                    self.entity.fame +=1
                if old < 4 and new >= 4:
                    self.entity.credits += 50
                    self.entity.fame +=1
                if old < 5 and new >= 5:
                    self.entity.credits += 100

        if this.level > 3 and entity.relic > 0:
            return A(engine, entity)

    def _advance(self, engine, entity):
        if self.level == 0:
            self.message = "Recover 1 Relic"
            engine.msg(self.message)
            self.level = .5

        elif self.level == 0.5:
            if entity.relic >= 1:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.relic -= 1
                entity.credits += 25
                entity.fame += 1

                self.level = 1
                return
            engine.msg(self.message)
        elif self.level == 1:
            self.message = "Take the relic to the Relic Museum"
            engine.msg(self.message)
            self.level = 1.5
            entity.relic += 1

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=5)
            foo = RelicsGuild.relic_museum(x,y,self)
            engine.game_map.add_location(foo)
            self.rm = foo

        elif self.level == 1.5:
            if hasattr(entity, "RM_QUEST1"):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.credits += 50
                entity.max_relic += 1

                self.level = 2
                return

            engine.msg(self.message)

        elif self.level == 2:
            self.message = ("Find a relic and take it to the new settlement.")
            engine.msg(self.message)
            self.level = 2.5

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=5)
            foo = guild_of_relics_settlment(x,y,self)
            engine.game_map.add_location(foo)
            self.new_settlement = foo


        elif self.level == 2.5:
            if entity.relic >= 1 and (entity.x, entity.y) == (self.new_settlement.x, self.new_settlement.y):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.relic -= 1

                entity.credits += 30
                #TODO recovery quests

                self.level = 3
                return

            engine.msg(self.message)

        elif self.level == 3:
            self.message = ("The Relic Museum requires additional donations.")
            engine.msg(self.message)
            self.level = 3.5
            self.rm.quest_level = 3.5
        elif self.level == 3.5:
            if hasattr(entity, "RM_QUEST2"):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                #TODO equipment upgrade
                entity.fame += 1

                self.level = 4
                return

            engine.msg(self.message)

        elif self.level == 4:
            self.message = "The Guild has almost finished their new Relic storage system"
            engine.msg(self.message)
            self.level = 4.5

            x,y = engine.game_map.nearest_empty(self.rm.x, self.rm.y, r=30, at_least=3)
            foo = stasis_system(x,y,self)
            engine.game_map.add_location(foo)


        elif self.level == 4.5:
            if hasattr(entity, "SS_QUEST"):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.max_relic += 1
                entity.stamina += entity.max_stamina
                entity.water += entity.max_water

                self.level = 5
                return

            engine.msg(self.message)
        elif self.level == 5:
            self.message = "Recvoer 4 Relics and return to relic museum"
            engine.msg(self.message)
            self.level = 5.5
            self.rm.quest_level = 5.5
        elif self.level == 5.5:
            if hasattr(entity, "RM_QUEST3"):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                #TODO Glider upgrade

                self.level = 6
                return

            engine.msg(self.message)
        elif self.level == 6:
            self.message = "Recover 6 Ancient House Artifacts and return to relic museum"
            engine.msg(self.message)
            self.level = 6.5
            self.rm.quest_level = 6.5


            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=20)
            foo = lost_great_house(x,y,self)
            engine.game_map.add_location(foo)
            self.new_settlement = foo

        elif self.level == 6.5:
            if hasattr(entity, "RM_QUEST4"):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                #TODO Glider upgrade

                self.level = 7
                return
            engine.msg(self.message)




class ExplorationGuild(Guild):
    label = "Guild of Exploration"

    class ancient_temple(locations.GuildUnique):
        level = 2
        @staticmethod
        def encounter(loc,entity,deck):
            if entity.quest >= 1 and entity.relic >= 1:
                entity.quest = 0
                entity.relic -= 1
                entity.AT_QUEST = 1

    class guild_of_exploration_settlment(locations.Settlement):
        def __init__(self,x,y,guild):
            super().__init__(x,y)
            self.guild = guild


    def guild_action(self, engine, entity):
        this = self
        class A(Action):
            FLAVOR = "Information Broker"
            def perform(self):
                old = this.old
                new = set()

                for m in entity.moves:
                    if isinstance(m, ExploreAction) and m.success:
                        new.add(m)

                new = len(new)
                this.old = new

                if old < 5 and new >= 5:
                    old = 5
                    self.entity.credits += 50
                if old < 10 and new >= 10:
                    old = 10
                    self.entity.fame += 1
                if old < 15 and new >= 15:
                    old = 15
                    self.entity.credits += 100
                if old < 20 and new >= 20:
                    old = 20
                    self.entity.fame += 1
                    self.entity.relic += 1
                if old < 21 and new >= 21:
                    self.entity.credits += 25


        if this.level >= 2:
            return A(engine, entity)

    def _advance(self, engine, entity):
        if self.level == 0:
            self.message = "If you want to be part of the guild, show them you can discover new things."
            engine.msg(self.message)
            self.level = .5
            self.idx = len(entity.moves)
            return

        #used below
        new = set()
        for m in entity.moves[self.idx:]:
            if isinstance(m, ExploreAction) and m.success:
                new.add(m)
        explored = len(new)
        new = set()
        for m in entity.moves[self.idx:]:
            if isinstance(m, RevealAction):
                new.add(m)
        revealed = len(new)


        if self.level == 0.5:

            if revealed >= 5 and explored >= 3:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.credits += 25
                entity.fame += 1

                self.level = 1
                return
            engine.msg(self.message)
        elif self.level == 1:
            self.message = "The Guild needs new location data on some empty locations."
            engine.msg(self.message)
            self.idx = len(entity.moves)
            self.level = 1.5

        elif self.level == 1.5:
            if explored > 3:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.credits += 50
                entity.fame += 1

                self.level = 2
                return

            engine.msg(self.message)

        elif self.level == 2:
            self.message = ("Another guild member has left clues.")
            engine.msg(self.message)
            self.level = 2.5


        elif self.level == 2.5:
            if entity.quest >= 4:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                #TODO equipment upgrade

                self.level = 3
                return

            engine.msg(self.message)

        elif self.level == 3:
            self.message = "Transport the mapping data to the guild camps"
            engine.msg(self.message)
            self.level = 3.5

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=5)
            foo = guild_of_exploration_settlment(x,y,self)
            engine.game_map.add_location(foo)
            self.settlement == foo

            self.quest = 1

        elif self.level == 3.5:
            if self.settlement.x == entity.x and self.settlement.y == entity.y:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.max_stamina += 1
                entity.stamina = entity.max_stamina
                entity.fuel = entity.max_fuel
                entity.water = entity.max_water

                self.level = 4
                return

            engine.msg(self.message)

        elif self.level == 4:
            self.message = "While the cartographer is hard at work, collect more data."
            engine.msg(self.message)
            self.level = 4.5
            self.idx = len(entity.moves)


        elif self.level == 4.5:
            if revealed >= 10 and entity.cargo >= 5:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.cargo -= 5
                entity.max_water += 1
                entity.credits += 50
                entity.fame += 1

                self.level = 5
                return

            engine.msg(self.message)
        elif self.level == 5:
            self.message = "Your hard work has paid off - an ancient temple is discovered."
            engine.msg(self.message)
            self.level = 5.5
            self.entity.quest = 1

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=5)
            foo = ancient_temple(x,y)
            engine.game_map.add_location(foo)

        elif self.level == 5.5:
            if hasattr(entity, "AT_QUEST1"):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.credits += 50
                entity.fame += 1

                self.level = 6
                return

            engine.msg(self.message)
        elif self.level == 6:
            self.message = "Recover 6 Ancient Texts and 10 cargo"
            engine.msg(self.message)
            self.level = 6.5
            self.rm.quest_level = 6.5


            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=20)
            foo = lost_great_house(x,y,self)
            engine.game_map.add_location(foo)
            self.new_settlement = foo

        elif self.level == 6.5:
            if entity.quest >= 4 and entity.cargo >= 10:
                engine.msg("Guild maxed.")
                entity.quest = 0
                entity.quest_guild = None

                entity.cargo -= 10
                entity.fame += 3
                entity.relic += 1
                entity.credits += 100

                self.level = 7
                return
            engine.msg(self.message)





class RestorationGuild(Guild):
    label = "Guild of Restoration"

    class recovery_center(locations.Settlement):
        def __init__(self,x,y,guild):
            super().__init__(x,y)
            self.guild = guild

    class green_archives(locations.GuildUnique):
        level = 2
        @staticmethod
        def encounter(loc,entity,deck):
            if entity.quest >= 1:
                entity.cargo -= 1
                entity.GA_QUEST = 1

    class renewal_machines(locations.GuildUnique):
        level = 2
        rc1 = True
        rc2 = True
        @staticmethod
        def encounter(loc,entity,deck):
            if loc.quest_level == 4.5 and loc.rc1:
                if entity.quest >= 1:
                    loc.rc1 = False
                    entity.quest -= 1
                    entity.RM1 += 1
            if loc.quest_level == 4.5 and loc.rc2:
                if entity.quest >= 1 and entity.cargo >= 5:
                    loc.rc2 = False
                    entity.quest -= 1
                    entity.cargo -= 5
                    entity.RM2 +=1

            if entity.cargo >= 8:
                entity.cargo -= 8
                entity.SS_QUEST = 1

    class solar_engine(locations.Settlement):
        def __init__(self,x,y,guild):
            super().__init__(x,y)
            self.guild = guild
        @staticmethod
        def encounter(loc,entity,deck):
            if entity.relic >= 2 and entity.cargo >= 10:
                entity.relic -= 2
                entity.cargo -= 10
                entity.SE1 = 1

    def guild_action(self, engine, entity):
        class A(Action):
            def perform(self):
                n = self.entity.cargo

                if n <= 5:
                    self.entity.water += 1
                    self.entity.fuel += 1
                    self.entity.credits += n*5

                if n > 5:
                    self.entity.water += 2
                    self.entity.fuel += 1
                    self.entity.credits += n*10

                self.entity.cargo = 0

            def available(self):
                return self.entity.cargo > 0
        if self.level >= 1:
            return A(engine, entity)

    def _advance(self, engine, entity):
        if self.level == 0:
            self.message = "Discover the ruins of the past."
            engine.msg(self.message)
            self.level = .5
            self.idx = len(entity.moves)
            return

        elif self.level == 0.5:
            #used below
            new = set()
            for m in entity.moves[self.idx:]:
                if isinstance(m, ExploreAction) and m.success:
                    new.add(m)
            explored = len(new)

            if explored >= 5:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.fame += 1

                self.level = 1
                return
            engine.msg(self.message)

        elif self.level == 1:
            self.message = "Recover cargo for the restoration workers."
            engine.msg(self.message)
            self.idx = len(entity.moves)

        elif self.level == 1.5:
            if entity.cargo >= 5 and entity.water >= 2 and entity.fuel >= 1 and entity.credits >= 25:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.cargo -= 5
                entity.water -= 2
                entity.fuel -= 1
                entity.credits -= 25
                entity.fame += 1

                #TODO free hotels

                self.level = 2
                return

            engine.msg(self.message)

        elif self.level == 2:
            self.message = ("The Restoration Center will be a key location for all future work.")
            engine.msg(self.message)
            self.level = 2.5

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=2)
            foo = recovery_center(x,y,self)
            engine.game_map.add_location(foo)
            self.rc == foo

        elif self.level == 2.5:
            if entity.quest >= 4 and (entity.x, entity.y) == (self.rc.x, self.rc.y):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.credits += 40
                entity.fame += 1

                self.level = 3
                return

            engine.msg(self.message)

        elif self.level == 3:
            self.message = "Transport the data to the green archives"
            engine.msg(self.message)
            self.level = 3.5

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=5)
            foo = green_archives(x,y,self)
            engine.game_map.add_location(foo)
            self.gc == foo

            self.quest = 1

        elif self.level == 3.5:
            if hasattr(entity, "GA_QUEST"):
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                #TODO Equip upgrade

                self.level = 4
                return

            engine.msg(self.message)

        elif self.level == 4:
            self.message = "Transport renewal keys to the three Renewal Machines."
            engine.msg(self.message)
            self.level = 4.5
            self.quest = 3
            entity.RM1 = 0

            x,y = entity.x, entity.y
            for _ in range(3):
                x,y = engine.game_map.nearest_empty(x, y, r=30, at_least=3)
                foo = renewal_machines(x,y,self)
                engine.game_map.add_location(foo)

        elif self.level == 4.5:
            if entity.RM1 >= 3:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.stamina = entity.max_stamina
                entity.water = entity.max_water

                #TODO free fuel
                self.level = 5
                return

            engine.msg(self.message)
        elif self.level == 5:
            self.message = "Each machine needs supplies."
            engine.msg(self.message)
            self.level = 5.5
            entity.RM2 = 0

        elif self.level == 5.5:
            if entity.RM2 >= 3:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                #TODO glider upgrade

                self.level = 6
                return

            engine.msg(self.message)
        elif self.level == 6:
            self.message = "Recover 6 Ancient Texts and 10 cargo"
            engine.msg(self.message)
            self.level = 6.5
            entity.SE1 = 0

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=20)
            foo = solar_engine(x,y,self)
            engine.game_map.add_location(foo)

        elif self.level == 6.5:
            if entity.SE1 > 0:
                engine.msg("Guild maxed.")
                entity.quest = 0
                entity.quest_guild = None

                entity.fame += 2
                entity.relic += 1
                entity.credits += 200

                self.level = 7
                return
            engine.msg(self.message)



class GliderGuild(Guild):
    label = "Guild of the Glider"

    class racetrack(locations.GuildUnique):
        xp = 999
        def __init__(self,x,y,guild):
            super().__init__(x,y)
            self.guild = guild

        @staticmethod
        def encounter(loc, entity, deck):
            target = deck.top.value
            upgrades = entity.speed + entity.fuel
            if target < upgrades:
                entity.rt_wins += 1
                entity.rt_streak += 1
                if target > entity.speed:
                    entity.fuel -= 1
            else:
                entity.rt_streak = 0

        def available(self):
            return True

    class glider_factory(locations.GuildUnique):
        level = 3
        xp = 999
        won  = False
        @staticmethod
        def encounter(loc,entity,deck):
            if deck.top.black:
                i = skill_check(loc, entity, "kr", deck)
                if i > 0 :
                    entity.stamina = max(0, entity.stamina - 1)
                    return i
                if not loc.won:
                    loc.won = True
                    entity.fame += 1
                    # TODO glider upgrade
                return earn(entity,loc.level, cargo=1, quest=1)
            else:
                i = skill_check(loc, entity, "h", deck)
                if i > 0 : return i
                if not loc.won:
                    loc.won = True
                    entity.fame += 1
                    # TODO glider upgrade
                return earn(entity,loc.level, cargo=2, quest=1)



    def _advance(self, engine, entity):
        upgrades = entity.speed_upgrade + entity.relic_upgrade + entity.cargo_upgrade + entity.fuel_upgrade

        if self.level == 0:
            self.message = "The first rule of this Guild is speed..."
            engine.msg(self.message)
            self.level = .5
            self.idx = len(entity.moves)
            return

        elif self.level == 0.5:
            #used below
            new = set()
            for m in entity.moves[self.idx:]:
                if isinstance(m, MovementAction):
                    new.add(m)
            moved = len(new)

            if moved >= 15:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.fame += 1
                entity.fuel = entity.max_fuel
                entity.credits += 30

                self.level = 1
                return
            engine.msg(self.message)

        elif self.level == 1:
            if self.fuel < 3:
                engine.msg("Note enough fuel for the quest")
                return
            self.message = "Fuel is the lifeblood"
            engine.msg(self.message)
            self.idx = len(entity.moves)

        elif self.level == 1.5:
            if entity.fuel == 0:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.fuel = entity.max_fuel
                entity.credits += 30

                self.level = 2
                return

            engine.msg(self.message)

        elif self.level == 2:
            self.message = ("A glider is nothing more than a shell without upgrades")
            engine.msg(self.message)
            self.level = 2.5


        elif self.level == 2.5:

            if upgrades > 0:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.fuel = entity.max_fuel
                entity.fame += 1

                self.level = 3
                return

            engine.msg(self.message)

        elif self.level == 3:
            self.message = "Time to go fast."
            engine.msg(self.message)
            self.level = 3.5

            x,y = engine.game_map.nearest_empty(entity.x, entity.y, r=30, at_least=5)
            foo = racetrack(x,y,self)
            engine.game_map.add_location(foo)
            entity.rt_wins = 0
            entity.rt_streak = 0


        elif self.level == 3.5:
            if entity.rt_wins >= 2:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.fame += 1

                self.level = 4
                return

            engine.msg(self.message)

        elif self.level == 4:
            self.message = "Your dedication and respect to the Glider has paid off."
            engine.msg(self.message)
            self.level = 4.5

            x,y = entity.x, entity.y
            x,y = engine.game_map.nearest_empty(x, y, r=30, at_least=3)
            foo = glider_factory(x,y,self)
            engine.game_map.add_location(foo)

        elif self.level == 4.5:
            if entity.quest >= 1:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                entity.fame += 1

                #TODO glider upgrade
                self.level = 5
                return

            engine.msg(self.message)
        elif self.level == 5:
            self.message = "If you want to ride with the best, you need the mods to keep up."
            engine.msg(self.message)
            self.level = 5.5

        elif self.level == 5.5:
            #used below
            new = set()
            for m in entity.moves[self.idx:]:
                if isinstance(m, MovementAction):
                    new.add(m)
            moved = len(new)

            if moved >= 30 and upgrades >= 3:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.quest_guild = None

                #TODO free fuel at racetrack
                entity.max_fuel += 1

                self.level = 6
                return

            engine.msg(self.message)
        elif self.level == 6:

            if upgrades < 5:
                engine.msg("Not enough upgrades to progress")
                return

            self.message = "Show the guild you are the best Glide rider on Eridoor"
            engine.msg(self.message)
            self.level = 6.5
            entity.SE1 = 0

        elif self.level == 6.5:
            if entity.rt_streak >= 3:
                engine.msg("Guild maxed.")
                entity.quest = 0
                entity.quest_guild = None

                entity.fame += 3

                self.level = 7
                return
            engine.msg(self.message)




class SmugglersGuild(Guild):
    #TODO
    label = "Smugglers"
    pass

items = [EcologyGuild(), RelicsGuild(), ExplorationGuild(), RestorationGuild(), GliderGuild(), None, None, None]

def draw(card):
    return items.pop(card.value % len(items)) if len(items) else None
