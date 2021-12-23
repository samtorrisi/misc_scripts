#!/bin/tcsh

# Script 3. An "AFNI-ized" version of the MICE function pool()
# https://stats.stackexchange.com/questions/327237/calculating-pooled-p-values-manually
# Special thanks to Gang Chen and Justin Rajendra. 3.4.18. by ST, SNFA, NIMH 

set m = 10 # number of mice imputations
set n = 60 # number of subjects
set k = 9  # number of covariates 

foreach iter (`count -d 1 1 $m`)

	echo $iter

	# make variance maps
	3dcalc -a mi_result_${iter}+tlrc.'[0..$(2)]' -b mi_result_${iter}+tlrc.'[1..$(2)]' \
        -expr '(a/b)^2' -prefix variance${iter}

	# make beta-only maps
	3dcalc -a mi_result_${iter}+tlrc.'[0..$(2)]' -expr 'a' -prefix onlycoefs${iter}
end

# pool the coefficients (aka betas)
3dMean -prefix coefs_pooled onlycoefs*+tlrc.HEAD

# pool the variances
3dMean -prefix betweenVar variance*+tlrc.HEAD

# two step process to get within variance:
3dMean -stdev -prefix varStd variance*+tlrc.HEAD
3dcalc -a 'varStd+tlrc.' -expr 'a^2' -prefix withinVar

# maddeningly cryptic degrees of freedom correction (dfc; thanks tcsh!)
# see https://earthsci.stanford.edu/computing/unix/programming/shell/expressions.php
alias MATH 'set \!:1 = `echo "\!:3-$" | bc -l`'
MATH dfc = ($m + 1) / $m

# Total variance (double quotes interprets variables):
3dcalc -a betweenVar+tlrc. -b withinVar+tlrc. -expr "a+(b*$dfc)" -prefix totalVar

# standard error
3dcalc -a totalVar+tlrc. -expr 'sqrt(a)' -prefix pooledSE

# See pp. 37-43 in FIMD by Stef van Buuren. Lambda = proportion of total variance 
# attributable to the missing data.
3dcalc -a withinVar+tlrc. -b totalVar+tlrc. -expr "(a + (a/$m))/b" -prefix lambda

# this is the R code to obtain "k", hard-coded in line 10 above. 
# In the example with simple linear regression k=2
# k <- length(coef(lm(chl~bmi,data = complete(nhimp,1))))

# Call the adjusted degrees of freedom adf.
3dcalc -a lambda+tlrc -expr "($m-1)/(a^2)" -prefix adf_old
@ k++ # increment for intercept, also "obs" = observed
@ adf_com = ($n - $k) 
3dcalc -a lambda+tlrc -expr "(${adf_com}+1)/(${adf_com}+3)*${adf_com}*(1-a)" -prefix adf_obs 
3dcalc -a adf_old+tlrc -b adf_obs+tlrc -expr '(a*b)/(a+b)' -prefix adf_br # Barnard & Rubin '99 adf

# manually calculate T-stats
3dcalc -a coefs_pooled+tlrc -b pooledSE+tlrc -expr 'a/b' -prefix manualTs

# get Z stats from from T-stats using voxel-specific adjusted degrees of freedom
3dcalc -t manualTs+tlrc. -a adf_br+tlrc. -expr 'step(a)*fitt_t2z(t,a)' -prefix adfTsToZs_bnst

# loop through each subbrick so afni recognizes it as a Z map. 
# ignore the _mean subbricks in the final output
set vols = `3dinfo -nv adfTsToZs_bnst+tlrc.`
foreach iter (`count -d 1 0 $vols`)
	3drefit -'fizt' -substatpar $iter fizt adfTsToZs_bnst+tlrc.
end
