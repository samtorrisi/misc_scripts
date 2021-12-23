# For creating multiple 3dttest++ analyses in AFNI,
# for calculating brain-behavior correlations when the correlations contain missing data.
# Initially inspired by R. Kabacoff, 2nd ed. Chpt 18
# Written for and used in https://pubmed.ncbi.nlm.nih.gov/30964612/
# Executing this script is followed by executing two more:
# 02_mice_cov_bnst.csh and 03_after3dttest_bnst.txt
# by ST, SNFA, NIMH, February 2018

library("graphics")
library("corrplot")
library("VIM")
library("mice")

setwd("/Users/torrisisj/Desktop/NIMH_LAB/7T_2_patientRS_SART7T/7T_patient/Multiple_Imputation")
hugematrix <- read.csv(file="7TPTrest_questionnaires_forR2.csv", header=TRUE, sep=",")
m <- 10 # number of imputations
subjnames <- c(001, 002, 003, 010, 011, 012, 013, 014, 017, 018, 019, 020, 022, 023, 024, 025, 026, 
	028, 029, 602, 603, 604, 605, 606, 607, 608, 610, 611, 612, 613, 401, 402, 403, 404, 405, 406, 
	407, 408, 409, 410, 411, 412, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 
	427, 428, 429, 431, 432)

# A priori variable removal (reasons):
# 1: subject IDs (meaningless)
# 4: STAI.state_post (no experiment anticipation)
# 5,6: Liebowitz anxiety/fear & avoidance (collinear with total)
# 13: life events (measure is more for post traumatic stress disorder)
# 16,17: MASQ_GDD/MASQ_AD (measures are more for depression) 
# 18-20: BIS.BAS: Drive, Fun Seeking, Reward Responsiveness (not anxiety relevant)
# 22: MPQ_HA harm avoidance (historically in SNFA an unclear relation / helpfulness)
# 25,26: ACS_Focusing, ACS_Shifting (collinear with Attention Control Scale total)
bigmatrix <- hugematrix[, -c(1, 4, 5, 6, 13, 16, 17, 18, 19, 20, 22, 25, 26)]

# remove BDI because >15% threshold for missingness. remove more for use with 3dttest++ or 3dMVM
#smallerMatrix <- subset(bigmatrix, select= -c(BDI, STAI.statepre, HH.SES, Self, Health_Concern, 
#Somatic_Awareness, Planning, Visual_Thought, Sleepiness, WASI..IQ., Comfort, ASI, Theory_of_Mind))
smallerMatrix <- subset(bigmatrix, select= -c(MASQ_GDA, BIS.BAS_BIS, TF20, Trait, BDI, 
	STAI.statepre, HH.SES, Self, Health_Concern, Planning, Visual_Thought, Sleepiness, WASI..IQ., 
	Comfort, ASI, Theory_of_Mind))

# correlation matrix with complete cases
onlyCompleteMtx <- cor(na.omit(smallerMatrix))
corrplot(onlyCompleteMtx, method = "number", title = "Complete Cases", mar=c(0,0,1,0), 
	tl.col = "black", tl.srt =45, tl.cex = 0.7, cl.ratio=0.18)

# print quick summary:
complt <- smallerMatrix[complete.cases(smallerMatrix),]
cat("complete cases =", nrow(complt), "of", nrow(smallerMatrix), "\n")
whole <- nrow(complt)
part <- nrow(smallerMatrix)

# for the plot to match an Excel spreadsheet, vertically flip it
bmFlip <- as.data.frame(apply(smallerMatrix, 2, rev))
matrixplot(bmFlip, main = bquote(paste("complete cases: ", .(whole), " of ", .(part))), 
	ylab = "subjects (top half hv)", cex.axis=0.6)
aggr(smallerMatrix, prop = TRUE, numbers=TRUE, cex.axis=0.4)

# Check if missing data are MCAR or MAR. Many ways to do so, e.g. using VIM's marginplot() with 
# variable pairs. Proceed to impute. Default for continuous variables is predictive mean matching 
# (Little, 1998), "..a general purpose semi-parametric imputation method." (van Buuren et al 2011):
imp <- mice(smallerMatrix, m = m, maxit = 20)

# see what it did
bwplot(imp)
densityplot(imp)

# imputed datasets written for 3dttest++. Manually add "SUBJ" at top left of these outputs
for(i in 1:m) 
  write.table(complete(imp, action = i), file = paste0('imputedDataset',i,'.txt'), 
	row.names = subjnames, quote = FALSE, sep="\t")
