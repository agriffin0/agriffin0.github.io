# Vinyl Picker
#### Video Demo:  https://www.youtube.com/watch?v=v6OH0J_ot4s
#### Description:
This web-based application uses Python, SQL, HTML, and Flask to electronically store your record collection, offer suggestions of what to listen to, and display stats about your library. Once you add albums to your library, you can define criteria (artist, genre, and/or decade) to receive a random album that meets the desired criteria. Also, you can view stats (total album count, listen count, artist count, genre count) about your collection.

I created this website using some ideas from the popular vinyl database website Discogs. However, their platform was missing many features that I wanted to use, including an album randomizer that allows user criteria, adding genres to each album, and a play count tracker. This was the inspiration for my site, to create something useful and helpful.

The website uses various templates, including, of course, the index and layout, as well as upload.html, stats.html, random.html, and counter.html. These pages use HTML and Jinja to display only the data associated with the signed-in user by utilizing “for loops.” They are each associated with the following functions:

On the homepage, the user sees two forms (random and upload) and a Collection table with a list of every album in their library, along with the album’s artist, year, and genre. The table is sorted alphabetically by Artist then chronologically by year. I used SQL commands to pull data to populate the two forms’ Select inputs and the Collection table.

Register, Login, and Logout are function that I borrowed from pset9: Finance. They ensure that each username is only used once and that the password associated with the account is saved as a hash, not as text, for enhanced security.

Random chooses an album using the randint() Python function. If Random is called via GET, it simply renders the page with the randomizer form. If called via POST, it displays a random album that meets the criteria defined by the user, using several nested if/else statements.

Upload allows the user to add additional albums to their collection. If called via POST, it adds the album to the table library, and it also either adds or updates the album in genre_stats and artist_stats. To populate their library, users choose from a list of genres, including Alternative, Classical, Country, Folk, Holiday, Jazz, Pop, Rap, Rock, Soul, and Soundtrack. Album and artist text written into the form is automatically capitalized using the .title() python function. The decade is automatically calculated and added to the Decade column using math.floor(int(year)/10) * 10.

Stats pulls from the genre_stats and artist_stats tables to populate the tables. Counter displays a list of albums that have been listened to, along with their play count. If called via POST, the function will add or update the album's play count.

The database contains 6 tables: users (holds usernames and hashes of passwords); library (containing album title, artist, year, genre, decade, and user_id as a reference); genre_stats (holds count of each genre); artist_stats (holds count of each artist); listen_count (holds count of each listen per album); and listen_history (holds record of each listen with timestamp).