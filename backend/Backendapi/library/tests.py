from django.test import TestCase

# Create your tests here.
import time
i = "b2b3b4b5"
dict = i.split("b")
for number in dict[1:]:
    id = int(number)

print time.time()