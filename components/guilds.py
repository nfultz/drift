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

    class MoistureCollection(location.GuildUnique):





    def _advance(self, engine, entity):
        if self.level == 0:
            self.message = "Recover 3 desert herbs"

            engine.msg(self.message)
            self.level = .5

        elif self.level == 0.5:
            if entity.quest >= 3:
                engine.msg("Quest Completed")
                entity.quest = 0
                entity.credits += 50
                entity.fame += 1

                self.level = 1
                entity.quest_guild = None
                return
            engine.msg(self.message)

        elif self.level == 1:
            self.message = "Recover 3 hydroponic storage units and return them to the moisture collector."
            engine.msg(self.message)
            #TODO
            self.level = 1.5

        elif self.level == 1.5:
            if False:#TODO
                self.level = 2
                entity.quest_guild = None
                return
            engine.msg(self.message)


        elif self.level == 2:
            self.message = "Recover 1 Relic and 2 Cargo, and transport to wind trap"
            engine.msg(self.message)
            self.level = 2.5
        elif self.level == 2.5:
            if False: #TODO
                self.level = 3
                entity.quest_guild = None
                return
            engine.msg(self.message)
        elif self.level == 3:
            self.message = "Recover 5 plant samples"
            engine.msg(self.message)
            self.level = 3.5
        elif self.level == 3.5:
            if entity.quest >= 5:
                entity.quest = 0
                engine.msg("Quest Completed")
                entity.max_water += 1
                entity.fame += 1
                self.level = 4
                entity.quest_guild = None
                return
            engine.msg(self.message)
        elif self.level == 4:
            self.message = "Recover 3 plant samples from desert locations"
            engine.msg(self.message)
            self.level = 4.5
        elif self.level == 4.5:
            if entity.quest >= 3:
                entity.quest = 0
                engine.msg("Quest Completed")
                entity.credits += 75
                entity.fame += 1
                self.level = 5
                entity.quest_guild = None
                return
            engine.msg(self.message)

        elif self.level == 5:
            self.message = "Transport Secret Growth Algorithm to Secret Garden"
            engine.msg(self.message)
            #TODO
            self.level = 5.5
        elif self.level == 5.5:
            if False: #TODO
                self.level = 6
                entity.quest_guild = None
                return
            engine.msg(self.message)
        elif self.level == 6:
            self.message = "Transport 6 cargo and 1 relic to to Secret Garden"
            engine.msg(self.message)
            self.level = 6.5
        elif self.level == 6.5:
            if False:
                self.level = 7
                entity.quest_guild = None
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
