#!/bin/bash

exp_dir=/eagle/RECUP/twang/miniapp-exp/ddmd-reprod

if [ -d ${exp_dir} ]
then
	echo "Error! Directory ${exp_dir} exists"
	exit -1
fi

mkdir -p ${exp_dir}/model
mkdir -p ${exp_dir}/data

python ../rct-scripts/ddmd-F.py	\
	--num_phases		2		\
	--mat_size 		10000		\
	--data_root_dir		"${exp_dir}/data"	\
	--num_step		48000		\
	--num_epochs_train	100		\
	--model_dir		"${exp_dir}/model"	\
	--num_sample		500		\
	--num_mult_train	4000		\
	--dense_dim_in		12544		\
	--dense_dim_out		128		\
	--preprocess_time_train	30		\
	--preprocess_time_agent	5		\
	--num_epochs_agent	100		\
	--num_mult_agent	1000		\
	--num_mult_outlier	100		\
	--project_id		RECUP		\
	--queue			"debug"		\
	--num_sim		4		\
	--num_nodes		1		\
	--io_json_file		"io_size.json"
