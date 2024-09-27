#!/bin/bash

exp_dir=/eagle/RECUP/twang/miniapp-exp/ddmd-reprod-v2

if [ -d ${exp_dir} ]
then
	echo "Error! Directory ${exp_dir} exists"
	exit -1
fi

mkdir -p ${exp_dir}/model
mkdir -p ${exp_dir}/data

num_phase=3
for((i=0; i<num_phase; i++))
do
	mkdir -p ${exp_dir}/data/phase${i}
done


python ../rct-scripts/ddmd-F-ddp.py	\
	--num_phases        ${num_phase}	\
	--mat_size 		20000		\
	--data_root_dir		"${exp_dir}/data"	\
	--num_step		30000		\
	--num_epochs_train	150		\
	--model_dir		"${exp_dir}/model"	\
	--conda_env		        "/eagle/RECUP/twang/env/rose-task-base-clone"	\
	--num_sample		1000		\
	--num_mult_train	4000		\
	--dense_dim_in		12544		\
	--dense_dim_out		256		\
	--preprocess_time_train	30		\
	--preprocess_time_agent	5		\
	--num_epochs_agent	150		\
	--num_mult_agent	2000		\
	--num_mult_outlier	200		\
    --allreduce_size    6422528 \
	--project_id		RECUP		\
	--queue			"debug"		\
	--num_sim		8		\
	--num_nodes		2		\
	--io_json_file		"io_size.json" 