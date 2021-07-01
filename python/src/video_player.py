"""A video player class."""
from collections import defaultdict

from .video_library import VideoLibrary
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.playing = ""
        self.paused = False
        self.playlists = defaultdict(list)
        self.playlists_original_names = {}
        self.flagged_videos_counter = 0

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        print("Here's a list of all available videos:")
        all_videos = self._video_library.get_all_videos()
        all_videos.sort(key=lambda v: v.title)

        for video in all_videos:
            display_msg = f"{video.title} ({video.video_id}) [{' '.join(video.tags) if len(video.tags) > 0 else ''}]"
            print((display_msg + f" - FLAGGED (reason: {video.flag_reason})") if video.flagged else display_msg)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        new_video = self._video_library.get_video(video_id)

        if new_video is None:
            print("Cannot play video: Video does not exist")
            return

        if new_video.flagged:
            print(f"Cannot play video: Video is currently flagged (reason: {new_video.flag_reason})")
            return

        if new_video.title == self.playing:
            print("Video is already playing")
            return

        if not self.playing == "":
            print(f"Stopping video: {self._video_library.get_video(self.playing).title}")

        self.playing = new_video.video_id
        print(f"Playing video: {self._video_library.get_video(self.playing).title}")
        self.paused = False

    def stop_video(self):
        """Stops the current video."""

        if self.playing == "":
            print("Cannot stop video: No video is currently playing")
            return

        print(f"Stopping video: {self._video_library.get_video(self.playing).title}")
        self.playing = ""
        self.paused = False

    def play_random_video(self):
        """Plays a random video from the video library."""
        all_videos = self._video_library.get_all_videos()
        if len(all_videos) == 0 or self.flagged_videos_counter == len(self._video_library.get_all_videos()):
            print("No videos available")
            return

        selected_video = random.choice(all_videos)
        self.play_video(selected_video.video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self.playing == "":
            print("Cannot pause video: No video is currently playing")
            return

        if self.paused:
            print(f"Video already paused: {self._video_library.get_video(self.playing).title}")
            return

        self.paused = True
        print(f"Pausing video: {self._video_library.get_video(self.playing).title}")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.playing == "":
            print("Cannot continue video: No video is currently playing")
            return

        if not self.paused:
            print("Cannot continue video: Video is not paused")
            return

        self.paused = False
        print(f"Continuing video: {self._video_library.get_video(self.playing).title}")

    def show_playing(self):
        """Displays video currently playing."""
        if self.playing == "":
            print("No video is currently playing")
            return

        current_video = self._video_library.get_video(self.playing)
        display_msg = f"Currently playing: {current_video.title} ({current_video.video_id}) " \
                      f"[{' '.join(current_video.tags) if len(current_video.tags) > 0 else ''}]"

        print((display_msg + " - PAUSED") if self.paused else display_msg)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.find(" ") != -1:
            print("Cannot create playlist: Playlist name must not contain whitespace")
            return

        if playlist_name.lower() in self.playlists.keys():
            print("Cannot create playlist: A playlist with the same name already exists")
            return

        self.playlists[playlist_name.lower()] = []
        self.playlists_original_names[playlist_name.lower()] = playlist_name
        print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.lower() not in self.playlists.keys():
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
            return

        video = self._video_library.get_video(video_id)

        if video is None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return

        if video.flagged:
            print(f"Cannot add video to my_playlist: Video is currently flagged (reason: {video.flag_reason})")
            return

        if video_id in self.playlists[playlist_name.lower()]:
            print(f"Cannot add video to {playlist_name}: Video already added")
            return

        self.playlists.get(playlist_name.lower()).append(video_id)
        print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self.playlists.keys()) == 0:
            print("No playlists exist yet")
            return

        print("Showing all playlists:")
        sorted_dict = sorted(self.playlists_original_names)
        for playlist in sorted_dict:
            print(self.playlists_original_names[playlist])

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self.playlists.keys():
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return

        print(f"Showing playlist: {playlist_name}")

        playlist_videos = self.playlists.get(playlist_name.lower())
        if len(playlist_videos) == 0:
            print("No videos here yet")
        else:
            for video in playlist_videos:
                video_details = self._video_library.get_video(video)
                display_msg = f"{video_details.title} ({video_details.video_id}) " \
                              f"[{' '.join(video_details.tags) if len(video_details.tags) > 0 else ''}]"

                print((display_msg + f" - FLAGGED (reason: {video_details.flag_reason})")
                      if video_details.flagged else display_msg)

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.lower() not in self.playlists.keys():
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return

        if self._video_library.get_video(video_id) is None:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return

        if video_id not in self.playlists.get(playlist_name.lower()):
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return

        self.playlists.get(playlist_name.lower()).remove(video_id)
        print(f"Removed video from {playlist_name}: {self._video_library.get_video(video_id).title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self.playlists.keys():
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return

        self.playlists[playlist_name.lower()] = []
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self.playlists.keys():
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return

        self.playlists.pop(playlist_name.lower())
        self.playlists_original_names.pop(playlist_name.lower())
        print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()

        # filtering for videos that match the search term
        filtered_videos = list(filter(lambda x: search_term.lower() in x.title.lower(), all_videos))

        # filtering again to remove flagged videos from results
        filtered_videos = list(filter(lambda x: not x.flagged, filtered_videos))

        filtered_videos.sort(key=lambda v: v.title)

        if len(filtered_videos) == 0:
            print(f"No search results for {search_term}")
            return

        print(f"Here are the results for {search_term}:")

        # nice Pythonic way of making a numbered list
        for idx, video in enumerate(filtered_videos):
            print(f"{idx+1}) {video.title} ({video.video_id}) [{' '.join(video.tags) if len(video.tags) > 0 else ''}]")

        print("Would you like to play any of the above? If yes, specify the number of the video.\n"
              "If your answer is not a valid number, we will assume it's a no.")

        try:
            choice = int(input())
        except ValueError:
            return

        if not 1 <= choice <= len(filtered_videos):
            return

        self.play_video(filtered_videos[choice-1].video_id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = self._video_library.get_all_videos()

        # filtering for videos with the searched tag. more readable than using filter()
        filtered_videos = []
        for video in all_videos:
            if video_tag.lower() in map(lambda x: x.lower(), video.tags):
                filtered_videos.append(video)

        # filtering out flagged videos
        filtered_videos = list(filter(lambda x: not x.flagged, filtered_videos))

        filtered_videos.sort(key=lambda v: v.title)

        if len(filtered_videos) == 0 or not video_tag[0] == "#":
            print(f"No search results for {video_tag}")
            return

        print(f"Here are the results for {video_tag}:")
        for idx, video in enumerate(filtered_videos):
            print(
                f"{idx + 1}) {video.title} ({video.video_id}) [{' '.join(video.tags) if len(video.tags) > 0 else ''}]")

        print("Would you like to play any of the above? If yes, specify the number of the video.\n"
              "If your answer is not a valid number, we will assume it's a no.")

        try:
            choice = int(input())
        except ValueError:
            return

        if not 1 <= choice <= len(filtered_videos):
            return

        self.play_video(filtered_videos[choice - 1].video_id)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
