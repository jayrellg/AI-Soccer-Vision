import cv2
import numpy as np
import os
from utils import read_video, save_video
from trackers import Tracker
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camara_movement_estimater import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistanceEstimator

def main():
    # Read Video
    video_frames = read_video('input_videos/08fd33_4.mp4')

    #Initialize Tracker
    tracker = Tracker('models/best.pt') 

    tracks  = tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path= 'stubs/track_stubs.pk1')


    # # save cropped image of a player
    # for track_id, player in tracks["players"][0].items():
    #     bbox = player["bbox"]
    #     frame = video_frames[0]

    #     # crop bbox from frame
    #     cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

    #     # save the cropped image
    #     cv2.imwrite("output_videos/cropped_image.jpg", cropped_image)
    #     break

    # Get object positions 
    tracker.add_position_to_tracks(tracks)

    # Camara movement estimator

    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames,
                                                                                read_from_stub=True,
                                                                                stub_path='stubs/camera_movement_stub.pkl')


    camera_movement_estimator.add_adjust_positions_to_tracks(tracks,camera_movement_per_frame)


    #View Transformer
    view_transformer  = ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)

     # Interpolate Ball positions (Fill in missing frames)
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])

    #Speed and diatnce estimator
    speed_and_distance_estimator = SpeedAndDistanceEstimator()
    speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)


    # Assign Player Teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])

    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num], track['bbox'], player_id)
            tracks['players'][frame_num][player_id]['team'] = team 
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]


    # Assign Ball Aquisition (Player with ball)
    player_assigner = PlayerBallAssigner()
    team_ball_control= [] # (Maybe have its own module)
    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)

        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(tracks['players'][frame_num][assigned_player]['team'])
        else:
            team_ball_control.append(team_ball_control[-1])
    team_ball_control= np.array(team_ball_control)

    ##Draw output
    #Draw object Tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks, team_ball_control)
    

    # Draw Camera movement
    output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames,camera_movement_per_frame)


    #Draw speed and distance
    speed_and_distance_estimator.draw_speed_and_distance(output_video_frames,tracks)

    # Save video
    # Create output directory if it doesn't exist
    os.makedirs('output_videos', exist_ok=True)
    save_video(output_video_frames, 'output_videos/output_video.avi')

if __name__ == "__main__":
    main()