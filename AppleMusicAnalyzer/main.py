from Music import Music

if __name__ == '__main__':
    music = Music()
    music.read('data.csv', 2019)
    music.generate_markdown(topK=20)
