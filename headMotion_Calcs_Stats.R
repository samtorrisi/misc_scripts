# script for net head motion calcs & stats across diff physical mitigators (head padding).
# dfile_rall*.1D is 3dvolreg's 6-param motion estimations from an afni_proc analysis (1 run per condition)
# abbreviations are caseforge1 (CF1), pearltec (PTC), nomoco (NOM), greenfoam (GRN), caseforge2 (CF2)
# check column order w/ 1dplot.py -sepscl -prefix rawmo.jpg -ylabels VOLREG -infiles dfile_rall.1D
# cols 1:3 are roll, pitch, yaw in degrees, cols 4:6 are HF, LR and AP in mm. see "-1Dfile"in 3dvolreg
# refactored May, 2022. now no siemens numbers in files or naming and padorder during loops is arbitrary 

require(tidyverse)
require(data.table)
setwd("padding_motion/S001_andS002_andScripts_OHBM_MOCO")

subs <- c("001", "002", "003", "004", "005")
subs <- formatC(subs, width = 2, format = "d", flag = "0")            #keep leading 0s
padorder <- c("pearltec", "nomoco", "greenfoam")
padorderacryn <- c("PTC", "NOM", "GRN")

stdSosMtx <- matrix(nrow = length(subs), ncol = length(padorder))     #std of sos of 3 trans
params <- c("roll", "pitch", "yaw", "HF", "LR", "AP")
pads6params <- matrix(nrow = length(subs)*length(padorder), ncol = 6) # 6 motion params
padding <- vector(mode="character", length=length(subs)*length(padorder))
sr = 0 #subject x condition iterable

# loop through subjects 
for (s in 1:length(subs)){
  
  # loop through paddings
  for (i in 1:length(padorder)){
      rawmo <- read.table(paste0("dfile_rall_SUB", subs[s], "_RFMRI_AP_", padorderacryn[i], ".results.1D"))
      
      sr=sr+1 
      #calculate and plot individual metrics
      netmo3 <- sqrt((rawmo$V4)^2 + (rawmo$V5)^2 + (rawmo$V6)^2)      # 3 translation parameters
      dt_lm_netmo3 <- lm(netmo3 ~c(1:length(netmo3)))                 # linear model
      dt_rs_netmo3 <- resid(dt_lm_netmo3)                             # residuals (detrended time series)

      matplot(rawmo[4:6], xlab="TR = 1 second", ylab="trans in mm", type = "l", lty = c(1,1,1), main = paste0("sub", subs[s], ": ", padorder[i]))
      legend(x = "bottomleft", legend = c("HF", "LR", "AP"), lty = c(1, 1, 1), col = c(1,2,3), lwd = 2, cex = 0.6)
      matplot(netmo3, xlab = "TR = 1 second", main = paste0("sub", subs[s], ": ", padorder[i]," net trans"), type = "l", ylab = "sqrt(a^2 + b^2 + c^2)")
      plot(dt_rs_netmo3, type="l", xlab = "TR = 1 second", ylab = "sqrt(a^2 + b^2 + c^2)", main = paste0("sub", subs[s], ": ", padorder[i], " detrend net trans"))

      #keep metrics for group-level stats:
      
      #for group-level version of orig abstract's Fig 1A. standard dev of all 6 motion parameters, demeaned
      rawmo_dm <- rawmo - colMeans(rawmo)
      pads6params[sr,] <- apply(rawmo_dm,2,sd) #each row a per subj x condition list of 6 motion param standard devs
      padding[sr] <- padorder[i]
      
      #for group-level version of orig abstract's Fig 1B. standard dev of motion made by demeaning before sum-of-squaring
      netmo3 <- sqrt((rawmo_dm$V4)^2 + (rawmo_dm$V5)^2 + (rawmo_dm$V6)^2)
      stdSosMtx[s,i] <- sd(netmo3)
  }
} 

#FOR GROUP-LEVEL FIGURE 1A (6 motion params)
sos_title <- "standard devs of sos, small group"
colnames(pads6params) = params
pads6paramsdf <- as.data.frame(pads6params)
alltogether <- cbind(pads6paramsdf, padding)
alltogether %>% select(everything()) %>%
  pivot_longer(., cols = c(roll, pitch, yaw, HF, LR, AP), names_to = "motion_params", values_to = "mm_or_deg") %>%
  ggplot(aes(x = motion_params, y = mm_or_deg, fill = padding)) +
  scale_fill_manual(values=c("#32a852", "#6173c7", "#d186b6")) +
  labs(title="std of demeaned motion parameters")+
  geom_boxplot(outlier.shape = NA) + 
  theme(text = element_text(size=15), legend.position = c(0.9,0.86)) +
  geom_point(position=position_jitterdodge(jitter.width = 0.05), alpha = 0.3)

#FOR GROUP-LEVEL FIGURE 1B (sum of squares standard deviations):
colnames(stdSosMtx) = padorder
rownames(stdSosMtx) = subs
sos_title <- "standard devs of sos, small group"
order <- c("pearltec", "nomoco", "greenfoam")
stdSosMtxdf <- as.data.frame(stdSosMtx)
# replaced gather() with pivot_longer():
pivot_longer(stdSosMtxdf, cols = all_of(order), names_to = "padding", values_to = "mm_std") %>%
  ggplot(., aes(x = padding, y=mm_std, fill=padding)) +
  geom_boxplot(outlier.shape = NA) + ggtitle(sos_title) + 
  scale_fill_manual(values=c("#32a852", "#6173c7", "#d186b6")) +
  geom_jitter(width = 0.2) +
  theme(text = element_text(size=15), legend.position = c(0.9,0.86))

#do some simple stats:
stdSosMtxTibb <- pivot_longer(stdSosMtxdf, cols = all_of(order), names_to = "padding", values_to = "mm_std")
summary(aov(mm_std ~ padding, data=stdSosMtxTibb)) # ANOVA not sig
nequals4 <- stdSosMtxdf[c(1:2,4:5),] #check without outlier sub003
stdSosMtxTibbN4 <- pivot_longer(nequals4, cols = all_of(order), names_to = "padding", values_to = "mm_std")
summary(aov(mm_std ~ padding, data=stdSosMtxTibbN4)) # ANOVA not sig
kruskal.test(mm_std ~ padding, data = stdSosMtxTibb) # non-parametric test not sig

#FOR GROUP-LEVEL FIGURE 2 (before and after smoothing estimates)
fwhm_data <- read.table("allFWHMs_clean.txt", header = TRUE)
fwhm_datadf <- as.data.frame(fwhm_data)
smoothness <- factor(fwhm_datadf$moco, levels = c("before", "after"))
fwhm_title <- "fwhm (mm) before and after motion correction"
ggplot(fwhm_datadf, aes(x=padding, y=combined_fwhm, fill=smoothness)) +
  scale_fill_manual(values=c("#fcba03", "#c29653")) +
  geom_boxplot(outlier.shape = NA) + ggtitle(fwhm_title) + 
  theme(text = element_text(size=15), legend.position = c(0.9,0.86)) +
  geom_point(position=position_jitterdodge())
