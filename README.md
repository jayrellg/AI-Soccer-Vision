# AI Soccer Vision

_End‑to‑end computer‑vision analytics for soccer footage built with Python & YOLOv8_

----------

## Features

-   **Object detection** of players, referees, and the ball with a custom‑trained **YOLOv8** model.
    
-   **Multi‑object tracking** with **ByteTrack** – persistent IDs across the full clip.
    
-   **Optical‑flow camera‑motion compensation** so player stats are field–, not camera–centric.
    
-   **Bird’s‑eye view (homography) transformation** – every detection mapped to metric field coordinates.
    
-   **Per‑player speed & distance** (km/h, m) computed over adjustable frame windows.
    
-   **Automatic team assignment** via K‑Means clustering of dominant jersey colours.
    
-   **Ball‑possession attribution** – find who has the ball and maintain rolling team‑control stats.
    
-   Annotated video output with bounding ellipses, possession triangles, speed/distance text, and camera‑movement readout.

## Directory Overview


AI-Soccer-Vision/
├── camara_movement_estimater/   # Optical‑flow camera‑motion estimation
├── input_videos/                # Raw test clips (mp4)
├── models/                      # YOLOv8 weights (best.pt)
├── player_ball_assigner/        # Ball‑to‑player linking logic
├── speed_and_distance_estimator/# Speed & distance metrics
├── team_assigner/               # Jersey‑colour K‑Means clustering
├── trackers/                    # YOLOv8 + ByteTrack wrapper
├── utils/                       # Helper utilities (video I/O, geometry)
├── view_transformer/            # Homography to field coordinates
├── training/                    # Notebooks & configs for detector training
└── main.py                      # Pipeline entrypoint

## Acknowledgements

-   [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
    
-   [Supervision](https://github.com/roboflow/supervision)
    
-   [Roboflow](https://roboflow.com/)
    
-   [OpenCV](https://opencv.org/)
    
-   [ByteTrack](https://github.com/ifzhang/ByteTrack)
    
-   The open‑source community :heart:



