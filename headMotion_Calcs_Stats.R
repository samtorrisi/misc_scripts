# script for net head motion calcs & stats across diff physical mitigators (head padding).
# dfile_rall.1D is 3dvolreg's raw, 6-param motion estimations from an afni_proc.py analysis.
# see email thread with subject "ISMRM abstract: padding comparison"
# raw data: /storage/raw/20211008AV_NOVA32_STX/VAARC_STUDYPROTOCOLS_20211008_140419_893000 (anon)
# analyses: /home/sam/Desktop/VAARC_STUDYPROTOCOLS_20211008_mocoCompare
# numbers represent: 07:caseforge1, 14:pearltec, 21:nomoco, 28:greenfoam, 35:caseforge2
# check column order w/ 1dplot.py -sepscl -prefix rawmo.jpg -ylabels VOLREG -infiles dfile_rall.1D
# cols 1:3 = roll, pitch, yaw (degs), cols 4:6 are HF, LR & AP in mm. see "-1Dfile"in 3dvolreg help

require(tidyverse)
require(data.table)
setwd("~/Desktop/Feinberg/VA_misc/OHBM_MOCO_FOR_JV")

# import caseforge1 data, calculate net motion from translation parameters, linear detrend
rawmo_cf1 <- read.table("dfile_rall_RFMRI_REST1_AP_0007.results.1D")
netmo3_cf1 <- sqrt((rawmo_cf1$V4)^2 + (rawmo_cf1$V5)^2 + (rawmo_cf1$V6)^2)
dtlm_netmo3_cf1 <- lm(netmo3_cf1 ~c(1:length(netmo3_cf1))) #detrending linear model
dtrs_netmo3_cf1 <- resid(dtlm_netmo3_cf1) #residuals of linear model (detrended time series)
matplot(rawmo_cf1[4:6], xlab = "TR = 1 second", ylab = "caseforge1 trans in mm", type = "l", 
      lty = c(1,1,1), main = "caseforge1")
legend(x = "bottomleft", legend = c("HF", "LR", "AP"), lty = c(1, 1, 1), col = c(1,2,3), lwd = 2, 
      cex = 0.6)
matplot(netmo3_cf1, xlab = "TR = 1 second", ylab = "caseforge1 net trans", type = "l", 
      main = "sqrt(a^2 + b^2 + c^2)")
plot(dtrs_netmo3_cf1, type="l", xlab = "TR = 1 second", main = 
       "caseforge1 detrended net translation")

# import pearltec data, calculate net motion from translation parameters, linear detrend
rawmo_pt <- read.table("dfile_rall_RFMRI_REST1_AP_0014.results.1D")
netmo3_pt <- sqrt((rawmo_pt$V4)^2 + (rawmo_pt$V5)^2 + (rawmo_pt$V6)^2)
dtlm_netmo3_pt <- lm(netmo3_pt ~c(1:length(netmo3_pt))) #detrending linear model
dtrs_netmo3_pt <- resid(dtlm_netmo3_pt) #residuals of linear model (detrended time series)
matplot(rawmo_pt[4:6], xlab = "TR = 1 second", ylab = "pearltec trans in mm", type = "l", 
        lty = c(1,1,1), main = "pearltec")
legend(x = "bottomleft", legend = c("HF", "LR", "AP"), lty = c(1, 1, 1), col = c(1,2,3), lwd = 2, 
       cex = 0.6)
matplot(netmo3_pt, xlab = "TR = 1 second", ylab = "pearltec net trans", type = "l", main = 
          "sqrt(a^2 + b^2 + c^2)")
plot(dtrs_netmo3_pt, type="l", xlab = "TR = 1 second", main = "pearltec detrended net translation")

# import nomoco data, calculate net motion from translation parameters, linear detrend
rawmo_nm <- read.table("dfile_rall_RFMRI_REST1_AP_0021.results.1D")
netmo3_nm <- sqrt((rawmo_nm$V4)^2 + (rawmo_nm$V5)^2 + (rawmo_nm$V6)^2)
dtlm_netmo3_nm <- lm(netmo3_nm ~c(1:length(netmo3_nm))) #detrending linear model
dtrs_netmo3_nm <- resid(dtlm_netmo3_nm) #residuals of linear model (detrended time series)
matplot(rawmo_nm[4:6], xlab = "TR = 1 second", ylab = "nomoco trans in mm", type = "l", 
        lty = c(1,1,1), main = "nomoco")
legend(x = "bottomleft", legend = c("HF", "LR", "AP"), lty = c(1, 1, 1), col = c(1,2,3), lwd = 2, 
       cex = 0.6)
matplot(netmo3_nm, xlab = "TR = 1 second", ylab = "nomoco net trans", type = "l", main = 
          "sqrt(a^2 + b^2 + c^2)")
plot(dtrs_netmo3_nm, type="l", xlab = "TR = 1 second", main = "nomoco detrended net translation")

