#!/bin/sh
if [ "$1" != "" ]; then
	CURRENT_DIR=$(pwd)
	SCRIPT_DIR=$(dirname $0)

	if [ $SCRIPT_DIR = '.' ]
	then
	  SCRIPT_DIR="$CURRENT_DIR"
	fi
	
	DISPLAY=:0 python3 $SCRIPT_DIR/stilas/stilas.py $1 $SCRIPT_DIR &
	
fi
