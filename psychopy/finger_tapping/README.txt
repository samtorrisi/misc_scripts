December 19, 2023, version 4, ST, SFVA

this is perhaps a more flexible version of the finger tapping task that Renzo Huber et al have used.
see https://github.com/layerfMRI/Phychopy_git
so it's really not my task or stimuli, more a re-packaging.

it's not TR-dependent and one can easily specify the block lengths of the tapping with an initial dialogue box

one can also specify a null period before the stimuli begins

these parameters are also saved for every experiment, along with other data, in a .csv

also, if a button box is used (and note the text displayed at the start), the experimenter can monitor subject performance and give feedback or decide whether to re-run anything. to enable this, summary counts of finger taps are printed in the PsychoPy stdout window at the end of each run.

finally there are 4 possible conditions: 
right tapping with touch, left with touch, right without touch, left without touch
although the last 2 don't make a ton of sense with button pushing...

how i converted the original pics to movies:
#first convert to an animated gif with imagemagick:
convert -delay 12 -loop 1 left_*.png lefttaps12.gif
#then convert that to an avi format that PsychoPy will read:
ffmpeg -y -i lefttaps12.gif -strict -2 -an -b:v 32M lefttaps.avi
#i also used ezgif.com to horizontally flip the 'right without touch'

the PsychoPy experiment was built in Builder, but with custom code components
