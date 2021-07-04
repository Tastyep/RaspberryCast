import { action, makeObservable, observable, computed } from "mobx";

import playerAPI from "services/api/player";
import playlistAPI from "services/api/playlist";
import videoAPI from "services/api/video";

export class AppStore {
  player = {};
  playlists = [];
  videos = {};

  constructor(eventDispatcher, modelFactory) {
    makeObservable(this, {
      player: observable,
      playlists: observable,
      videos: observable,

      setPlayer: action,
      setPlaylists: action,
      setVideos: action,
      insertPlaylistVideo: action,
      removePlaylistVideo: action,

      removeVideo: action,
      addVideo: action,

      addPlaylist: action,
      removePlaylist: action,
    });

    this.modelFactory = modelFactory;

    eventDispatcher.observe({
      VideoCreated: (e) => this.onVideoCreated(e),
      VideoDeleted: (e) => this.removeVideo(e.model_id),
      PlaylistCreated: (e) => this.onPlaylistCreated(e),
      PlaylistDeleted: (e) => this.removePlaylist(e.model_id),
    });
  }

  load() {
    this.loadPlayer();
    this.loadVideos();
    this.loadPlaylists();
  }

  loadPlayer() {
    playerAPI
      .get()
      .then((response) => {
        this.setPlayer(response.data);
      })
      .catch((error) => console.log(error));
  }
  loadVideos() {
    videoAPI
      .list()
      .then((response) => {
        this.setVideos(response.data.videos);
      })
      .catch((error) => console.log(error));
  }
  loadPlaylists() {
    playlistAPI
      .list()
      .then((response) => {
        this.setPlaylists(response.data.playlists);
      })
      .catch((error) => console.log(error));
  }

  onVideoCreated(evt) {
    videoAPI
      .get(evt.model_id)
      .then((response) => {
        this.addVideo(response.data);
      })
      .catch((error) => console.log(error));
  }

  onPlaylistCreated(evt) {
    playlistAPI
      .get(evt.model_id)
      .then((response) => {
        this.addPlaylist(response.data);
      })
      .catch((error) => console.log(error));
  }

  setPlayer(player) {
    this.player = this.modelFactory.makePlayer(player);
  }

  setPlaylists(playlists) {
    for (const playlist of playlists) {
      this.playlists.push(this.modelFactory.makePlaylist(playlist));
    }
  }

  addPlaylist(playlist) {
    this.playlists.push(this.modelFactory.makePlaylist(playlist));
  }

  removePlaylist(id) {
    this.playlists = this.playlists.filter((playlist) => playlist.id !== id);
  }

  insertPlaylistVideo(playlistId, videoId, index) {
    let playlist = this.playlists.find(
      (playlist) => playlist.id === playlistId
    );
    if (playlist) {
      playlist.ids.splice(index, 0, videoId);
    }
  }

  removePlaylistVideo(playlistId, videoId) {
    let playlist = this.playlists.find(
      (playlist) => playlist.id === playlistId
    );
    if (playlist) {
      playlist.ids = playlist.ids.filter((id) => id !== videoId);
    }
  }

  playlist(id) {
    return this.playlists.find((playlist) => playlist.id === id);
  }

  playlistVideos(id) {
    return computed(() => {
      const playlist = this.playlists.find((playlist) => playlist.id === id);
      if (!playlist) {
        return [];
      }
      let videos = [];
      for (const id of playlist.ids) {
        videos.push(this.videos[id]);
      }
      return videos;
    }).get();
  }

  setVideos(videos) {
    for (const video of videos) {
      this.videos[video.id] = this.modelFactory.makeVideo(video);
    }
  }

  addVideo(video) {
    this.videos[video.id] = this.modelFactory.makeVideo(video);
  }
  removeVideo(id) {
    delete this.videos[id];
  }
}
