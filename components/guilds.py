from .actions import Action
from .locations import Location

class Guild():
    level = 0
    def advance(self, entity):
        pass

    def guild_action(self):
        pass


class EcologyGuild(Guild):
    label = "Guild of Ecology"
    pass
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
class GliderGuild(Guild):
    label = "Guild of the Glider"

    def guild_action(self, engine, entity):
        class A(Action):
            def perform(self):
                pass
            def available(self):
                return False
        return A(engine, entity)
class SmugglersGuild(Guild):
    #TODO
    label = "Smugglers"
    pass

items = [EcologyGuild(), RelicsGuild(), ExplorationGuild(), RestorationGuild(), GliderGuild()]

def draw(card):
    return items.pop(card.value % len(items)) if len(items) else None
