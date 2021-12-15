changePoss <- function(team) {
  if (team == 'A') {
    return ('B')
  }
  return ('A')
}
computePN <- function(team) {
  if (team == 'A') {
    return (1)
  }
  return (-1)
}
calcDist <- function(fieldPosition) {
  #p(pass) = 0.5278036; p(run)=0.4721964
  rp_play <- sample(c('R', 'P'), size = 1, replace = TRUE, prob = c(0.4721964, 0.5278036))
  if(rp_play == 'P') {
    rp_play <- sample(c('dpc', 'dpic', 'ndpc', 'ndpic', 'fumble'), size=1, replace=TRUE,
                      prob=c(0.04527526, 0.08498619, 0.4619231, 0.200062, 0.01543923))
    if (rp_play == 'dpic' | rp_play == 'ndpic' | rp_play == 'fumble') {
      distance <- 0
    }
    else {
      distance <- calculateBin(fieldPosition, rp_play)
    }
  }
  else if (rp_play == 'R') {
    run_play <- sample(c('success', 'fumble'), size = 1, replace = TRUE,
                       prob = c(0.9818766, 0.01812342))
    if (run_play == 'fumble') {
      distance <- 0
      rp_play <- 'fumble'
    }
    distance <- calculateBin(fieldPosition, rp_play)
  }
  distPlay <- list("distance"=distance, "play"=rp_play)
  return(distPlay)
}

