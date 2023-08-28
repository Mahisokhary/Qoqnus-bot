from pathlib import Path
from random import randint
import time
import numpy

with open("price", "w") as price:
	x = str(randint(1, 10000))
	price.write(x + "-nothing-0")
	price.close()

while True:
	with open("price", "r") as price: x = int(price.read().split("-")[0]); price.close()
	y = randint(-30, 30)
	x += y
	if y > 0: z="up"
	elif y < 0: z="down"
	else: z="nothing"
	print(open("price", "r").read())
	with open("price", "w") as price: price.write(str(x) + "-" + z + "-" + str(numpy.abs(y))); price.close()
	time.sleep(3)
 