# textbook-to-csv
Flash card apps are a fast way to memorize things, but making all the cards takes a long time. textbook-to-csv uses optical character recognition to do the tedious transcription for you. Just take a picture of your textbook, drag boxes around the stuff you want to learn, and hit space to get a neat spread sheet to import into your favorite memorization app!

## How to use
Instantiate the GUI class and call start() on it. Click and drag to place a box on your image. Try to box as close to the text as possible. Hit space to extract the words to CSV.
If there are two related columns (eg. words and their definitions), drag a box around the leftmost one first. Then press 2 to begin placing a box around the second column. Press 1 to go back to adjusting the first box. Hit space when you're done to extract the data to CSV.
