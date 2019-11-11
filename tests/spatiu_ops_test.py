import unittest
from src.problema import Problema

class SpatiuOpstests(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from random import random
        import numpy as np
        # Spatiul problemei 
        self.Space = {
            'x': [x for x in np.arange(-10, 10, 0.0001)],
            'y': [x for x in np.arange(-10, 10, 0.0001)],   
            'vars': ['x', 'y'],

        } 
        # Functia de maximizat per i=individ
        def my_fitness( i ):
            return -i['x']**2 + 1 -i['y']**2
        self.f = my_fitness
        

    def test_make_problema(self):

        fu    = [ lambda x: 0 ] * 5
        fu[0] = lambda x: 0
        fu[1] = lambda x: x
        fu[2] = lambda x: x**2
        fu[3] = lambda x: x**3

        o     = [ 1,2,3,4,5 ] 
        df = pd.DataFrame()
        df['a'] = [2]*5
        df['b'] = [3]*5

        v = 0
        for k in range(len(fu)):
            v = v + fu[k]( o[k] )


        print( fu )
        print( '\n\n\nValue: ', v )
        self.assertEqual(v, 14, "Shall be as per calculated value 14 ")
     



if __name__ == '__main__':
    unittest.main()

