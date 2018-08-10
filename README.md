# MULTI ARMED BANDIT

**What?** Compare different versions of something to figure out which one is better, can be used as an alternative to AB testing.

**Why?** To *mitigate the regret* introduced in AB test, the regret about the lost conversion you experience while sending people to the potentially worse variation in a test. Rather than splitting people to two groups and run a test, the algorithm updates the split through the experiment, pulling the winning slot machine arm most often, i.e. it moves traffic towards the winning variation gradually.

**How?** Starts by sending traffic to two (or more) pages: the original and the variation, then, in an attempt to *pull the winning slot machine arm most often*, the algorithm updates based on whether or not a variation is ‘winning'. (There is also the randomization part though - the randomization of for example 10% - these trials would be used to explore the options, no matter the winning arm. It is a trade-off between trying new things in hopes of something better, and sticking with what it knows will work.)

-----------------------------------


# AB TEST

**What?** Compare two versions of something to figure out which one is better.

**Why?** To take the guesswork out of website optimization and enable data-informed decisions.

**How?** By measuring the impact the change has on your metrics.
