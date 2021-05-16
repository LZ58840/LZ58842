# /u/LZ58842
A specialized reddit bot designed to handle trivial `/r/Animewallpaper` moderation jobs.

It is currently able to evaluate incoming/unmoderated submissions that fall in one or more of the following cases:
- **(rule 2)** Resolution does not satisfy the subreddit rule requirements
- **(rule 2)** Aspect ratio does not satisfy the subreddit rule requirements
- **(rule 3)** No resolution stated in title
- **(rule 3)** Misleading resolution in title

Should a submission fall under the above cases, the bot will automatically remove it and provide an appropriate comment.

**Currently documented modes**: Operational, Shadow, Suspended, Timed Suspended, Shutdown

###Future features to include:
- **(rule 3)** No source anime stated in title
- **(rule 4)** Incorrect flair assigned 
- **(rule 5)** No source artwork/artist in the comments within 1 hour
- `Collection` support
- Unauthorized text posts

###Planned future development:
- Discord and Reddit PM frontend