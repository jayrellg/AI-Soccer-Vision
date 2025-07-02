import sys
from utils import get_center_of_bbox, measure_euclidean_distance

class PlayerBallAssigner():
    def __init__(self):
        self.max_player_ball_distance = 70
    
    def assign_ball_to_player(self,players,ball_bbox):
        """
        Parameters
        ----------
        players : dict
            {player_id: {'bbox': [x1, y1, x2, y2]}, …}
        ball_bbox : list[int]
            Bounding box [x1, y1, x2, y2] for the detected ball.

        Returns
        -------
        int
            player_id of the closest eligible player, or -1 if none within
            'self.max_player_ball_distance'.
        """
                
        ball_position = get_center_of_bbox(ball_bbox)

        miniumum_distance = 99999
        assigned_player=-1


         # Iterate over every tracked player in this frame
        for player_id, player in players.items():
            player_bbox = player['bbox']

            
            # Feet are approximated by the bottom-left and bottom-right
            left_foot  = (player_bbox[0], player_bbox[-1])   # (x1, y2)
            right_foot = (player_bbox[2], player_bbox[-1])   # (x2, y2)

            # Distances from each foot to the ball
            distance_left  = measure_euclidean_distance(left_foot,  ball_position)
            distance_right = measure_euclidean_distance(right_foot, ball_position)
            
            # Use closest foot to ball
            distance = min(distance_left,distance_right)

            # If player is within min radius AND closest to ball --> make them new ball owner
            if distance < self.max_player_ball_distance:
                if distance < miniumum_distance:
                    miniumum_distance = distance
                    assigned_player = player_id

        return assigned_player