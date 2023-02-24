library(MGDrivE)
library(doParallel)
library(foreach)
# ###VARIABLE IMPORTING####
args = commandArgs(trailingOnly=TRUE)
days_egg <<- as.numeric(args[1])
days_larvae <<- as.numeric(args[2])
days_pupae <<- as.numeric(args[3])
eggs_per_mother <<- as.numeric(args[4])
pop_growth_rate <<- as.numeric(args[5])
rate_of_death_per_day <<- as.numeric(args[6])
nRep <<- as.numeric(args[7])
tmax <<- as.numeric(args[8])
ad_pop_eq <<- as.numeric(args[9])
mate_comp <<- as.numeric(args[10])
lifespan_red <<- as.numeric(args[11])
batch_migration <<- as.numeric(args[12])
multiprocessing <<- as.numeric(args[13])
default_bioparms <<- as.numeric(args[14])
default_sim <<- as.numeric(args[15])
rel_start <<- as.numeric(args[16])
rel_num <<- as.numeric(args[17])
rel_int <<- as.numeric(args[18])
rel_prop <<- as.numeric(args[19])
outfolder <<- as.character(args[20])
wd <<- as.character(args[21])
wd2 = setwd(wd)
x = 1

####TESTING BRANCH####

# days_egg = 5
# batch_migration = 1
# days_larvae =6
# days_pupae = 4
# eggs_per_mother = 20
# pop_growth_rate = 1.175
# rate_of_death_per_day = .09
# nRep = 2
# tmax = 700
# ad_pop_eq = 2000
# mate_comp = .75
# lifespan_red = .75
# bm = 0
# multiprocessing = 0
# default_bioparms = 0
# rel_start = 0
# rel_num = 10
# rel_int = 20
# rel_prop = 200
# #outFolder = "Staging Branch3"
# rel_patches = 0


###PRINT OUT####
# cat("days_egg", days_egg, "\n")
# cat("days larv 1:", days_larvae, "\n")
# cat("days pup 2:", days_pupae, "\n")
# cat("eggs per:", eggs_per_mother, "\n")
# cat("rate death", rate_of_death_per_day, "\n")
# cat("number Reps", nRep, "\n")
# cat("tmax", tmax, "\n")
# cat("ad_pop", ad_pop_eq, "\n")
# cat("matecomp", mate_comp, "\n")
# cat("lifespan_red", lifespan_red, "\n")
# cat("batch", batch_migration, "\n")
# cat("multicore", multiprocessing, "\n")
# cat("default_bioparm", default_bioparms, "\n")
# cat("rel start", rel_start, "\n")
# cat("rel Num", rel_num, "\n")
# cat("rel int", rel_int, "\n")
# cat("rel Prop", rel_prop, "\n")
# cat("outfolder =", outfolder, "\n")
# cat("Rel_patches", rel_patches, "\n")
# cat("Working Directory", wd2, "\n")

####IF CONDITIONALS####
if (batch_migration ==1){
  bm = .25
}else{
  bm = .0000001
}

if(default_bioparms ==1){
  days_egg = 2
  days_pupae =1
  days_larvae = 5
  pop_growth_rate = 1.175
  rate_of_death_per_day = .09
}


if(multiprocessing ==1){
  numCores = detectCores()
  cl <- makeCluster(numCores)
  registerDoParallel(cl)
}

if(default_sim ==1){
  nRep=2
  tmax = 365*4
  ad_pop_eq =2000
  mate_comp = .25
  lifespan_red = .75
}

outFolder <- outfolder
dir.create(path = outFolder)


folderNames <- file.path(outFolder,
                         formatC(x = 1:nRep, width = 3, format = "d", flag = "0"))

tMax <- tmax

# entomological parameters
bioParameters <- list(betaK=eggs_per_mother, tEgg=days_egg, tLarva=days_larvae, tPupa=days_pupae, popGrowth=pop_growth_rate, muAd=rate_of_death_per_day)




