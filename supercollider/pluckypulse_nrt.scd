// Generate audible pulse in SuperCollider (SC) for fMRI fingertapping experiment.
// This ver of script for non-realtime sound file rendering (and therefore manual triggering
// at console). Note: SC is an open source platform for audio synthesis and algorithmic music composition.
// Alter lines 15-29, depending on the desired experiment. Written for a scanner suite with
// audio but no video or triggering capabilities. Oct & Nov 2025, salvatore.torrisi@ucsf.edu

// FIRST, SELECT AND BOOT THE AUDIO ENGINE WITH THIS SINGLE LINE:
s.boot;

// SECOND, SELECT AND EXECUTE THE REST OF THE CODE:
(
// USER CONFIGS - modify these experiment parameters:

// Output file configuration:
var outputFileName = "pluckyBlocksExample";
var outputFilePath = "/path/where/you/want/to/save/file/";
var headerFormat = "wav";   // or many others

// Block design:
var beginSilence = 5;       // seconds of silence at start (baseline estimate)
var pluckBlockDur = 15;     // seconds of plucking blocks
var silenceBlockDur = 15;   // seconds of silence between plucking blocks
var numRepeats = 10;        // how many pluck-silence block pairs
var endSilence = 5;         // seconds of silence at end (baseline estimate)

// Sound properties:
var pluckRate = 2;          // pluck (and therefore tapping) speed in Hz
var decay = 3;              // decay time for each pluck
var freq = 675;             // sound frequency in Hz
var amp = 0.95;             // amplitude

// Computed variables:
var dur = 1 / pluckRate;    // time between plucks
var plucksPerBlock, scoreEvents, time, nodeID, score, totalDuration;


// MAIN SECTION:

// SYNTHDEF. Tweak sounds for audibility over scanner noise. Test w/ someone in there while seq runs!
SynthDef(\pluck, {
    arg freq = 440, amp = 0.8, decay = 2;
    var trig = 1;
    var sig, env, noise;

    noise = Mix([
        PinkNoise.ar(0.2),
        WhiteNoise.ar(0.15),
        LFNoise1.ar(8000).range(-0.15, 0.15)
    ]);
    // Mix different plucks for desired timbre and envelope
    sig = Mix([
        Pluck.ar(
            noise,
            trig,
            maxdelaytime: 0.1,
            delaytime: freq.reciprocal,
            decaytime: 4,
            coef: 0.25
        ),
        Pluck.ar(
            noise * 0.7,
            trig,
            maxdelaytime: 0.1,
            delaytime: (freq * 1.5).reciprocal,
            decaytime: 3,
            coef: 0.3
        ),
        Pluck.ar(
            noise * 0.5,
            trig,
            maxdelaytime: 0.1,
            delaytime: (freq * 2.01).reciprocal,
            decaytime: 2.5,
            coef: 0.35
        )
    ]);
    env = EnvGen.kr(Env.perc(0.01, decay), doneAction: 2);
    sig = sig * env * amp * 3;
    sig = Limiter.ar(sig, 0.995);  // no clipping
    Out.ar(0, sig ! 2);
}).store;  // write to disk

// BUILD SCORE EVENTS
plucksPerBlock = (pluckBlockDur / dur).floor.asInteger;
scoreEvents = List.new;
time = 0;
nodeID = 1000;

time = time + beginSilence;

numRepeats.do({
    // Pluck block
    plucksPerBlock.do({
        scoreEvents.add([time, [\s_new, \pluck, nodeID, 0, 0,
            \freq, freq,
            \decay, decay,
            \amp, amp
        ]]);
        nodeID = nodeID + 1;
        time = time + dur;
    });

    // Silence block
    time = time + silenceBlockDur;
});

time = time + endSilence;

// Create and render score
score = Score(scoreEvents);
totalDuration = time + 2;       // short end buffer for final decay

score.recordNRT(
    outputFilePath: (outputFilePath ++ outputFileName ++ "." ++ headerFormat).standardizePath,
    headerFormat: headerFormat,
    sampleFormat: "int24",      // or, e.g., int16 for smaller files
    options: ServerOptions.new
        .numOutputBusChannels_(2)
        .sampleRate_(44100),
    duration: totalDuration,
    action: {
        ("Rendering complete. File saved as " ++ outputFileName ++ "." ++ headerFormat).postln;
        ("Total duration: " ++ totalDuration ++ " seconds").postln;
    }
);
)
