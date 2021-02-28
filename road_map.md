# Road Map

#### What does it do?
The system uses audio features to generate bass guitar midi, including what to generate and the choices of algorithms and parameters.


In particular, the data for the generation includes bass drum onset, accompanied tracks' onset, beat, downbeat, pre-programmed patterns, chord detection, lead melody, and bass melody. Other features (tempo, genre, structure) help to decide on how much of the data from each category the algorithm is leaning on.

#### How to do it?

1. Quantize chord detection with beat detection
2. **Map the onset midi to root note midi**
3. Decide if the beat detection and tempo tracking can improve the onset position (can wait after drum transcription)
4. **Create a simple bass pattern and apply it to the beat detection, output bass pattern midi**
5. **Find a way to morph between the onset midi and the programed pattern midi**
6. **Add tempo into the consideration (long note for ballads)**
7. Try genre classification, and take a few genres into the consideration
8. Try source separation
9. Try drum transcription
10. Redo the chord detection without drums
11. Redo the onset detection without drums
12. (Bass transcription and lead transcription if possible)
13. Stable the performance in one song, replace small variations with repetitions
14. Try structure identification
15. Add more programmed bass patterns
16. Stable the performance in one section
17. Create a simple GUI for audio input and midi output
18. Add controls in GUI (quantization, complexity..)






