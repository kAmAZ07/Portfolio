It was necessary to develop a console application "Music Organizer", which should:
1. Store data about music tracks in a text file
2. 
  • The application must read the track data from the file at startup.
  • The path to the directory file must be requested from the user.
  • The application must verify the correctness of the path and handle errors.

3. Provide the user with the opportunity:
  • View all tracks (as a list: Name, Artist, Album, Year, Genre).
  • Adding a new track. Ask the user for the name, artist, album, year of release, genre.
  • Edit track information. The user selects a track and can change any field.
  • Deleting a track. The user selects a track to delete.

4. Filtering and sorting tracks:
  • Filtering by artist, album, year of release (range) or genre.
  • Sort (ascending/descending):
  ‣ By track name.
  , By performer.
  , By album.
  , By year of graduation.
  • Ability to combine filters and sorting

5. Visualization using Spectre.Console:
  • Table: Displays tracks in tabular form with the ability to scroll and interactively filter/sort in the table.
  • The tree: Displaying the hierarchy "Artist -> Album -> Track". Can be implemented using A TreeView from Spectre.Console.
  • Progress Bar: Displays the playback progress of a track (if playback emulation is added). You can use Progress from Spectre.Console.

6. Integration with the MusicBrainz API:
  • Implement automatic acquisition of track information (artist, album, year of release, genre,
  album cover) based on the track name and/or artist. Use the MusicBrainz API
  (it will require working with JSON and HTTP requests). It is recommended to use the library
  MetaBrainz.MusicBrainz (NuGet). It will simplify working with the API.
  • Supplement/correct data in the catalog based on information from MusicBrainz.
  • MBID Search: Add the ability to search tracks by their unique MusicBrainz ID
  (MBID). Store this value for each track.
  • Getting information about the performer: Implement getting additional information about
  the performer (country, date of foundation/breakup, band members).
  • Getting information about the album: Implement getting additional information about the album
  (tracklist, label, release date in different countries).
  • Links: Add the ability to display links to the artist/album/track page on
  MusicBrainz.

7. Audio playback:
  • Add track playback. When selecting a track, display that the track is playing, and after it finishes,
  report that the track has ended. Add the option to end listening ahead of schedule.

9. Import/Export:
  • Add metadata import from CSV files.
  • Add metadata export to CSV formats.

10. Automatic folder scanning:
  • Implement the function of automatically scanning the folder specified by the user for the presence of
  music files (for example, MP3, FLAC, Ogg Vorbis).
  • Extract metadata from files and use the MusicBrainz API to refine and supplement
  information (as in the main task). This will allow you to get more accurate and complete data. 
  You can use the TagLibSharp library to work with audio file tags.
11. Display information about tracks on the console
12. Save the directory changes back to the file when the application is shut down
