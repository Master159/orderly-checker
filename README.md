# orderly-checker
The Order Network checker for any wallet address in the leaderboard, a checker for statistics for any epoch, uploading data on all wallet addresses for any epoch.

Just select the necessary option and go with the flow:

1. Show information about a certain epoch
2. Find information about the address you are looking for
3. Create a text file with data about the participants
0. Exit

Keep in mind that when choosing a certain epoch, statistics for all epochs before it are shown, inclusive. That is, if you enter 3, the statistics for 1+2+3 epochs, if 2, then 1+2 epochs, etc.

Also, if the 5th epoch is passing now, then look at the statistics for it in the format 1+2+3+4+5 It won't work. You need to wait for it to end and only then the necessary data will be available via the API.
