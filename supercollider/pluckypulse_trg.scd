// Generate audible pulse in SuperCollider (SC) for fMRI fingertapping experiment.
// This version of script is for scanner triggering at the console. Saves a param file.
// Note: SC is an open source platform for audio synthesis and algorithmic music composition.
// Alter lines 15-24, depending on the desired experiment. Written for a scanner suite
// with audio + triggering but no video capabilities. Oct & Nov 2025, salvatore.torrisi@ucsf.edu

// FIRST, SELECT AND BOOT THE AUDIO ENGINE WITH THIS SINGLE LINE:
s.boot;

// SECOND, SELECT AND EXECUTE THE REST OF THE CODE:
(
// USER CONFIGS - modify these experiment parameters:

// Block design:
var beginSilence = 5;       // seconds of silence at start (baseline)
var pluckBlockDur = 15;     // seconds of plucking blocks
var silenceBlockDur = 15;   // seconds of silence between plucking blocks
var numRepeats = 10;        // how many pluck-silence block pairs
var endSilence = 5;         // seconds of silence at end (baseline)

// Sound properties:
var pluckRate = 2;          // pluck (and therefore tapping) speed in Hz
var decay = 3;              // decay time for each pluck
var freq = 675;             // sound frequency in Hz
var amp = 0.95;             // amplitude

// Computed variables:
var dur = 1 / pluckRate;    // time between plucks
var plucksPerBlock = (pluckBlockDur / dur).floor.asInteger;
var timestamp, filename, filepath, file, paramString, docDir;


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
    sig = Limiter.ar(sig, 0.995); // no clipping
    Out.ar(0, sig ! 2);
}).add;

// Flag to track if experiment is running (instantiate sounds once)
~experimentRunning = false;

// Define experiment design and set up keyboard capture
~playBlockDesign = {
    ~experimentRunning = true;
    "Experiment started - ignoring further triggers".postln;

    timestamp = Date.getDate;
    filename = "%_%_%_%_pluckyExp.txt".format(
        timestamp.year.asString ++ timestamp.month.asString.padLeft(2, "0") ++ timestamp.day.asString.padLeft(2, "0"),
        timestamp.hour.asString.padLeft(2, "0"),
        timestamp.minute.asString.padLeft(2, "0"),
        timestamp.second.asString.padLeft(2, "0")
    );

    docDir = Document.current.path.dirname;
    filepath = docDir +/+ filename;

    paramString = "Plucky Experiment Parameters\n" ++
    "============================\n" ++
    "Date: %-%-% \n".format(timestamp.year, timestamp.month.asString.padLeft(2, "0"), timestamp.day.asString.padLeft(2, "0")) ++
    "Time: %:%:% \n".format(timestamp.hour.asString.padLeft(2, "0"), timestamp.minute.asString.padLeft(2, "0"), timestamp.second.asString.padLeft(2, "0")) ++
    "\nBlock Design Parameters:\n" ++
    "beginSilence: % seconds\n".format(beginSilence) ++
    "pluckBlockDur: % seconds\n".format(pluckBlockDur) ++
    "silenceBlockDur: % seconds\n".format(silenceBlockDur) ++
    "numRepeats: % \n".format(numRepeats) ++
    "endSilence: % seconds\n".format(endSilence) ++
    "\nSound Parameters:\n" ++
    "pluckRate: % Hz\n".format(pluckRate) ++
    "dur: % seconds\n".format(dur) ++
    "decay: % \n".format(decay) ++
    "freq: % Hz\n".format(freq);

    // Write info to a file to keep a record, esp. useful during acq devel at console
	// (e.g. for "methods labs" where things change dynamically).
    try {
        file = File(filepath, "w");
        file.write(paramString);
        file.close;
        "Parameters saved to: %".format(filepath).postln;
    } {
        "ERROR: Could not write parameter file to %".format(filepath).postln;
    };

    // THE MAIN PART:
    Routine({
        beginSilence.wait;
        numRepeats.do({
            plucksPerBlock.do({
                Synth(\pluck, [
                    \freq, freq,
                    \decay, decay,
                    \amp, amp
                ]);
                dur.wait;
            });
            silenceBlockDur.wait;
        });
        endSilence.wait;
        "Block design complete".postln;
        ~experimentRunning = false;
        "Ready for next trigger".postln;
    }).play;
};

// Create window to capture keyboard input
~triggerWindow = Window("fMRI Trigger Listener", Rect(100, 100, 450, 180)).front.alwaysOnTop_(true);

~triggerWindow.view.keyDownAction = { |view, char, modifiers, unicode, keycode|
    if((char == $t) || (char == $5), {
        if(~experimentRunning, {
            "Trigger ignored - experiment already running".postln;
        }, {
            "First trigger received: '%' - Starting block design...".format(char).postln;
            ~playBlockDesign.value;
        });
    });
};

StaticText(~triggerWindow, Rect(20, 20, 410, 140))
    .string_("Ready to receive triggers.\n\nListening for 't' or '5'.\n\nCommand+. to stop audio")
    .align_(\center)
    .font_(Font("Arial", 18));

~triggerWindow.onClose = {
    "Trigger window closed. Keyboard listening stopped.".postln;
};

"Setup complete".postln;
"Trigger window is open and listening for 't' or '5'".postln;
"Keep the window in focus to receive scanner triggers".postln;
"Command+. to stop audio playback".postln;
)
