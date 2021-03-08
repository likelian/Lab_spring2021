# Road Map

#### What does it do?
The system uses audio features to generate bass guitar midi, including what to generate and the choices of algorithms and parameters.


In particular, the data for the generation includes bass drum onset, accompanied tracks' onset, beat, downbeat, pre-programmed patterns, chord detection, lead melody, and bass melody. Other features (tempo, genre, structure) help to decide on how much of the data from each category the algorithm is leaning on.

#### How to do it?

1. Examine if quantizing the chord detection with beat detection is still meaningful
2.  **Map the onset midi to root note midi**
3. find the note/beat ratio data, or extract such data from MIDI datasets, regarding to some specific genre
4. An algorithm that uses note/beat ratio to tune the parameter in onset detection
5. Implement genre classification
6. Assist the above algorithm with genre classification
7. Source separation
8. Drum transcription
9. Redo the chord detection without drums
10. Redo the onset detection without drums
11. Add tempo into the consideration of note duration
    1. find existing data
    2. apply the extracted data to the algorithm
12. (Structure identification)
13. User study




# Evaluation


#### Self-Assessment Frameworks
>Another popular approach is to have the author of the system describe the way it works and how it can be considered creative or not, and to what degree.


## Quantitative Metrics

* Probabilistic measure
* Model-specific metrics
* Metrics based on domain knowledge

### Rhythm-based features

* Note count (NC)
* Average inter-onset-interval (IOI)
* Note length histogram (NLH)
* Note length transition matrix (NLTM)


## User test

### Turing Test-Like Approaches

...

### Efficiency test
Since this is assisted music genreation, we can compare the efficiency imporvement it provides. Within the given amount of time of music making, compare the final results of the bass guitar parts from subjective listening. In one group, composers start with the audio and the midi parts generated from the tool (adding the time using the tool). In the other group, composers can start with midi transcription? (studio one?).







[https://www.frontiersin.org/articles/10.3389/frai.2020.00014/full](https://www.frontiersin.org/articles/10.3389/frai.2020.00014/full)

[https://link.springer.com/article/10.1007/s00521-018-3849-7?wt_mc=Internal.Event.1.SEM.ArticleAuthorOnlineFirst&utm_source=ArticleAuthorOnlineFirst&utm_medium=email&utm_content=AA_en_06082018&ArticleAuthorOnlineFirst_20181106&error=cookies_not_supported&code=499f84ea-1632-4009-93ee-07a77a78629b](https://link.springer.com/article/10.1007/s00521-018-3849-7?wt_mc=Internal.Event.1.SEM.ArticleAuthorOnlineFirst&utm_source=ArticleAuthorOnlineFirst&utm_medium=email&utm_content=AA_en_06082018&ArticleAuthorOnlineFirst_20181106&error=cookies_not_supported&code=499f84ea-1632-4009-93ee-07a77a78629b)