#### BY HAND NODES####
lat_longs <- matrix(data = c(-17.014905170964997, -149.59148774424466,
                             -17.01586274460393, -149.58869593704335,
                             -17.016210951985624, -149.58948492603503,
                             -17.016762279015463, -149.58956079036113,
                             -17.016805804764452, -149.590091840644,
                             -17.016776787599582, -149.59048633513981,
                             -17.016544650118693, -149.58956079036113,
                             -17.01650112430898, -149.58998563058742,
                             -17.01628349510862, -149.58971251901337,
                             -17.01628349510862, -149.58974286474384,
                             -17.01626898648627, -149.58995528485698,
                             -17.01673326184384, -149.59116911407492,
                             -17.022076627843923, -149.59006906292683,
                             -17.021076389504838, -149.5919305159538,
                             -17.02295888491605, -149.591812498759,
                             -17.022712674058514, -149.5922201945228,
                             -17.02238952181641, -149.5924669577483,
                             -17.022276674866635, -149.59286392468064,
                             -17.022148439616426, -149.59315360325314,
                             -17.02210740431829, -149.59346473949395,
                             -17.022092016079853, -149.59377587579877,
                             -17.02223051018639, -149.59437132619067,
                             -17.02254340390368, -149.59490240355544,
                             -17.02265112129115, -149.5952189042142,
                             -17.022892202838406, -149.59541738767817,
                             -17.022379263003568, -149.59562123556006,
                             -17.022112533733832, -149.5957070662472,
                             -17.023287165553153, -149.5958143546061,
                             -17.02322561297712, -149.59600747365212,
                             -17.022851167703358, -149.59622741478788,
                             -17.0224869804855, -149.5963829829083,
                             -17.022204863139446, -149.59635616081854,
                             -17.021897098276906, -149.59627033013143,
                             -17.021614980041633, -149.59625960129554,
                             -17.021317473078277, -149.59623814362376,
                             -17.02099431842708, -149.59623277920582,
                             -17.020742975534837, -149.59618449944432,
                             -17.02044732328236, -149.5962076407307,
                             -17.02019085019028, -149.59612717446154,
                             -17.019939506219064, -149.59600915726676,
                             -17.019734327201856, -149.59581067380051,
                             -17.019513759523626, -149.59561755475448,
                             -17.019267544125643, -149.59537615594397,
                             -17.019098270857366, -149.5951293927185,
                             -17.018621227175423, -149.5947163325258,
                             -17.018416046728156, -149.5944910269721,
                             -17.018169829889764, -149.59434082326712,
                             -17.017009476322098, -149.59100800913154,
                             -17.01710740911379, -149.59090179907497,
                             -17.017152748351855, -149.5907671398961,
                             -17.01726700318308, -149.5905888587297,
                             -17.017145494074494, -149.59052627066066,
                             -17.017013103463437, -149.59060213498677,
                             -17.01694056062315, -149.59074058738193,
                             -17.016880712758756, -149.59084679743853,
                             -17.01757963769141, -149.59194615137585,
                             -17.017790011132625, -149.59127095887337,
                             -17.017897011326685, -149.59139992822776,
                             -17.01630138691243, -149.5917017974789,
                             -17.016227030218097, -149.5914666180679,
                             -17.016167182124967, -149.5905846952668,
                             -17.015927789557697, -149.59055814274805),
                    nrow = 62, ncol = 2, byrow = TRUE,
                    dimnames = list(NULL, c('Lat','Lon')))

distMat <- MGDrivE::calcVinEll(latLongs = lat_longs)



p0 <- 0.991
rate <- 1/55.5

moveMat <- MGDrivE::calcHurdleExpKernel(distMat = distMat, rate = rate, p0 = p0)


sitesNumber <- nrow(moveMat)

adpopreal = ad_pop_eq/sitesNumber
adultPopEquilibrium <- c(adpopreal)


paramCombo <- as.matrix(expand.grid("matingComp" = seq.int(from = mate_comp-1, to = mate_comp-1, by = 0.00)) )


oRed <- MGDrivE::calcOmega(mu = bioParameters$muAd,
                           lifespanReduction = lifespan_red)

cube <- MGDrivE::cubeRIDL(xiF = c("WR"=0, "RR"=0),
                          eta = list(c("WR", 1+paramCombo[[x,'matingComp']]),
                                     c("RR", 1+paramCombo[[x,'matingComp']])),
                          omega = c("WR"=oRed, "RR"=oRed))


patchReleases <- replicate(n=sitesNumber,
                           expr={list(maleReleases=NULL,femaleReleases=NULL,
                                      eggReleases=NULL,matedFemaleReleases=NULL)},
                           simplify=FALSE)


releasesParameters <- list(releasesStart=rel_start,
                           releasesNumber=rel_num,
                           releasesInterval=rel_int,
                           releaseProportion=rel_prop)

# generate male release vector
maleReleasesVector <- generateReleaseVector(driveCube=cube,
                                            releasesParameters=releasesParameters)


# put releases into the proper place in the release list

