
class ElijahStrategyPlayer(Player):
    def will_colonize_planet(self, colony_ship, planet, game):
        return True

    def decide_ship_movement(self, ship, game):
        # Each move function will return coordinates
        if len(game.planets) == 0:
            if ship == colony_ship:
                ship.move_to_nearest_unoccupied_planet
            elif len(board[closest_colony]) < 3:
                ship.move_to_colony()
            else:
                enemy_colony_pos = board.closest_enemy_colony
                ship.move_to(enemy_colony_pos)
        else:
            if len(board[any_colony]) < 1:
                ship.move_to_colony
            else:
                if near_colony_ship:
                    escort()
                else:
                    destroy_enemy_ships
