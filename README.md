# Apple-Music-Year's-Report
At the end of a year, QQ Music and Music 163 will give you a year's report. However, apple music will not. This project enables you to create your own report.

First of all, you need to contact privacy_response@apple.com to get all your personal data. They may ask you to provide some personal information to conform your identity, finally you will receive a csv file.

Put the csv file in the workding directory, then run main.py.

music.read('data.csv', 2019) # 2019 refers to the year you want create report of
music.generate_markdown(topK=20) # topK refers to how many items you want

environment: python 3.6, pandas, tqdm, matplotlib, calmap.
