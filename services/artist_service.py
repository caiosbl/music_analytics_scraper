from models.artist import Artist

class ArtistService:
    def __init__(self, session, repositories):
        self.session = session
        self.repositories = repositories
    
    def insert_artist(
        self,
        name,
        spotify_id,
        youtube_id,
        deezer_id,
        apple_music_id,
        amazon_music_id,
        tidal_id
    ):
        artist = Artist(
            name=name,
            spotify_id=spotify_id or None,
            youtube_id=youtube_id or None,
            deezer_id=deezer_id or None,
            apple_music_id=apple_music_id or None,
            amazon_music_id=amazon_music_id or None,
            tidal_id=tidal_id or None
        )
        return self.artist_repository.insert_artist(artist)
    
    def update_artist(
        self,
        artist_id,
        name,
        spotify_id,
        youtube_id,
        deezer_id,
        apple_music_id,
        amazon_music_id,
        tidal_id
    ):
        artist = self.artist_repository.get_artist(artist_id)

        if not artist:
            raise ArtistNotFoundError(f"Artist with id {artist_id} not found")


        if name:
            artist.name = name

        if spotify_id:
            artist.spotify_id = spotify_id
        if youtube_id:
            artist.youtube_id = youtube_id

        if deezer_id:
            artist.deezer_id = deezer_id
        
        if apple_music_id:
            artist.apple_music_id = apple_music_id

        if amazon_music_id:
            artist.amazon_music_id = amazon_music_id

        if tidal_id:
            artist.tidal_id = tidal_id

        self.session.commit()


class ArtistNotFoundError(Exception):
    pass
