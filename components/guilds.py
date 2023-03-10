from .actions import Action
from .locations import Location

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
        pass

    def _advance(self,engine, entity):
        pass


class EcologyGuild(Guild):
    label = "Guild of Ecology"

    class moisture_collector(location.GuildUnique):
        level = 1
        @staticmethod
        def encounter(loc,entity,deck):
            if entity.quest >= 3 and entity.cargo >= 3:
                entity.quest = 0
                entity.cargo -= 3
                entity.MC_QUEST = 1

    class wind_trap(location.GuildUnique):
        level = 2
        @staticmethod
        def encounter(loc,entity,deck):
            if entity.relic >= 1 and entity.cargo >= 2:
                entity.relic -= 1
                entity.cargo -= 2
                entity.WT_QUEST = 1

    class secret_garden(location.GuildUnique):
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
            mc = moisture_collector(x,y,self)
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
    relics_returned = 0

    def guild_action(self, engine, entity):
        class A(Action):
            def perform(self):
                pass
            def available(self):
                return False
        return A(engine, entity)

    def _advance(self, engine, entity):
        if self.level == 0:
            engine.msg("Recover 3 desert herbs")
            self.level = .5
        elif self.level == 0.5:

            self.level = 1
            entity.quest_guild = None
        elif self.level == 1:
            engine.msg("Recover 3 hydroponic storage units and return them to the moisture collector.")
            self.level = 1.5

        elif self.level == 1.5:
            engine.msg("Recover 3 hydroponic storage units and return them to the moisture collector.")
            self.level = 2
            entity.quest_guild = None

        elif self.level == 2:
            self.level = 2.5
        elif self.level == 2.5:
            self.level = 3
            entity.quest_guild = None
        elif self.level == 3:
            self.level = 3.5
        elif self.level == 3.5:
            self.level = 4
            entity.quest_guild = None
        elif self.level == 4:
            self.level = 4.5
        elif self.level == 4.5:
            self.level = 5
            entity.quest_guild = None
        elif self.level == 5:
            self.level = 5.5
        elif self.level == 5.5:
            self.level = 6
            entity.quest_guild = None
        elif self.level == 6:
            self.level = 6.5
        elif self.level == 6.5:
            self.level = 7
            entity.quest_guild = None




class ExplorationGuild(Guild):
    label = "Guild of Exploration"

    locations_explored = 0
    def guild_action(self, engine, entity):
        class A(Action):
            def perform(self):
                pass
            def available(self):
                return False
        return A(engine, entity)

    def _advance(self, engine, entity):
        if self.level == 0:
            engine.msg("Recover 3 desert herbs")
            self.level = .5
        elif self.level == 0.5:

            self.level = 1
            entity.quest_guild = None
        elif self.level == 1:
            engine.msg("Recover 3 hydroponic storage units and return them to the moisture collector.")
            self.level = 1.5

        elif self.level == 1.5:
            engine.msg("Recover 3 hydroponic storage units and return them to the moisture collector.")
            self.level = 2
            entity.quest_guild = None

        elif self.level == 2:
            self.level = 2.5
        elif self.level == 2.5:
            self.level = 3
            entity.quest_guild = None
        elif self.level == 3:
            self.level = 3.5
        elif self.level == 3.5:
            self.level = 4
            entity.quest_guild = None
        elif self.level == 4:
            self.level = 4.5
        elif self.level == 4.5:
            self.level = 5
            entity.quest_guild = None
        elif self.level == 5:
            self.level = 5.5
        elif self.level == 5.5:
            entity.quest_guild = None
            self.level = 6
        elif self.level == 6:
            self.level = 6.5
        elif self.level == 6.5:
            self.level = 7
            entity.quest_guild = None



class RestorationGuild(Guild):
    label = "Guild of Restoration"
    restoration_level = 0
    def guild_action(self, engine, entity):
        class A(Action):
            def perform(self):
                pass
            def available(self):
                return False
        return A(engine, entity)
    def _advance(self, engine, entity):
        if self.level == 0:
            engine.msg("Recover 3 desert herbs")
            self.level = .5
        elif self.level == 0.5:

            self.level = 1
            entity.quest_guild = None
        elif self.level == 1:
            engine.msg("Recover 3 hydroponic storage units and return them to the moisture collector.")
            self.level = 1.5

        elif self.level == 1.5:
            engine.msg("Recover 3 hydroponic storage units and return them to the moisture collector.")
            self.level = 2
            entity.quest_guild = None

        elif self.level == 2:
            self.level = 2.5
        elif self.level == 2.5:
            self.level = 3
            entity.quest_guild = None
        elif self.level == 3:
            self.level = 3.5
        elif self.level == 3.5:
            self.level = 4
            entity.quest_guild = None
        elif self.level == 4:
            self.level = 4.5
        elif self.level == 4.5:
            self.level = 5
            entity.quest_guild = None
        elif self.level == 5:
            self.level = 5.5
        elif self.level == 5.5:
            self.level = 6
            entity.quest_guild = None
        elif self.level == 6:
            self.level = 6.5
        elif self.level == 6.5:
            self.level = 7
            entity.quest_guild = None



class GliderGuild(Guild):
    label = "Guild of the Glider"

    def guild_action(self, engine, entity):
        class A(Action):
            def perform(self):
                pass
            def available(self):
                return False
        return A(engine, entity)
    def _advance(self, engine, entity):
        if self.level == 0:
            engine.msg("Recover 3 desert herbs")
            self.level = .5
        elif self.level == 0.5:

            self.level = 1
            entity.quest_guild = None
        elif self.level == 1:
            engine.msg("Recover 3 hydroponic storage units and return them to the moisture collector.")
            self.level = 1.5

        elif self.level == 1.5:
            engine.msg("Recover 3 hydroponic storage units and return them to the moisture collector.")
            self.level = 2
            entity.quest_guild = None

        elif self.level == 2:
            self.level = 2.5
        elif self.level == 2.5:
            self.level = 3
            entity.quest_guild = None
        elif self.level == 3:
            self.level = 3.5
        elif self.level == 3.5:
            self.level = 4
            entity.quest_guild = None
        elif self.level == 4:
            self.level = 4.5
        elif self.level == 4.5:
            self.level = 5
            entity.quest_guild = None
        elif self.level == 5:
            self.level = 5.5
        elif self.level == 5.5:
            self.level = 6
            entity.quest_guild = None
        elif self.level == 6:
            self.level = 6.5
        elif self.level == 6.5:
            self.level = 7
            entity.quest_guild = None



class SmugglersGuild(Guild):
    #TODO
    label = "Smugglers"
    pass

items = [EcologyGuild(), RelicsGuild(), ExplorationGuild(), RestorationGuild(), GliderGuild(), None, None, None]

def draw(card):
    return items.pop(card.value % len(items)) if len(items) else None
