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
        print("create_playlist needs implementation")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        print("add_to_playlist needs implementation")

    def show_all_playlists(self):
        """Display all playlists."""

        print("show_all_playlists needs implementation")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("show_playlist needs implementation")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        print("remove_from_playlist needs implementation")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("clears_playlist needs implementation")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("deletes_playlist needs implementation")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

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
