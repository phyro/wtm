GAME_BUILDINGS = []
_BUILDINGS_NR = 4

class Building():
    """Defines a building/research.
        @dependencies: String representation of buildings and their levels.
        @building_type: 0 -> building, 1 -> research
        @dep_pos: position of building in string representation Player.buildings.status.
    """

    def __init__(self, name, description, building_type, dependencies_tupple, cost_gold, cost_metal, \
            ticks_to_complete, dep_pos):
        self.name = name
        self.description = description
        self.building_type = building_type
        self.cost_gold = cost_gold
        self.cost_metal = cost_metal
        self.ticks_to_complete = ticks_to_complete
        self.dep_pos = dep_pos
        self.dependencies = self.set_dependencies(dependencies_tupple)

    def set_dependencies(self, dependencies_tupple):
        """Returns a string representation of its dependencies."""
        dep = "0" * _BUILDINGS_NR
        for (name, level) in dependencies_tupple:
            dep = dep[:self.dep_pos-1] + str(level) + dep[self.dep_pos:]
        return dep


#TODO: Dont ignore building level...

GAME_BUILDINGS = [
    Building("Gold research", "Gain 1000 gold every tick.", 1,
            [],
            0, 0,
            2,
            0 #dep_pos
    ),
    Building("Metal research", "Gain 500 metal every tick.", 1,
            [("Gold research", 1)],
            1000, 0,
            2,
            1 #dep pos
    ),
    Building("Baracks", "Build low budget spaceships.", 0,
            [("Gold research", 1),
             ("Metal research", 1)
            ],
            1000, 1000,
            3,
            2 #dep pos
    ),
    Building("Baracks", "Build high budget tanks.", 0,
            [("Baracks", 1)],
            1000, 1000,
            3,
            3 #dep pos
    )
]
