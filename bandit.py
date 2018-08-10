import numpy as np
from scipy.stats import beta #prior/posterior distribution
from scipy.stats import binom #likelihood
from scipy.stats import bernoulli #generating testing samples (click/no click)
import datetime #set the running time of the experiment
from scipy.stats import itemfreq #MC simulation of arm probabilities


class Bandit_TS(object):
    def __init__(self, n_arm=3):
        self.n_arm =  n_arm #number of arms
        self.arm_distr = np.array([[1 for x in range(2)] for y in range(n_arm)]) #prior beta(1,1) for each arm
        self.count = np.array([0] * n_arm) #step count for each arm - number of views
        self.reward = np.array([0] * n_arm) #payoff for each arm - number of clicks
        self.k = 0 #step count
    
    
    def evaluate(self):
        """
        Update final state of beta distributions
        Output the optimal arm
        Compute optimal arm probabilities by simulation
        
        """
        for i in range(self.n_arm):
            self.arm_distr[self.n_arm-1] = np.array([1 + self.reward[self.n_arm-1], 1 + 1*self.count[self.n_arm-1] - self.reward[self.n_arm-1]])
        

    def bandit(self, stop_alpha=0.05, stop_value=0.95, iterat=1000):
        """
        Run bandit
        Stop criterion: 
        1st Use Bayes' theorem to compute the probability that variation beats others, if 95% sure that a variation beats the others then "a winner has been found"
        2nd Potential value remaining in the experiment - the "value remaining" is the amount of increased conversion rate we could get by switching away from the current champion
        """   
        simul_m = np.zeros((10000,self.n_arm))
        stop_first = np.zeros((10000,1))
        while ((iterat!=None) and (iterat>=self.k) ):
            self.choose_arm()
            for i in range(10000):
                simul_m[i] = beta.rvs(1 + self.reward, 1 + 1*self.count - self.reward)
                stop_first[i] = np.argmax(simul_m[i])
            unique, counts = np.unique(stop_first, return_counts=True)
            arm_prob = np.array((unique, counts/10000.0),dtype='float64').T
        
            opt_arm = int(arm_prob[np.argmax(arm_prob[:,1], axis=0),0])
            stop_second = np.percentile((np.max(simul_m,axis=1) - simul_m[:,opt_arm])/ simul_m[:,opt_arm], stop_value*100)
            if np.max(arm_prob[:,1])>=(1-stop_alpha):
                opt_arm = arm_prob[np.argmax(arm_prob[:,1], axis=0),0]
                print('The winner has been found! The arm number {} has been found as optimal at the {} confidence level after {} page views.'.format(opt_arm,stop_alpha, self.k))
                break
            elif arm_prob[np.argmax(arm_prob[:,1], axis=0),1]*0.01 >=stop_second:
                print('The winner has been found! The arm number {} has been found as optimal, as with {}% probability, the value remaining in the experiment is less than 1% possible improvement{}.'.format(opt_arm,stop_value*100,self.k))
                break   
            elif iterat==self.k:
                print('After {} iterations, the winning arm is number {}.'.format(iterat, opt_arm))    
                
        
    def choose_arm(self):
        """Choose an arm: explore x exploit.
        Take random sample from each bandit with its current Beta(a, b) and select largest sample
        """
        
        draw_arm = np.argmax(beta.rvs(1 + self.reward, 1 + 1*self.count - self.reward))
        new_reward = self.pull(draw_arm)
        self.count[draw_arm] += 1
        self.reward[draw_arm] += new_reward
        self.k += 1
             
    def pull(self, i):
        """Pull arm and fill randomly from bernoulli distr (replace this with click results: 1-click, 0-no click)
        """
        sample_bern = np.linspace(0.7,0.75,self.n_arm) #1st arm lowest probability of click, last arm highest prob. of click
        return bernoulli.rvs(sample_bern[i], size=1)
