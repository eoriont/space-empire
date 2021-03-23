game_state = {
    'turn': 1,
    'board_size': [7, 7],
    'phase': 'Movement',
    'round': None,
    'current_player': 2,
    'winner': None,
    'players': {
        1: {'cp': 0,
            'homeworld': {'coords': (3,0), 'type': 'Homeworld', 'hits_left': 3, 'turn_created': 1},
            'units': [
                {'coords': (0,0), 'type': 'Scout', 'num': 1, 'hits_left': 1, 'turn_created': 1,
                    'technology': {
                        'attack': 0,
                        'defense': 0,
                        'movement': 1,
                        'shipsize': 1
                    }
                },
                {'coords': (0,0), 'type': 'Scout', 'num': 2, 'hits_left': 1, 'turn_created': 1,
                    'technology': {
                        'attack': 0,
                        'defense': 0,
                        'movement': 1,
                        'shipsize': 1
                    }
                },
                {'coords': (3,0), 'type': 'Shipyard', 'num': 1, 'hits_left': 1, 'turn_created': 1,
                    'technology': {
                        'attack': 0,
                        'defense': 0,
                        'movement': 1,
                        'shipsize': 1
                    }
                },
                {'coords': (3,0), 'type': 'Shipyard', 'num': 2, 'hits_left': 1, 'turn_created': 1,
                    'technology': {
                        'attack': 0,
                        'defense': 0,
                        'movement': 1
                    }
                }],
            'technology': {'attack': 0, 'defense': 0, 'movement': 1, 'shipsize': 0}
        },
        2: {'cp': 0,
            'homeworld': {'coords': (3,6), 'type': 'Homeworld', 'hits_left': 3, 'turn_created': 1},
            'units': [
                {'coords': (0,6), 'type': 'Scout', 'num': 1, 'hits_left': 1, 'turn_created': 1,
                    'technology': {
                        'attack': 0,
                        'defense': 0,
                        'movement': 1
                    }
                },
                {'coords': (0,6), 'type': 'Scout', 'num': 2, 'hits_left': 1, 'turn_created': 1,
                    'technology': {
                        'attack': 0,
                        'defense': 0,
                        'movement': 1
                    }
                },
                {'coords': (0,6), 'type': 'Scout', 'num': 3, 'hits_left': 1, 'turn_created': 1,
                    'technology': {
                        'attack': 0,
                        'defense': 0,
                        'movement': 1
                    }
                },
                {'coords': (3,6), 'type': 'Shipyard', 'num': 1, 'hits_left': 1, 'turn_created': 1,
                    'technology': {
                        'attack': 0,
                        'defense': 0,
                        'movement': 1
                    }
                }],
            'technology': {'attack': 0, 'defense': 0, 'movement': 1, 'shipsize': 0}
        }
    },
    'planets': [(3,0), (3,6)],
    'unit_data': {
        'Battleship': {'cp_cost': 20, 'hullsize': 3, 'shipsize_needed': 5, 'tactics': 5, 'attack': 5, 'defense': 2, 'maintenance': 3},
        'Battlecruiser': {'cp_cost': 15, 'hullsize': 2, 'shipsize_needed': 4, 'tactics': 4, 'attack': 5, 'defense': 1, 'maintenance': 2},
        'Cruiser': {'cp_cost': 12, 'hullsize': 2, 'shipsize_needed': 3, 'tactics': 3, 'attack': 4, 'defense': 1, 'maintenance': 2},
        'Destroyer': {'cp_cost': 9, 'hullsize': 1, 'shipsize_needed': 2, 'tactics': 2, 'attack': 4, 'defense': 0, 'maintenance': 1},
        'Dreadnaught': {'cp_cost': 24, 'hullsize': 3, 'shipsize_needed': 6, 'tactics': 5, 'attack': 6, 'defense': 3, 'maintenance': 3},
        'Scout': {'cp_cost': 6, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 1, 'attack': 3, 'defense': 0, 'maintenance': 1},
        'Shipyard': {'cp_cost': 3, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 3, 'attack': 3, 'defense': 0, 'maintenance': 0},
        'Decoy': {'cp_cost': 1, 'hullsize': 0, 'shipsize_needed': 1, 'tactics': 0, 'attack': 0, 'defense': 0, 'maintenance': 0},
        'Colonyship': {'cp_cost': 8, 'hullsize': 1, 'shipsize_needed': 1, 'tactics': 0, 'attack': 0, 'defense': 0, 'maintenance': 0},
        'Base': {'cp_cost': 12, 'hullsize': 3, 'shipsize_needed': 2, 'tactics': 5, 'attack': 7, 'defense': 2, 'maintenance': 0},
    },
    'technology_data': {
        'shipsize': [0, 10, 15, 20, 25, 30],
        'attack': [20, 30, 40],
        'defense': [20, 30, 40],
        'movement': [0, 20, 30, 40, 40, 40],
        'shipyard': [0, 20, 30]
    }
}
