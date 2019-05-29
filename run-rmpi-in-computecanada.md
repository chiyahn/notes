# Run Rmpi in ComputeCanada clusters
## Prep
Save the following lines named `Rprofile` (without extension) in your home directory, `/home/$YOUR_USERNAME/Rprofile` where `$YOUR_USERNAME` is your username in Graham / Cedar. Note that this has to be done in each cluster just once.

```R
# This R profile can be used when a cluster does not allow spawning or a job 
# scheduler is required to launch any parallel jobs. Saving this file as 
# .Rprofile in the working directory or root directory. For unix platform, run
# mpirun -n [cpu numbers] R --no-save -q

# Another way is to modify R_home_dir/bin/R by adding the following line after
# R_HOME_DIR
# R_PROFILE=${R_HOME_DIR}/library/Rmpi/Rprofile; export R_PROFILE

# For windows platform with mpich2, use mpiexec wrapper and specify a working 
# directory where .Rprofile is inside.

# Cannot be used as Rprofile.site because it will not work

# If no CPU consumptions of slaves while waiting are desirable, change 
# nonblocak=FALSE to nonblock=TRUE and change sleep time accordingly

# Following system libraries are not loaded automatically. So manual loads are 
# needed.
library(utils)
library(stats)
library(datasets)
library(grDevices)
library(graphics)
library(methods)

#Change to TRUE if you don't want any slave host info
quiet=FALSE

if (!invisible(library(Rmpi,logical.return = TRUE))){
    warning("Rmpi cannot be loaded")
    q(save = "no")
}

options(error=quote(assign(".mpi.err", FALSE, envir = .GlobalEnv)))

if (mpi.comm.size(0) > 1)
    invisible(mpi.comm.dup(0,1))

if (mpi.comm.rank(0) >0){
    #sys.load.image(".RData",TRUE)
    options(echo=FALSE)
    .comm <- 1
    mpi.barrier(0)
    repeat 
		try(eval(mpi.bcast.cmd(rank=0,comm=.comm, nonblock=FALSE, sleep=0.1)),TRUE)
	if (is.loaded("mpi_comm_disconnect")) 
        mpi.comm.disconnect(.comm)
    else mpi.comm.free(.comm)
    mpi.quit()
}
    
if (mpi.comm.rank(0)==0) {
    #options(echo=TRUE)
    mpi.barrier(0)
    if(mpi.comm.size(0) > 1 && !quiet)
        slave.hostinfo(1)
}

.Last <- function(){
    if (is.loaded("mpi_initialize")){
        if (mpi.comm.size(1) > 1){
            print("Please use mpi.close.Rslaves() to close slaves")
            mpi.close.Rslaves(comm=1)
    	}
    }
    #print("Please use mpi.quit() to quit R")
	if (is.loaded("mpi_initialize"))
       .Call("mpi_finalize",PACKAGE = "Rmpi")
}

```
## Opening R & Installing packages
Whenever you want to install new packages, run the following line first:
```
module load r/3.4.0
```
(Not `R/3.4.0`!) and run
```
R
```
(Not `r`!)
## Running the jobs
Suppose you want to run the following experiment:

```r
################################################################################
# Compute MLEs for normal samples using Rmpi
################################################################################
## LIBRARY
library(Rmpi)

## CONFIG
NAME <- "rmpi-test"
RMPI <- FALSE # determines whether RMPI is used
REPLICATIONS <- 100 # number of replications
N <- 400 # number of obseravtions in each replication

EstimateModel <- function (sample) {
  return (list(mu = mean(sample), sigma = sqrt(var(sample))))
}

## SAMPLE DATA GENERATION
set.seed(123456)
samples.list <- lapply(1:REPLICATIONS, function (x) rnorm(N))

## RMPI SETUP
print("collecting workers..")
# mpi.spawn.Rslaves()
mpi.setup.rngstream()
mpi.bcast.Robj2slave(EstimateModel, all=TRUE)
print("workers loaded.")
## ====== BEGIN EXPERIMENT =====

if (RMPI) {
  results <- mpi.applyLB(samples.list, EstimateModel)
} else {
  results <- lapply(samples.list, EstimateModel)
}

## ====== END EXPERIMENT ======
## RMPI TERMINATION
mpi.close.Rslaves()

## ====== REPORT ======
# extract data
mus <- t(sapply(results, "[[", "mu"))
sigmas <- t(sapply(results, "[[", "sigma"))

# expprt
write.csv(mus, paste0(NAME, ".csv"))
write.csv(sigmas, paste0(NAME, ".csv"))
```

1. Save the above lines as `rmpi-test.R`.
2. In SLURM (job submission software used by Graham and Cedar) you have to submit a submmission script to get the job done. Save the following lines as `rmpi-test.sh` in the same directory as `rmpi-test.R` is located:
```
#!/bin/bash
#
#SBATCH --job-name="rmpi-test"
#SBATCH -o rmpi-test.err
#SBATCH -e rmpi-test.out
#SBATCH --ntasks=8
#SBATCH --mem-per-cpu=1024M
#SBATCH --time=1:00:00

module load r/3.4.0
export R_PROFILE=/home/$YOUR_USERNAME/Rprofile

mpirun -n 8 Rscript rmpi-test.R
```
Replace `$YOUR_USERNAME` with your username in Graham/ Cedar. 

3. Set your working directory as the directory where `rmpi-test.R` is located, and run the following line:
```
sbatch rmpi-test.sh
```
To see the status of your job, run the following line:
```
squeue -u $YOUR_USERNAME
```
replace `$YOUR_USERNAME` with your username. To cancel your job, run the following line:
```
scancel $JOB_NUMBER
```
where `$JOB_NUMBER` is the job number assigned with the task assigned (you can check it by using `squeue -u $YOUR_USERNAME` as above.).


## Tips on getting jobs run earlier
1. ComputeCanada puts heavy weights on memory requirements -- if you want your jobs to be run fast, let memory requirements to be minimal as possible. For the bootstrap experiments I have run so far (which requires fair amount of memory), I found `2048M` (2GB) enough.
2. Each job is categorized and queued by the group defined by time limit -- one for jobs that require less or equal to 30 minutes, 3 hours, 12 hours, and 24 hours etc.
3. Note that each node can run up to 32 tasks in Graham and Cedar; hence it is the best practice to set `--ntasks` set to be the multiple of 32.
4. It seems like queues in Graham and Cedar are independent with each other -- use both if there are jobs that you want to be done fast. My experience is that Cedar has less users.

