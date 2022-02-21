#!/bin/tcsh

#title           :ssAlign.sh
#description     :skull-strips and aligns multiple images
#author          :ST, for J Stockmann
#date            :20211007
#version         :1.0
#notes           :requires AFNI
#tcsh_version    :6.21

# registers skull-stripped brains together with decent masking.
# assumes all scans are same subject + similar tissue weighting.
# for SNR comparisons, but could be used for other purposes.

foreach file (`ls -1 *.nii`)
    set base = `basename -s .nii ${file}`
    3dUnifize -prefix ${base}_uni.nii $file
    echo "skull-stripping ${base}_uni.nii ..."
    3dSkullStrip -mask_vol -prefix ${base}_mask.nii -input ${base}_uni.nii
    3dcalc -a ${base}_mask.nii -expr 'step(a-1)' -prefix ${base}_binmask.nii
    3dcalc -a $file -b ${base}_binmask.nii -expr 'a*b' -prefix ${base}_orig_ss.nii
end

# register an N number of bias-corrected brains. 
# retain the affine matrix transforms for final step
echo ""; echo "registering brains 2 through N to brain1..."; echo ""
set allfiles = (`ls -1 *_uni.nii`)

set ac = 2
while ($ac <= $#allfiles)
    set base = `basename -s .nii $allfiles[$ac]`

        3dAllineate -prefix ${base}_al.nii -1Dmatrix_save ${base}_al.1D -source_automask \
                    -cost lpa -warp shift_rotate -final wsinc5 \
                    -source $allfiles[$ac] -base $allfiles[1]
        @ ac ++
end

echo ""; echo "registering brain1 to Nth_al to match resampling"; echo ""
@ ac --
set orig = `basename -s .nii $allfiles[1]`
set orig_al = ${orig}_al.nii
set last = `basename -s .nii $allfiles[$ac]`
set last_al = ${last}_al.nii
    3dAllineate -prefix $orig_al -1Dmatrix_save ${orig}_al.1D -source_automask \
                -cost lpa -warp shift_rotate -final wsinc5 \
                -source $allfiles[1] -base $last_al

# apply matrix transforms 
# retain skull-stripped, registered images without bias-correction
echo ""; echo "applying matrix transforms:"; echo ""
foreach xfrm (`ls *.1D`)
    set root = `basename -s _uni_al.1D $xfrm`
#    3dAllineate -base ${root}_uni_al.nii -1Dmatrix_apply $xfrm \
#        -prefix final_${root}_maskreg.nii ${root}_binmask.nii
    3dAllineate -base ${root}_uni_al.nii -1Dmatrix_apply $xfrm \
        -prefix final_${root}_ssreg.nii ${root}_orig_ss.nii
end

# clean-up
rm *_mask.nii *_uni* *orig_ss.nii *binmask.nii
