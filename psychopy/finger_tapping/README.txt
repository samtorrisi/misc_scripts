March 25, 2023, version 2, ST, SFVA

this is a perhaps more flexible version of the finger tapping task that Renzo Huber et al use.
see https://github.com/layerfMRI/Phychopy_git
so it's really not my task, or stimuli, just a re-packaging.

it's not TR-dependent and one can easily specify the block lengths of the tapping

in addition to a null period before the stimuli begins

there are 4 possible conditions: 
right tapping with touch, left with touch, right without touch, left without touch

also, how i converted the individual pics to movies:

#first convert to an animated gif with imagemagick:
convert -delay 12 -loop 1 left_*.png lefttaps12.gif

#then convert that to an avi format that psychopy will read:
ffmpeg -y -i lefttaps12.gif -strict -2 -an -b:v 32M lefttaps.avi

also used ezgif.com to horizontally flip the 'right without touch'

psychopy experiment was then mostly built in Builder, but with custom Python code components