import pandas as pd
from collections import Counter
from tqdm import tqdm
import matplotlib.pyplot as plt
import calmap


class Song:
    start_time = ''
    song_name = ''
    artist_name = ''
    container_name = ''
    device = ''

    def __init__(self, start_time='', name='', artist='', container='', device=''):
        self.start_time = start_time
        self.song_name = name
        self.artist_name = artist
        self.container_name = container
        if type(device) == str:
            if 'iTunes' in device:
                self.device = 'MacBook Pro'
            elif 'iPhone' in device:
                self.device = 'iPhone'
        else:
            self.device = 'iPhone'

    def __str__(self):
        return 'Start Time: {0}, Song Name: {1}, Artist Name: {2}, Container Name: {3}, Device: {4}.' \
            .format(self.start_time, self.song_name, self.artist_name, self.container_name, self.device)


class Music:
    year = ''
    songs = []

    top_songs = []
    song_number = 0

    top_artists = []
    artists_number = 0

    top_albums = []
    albums_number = 0

    def read(self, filename, year):
        self.year = str(year)
        data = pd.read_csv(filename)
        data.is_copy = False
        length = len(data)
        cnt = 0
        print('Loading data from file...')
        for idx in tqdm(range(0, length)):
            # Deal with missing data
            if pd.isnull(data['Event Start Timestamp'][idx]) and pd.isnull(data['Event End Timestamp'][idx]):
                continue
            elif pd.isnull(data['Event Start Timestamp'][idx]):
                data.loc[idx, 'Event Start Timestamp'] = data.loc[idx, 'Event End Timestamp']
            elif pd.isnull(data['Event End Timestamp'][idx]):
                data.loc[idx, 'Event End Timestamp'] = data.loc[idx, 'Event Start Timestamp']
            if pd.isnull(data['Song Name'][idx]):
                continue
            # Filter data according to year
            t = pd.to_datetime(data['Event Start Timestamp'][idx])
            if t.year == year:
                song = Song(start_time=data['Event Start Timestamp'][idx],
                            name=data['Song Name'][idx],
                            artist=data['Artist Name'][idx],
                            container=data['Container Name'][idx],
                            device=data['Build Version'][idx])
                self.songs.append(song)
                cnt += 1
        print('Loaded {} songs.'.format(cnt))

    def getTopSongs(self, number):
        counters = []
        for _ in range(0, 13):
            counters.append(Counter())

        for song in self.songs:
            if not pd.isnull(song.song_name):
                t = pd.to_datetime(song.start_time).tz_localize('UTC').tz_convert('Asia/Shanghai')
                counters[t.month][song.song_name] += 1
                counters[0][song.song_name] += 1
        for idx in range(0, 13):
            self.top_songs.append(counters[idx].most_common(number))
        self.song_number = len(counters[0])

    def getTopArtists(self, number):
        counters = []
        for _ in range(0, 13):
            counters.append(Counter())

        for song in self.songs:
            if not pd.isnull(song.artist_name):
                t = pd.to_datetime(song.start_time).tz_localize('UTC').tz_convert('Asia/Shanghai')
                counters[t.month][song.artist_name] += 1
                counters[0][song.artist_name] += 1
        for idx in range(0, 13):
            self.top_artists.append(counters[idx].most_common(number))
        self.song_number = len(counters[0])

    def getTopAlbums(self, number):
        counters = []
        for _ in range(0, 13):
            counters.append(Counter())

        for song in self.songs:
            if not pd.isnull(song.container_name):
                t = pd.to_datetime(song.start_time).tz_localize('UTC').tz_convert('Asia/Shanghai')
                counters[t.month][song.container_name] += 1
                counters[0][song.container_name] += 1
        for idx in range(0, 13):
            self.top_albums.append(counters[idx].most_common(number))
        self.song_number = len(counters[0])

    def getHeatMap(self):
        print('Getting heat map...')
        c = Counter()
        for song in self.songs:
            t = pd.to_datetime(song.start_time).tz_localize('UTC').tz_convert('Asia/Shanghai')
            c[pd.to_datetime(t.date())] += 1
        events = pd.Series(list(c.values()), index=list(c.keys()))
        calmap.yearplot(events, year=int(self.year))
        plt.savefig('HeatMap{}.png'.format(self.year), dpi=300)

    def getTop(self, number):
        print('Getting top songs...')
        self.getTopSongs(number)
        print('Getting top albums...')
        self.getTopAlbums(number)
        print('Getting top artists...')
        self.getTopArtists(number)

    def generate_markdown(self, topK=10):
        self.getTop(topK)
        self.getHeatMap()
        print('Generating markdown file...')
        md = ''
        md += '# {} Year\'s Report\n'.format(self.year)
        for month in range(0, 13):
            if month == 0:
                md += '## Overall\n'
            else:
                md += '## {}.{}\n'.format(self.year, str(month))
            if not self.top_songs[month]:
                md += 'No data\n'
                continue
            md += '### Top Songs\n'
            md += '| Song Name | Play Times |\n'
            md += '| --------- | ---------- |\n'
            for song in self.top_songs[month]:
                md += '| {} | {} |\n'.format(song[0], song[1])

            md += '### Top Artists\n'
            md += '| Artist Name | Play Times |\n'
            md += '| --------- | ---------- |\n'
            for artist in self.top_artists[month]:
                md += '| {} | {} |\n'.format(artist[0], artist[1])

            md += '### Top Albums\n'
            md += '| Album Name | Play Times |\n'
            md += '| --------- | ---------- |\n'
            for album in self.top_albums[month]:
                md += '| {} | {} |\n'.format(album[0], album[1])

        md += '## HeatMap\n'
        md += '![HeatMap](HeatMap{}.png)\n'.format(self.year)
        with open('{} Year\'s Reporter.md'.format(self.year), 'w') as f:
            f.write(md)
