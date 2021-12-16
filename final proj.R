calcDist <- function(fieldPos) {
  play <- sample(c('R', 'P'), size = 1, replace = TRUE, prob = c(0.472, 0.528))
  
  if(play == 'R') {
    simulate_play <- sample(c('success', 'fumble'), size = 1, replace = TRUE,
                            prob = c(0.982, 0.018))
    if (simulate_play == 'fumble') {
      distance <- 0
      play <- 'fumble'
    }
    distance <- bin(fieldPos, play)
  }
  
  else if (play == 'P') {
    play <- sample(c('complete', 'incomplete'), size=1, replace=TRUE,
                   prob=c(0.507, 0.285))
    distance <- bin(fieldPos, play)
  }
  
  distance_of_play <- list("distance"=distance, "play"=play)
  return(distance_of_play)
}

nScore <- function(fieldLoc, down, YTG, poss) {
  calcDistRes <- calcDist(fieldLoc)
  changeDist <- calcDistRes$distance
  currPlay <- calcDistRes$play
  newYTG <- YTG - changeDist
  nFL <- fieldLoc + changeDist
  nSV <- 0
  if (down <=4) {
    if (currPlay == 'fumble') {
      nFL <- 100 - fieldLoc
      down <- 1
      newYTG <- 10
    }
    else if (down == 4 & newYTG > 0) {
      poss <- changePoss(poss)
      nFL <- 100 - nFL
      down <- 1
      newYTG <- 10
    }
    if (newYTG <= 0 | nFL >= 100 | currPlay == 'fumble') {
      down <- 1
      newYTG <- 10
    }
    else {
      down <- down + 1
    }
  }
  else {
    fDownRes <- fDown(fieldLoc)
    currPlay <-fDownRes$play
    if (currPlay == 'fg') {
      nSV <- 3 * computePN(poss)
      nFL <- 25
    }
    else if (currPlay == 'miss') {
      nFL <- 100 - fieldLoc
    }
    else {
      nFL <- fieldLoc + fDownRes$distance
    }
    down <- 1
    poss <- changePoss(poss)
    newYTG <- 10
  }
  if (nFL >= 100) {
    if (currPlay != 'punt') {
      currPlay <- 'touchdown'
      nSV <- 6 * computePN(poss)
      extrapoint <- sample(c(1, 0), size=1, replace = TRUE, prob = c(0.77, 0.23))
      extrapoint <- extrapoint * computePN(poss)
      nSV <- nSV + extrapoint
    }
    poss <- changePoss(poss)
    nFL <- 25
    down <- 1
  }
  if (nFL <=0) {
    nSV <- -2 * computePN(poss)
    down <- 1
    poss <- changePoss(poss)
    nFL <- 25
    currPlay <- 'safety'
  }
  returnVal <- list("nSV"=nSV, "nFL"=nFL,
                    "down"=down, "newYTG"=newYTG, "poss"=poss,
                    "changeDist"=changeDist, "play"=currPlay)
  return (returnVal)
}
bin <- function(fieldPos, play) {
  changeDist <- 0
  if (fieldPos <= 25) {
    if (play == 'R'){
      shape <- 10.69
      rate <- 0.457
      changeDist <- rgamma(1, shape, rate)-16
    }
    if (play == 'complete'){
      shape <- 8.99
      rate <- 0.334
      changeDist <- rgamma(1, shape, rate) - 15
    }
  }
  else if(fieldPos > 25 & fieldPos <= 50){
    if (play == 'R'){
      shape <- 14.356
      rate <- 0.522
      changeDist <- rgamma(1, shape, rate)-22
    }
    if (play == 'complete'){
      shape <- 7.758
      rate <- 0.317
      changeDist <- rgamma(1, shape, rate) - 12
    }
  }
  else if(fieldPos > 50 & fieldPos <= 75){
    if (play == 'R'){
      shape <- 13.151
      rate <- 0.566
      changeDist <- rgamma(1, shape, rate)-18
    }
    if (play == 'complete'){
      shape <- 11.853
      rate <- 0.434
      changeDist <- rgamma(1, shape, rate)
    }
  }
  else{
    if (play == 'R'){
      shape <- 29.71
      rate <- 1.27
      changeDist <- rgamma(1, shape, rate)-20
    }
    if (play == 'complete'){
      shape <- 12.750
      rate <- 2.423
      changeDist <- rgamma(1, shape, rate)
    }
  }
  return(changeDist)
}
fDown <- function(fieldPos) {
  changeDist <- 0
  play <- ' '
  if (100 - fieldPos > 50) {
    changeDist <- rlogis(1, 39.6, 4.99)
    play <- 'punt'
  }
  else {
    changeDist <- 0
    if (100 - fieldPos <=10) {
      play <- 'fg'
    }
    else if (100 - fieldPos > 10 & 100 - fieldPos <= 20) {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.897, 0.103))
    }
    else if (100 - fieldPos > 20 & 100 - fieldPos <= 30) {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.82, 0.18))
    }
    else if (100 - fieldPos > 30 & 100 - fieldPos <= 40) {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.75, 0.25))
    }
    else {
      play <- sample(c('fg', 'miss'), size = 1, replace = TRUE, prob = c(0.667, 0.33))
    }
  }
  fourthDownResult <- list("distance"=changeDist, "play"=play)
  return (fourthDownResult)
}

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
sim <- function(fp, down, ytg, team) {
  d <- c(NA)
  its <- 0
  di <- c(NA)
  score <- 0
  p <- c(NA)
  poss <- c(NA)
  fieldLoc <- c(NA)
  nV <- nScore(fp, down, ytg, team)
  while (score == 0) {
    nV <- nScore(nV$nFL, nV$down,
                         nV$newYTG, nV$poss)
    score <- nV$nSV
    its <- its + 1
    di <- c(di, nV$changeDist)
    p <- c(p, nV$play)
    d <- c(d, nV$down)
    poss <- c(poss, nV$poss)
    fieldLoc <- c(fieldLoc, nV$nFL)
  }
  simfo <- list("score"=score, "iterations"=its,
                         "changedDistances"=di, "p"=p,
                         "d"=d, "poss"=poss,
                         "fieldLoc"=fieldLoc)
  return (simfo)
}
testSim <- function() {
  allScores <- c(NA)
  for (it in 1:12) {
    for (fp in 80:90){
      for (ytg in 1:10) {
        allScores <- c(allScores, sim(fp, 4, ytg, 'A')$score)
      }
    }
  }
  return (allScores)
}
simScores <- testSim()
simScores <- simScores[!is.na(simScores)]
table(simScores)
simScores <- as.numeric(table(simScores))
expectedPoints <- (simScores[1]/1000 *-7 + simScores[2]/1000 * -6 + simScores[3]/1000*-2 + simScores[4]/1000*2 + simScores[5]/1000*6 + simScores[6]/1000 * 7)
expectedPoints
