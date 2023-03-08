
class Guild():
    def advance(self, entity):
        pass


class EcologyGuild(Guild):
    label = "Guild of Ecology"
    pass
class RelicsGuild(Guild):
    label = "Guild of Relics"
    pass
class ExplorationGuild(Guild):
    label = "Guild of Exploration"
    pass
class RestorationGuild(Guild):
    label = "Guild of Restoration"
    pass
class GliderGuild(Guild):
    label = "Guild of the Glider"
    pass
class SmugglersGuild(Guild):
    label = "Smugglers"
    pass

items = [EcologyGuild, RelicsGuild, ExplorationGuild, RestorationGuild, GliderGuild, SmugglersGuild]

def draw(card):
    return items.pop(card.value % len(items))() if len(items) else None