nScore <- function(fieldLoc, down, YTG, poss) {
  calcDistRes <- calcDist(fieldLoc)
  changedDistance <- calcDistRes$distance
  currPlay <- calcDistRes$play
  newYTG <- YTG - changedDistance
  newFieldLocation <- fieldLoc + changedDistance
  nextScoreVal <- 0
  if (down <=4) {
    if (currPlay == 'fumble') {
      newFieldLocation <- 100 - fieldLoc
      down <- 1
      newYTG <- 10
    }
    else if (down == 4 & newYTG > 0) {
      poss <- changePoss(poss)
      newFieldLocation <- 100 - newFieldLocation
      down <- 1
      newYTG <- 10
    }
    if (newYTG <= 0 | newFieldLocation >= 100 | currPlay == 'fumble') {
      down <- 1
      newYTG <- 10
    }
    else {
      down <- down + 1
    }
  }
  else {
    #field goals and punts
    fourthDownResults <- fourthDown(fieldLoc) #changeDistance, play
    currPlay <-fourthDownResults$play
    if (currPlay == 'fg') {
      nextScoreVal <- 3 * computePN(poss)
      newFieldLocation <- 25
    }
    else if (currPlay == 'miss') {
      newFieldLocation <- 100 - fieldLoc
    }
    else {
      newFieldLocation <- fieldLoc + fourthDownResults$distance
    }
    down <- 1
    poss <- changePoss(poss)
    newYTG <- 10
  }
  if (newFieldLocation >= 100) {
    if (currPlay != 'punt') {
      currPlay <- 'touchdown'
      nextScoreVal <- 6 * computePN(poss)
      extrapoint <- sample(c(1, 0), size=1, replace = TRUE, prob = c(0.7693, 0.2307))
      1
      extrapoint <- extrapoint * computePN(poss)
      nextScoreVal <- nextScoreVal + extrapoint
    }
    poss <- changePoss(poss)
    newFieldLocation <- 25
    down <- 1
  }
  if (newFieldLocation <=0) {
    nextScoreVal <- -2 * computePN(poss)
    down <- 1
    poss <- changePoss(poss)
    newFieldLocation <- 25
    currPlay <- 'safety'
  }
  returnVal <- list("nextScoreVal"=nextScoreVal, "newFieldLocation"=newFieldLocation,
                    "down"=down, "newYTG"=newYTG, "poss"=poss,
                    "changedDistance"=changedDistance, "play"=currPlay)
  return (returnVal)
}
calculateBin <- function(fieldPosition, play) {
  changeDistance <- 0
  if (fieldPosition <= 25) {
    if (play == 'R'){
      shape <- 10.690340954
      rate <- 0.456578081
      changeDistance <- rgamma(1, shape, rate)-16
    }
    if (play == 'dpc'){
      shape <- 5.742605
      rate <- 0.1409833
      changeDistance <- rgamma(1, shape, rate)
    }
    if (play == 'ndpc'){
      shape <- 9.295788630
      rate <- 0.353020303
      changeDistance <- rgamma(1, shape, rate)-16
    }
  }
  else if(fieldPosition > 25 & fieldPosition <= 50){
    if (play == 'R'){
      shape <- 14.356134207
      rate <- 0.521790696
      changeDistance <- rgamma(1, shape, rate)-22
    }
    if (play == 'dpc'){
      shape <- 8.673703198
      rate <- 0.222168271
      changeDistance <- rgamma(1, shape, rate)
    }
    if (play == 'ndpc'){
      shape <- 7.671019924
      rate <- 0.325964551
      changeDistance <- rgamma(1, shape, rate)-13
    }
  }
  else if(fieldPosition > 50 & fieldPosition <= 75){
    if (play == 'R'){
      shape <- 13.151145571
      rate <- 0.565530395
      changeDistance <- rgamma(1, shape, rate)-18
    }
    if (play == 'dpc'){
      shape <- 20.86177422
      rate <- 0.65467692
      changeDistance <- rgamma(1, shape, rate)
    }
    if (play == 'ndpc'){
      shape <- 10.984156182
      rate <- 0.413641568
      changeDistance <- rgamma(1, shape, rate)-16
    }
  }
  else{
    if (play == 'R'){
      shape <- 29.71484179
      rate <- 1.27534603
      changeDistance <- rgamma(1, shape, rate)-20
    }
    if (play == 'dpc'){
      shape <- 7.1307362
      rate <- 20.8490961
      changeDistance <- rweibull(1, shape, rate)
    }
    if (play == 'ndpc'){
      shape <- 13.29157668
      rate <- 0.64467872
      changeDistance <- rgamma(1, shape, rate)-16
    }
  }
  return(changeDistance)
}
fourthDown <- function(fieldPosition) {
  changedDistance <- 0
  play <- ' '
  if (100 - fieldPosition > 50) {
    changeDistance <- rlogis(1, 39.6, 4.99)
    play <- 'punt'
  }
  else {
    changeDistance <- 0
    if (100 - fieldPosition <=10) {
      play <- 'fg'
    }
    else if (100 - fieldPosition > 10 & 100 - fieldPosition <= 20) {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.8961, 0.1039))
    }
    else if (100 - fieldPosition > 20 & 100 - fieldPosition <= 30) {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.8193, 0.1807))
    }
    else if (100 - fieldPosition > 30 & 100 - fieldPosition <= 40) {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.7485, 0.2515))
    }
    else {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.6667, 0.3333))
    }
  }
  fourthDownResult <- list("distance"=changeDistance, "play"=play)
  return (fourthDownResult)
}
runSimulation <- function(fp, down, ytg, team) {
  iterator <- 0
  score <- 0
  allDistances <- c(NA)
  allPlays <- c(NA)
  allDowns <- c(NA)
  poss <- c(NA)
  fieldLocations <- c(NA)
  newVals <- nextScore(fp, down, ytg, team)
  while (score == 0) {
    newVals <- nextScore(newVals$newFieldLocation, newVals$down,
                         newVals$newYTG, newVals$poss)
    score <- newVals$nextScoreVal
    iterator <- iterator + 1
    allDistances <- c(allDistances, newVals$changedDistance)
    allPlays <- c(allPlays, newVals$play)
    allDowns <- c(allDowns, newVals$down)
    poss <- c(poss, newVals$poss)
    fieldLocations <- c(fieldLocations, newVals$newFieldLocation)
    # print(newVals)
  }
  simulationInfo <- list("score"=score, "iterations"=iterator,
                         "changedDistances"=allDistances, "allPlays"=allPlays,
                         "allDowns"=allDowns, "poss"=poss,
                         "fieldLocations"=fieldLocations)
  return (simulationInfo)
}
testSimulation <- function() {
  #field position range: 50-60
  #YTG range: 1-10
  allScores <- c(NA)
  for (i in 1:10) {
    for (fp in 80:90){
      for (ytg in 1:10) {
        allScores <- c(allScores, runSimulation(fp, 4, ytg, 'A')$score)
      }
    }
  }
  return (allScores)
}
simulationScores <- testSimulation()
simulationScores <- simulationScores[!is.na(simulationScores)]
table(simulationScores)