# import green foam data, calculate net motion from translation parameters, linear detrend
rawmo_gf <- read.table("dfile_rall_RFMRI_REST1_AP_0028.results.1D")
netmo3_gf <- sqrt((rawmo_gf$V4)^2 + (rawmo_gf$V5)^2 + (rawmo_gf$V6)^2)
dtlm_netmo3_gf <- lm(netmo3_gf ~c(1:length(netmo3_gf))) #detrending linear model
dtrs_netmo3_gf <- resid(dtlm_netmo3_gf) #residuals of linear model (detrended time series)
matplot(rawmo_gf[4:6], xlab = "TR = 1 second", ylab = "greenfoam trans in mm", type = "l", 
        lty = c(1,1,1), main = "greenfoam")
legend(x = "bottomleft", legend = c("HF", "LR", "AP"), lty = c(1, 1, 1), col = c(1,2,3), lwd = 2, 
       cex = 0.6)
matplot(netmo3_gf, xlab = "TR = 1 second", ylab = "greenfoam net trans", type = "l", main = 
          "sqrt(a^2 + b^2 + c^2)")
plot(dtrs_netmo3_gf, type="l", xlab = "TR = 1 second", main = "greenfoam detrended net translation")

# import caseforge2 data, calculate net motion from translation parameters, linear detrend
rawmo_cf2 <- read.table("dfile_rall_RFMRI_REST1_AP_0035.results.1D")
netmo3_cf2 <- sqrt((rawmo_cf2$V4)^2 + (rawmo_cf2$V5)^2 + (rawmo_cf2$V6)^2)
dtlm_netmo3_cf2 <- lm(netmo3_cf2 ~c(1:length(netmo3_cf2))) #detrending linear model
dtrs_netmo3_cf2 <- resid(dtlm_netmo3_cf2) #residuals of linear model (detrended time series)
matplot(rawmo_cf2[4:6], xlab = "TR = 1 second", ylab = "caseforge2 trans in mm", type = "l", 
        lty = c(1,1,1), main = "caseforge2")
legend(x = "bottomleft", legend = c("HF", "LR", "AP"), lty = c(1, 1, 1), col = c(1,2,3), lwd = 2, 
       cex = 0.6)
matplot(netmo3_cf2, xlab = "TR = 1 second", ylab = "caseforge2 net trans", type = "l", main = 
          "sqrt(a^2 + b^2 + c^2)")
plot(dtrs_netmo3_cf2, type="l", xlab = "TR = 1 second", main = 
       "caseforge2 detrended net translation")

# one way to summarize data with info that i want, but output formatting sux. fix later
allsumsRaw <- cbind(netmo3_cf1, netmo3_pt, netmo3_nm, netmo3_gf, netmo3_cf2)
collectionorder <- c("caseforge1", "pearltec", "nomoco", "greenfoam", "caseforge2")
colnames(allsumsRaw) = collectionorder
allsumsRawdf <- as.data.frame(allsumsRaw)
allsumsRawdf %>% 
  summarise(across(everything(), list(min=min, max=max, median=median, sd=sd))) %>% 
  dplyr::mutate_if(is.numeric, round, 3)

# putting all motion params together as factor and group
params <- c("roll", "pitch", "yaw", "HF", "LR", "AP")
verticalcat <- rbindlist(list(rawmo_cf1, rawmo_pt, rawmo_nm, rawmo_gf, rawmo_cf2))
colnames(verticalcat) = params
padding <- as.data.frame(rep(collectionorder, each=298))
colnames(padding) = "padding"
alltogether <- cbind(verticalcat, padding)
alltogether %>% select(everything()) %>%
  pivot_longer(., cols = c(roll, pitch, yaw, HF, LR, AP), names_to = "motion_params", 
               values_to = "mm") %>%
  ggplot(aes(x = motion_params, y = mm, fill = padding)) +
  geom_boxplot()+
  labs(title="subject 1: raw motion")

## plot sos of xyz, counterbalance order:
#sos_title <- "subject 1 sum of squares translation parameters"
#sosbound <- as.data.frame(cbind( netmo3_cf1, netmo3_pt, netmo3_nm, netmo3_gf, netmo3_cf2))
#colnames(sosbound) = collectionorder
#forsosplot <- gather(sosbound, condition, mm, caseforge1:caseforge2, factor_key=TRUE)
#ggplot(forsosplot, aes(x = factor(condition, level=collectionorder), y=mm)) +
#  geom_boxplot() + ggtitle(sos_title) + theme(text = element_text(size=12), plot.title = 
#                                                element_text(hjust = 0.5))+ geom_boxplot()
#
## plot sos of xyz, alphabetized:
#sos_title <- "subject 1 sum of squares translation parameters"
#alphabetorder <- c("caseforge1", "caseforge2", "greenfoam", "nomoco", "pearltec")
#sosbound <- as.data.frame(cbind( netmo3_cf1, netmo3_cf2, netmo3_gf, netmo3_nm, netmo3_pt))
#colnames(sosbound) = alphabetorder
#forsosplot <- gather(sosbound, condition, mm, caseforge1:pearltec, factor_key=TRUE)
#ggplot(forsosplot, aes(x = factor(condition, level=alphabetorder), y=mm)) +
#  geom_boxplot() + ggtitle(sos_title) + theme(text = element_text(size=12), plot.title = 
#                                                element_text(hjust = 0.5))+ geom_boxplot()

