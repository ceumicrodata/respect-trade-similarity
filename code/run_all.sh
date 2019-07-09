cd ..
. env/bin/activate

cd code/

python 1_exp_imp_multi.py
python 2_create_index.py
python 3_make_pivot.py
python 4_clean_index.py

deactivate
