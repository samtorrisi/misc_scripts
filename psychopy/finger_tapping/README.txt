December 19, 2023, version 4, ST, SFVA

this is a perhaps more flexible version of the finger tapping task that Renzo Huber et al have used.
see https://github.com/layerfMRI/Phychopy_git
so it's really not my task, or stimuli, just a re-packaging.

it's not TR-dependent and one can easily specify the block lengths of the tapping with an initial dialogue box

one can also specify a null period before the stimuli begins

these parameters are also saved for every experiment, along with other data, in a .csv

also, if one a button box is used the experimenter can keep tabs on subject performance and give between-run feedback or decide whether to re-run anything. summary counts of finger taps are printed in the psychopy stdout window at the end of each run.

finally there are 4 possible conditions: 
right tapping with touch, left with touch, right without touch, left without touch
although the last 2 don't make sense with button pushing...

just fyi, how i converted the original pics to movies:
#first convert to an animated gif with imagemagick:
convert -delay 12 -loop 1 left_*.png lefttaps12.gif
#then convert that to an avi format that psychopy will read:
ffmpeg -y -i lefttaps12.gif -strict -2 -an -b:v 32M lefttaps.avi
#i also used ezgif.com to horizontally flip the 'right without touch'

the PsychoPy experiment was built in Builder, but with custom code components
