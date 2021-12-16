computePN <- function(team) {
  if (team == 'A') {
    return (1)
  }
  return (-1)
}

changePoss <- function(team) {
  if (team == 'A') {
    return ('B')
  }
  return ('A')
}
calcDist <- function(fieldPos) {
  play <- sample(c('R', 'P'), size = 1, replace = TRUE, prob = c(0.472, 0.528))
  
  if(play == 'P') {
    play <- sample(c('complete', 'incomplete'), size=1, replace=TRUE,
                      prob=c(0.507, 0.285))
    distance <- calculateBin(fieldPos, play)
  }
  
  else if (play == 'R') {
    simulate_play <- sample(c('success', 'fumble'), size = 1, replace = TRUE,
                       prob = c(0.982, 0.018))
    if (simulate_play == 'fumble') {
      distance <- 0
      play <- 'fumble'
    }
    distance <- calculateBin(fieldPosition, play)
  }
  
  distance_of_play <- list("distance"=distance, "play"=play)
  return(distance_of_play)
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
    fourthDownResults <- fourthDown(fieldLoc)
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
      extrapoint <- sample(c(1, 0), size=1, replace = TRUE, prob = c(0.77, 0.23))
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
      shape <- 10.69
      rate <- 0.457
      changeDistance <- rgamma(1, shape, rate)-16
    }
    if (play == 'complete'){
      shape <- 8.99
      rate <- 0.334
      changeDistance <- rgamma(1, shape, rate) - 15
    }
  }
  else if(fieldPosition > 25 & fieldPosition <= 50){
    if (play == 'R'){
      shape <- 14.356
      rate <- 0.522
      changeDistance <- rgamma(1, shape, rate)-22
    }
    if (play == 'complete'){
      shape <- 7.758
      rate <- 0.317
      changeDistance <- rgamma(1, shape, rate) - 12
    }
  }
  else if(fieldPosition > 50 & fieldPosition <= 75){
    if (play == 'R'){
      shape <- 13.151
      rate <- 0.566
      changeDistance <- rgamma(1, shape, rate)-18
    }
    if (play == 'complete'){
      shape <- 11.853
      rate <- 0.434
      changeDistance <- rgamma(1, shape, rate) -15
    }
  }
  else{
    if (play == 'R'){
      shape <- 29.71
      rate <- 1.27
      changeDistance <- rgamma(1, shape, rate)-20
    }
    if (play == 'complete'){
      shape <- 12.750
      rate <- 2.423
      changeDistance <- rgamma(1, shape, rate) -15
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
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.897, 0.103))
    }
    else if (100 - fieldPosition > 20 & 100 - fieldPosition <= 30) {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.82, 0.18))
    }
    else if (100 - fieldPosition > 30 & 100 - fieldPosition <= 40) {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.75, 0.25))
    }
    else {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.667, 0.33))
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
  }
  simulationInfo <- list("score"=score, "iterations"=iterator,
                         "changedDistances"=allDistances, "allPlays"=allPlays,
                         "allDowns"=allDowns, "poss"=poss,
                         "fieldLocations"=fieldLocations)
  return (simulationInfo)
}
testSimulation <- function() {
  allScores <- c(NA)
  for (i in 1:12) {
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
simScores <- as.numeric(table(simulationScores))
expectedPoints <- (simScores[1]/1000 *-7 + simScores[2]/1000 * -6 + simScores[3]/1000*-2 + simScores[4]/1000*2 + simScores[5]/1000*6 + simScores[6]/1000 * 7)
expectedPoints
