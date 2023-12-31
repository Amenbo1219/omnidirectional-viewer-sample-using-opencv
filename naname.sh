#! /bin/bash
cnt=0
z=100
y=5
#for j ((j=0,j<=$y,j=j+1))

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
		let pitch2=pitch+10
		let yaw2=yaw+20
		echo "frames:${cnt}"
		echo "$yaw,$pitch"
		
		python 01_simple_image_convert.py --image ./naname.jpg  --width 1920 --height 1080 --output ./naname-mix/images/train_${cnt}.png --imagepoint 1 --roll 0 --pitch ${pitch} --yaw  ${yaw}
		python 01_simple_image_convert.py --image ./naname.jpg  --width 1920 --height 1080 --output ./naname-mix/images/test_${cnt}.png --imagepoint 1 --roll 0 --pitch ${pitch2} --yaw  ${yaw2}

		done
done	

