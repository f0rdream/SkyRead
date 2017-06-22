from django.test import TestCase

# Create your tests here.
dict = {'a':1,'b':2,'c':{'d':1}}
print dict['c']
dict['c'].pop('d')
print dict
