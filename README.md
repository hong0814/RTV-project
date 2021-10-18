# RTV-project
## Table-to-Text



### 1. Requirement(t2t)
~~~
python=3.7
tensorflow==1.14.0
nltk
rouge-score
pip install "numpy<1.17"
sklearn
~~~
### 2. Process : our code
1) Directory Structure
```sh
.
└── RTV-project
    ├── ...
    ├── mapping_dict.json
    ├── RTV-data
    │       ├── 정형모의전장자료
    │       │           └── new_CSV
    │       │                   ├── T_AIRFORCE_DETECT.csv
    │       │                   ├── T_AIRFORCE_DETONATION_SAM.csv
    │       │                   └── T_AIRFORCE_FIRE_SAM.csv
    │       └── 비정형모의전장자료
    │                   ├── 1. 수시상황보고서
    │                   │   ├── 01_수시상황보고서_01.txt
    │                   │   ├── ...
    │                   ├── 2. 적기 공격 임박 보고서
    │                   │   ├── 01_적기공격임박보고서_01.txt
    │                   │   ├── ...
    │                   └── 3. 지대공 미사일 사격 보고서
    │                       ├── 11_지대공미사일사격보고서_01.txt
    │                        └── ...
    └── txt_processed
                ├── 1. 수시상황보고서
                │   ├── 01_수시상황보고서_01.txt
                │   ├── ...
                ├── 2. 적기 공격 임박 보고서
                │   ├── 01_적기공격임박보고서_01.txt
                │   ├── ...
                └── 3. 지대공 미사일 사격 보고서
                    ├── 11_지대공미사일사격보고서_01.txt
                    └── ...
```
2) Preprocess
~~~
python ychange.py --shuffle_ration 0.2 --josa True --punctuation True
python mypreprocess.py
~~~
3) Main
~~~
python myMain.py
~~~

### #. Process : original code (forked from [tyliupku/wiki2bio](https://github.com/tyliupku/wiki2bio))
1) Original Data Download : RTV-Project 폴더 내에 다운받은 original_data 폴더 넣기  
https://drive.google.com/drive/folders/1kCTwTwEk_CE9nc6q0snXm3lALrz_ZUDN?usp=sharing 
2) Preprocess
~~~
python preprocess.py
~~~
3) Main
~~~
python Main.py
~~~
