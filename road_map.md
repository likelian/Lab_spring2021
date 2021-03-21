# Road Map









#### How to define the complexity(tension) to note density, ~~duration~~, velocity?


I can’t find anything about note duration. So I will simply extend the note duration to the start of next note, or the change in harmony.

According to the following, <u>**velocity and note density is positively correlated to the tension level.**</u>

>"The tension levels tended to increase within segments, with accompanying increases in dynamics and note density."
>
>Krumhansl, Carol L. "Music: A link between cognition and emotion." Current directions in psychological science 11, no. 2 (2002): 45-50.

>"However, the design of the arrangement also implies control of a number of musical aspects on a global scale. These can be summarized in a tension curve, that includes aspects ⇐= such as melodic curves (high and low points), harmonic consonance and dissonance, dynamics (soft-loud), orchestration (instrumentation, register, special playing techniques and effects) and part density (between unisono and tutti). The total duration of the arrangement follows from the tempo."
>
>p.207
>[https://www.fransabsil.nl/archpdf/arrbook.pdf](https://www.fransabsil.nl/archpdf/arrbook.pdf)



#### How to create the approximated tension contour?

1. Initial the tension value.
2. Analyze the LUFS of the input audio.
3. Analyze the structure of the music.
4. Analyze the LUFS of each section of the music.
5. Change the tension contour of each sections based on the difference of the sectional LUFS and the overall LUFS.
6. Analyze the genre of the input audio.
7. From the note density value gathered previously through midi data in each genre, the algorithm iterates over the parameters of the onset detection function in each section with the consideration of relative tension, till the overall onset density approaches the desired value.
8. Change the tension contour accordingly.



#### Melody:
* Jumps in the bassline
    * possible **fifth** and **octave**, not on the first note in a chord, and back to the root note after the fifth or the octave
    * jump to the octave more often than the fifth
* Connection two chords with **passing notes**
    * chromatic passing notes
    * diatonic passing notes
* Use chord **inversion** to form a smooth bassline in a series of chords
* Automatic voicing to avoid spectral masking


[https://www.musicianonamission.com/how-to-write-a-bassline/](https://www.musicianonamission.com/how-to-write-a-bassline/)



#### What does it do?
The system uses audio features to generate bass guitar midi, including what to generate and the choices of algorithms and parameters.

>audio => tempo estimation, genre classification, beat/downbeat detection, dynamic range, loudness contour, (structure identification)
>
>audio => source separation => onset detection, chord detection


| Melody |Onset  |~~Duration~~  |Velocity  |
| --- | --- | --- | --- |
|downbeat on root | <u>**density by genre**</u>  | <u>**genre**</u>  |beat and downbeat  |
|passing tones  | density by tempo  | <u>**tempo**</u> |**<u>loudness</u>**  |
|grace notes  |density by complexity/loudness   |complexity  |complexity  |
|5th&8th  |density by dynamic range  | <u>**loudness**</u> |  |
|**voicing from spectral analysis**  |quantization from tempo (ignore outliners)  |  |
|**follow the bass/lead note** | **follow the drums or others** ||


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


* * *


**Follow the drum?:** It will mark the sections with or without the drums, and treat the sections differently.

**Interactive Control:** Users can draw a line(automation) and tell the system to change the degree of complexity according to the line. For example, in the intro section, the user want less notes and quiter playing. The system will also provide a suggested line(automation) by analyzing the tempo, genre, etc..

**Reduce variations:** find some patterns(riff) in the generated midi, and copy this pattern to parts that are very similar to the pattern, so the riff is not interrupted by the error of feature extractions.



>#### How to do it?
>
>1. Examine if quantizing the chord detection with beat detection is still meaningful
>2.  **Map the onset midi to root note midi**
>3. find the note/beat ratio data, or extract such data from MIDI datasets, regarding to some specific genre
>4. An algorithm that uses note/beat ratio to tune the parameter in onset detection
>5. Implement genre classification
>6. Assist the above algorithm with genre classification
>7. Source separation
>8. Drum transcription
>9. Redo the chord detection without drums
>10. Redo the onset detection without drums
>11. Add tempo into the consideration of note duration
>    1. find existing data
>    2. apply the extracted data to the algorithm
>12. (Structure identification)
>13. User study
>
