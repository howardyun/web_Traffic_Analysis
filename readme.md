## Folder structure
    .
    ├─📁 attacks----------------- # WF attacks 
    │ ├─📁 after-split-attack---- # customized kNN codes for evaluating Glue
    │ ├─📁 cumul----------------- # CUMUL using SVM
    │ ├─📁 decision-------------- # Split decision using Random Forest (Used for evaluating Glue)
    │ ├─📁 df-------------------- # Deep Fingerprinting
    │ ├─📁 kfingerprinting------- # kFP using Random Forest
    │ ├─📁 knn------------------- # kNN using k Nearest Neighbor
    │ ├─📁 split----------------- # Cut l-traces according to result from split finding (Used for evaluating Glue) 
    │ └─📁 xgboost--------------- # Split finding using xgboost (Used for evaluating Glue) 
    ├─📁 Defence----------------- # WF defenses
    │ ├─📁 data------------------ # Raw data folder
    │ ├─📁 try2
    │ ├─📁 try2data
    │ └─📁 WFP-Defence----------- # WF defenses
    │   ├─📁 front--------------- # FRONT defense
    │   ├─📁 glue---------------- # Glue defense
    │   ├─📁 results------------- # a folder to generate datasets defended by one of the defenses
    │   ├─📁 tamaraw------------- # Tamaraw defense
    │   └─📁 wtfpad-------------- # WTF-PAD defense
    ├─📁 ShowTrajData------------ # a folder to show sequence-similarity
    └─📁 ysx

## Running examples

To run defenses, go to a defense folder.
To run attacks, go to an attack folder.

### Run FRONT

FRONT takes in a dataset folder, output a defended dataset into "defenses/results/" folder 
```
python3 main.py ../../data/20000/
```
This generates a dataset into ../results/ folder using FRONT defense.

### Run GLUE
```
python3 main-base-rate.py ../../data/tor2-5-1/ -n 4000 -b 1 -m 2 -noise True -mode fix
```
n: number of l-traces; m: l; b: base rate; noise: add noise or not; 
mode: fix -> all traces are m length; random -> length is randomly chosen from (2, m)

Generate 4000 noisy 2-traces with base rate 1   

**NOTE**: When `-noise True`, the program requires a list of non-monitored sites (saved in `nonsens.txt`), which are randomly sampled as GLUE noise traces to inject into an \ell-trace. You should creat your own list of glue noise traces and put them in the right place. Otherwise, you will get `FileNotFoundError`. The `nonsens.txt` is loaded at Line 92 of `main-base-rate.py`.

### WTF-PAD or TAMARAW

They are same as FRONT.


## Run kFP or CUMUL or DF attack
Go to an attack folder

To evaluate FRONT, 
First extract features
```
python3 extract.py ../../defense/results/xxx/
```
Then 
```
python3 new_main.py(or main.py) ./results/test.npy 
```
This will generate results of a 10 cross validation result. 

To evaluate Glue,
Use mp-extract.py to extract features, it will generate features for the first page and the other pages seperately (since they need to be evaluated using two WF models).
Then
```
python3 evaluate.py -m a-saved-model.pkl -o leaf.npy(needed for kFP)/training_data.npy(needed for cumul) -p ./results/test.npy
```

random-evaluate.py is used under split with decision scenario. used together with random_attack.py.

## Run kNN
```
./run_attack.sh data_folder log_dir
```
The data_folder should be located in attacks/knn . you can use Symbolic Link to link the defended dataset

## Run kNN on glue
cd after-split-attack, mp-kNN contains customized kNN for split finding case; randomkNN2 contains customized kNN for split decision + finding case

For example, cd mp-kNN, run
```
./run_attack_head.sh train_folder test_folder log_dir
```
This evaluate the first split webpages.
```
./run_attack_other.sh train_folder test_folder log_dir
```
This evaluate the other split webpages.

## Split decision 
Go to "attacks/decision" 
```
python3 run_attack.py -train trainset -test testset -num l
```
This corresponds to split decision process.       
It will generate a ".npy" file telling the prediction of l of all l-traces in testset.       
"-num" indicates this testset contains traces of length l.       
trainset contains l-traces of different l; testset only contains traces of the same l.         

## Split finding
Go to "attack/xgboost"
```
python3 run_attack.py -train trainset -test testset -mode decision/finding -kdir ../decision/results/testset.npy
```
This corresponds to split finding process.    
It will generate a splitresult.txt file telling where the splits are in a trace.     
"-mode" whether you run split decision or not.     
Note if mode is decision, then you should give the predicition of "l" using "-kdir "

