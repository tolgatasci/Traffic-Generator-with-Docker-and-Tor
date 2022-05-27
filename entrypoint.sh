#!/bin/sh
HASHED_PASS=$(tor --hash-password abcdef| grep 16)
sed -i "s/#HashedControlPassword 16:x/HashedControlPassword $HASHED_PASS/g" /etc/tor/torrc

tor -f /etc/tor/torrc &>/dev/null &
n=0

# continue until $n equals 5
while [ $n -le $2 ]
do
	# shellcheck disable=SC2068
	python3 hit.py $@
	python3 refreship.py
	n=$(( n+1 ))	 # increments $n
done