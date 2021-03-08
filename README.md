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