# plot absolute raw 6 mo params in subj1's cb order:
absrawmo_cf1 <- abs(rawmo_cf1)
absrawmo_pt <- abs(rawmo_pt)
absrawmo_nm <- abs(rawmo_nm)
absrawmo_gf <- abs(rawmo_gf)
absrawmo_cf2 <- abs(rawmo_cf2)
vertcatabs <- rbindlist(list(absrawmo_cf1, absrawmo_pt, absrawmo_nm, absrawmo_gf, absrawmo_cf2))
colnames(vertcatabs) = params
alltogetherabs <- cbind(vertcatabs, padding)
alltogetherabs %>% select(everything()) %>%
  pivot_longer(., cols = c(roll, pitch, yaw, HF, LR, AP), names_to = "motion_params", 
               values_to = "mm_or_deg") %>%
  ggplot(aes(x = motion_params, y = mm_or_deg, fill = padding)) +
  geom_boxplot()+
  labs(title="subject 1: absolute (rectified) raw motion")

# demean raw and then absolute the 6 mo params in subj1's cb order:
demn_rawmo_cf1 <- rawmo_cf1 - colMeans(rawmo_cf1)
abs_demn_rawmo_cf1 <- abs(demn_rawmo_cf1)

demn_rawmo_pt <- rawmo_pt - colMeans(rawmo_pt)
abs_demn_rawmo_pt <- abs(demn_rawmo_pt)

demn_rawmo_nm <- rawmo_nm - colMeans(rawmo_nm)
abs_demn_rawmo_nm <- abs(demn_rawmo_nm)

demn_rawmo_gf <- rawmo_gf - colMeans(rawmo_gf)
abs_demn_rawmo_gf <- abs(demn_rawmo_gf)

demn_rawmo_cf2 <- rawmo_cf2 - colMeans(rawmo_cf2)
abs_demn_rawmo_cf2 <- abs(demn_rawmo_cf2)

vertcat_abs_demn <- rbindlist(list(abs_demn_rawmo_cf1, abs_demn_rawmo_pt, abs_demn_rawmo_nm, 
                                   abs_demn_rawmo_gf, abs_demn_rawmo_cf2))
colnames(vertcat_abs_demn) = params
alltogetherdemnabs <- cbind(vertcat_abs_demn, padding)
alltogetherdemnabs %>% select(everything()) %>%
  pivot_longer(., cols = c(roll, pitch, yaw, HF, LR, AP), names_to = "motion_params", 
               values_to = "mm_or_deg") %>%
  ggplot(aes(x = motion_params, y = mm_or_deg, fill = padding)) +
  geom_boxplot()+ theme(text = element_text(size=15)) +
  labs(title="subject 1: demeaned & absolute (rectified) motion")

# plot sos of xyz, alphabetized order and also demeaned before sos'ing:
demn_rawmo_cf1 <- rawmo_cf1 - colMeans(rawmo_cf1)
demn_netmo3_cf1 <- sqrt((demn_rawmo_cf1$V4)^2 + (demn_rawmo_cf1$V5)^2 + (demn_rawmo_cf1$V6)^2)
demn_rawmo_pt <- rawmo_pt - colMeans(rawmo_pt)
demn_netmo3_pt <- sqrt((demn_rawmo_pt$V4)^2 + (demn_rawmo_pt$V5)^2 + (demn_rawmo_pt$V6)^2)
demn_rawmo_nm <- rawmo_nm - colMeans(rawmo_nm)
demn_netmo3_nm <- sqrt((demn_rawmo_nm$V4)^2 + (demn_rawmo_nm$V5)^2 + (demn_rawmo_nm$V6)^2)
demn_rawmo_gf <- rawmo_gf - colMeans(rawmo_gf)
demn_netmo3_gf <- sqrt((demn_rawmo_gf$V4)^2 + (demn_rawmo_gf$V5)^2 + (demn_rawmo_gf$V6)^2)
demn_rawmo_cf2 <- rawmo_cf2 - colMeans(rawmo_cf2)
demn_netmo3_cf2 <- sqrt((demn_rawmo_cf2$V4)^2 + (demn_rawmo_cf2$V5)^2 + (demn_rawmo_cf2$V6)^2)
sos_title <- "subject 1 sos translation parameters, demeaned"
alphabetorder <- c("caseforge1", "caseforge2", "greenfoam", "nomoco", "pearltec")
sosbound <- as.data.frame(cbind(demn_netmo3_cf1, demn_netmo3_cf2, demn_netmo3_gf, demn_netmo3_nm, 
                                demn_netmo3_pt))
colnames(sosbound) = alphabetorder
forsosplot <- gather(sosbound, condition, mm, caseforge1:pearltec, factor_key=TRUE)
ggplot(forsosplot, aes(x = factor(condition, level=alphabetorder), y=mm)) +
  geom_boxplot() + ggtitle(sos_title) + theme(text = element_text(size=15), plot.title = 
                                                element_text(hjust = 0.5))+ geom_boxplot()