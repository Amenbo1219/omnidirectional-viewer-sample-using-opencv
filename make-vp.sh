#! /bin/bash
cnt=0
z=100
y=10
path=$(basename $1)
#for j ((j=0,j<=$y,j=j+1))
echo "input = "$1
echo "path="$path
for j in `seq $y`
do
	echo "$j"

	#let pitch=(180*j/y)-90
	#let pitch=(160*j/y)-80
	#let pitch=(140*j/y)-70
	#let pitch=(120*j/y)-60
	#let pitch=(100*j/y)-50
	let pitch=(80*j/y)-40
	#let pitch=(60*j/y)-30
	#let pitch=(40*j/y)-20
	#let pitch=(20*j/y)-10
	#let pitch=(10*j/y)-0
	#for i in ((i=0,i<=$z,i=i+1))
	for i in `seq $z`

	do
		let cnt=${cnt}+1
		let yaw=(360*i/z)-180
		let yaw2=yaw+20
		let pitch2=pitch+10
		let roll2=(${cnt}%10*36)
		let point2=2
		

		echo "frames:${cnt}"
		echo "$yaw,$pitch"
		python 01_simple_image_convert.py --image $1 --width 1920 --height 1080 --output ./out/$path/images/train_${cnt}.png --imagepoint 1 --roll 0 --pitch ${pitch} --yaw  ${yaw}
		echo "$yaw2,$pitch2,$roll2,$point2"
		python 01_simple_image_convert.py --image $1 --width 1920 --height 1080 --output ./out/$path/images/test_${cnt}.png --imagepoint ${point2} --roll ${roll2} --pitch ${pitch2} --yaw  ${yaw2}

		done
done	

