# Lab_spring2021

2/7 meeting
---------------
**Last weeek (1/31 - 2/7):**
1. madmom library, audio => chroma => chord symbol & timestamp => root note & timestamp =...90%...> midi for bass
2. install Open-Unmix 0% done (skip it)

**meeting discussion:**
- What kind of audio as input? with or without drums?
- Genre specific or not? (Metal?)
- If this is user-driven using summed track, is it really easy to use except python environment? (genre identification)
- Is source seperation necessary?
- Tempo?


**Next Week (2/8 - 2/14):**
1. checkout Studio One
2. finish midi for bass
3. Come up with an alternative plan if one or current libraries doesn’t work (individual tracks?)
4. Look at many genres, find music textbook
5. Start with onset/drum/tempo...

--------------
**Last weeek (2/8 - 2/14):**
1. Studio One has very good chord detection and basic bass line generation. It doesn’t consider rhythmic information unless the user write it out.
    * [Offical documentation](https://s1manual.presonus.com/Content/Arranging_Topics/Chord%20Track.html)
    * [One YouTube video](https://www.youtube.com/watch?v=flrFapH7RnY)
    * [Another video](https://www.youtube.com/watch?v=A_3CMsyfWqo)
2. Found a book [Bassist's Bible](http://www.bassistsbible.com/). This book has somehow detailed knowledge about bass patterns in many popular music genres. Metal and Punk have shorter chapters than other genres, so it's easier to implement these two. Some Electronic music genres have simple bass patterns. I can go with that direction if sound design is not part of the project.


--------------
**Last weeek (2/15 - 2/21):**
1. Tried out onset, beat, and downbeat dectection.
    * [madmom.features.beats](https://madmom.readthedocs.io/en/latest/modules/features/beats.html)
    * [madmom.features.beats_crf](https://madmom.readthedocs.io/en/latest/modules/features/beats_crf.html)
    * [madmom.features.beats_hmm](https://madmom.readthedocs.io/en/latest/modules/features/beats_hmm.html)
    * [madmom.features.downbeats](https://madmom.readthedocs.io/en/latest/modules/features/downbeats.html)
    * [madmom.features.tempo](https://madmom.readthedocs.io/en/latest/modules/features/tempo.html)
2. Onset detection seems to work nicely. For analysizing a full track, threshold around 7 is good. For a track below 150Hz, threshold below 1.
3. Convert onset locations to midi.
4. Manually quantize onsets to 16th notes.
5. Manually join onsets and root notes (a few bars) together. It sounds pretty good.


**Next Week (2/22 - 2/28):**

Possible directions:
1. Drum separation -> drum transcription, replace onset detection
2. Beat detection -> downbeat detection -> bass pattern based on style
3. Tempo tracking -> auto quantization

--------------
**Last weeek (2/22 - 2/28):**
1. Worked on beat detection. The result is not as accurate as expected.

**Meeting**
1. A plan is needed
2. Test on the beat detection
3. Evaluation method for this project


**Next Week (2/28 - 3/7):**

1. A plan
2. Test on the beat detection
3. Evaluation method


--------------
**Last weeek (2/28 - 3/7):**
1. Tested and evaluated different beat detection algorthms
2. in this project, beat detection only works when a constant tempo is assumed, and the audio is edited

**Meeting**
1. Structure identification combined, not a good idea
2. Note density idea is good, more than note/tempo ratio? More evidence to support this idea


**Next Week (3/7 - 3/14):**
1. Build a baseline this week, root + onset
2. Export 10 generated pieces, several genres
3. Think a bigger plan that is not limited by the current technology
4. Find a path to the plan


--------------
**Last weeek (3/7 - 3/14):**
1. Built the baseline system
2. Test on ten songs
    * Good: Blues, Country, Hiphop, Electronic, Pop
    * Bad: Metal and Rock due to the small dynamic range; Reggae due to the short chord length

**Meeting**
1. Variation reduction needs more explanation
2. based on what evidence you derive your definition of complexity, why your definition is not arbitrary, and why your definition is more fitting than possible alternative ways of defining complexity, and
3. how you actually plan to model/approximate this complexity algorithmically and how you verify that your model fits the definition.
4. Melody??


**Next Week (3/15 - 3/21):**
1. Melody ideas
2. Evidence of complexity mapping
3. Plan for complexity approximation
4. Source separation


--------------
**Last weeek (3/15 - 3/21):**
1. Found a midi [dataset](freemidi.org)
    * Labelled genres on webpage: Rock, Pop, Hip-Hop, R&B Soul, ~~Classical~~, Country, Folk, Jazz, Blues, Dance/Electric, Folk, Punk, ~~Newage~~
    * Many have constant velocity
    * Tempo and time signature inherited in midi files
2. Installed [Open-unmix](https://sigsep.github.io/open-unmix/#using-the-pytorch-version)
3. Found some literature about note density and velocity


**Meeting**
1. Randomess no good
2. Key detection needed for passing notes
3. What is the distance between root notes
4. Stylistic selection?
5. A list of priority
6. A schedule


**Next Week (3/21 - 3/28):**
1. A list of priority
2. A schedule


--------------
**Last weeek (3/21 - 3/28):**
1. Implemented the basic note density search algorithm
2. Improve the note duration so it matches the next note
3. Came up with a schedule

**Meeting**
1. Make sure the algorithm converge
2. Understand loudness metrics


**Next Week (3/28 - 4/4):**
1. Implement structure idenntification
2. Implement loudness analysis



--------------
**Last weeek (3/28 - 4/4):**
1. Integrated structure idenntification, no proper evaluation
2.Implemented LUFS for each section

**Meeting**
1. no evaluation is fine
2. DBa???
3. Is the library reliable?

**Next Week (4/4 - 4/11):**
1. GUI
2. Real-time playing


--------------
**Last weeek (4/4 - 4/11):**
1. Playback (need: reload of midi, a slider for playback position?)
2. Display of music structure
3. Audio mix control
4. One slider for density
5. Create all sliders (don't do anything yet)

**Meeting**
1. Midi audio sync?
2. Label time axis
3. label gain knob
4. normal gain knob is log scale
5. number the sliders with each section!
6. Overall slider?
7. playback control?
8. Stop
9. Quantized slider

**Next Week (4/11 - 4/17):**
1. Make all sliders works!
3. More clear explaination
4. Figure out the mapping


--------------
**Last weeek (4/11 - 4/17):**
1. Failed to imporve the playback (unable to do anything to the midi playback)
2. All sliders work now
3. Provides suggested slider position based on loudness
4. slider^3 gain control
5. Label time axis

**Meeting**
1.

**Next Week (4/17 - 4/):**
1. Splice the midi files
2. New mapping of the sliders
3. try on 30 songs, pick the good and bad ones
4. Slider labels
5. passing notes


--------------
**Last weeek (4/17 - 4/25):**
1. Tested on 30 songs
2. New slider mapping
3. Section playback
4. passing notes

**Meeting**
1.number the visual segments
2.DONE gain knob initial position
3.without bass, loud bass, normal bass
4. 60s talk: motivation, outcome, methods
5. poster, all 3rd libraries; audio and corresponding settings
