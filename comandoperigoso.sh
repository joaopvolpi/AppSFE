#!/bin/bash

git add .
git commit -m $1
git push -u origin master
ssh root@67.205.161.203 <<EOF
	su volpi
	cd ~/projeto
	ls
	git pull origin master
EOF
