from sklearn.cluster import KMeans

class TeamAssigner:
    def __init__(self): 
        self.team_colors = {} # {team_id: RGB centroid}; will be filled after assign_team_color()
        self.player_team_dict = {} # {player_id: team_id}; used to avoid recomputing a player’s team
    

    #Run 2-colour K-means on a RGB image
    def get_clustering_model(self,image):
        """
        Parameters
        ----------
        image : np.ndarray
            3-channel RGB image, shape (H, W, 3).

        Returns
        -------
        sklearn.cluster.KMeans
            Fitted model with 2 colour centroids.
        """

        #Flatten the (H, W, 3) image into a 2-D array, each row = one pixel --> (H × W, 3)
        image_2d = image.reshape(-1,3)

        # Preform K-means with 2 clusters
        # n_clusters = 2 : want two dominant colours
        # init = "k-means++" : smart centroid initialisation
        #  n_init = 1 : run the algorithm once (faster; deterministic if a random_state is set globally)
        kmeans = KMeans(
            n_clusters=2,
            init="k-means++",
            n_init=1
        )

        #Fit on all pixel RGB vectors
        kmeans.fit(image_2d)

        return kmeans

    # Extract the dominant jersey colour for a *single* player
    def get_player_color(self,frame,bbox):
        """
        Return the dominant jersey colour (RGB centroid) for the player inside `bbox`.

        Parameters
        ----------
        frame : np.ndarray
            Full RGB video frame of shape (H, W, 3).
        bbox : list[int] | tuple[int, int, int, int]
            Bounding box `[x1, y1, x2, y2]` for the player.

        Returns
        -------
        np.ndarray
            A length-3 vector `[R, G, B]` giving the player’s dominant
            jersey colour.
        """


        # Crop the player from the full video frame
        # Crop order is [y1:y2, x1:x2]
        image = frame[
            int(bbox[1]):int(bbox[3]),  # rows → y-axis
            int(bbox[0]):int(bbox[2])   # cols → x-axis
        ]

        
        # Use only the upper half of the crop (we want main shirt color)
        top_half_image = image[0:int(image.shape[0]/2),:]


        # Run K-means clustering (2 clusters: jersey vs. background)
        kmeans = self.get_clustering_model(top_half_image)

        # Labels is a flat 1D array with cluster index (0 or 1) for every pixel
        labels = kmeans.labels_

        #  Reshape labels back to 2D image format (H × W)
        clustered_image = labels.reshape(top_half_image.shape[0],top_half_image.shape[1])

        # Detect which cluster is background by sampling four corners
        corner_clusters = [
            clustered_image[0, 0],         # top-left
            clustered_image[0, -1],        # top-right
            clustered_image[-1, 0],        # bottom-left
            clustered_image[-1, -1]        # bottom-right
        ]        

        # Get the cluster label (0 or 1) that appears most frequently in corners (presumably the  background)
        non_player_cluster = max(set(corner_clusters),key=corner_clusters.count)
        
        # Get player cluster
        player_cluster = 1 - non_player_cluster


        #Return the RGB centroid of the player cluster
        player_color = kmeans.cluster_centers_[player_cluster]

        return player_color


    def assign_team_color(self,frame, player_detections):
        """
        Clusters all detected players into 2 teams based on their jersey colors.
        
        Parameters
        ----------
        frame : np.ndarray
            The full video frame (RGB image) from which player crops will be extracted.
            
        player_detections : dict
            A dictionary of player detections. Each entry contains a 'bbox' key
            with the bounding box coordinates.
        """
        
        # Will hold RGB vectors  for each player[R, G, B]
        player_colors = [] 
        
        
        for _, player_detection in player_detections.items():
            bbox = player_detection["bbox"]
            
            # Use get_player_color to isolate the dominant color in the shirt region
            player_color =  self.get_player_color(frame,bbox)
            
            # Save it for clustering
            player_colors.append(player_color)
        
        #Run K-means to group similar jersey colors
        kmeans = KMeans(
            n_clusters=2,     # We assume exactly 2 teams on the field
            init="k-means++", # Smart initialization of centroids
            n_init=10)        # Run 10 times with different centroid seeds for stability

        # Fit clustering model on the player colors (shape: num_players × 3)
        kmeans.fit(player_colors)


        # Save the fitted KMeans model for use in team prediction later
        self.kmeans = kmeans


        #Save the resulting team centroids (average jersey colors)
        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]


    def get_player_team(self,frame,player_bbox,player_id):

        """
        Predicts the team ID (1 or 2) for a given player.

        Parameters
        ----------
        frame : np.ndarray
            The full video frame containing the player.
            
        player_bbox : list or tuple
            The bounding box [x1, y1, x2, y2] for the player.
            
        player_id : int
            The unique ID assigned to the player by the tracker.

        Returns
        -------
        int
            The predicted team ID (1 or 2).
        """

        #If we've already assigned a team to this player, return it
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]


        #Extract this player's jersey color from their top-half bounding box
        player_color = self.get_player_color(frame,player_bbox)


        # Use the trained KMeans model to predict the closest team centroid returns either 0 or 1 
        team_id = self.kmeans.predict(player_color.reshape(1,-1))[0]
        team_id+=1

        #Hard coded Edge casses for goalies, should find a way to improve this!!!!!!!!!!!!
        if player_id == 78:
            team_id =2
        
        if player_id == 188:
            team_id = 1

        self.player_team_dict[player_id] = team_id

        return team_id