patchReleases[[1]]$maleReleases <- maleReleasesVector
patchReleases[[2]]$maleReleases <- maleReleasesVector
patchReleases[[3]]$maleReleases <- maleReleasesVector
patchReleases[[4]]$maleReleases <- maleReleasesVector
patchReleases[[5]]$maleReleases <- maleReleasesVector
patchReleases[[6]]$maleReleases <- maleReleasesVector
patchReleases[[7]]$maleReleases <- maleReleasesVector
patchReleases[[8]]$maleReleases <- maleReleasesVector
patchReleases[[9]]$maleReleases <- maleReleasesVector
patchReleases[[10]]$maleReleases <- maleReleasesVector
patchReleases[[11]]$maleReleases <- maleReleasesVector
patchReleases[[12]]$maleReleases <- maleReleasesVector
patchReleases[[13]]$maleReleases <- maleReleasesVector
patchReleases[[14]]$maleReleases <- maleReleasesVector
patchReleases[[15]]$maleReleases <- maleReleasesVector
patchReleases[[16]]$maleReleases <- maleReleasesVector
patchReleases[[17]]$maleReleases <- maleReleasesVector
patchReleases[[18]]$maleReleases <- maleReleasesVector
patchReleases[[19]]$maleReleases <- maleReleasesVector
patchReleases[[20]]$maleReleases <- maleReleasesVector
patchReleases[[21]]$maleReleases <- maleReleasesVector
patchReleases[[22]]$maleReleases <- maleReleasesVector
patchReleases[[23]]$maleReleases <- maleReleasesVector
patchReleases[[24]]$maleReleases <- maleReleasesVector
patchReleases[[25]]$maleReleases <- maleReleasesVector
patchReleases[[26]]$maleReleases <- maleReleasesVector
patchReleases[[27]]$maleReleases <- maleReleasesVector
patchReleases[[28]]$maleReleases <- maleReleasesVector
patchReleases[[29]]$maleReleases <- maleReleasesVector
patchReleases[[30]]$maleReleases <- maleReleasesVector
patchReleases[[31]]$maleReleases <- maleReleasesVector
patchReleases[[32]]$maleReleases <- maleReleasesVector
patchReleases[[33]]$maleReleases <- maleReleasesVector
patchReleases[[34]]$maleReleases <- maleReleasesVector
patchReleases[[35]]$maleReleases <- maleReleasesVector
patchReleases[[36]]$maleReleases <- maleReleasesVector
patchReleases[[37]]$maleReleases <- maleReleasesVector
patchReleases[[38]]$maleReleases <- maleReleasesVector
patchReleases[[39]]$maleReleases <- maleReleasesVector
patchReleases[[40]]$maleReleases <- maleReleasesVector
patchReleases[[41]]$maleReleases <- maleReleasesVector
patchReleases[[40]]$maleReleases <- maleReleasesVector
patchReleases[[41]]$maleReleases <- maleReleasesVector
patchReleases[[42]]$maleReleases <- maleReleasesVector
patchReleases[[43]]$maleReleases <- maleReleasesVector
patchReleases[[44]]$maleReleases <- maleReleasesVector
patchReleases[[45]]$maleReleases <- maleReleasesVector
patchReleases[[46]]$maleReleases <- maleReleasesVector
patchReleases[[47]]$maleReleases <- maleReleasesVector
patchReleases[[48]]$maleReleases <- maleReleasesVector
patchReleases[[49]]$maleReleases <- maleReleasesVector
patchReleases[[50]]$maleReleases <- maleReleasesVector
patchReleases[[51]]$maleReleases <- maleReleasesVector
patchReleases[[52]]$maleReleases <- maleReleasesVector
patchReleases[[53]]$maleReleases <- maleReleasesVector
patchReleases[[54]]$maleReleases <- maleReleasesVector
patchReleases[[55]]$maleReleases <- maleReleasesVector
patchReleases[[56]]$maleReleases <- maleReleasesVector
patchReleases[[57]]$maleReleases <- maleReleasesVector
patchReleases[[58]]$maleReleases <- maleReleasesVector
patchReleases[[59]]$maleReleases <- maleReleasesVector
patchReleases[[60]]$maleReleases <- maleReleasesVector
patchReleases[[61]]$maleReleases <- maleReleasesVector
patchReleases[[62]]$maleReleases <- maleReleasesVector


batchMigration <- basicBatchMigration(batchProbs = bm,
                                      sexProbs=c(.5,.5),
                                      numPatches=sitesNumber)

setupMGDrivE(stochasticityON = TRUE, verbose = FALSE)
netPar <- parameterizeMGDrivE(runID=100, simTime=tMax, sampTime = 7, nPatch=sitesNumber,
                              beta=bioParameters$betaK, muAd=bioParameters$muAd,
                              popGrowth=bioParameters$popGrowth, tEgg=bioParameters$tEgg,
                              tLarva=bioParameters$tLarva, tPupa=bioParameters$tPupa,
                              AdPopEQ=adpopreal, inheritanceCube = cube)



MGDrivESim <- Network$new(params=netPar,
                          driveCube=cube,
                          patchReleases=patchReleases,
                          migrationMale=moveMat,
                          migrationFemale=moveMat,
                          migrationBatch=batchMigration,
                          directory=folderNames,
                          verbose = FALSE)
MGDrivESim$multRun(verbose = FALSE)


####################
# Setup releases and batch migration
####################

