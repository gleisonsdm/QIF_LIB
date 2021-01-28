# QIF_LIB
A Quantitative Information Flow Open Source Library

## Software present in the lib

This section is organized by modules.
### 1.0 Basic functions
- [X] 1.1: Given a vector of numbers, verify whether it constitutes a valid probability distribution.
- [X] 1.2: Given a matrix of number, verify whether it constitutes a valid channel matrix.
- [X] 1.3: Print beautifully a prior on the screen.
- [X] 1.4: Print beautifully a channel matrix on the screen.
### 2.0 Update of knowledge using priors and channels
- [X] 2.1: Given a prior and a channel matrix, compute the corresponding joint probability distribution.
- [X] 2.2: Given a prior and a channel matrix, compute the corresponding hyper-distribution (i.e., the set of posterior distributions and the outer distribution on them).
### 3.0 Prior measures of information
- [X] 3.1: Given a prior distribution, compute its Shannon entropy.
- [X] 3.2: Given a prior distribution, compute its Guessing entropy.
- [X] 3.3: Given a prior distribution, compute its Bayes vulnerability.
- [X] 3.4: Given a prior distribution and a value n>=1, compute the probability of guessing correctly within n tries. (Note that when n = 1 this function coincides with Bayes vulnerability).
- [X] 3.5: Given a prior distribution and a gain function, compute the g-vulnerability. (Note that when the g-function is gid, you recover Bayes vulnerability). 
### 4.0 Posterior measures of information 
- 4.1: Create functions that, given a prior and a channel matrix, compute the corresponding posterior information measures as in the items (a)-(e) of item (3) above.
- [X] 4.1.1: Compute its Shannon entropy.
- [X] 4.1.2: Compute its Guessing entropy.
- [X] 4.1.3: Compute its Bayes vulnerability.
- [X] 4.1.4: Given a posterior distribution and a value n>=1, compute the probability of guessing correctly within n tries.
- [X] 4.1.5: Given a posterior distribution and a gain function, compute the g-vulnerability.
#
### 5.0 Leakage measures
- [ ] 5.1: Given a prior, a channel matrix, and an information function, compute the corresponding additive leakage.
- [ ] 5.2: Given a prior, a channel matrix, and an information function, compute the corresponding multiplicative leakage.
