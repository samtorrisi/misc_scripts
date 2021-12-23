# Script 2. These bring in the text files created by
# 01_import_whittle_impute.R
# and create 'm' different group-level fMRI analyses.
# Note that the zMap_BNSTs* below are fisher-transformed BNST 
# seed resting state correlation maps. The afni_proc.py and
# correlation procedures to prep those corr maps are not shown.

set m = 10 # the number of imputations from R
foreach imputation (`count -d 1 1 ${m}`)
    3dttest++ -prefix mi_result_${imputation}  \
        -setA healthy			   \
        1 "../zMap_BNSTs_001+tlrc.HEAD[0]" \
        3 "../zMap_BNSTs_003+tlrc.HEAD[0]" \
        10 "../zMap_BNSTs_010+tlrc.HEAD[0]" \
        11 "../zMap_BNSTs_011+tlrc.HEAD[0]" \
        13 "../zMap_BNSTs_013+tlrc.HEAD[0]" \
        14 "../zMap_BNSTs_014+tlrc.HEAD[0]" \
        18 "../zMap_BNSTs_018+tlrc.HEAD[0]" \
        19 "../zMap_BNSTs_019+tlrc.HEAD[0]" \
        20 "../zMap_BNSTs_020+tlrc.HEAD[0]" \
        22 "../zMap_BNSTs_022+tlrc.HEAD[0]" \
        23 "../zMap_BNSTs_023+tlrc.HEAD[0]" \
        24 "../zMap_BNSTs_024+tlrc.HEAD[0]" \
        25 "../zMap_BNSTs_025+tlrc.HEAD[0]" \
        26 "../zMap_BNSTs_026+tlrc.HEAD[0]" \
        28 "../zMap_BNSTs_028+tlrc.HEAD[0]" \
        29 "../zMap_BNSTs_029+tlrc.HEAD[0]" \
        602 "../zMap_BNSTs_602+tlrc.HEAD[0]" \
        603 "../zMap_BNSTs_603+tlrc.HEAD[0]" \
        604 "../zMap_BNSTs_604+tlrc.HEAD[0]" \
        605 "../zMap_BNSTs_605+tlrc.HEAD[0]" \
        606 "../zMap_BNSTs_606+tlrc.HEAD[0]" \
        607 "../zMap_BNSTs_607+tlrc.HEAD[0]" \
        608 "../zMap_BNSTs_608+tlrc.HEAD[0]" \
        610 "../zMap_BNSTs_610+tlrc.HEAD[0]" \
        612 "../zMap_BNSTs_612+tlrc.HEAD[0]" \
        613 "../zMap_BNSTs_613+tlrc.HEAD[0]" \
        -setB patient			     \
        401 "../zMap_BNSTs_401+tlrc.HEAD[0]" \
        402 "../zMap_BNSTs_402+tlrc.HEAD[0]" \
        403 "../zMap_BNSTs_403+tlrc.HEAD[0]" \
        405 "../zMap_BNSTs_405+tlrc.HEAD[0]" \
        406 "../zMap_BNSTs_406+tlrc.HEAD[0]" \
        407 "../zMap_BNSTs_407+tlrc.HEAD[0]" \
        408 "../zMap_BNSTs_408+tlrc.HEAD[0]" \
        409 "../zMap_BNSTs_409+tlrc.HEAD[0]" \
        410 "../zMap_BNSTs_410+tlrc.HEAD[0]" \
        411 "../zMap_BNSTs_411+tlrc.HEAD[0]" \
        412 "../zMap_BNSTs_412+tlrc.HEAD[0]" \
        414 "../zMap_BNSTs_414+tlrc.HEAD[0]" \
        416 "../zMap_BNSTs_416+tlrc.HEAD[0]" \
        417 "../zMap_BNSTs_417+tlrc.HEAD[0]" \
        418 "../zMap_BNSTs_418+tlrc.HEAD[0]" \
        419 "../zMap_BNSTs_419+tlrc.HEAD[0]" \
        420 "../zMap_BNSTs_420+tlrc.HEAD[0]" \
        421 "../zMap_BNSTs_421+tlrc.HEAD[0]" \
        422 "../zMap_BNSTs_422+tlrc.HEAD[0]" \
        423 "../zMap_BNSTs_423+tlrc.HEAD[0]" \
        424 "../zMap_BNSTs_424+tlrc.HEAD[0]" \
        425 "../zMap_BNSTs_425+tlrc.HEAD[0]" \
        427 "../zMap_BNSTs_427+tlrc.HEAD[0]" \
        428 "../zMap_BNSTs_428+tlrc.HEAD[0]" \
        429 "../zMap_BNSTs_429+tlrc.HEAD[0]" \
        431 "../zMap_BNSTs_431+tlrc.HEAD[0]" \
        -mask all60gmMask+tlrc. -covariates imputedDataset${imputation}.txt -center SAME
end
