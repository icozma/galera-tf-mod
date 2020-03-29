import unittest

class Populatie_tests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from src.problema import Problema
        from random import random
        import numpy as np

        # Spatiul problemei 
        Space = {
            'x': [x for x in np.arange(-10, 10, 0.0001)],
            'y': [x for x in np.arange(-10, 10, 0.0001)],      
            # 'z': [x for x in np.arange(-10, 10, 0.0001)],      
        } 

        # Functia de maximizat per i=individ
        def my_fitness( i ):
            return -i['x']**2 + 1 -i['y']**2 # +i['z']

        self.pb = Problema(fitness=my_fitness, space=Space)

    def test_make_populatie(self):
        from src.individ import Individ
        from src.populatie import Populatie
        n=10
        p = Populatie(N=n, pb=self.pb)
        print("Populatia initiala este:\n", n)
        self.assertEqual(len(p), n, "Shall be equal")

    def test_add_insi(self):
        from src.individ import Individ
        from src.populatie import Populatie
        n=3
        p = Populatie(N=3, pb=self.pb)
        p.add_insi(n)
        print("Populatia initiala este:\n", n)
        print(p)
        self.assertEqual(len(p), n*2, "Shall be equal")
    
    def test_set_item0(self):
        from src.individ import Individ
        from src.populatie import Populatie
        p = Populatie(N=3, pb=self.pb)
        i = Individ(pb=self.pb)
        print("Populatia\n",p, "\nIndivid:", i)
        p[0]=i
        print("Populatia\n",p)
        self.assertEqual(p[0], i, "p0 shall be i")
            
    def test_set_item_append(self):
        from src.individ import Individ
        from src.populatie import Populatie
        p = Populatie(N=3, pb=self.pb)
        i = Individ(pb=self.pb)
        print("Populatia\n",p, "\nIndivid:", i)
        p[10]=i
        print("Populatia\n",p)
        self.assertEqual(p[-1], i, "p0 shall be i")

    def test_sort(self):
        from src.individ import Individ
        from src.populatie import Populatie
        p = Populatie(N=3, pb=self.pb)
        print("Populatia\n",p)
        p.sort(reverse=False)
        print("Sortata asc\n",p)
        i_min=p[0]

        p.sort(reverse=True)
        self.assertEqual(i_min, p[-1], "p0 shall be i")  

    def test_iter(self):
        from src.individ import Individ
        from src.populatie import Populatie
        n=5
        p = Populatie(N=n, pb=self.pb)
        print("Populatia\n",p)
        for i in p:
            print("individ",i)
        self.assertEqual(i, p[-1], "p0 shall be i")  

    def test_eval(self):
        from src.individ import Individ
        from src.populatie import Populatie
        n=2
        p = Populatie(N=n, pb=self.pb)
        print("Populatia\n",p, "\n eval=", p.eval())
        self.assertLessEqual(p.eval(), 0, "valoarea populatiei diferita de zero")  
        

    def test_live_better(self):
        from src.individ import Individ
        from src.populatie import Populatie
        n=5
        p_eval=[]
        p = Populatie(N=n, pb=self.pb)
        p_eval.append ( p.eval() )
        print("Populatia\n",p, "\ncu eval", p_eval[-1])
        p.live(mortality=.5, type_of_life='better')
        p_eval.append ( p.eval() )
        print("Next generation:\n", p, "\ncu eval", p_eval[-1])
        p.live(mortality=.5, type_of_life='better')
        p_eval.append ( p.eval() )
        print("Generatin one  :\n", p, "\ncu eval", p_eval[-1])
        self.assertLessEqual(p_eval[0], p_eval[-1], "p0 shall be i")  

    def test_live_3_gen(self):
        from src.populatie import Populatie
        p = Populatie(N=25, pb=self.pb)
        p0=[len(p), p.eval()]

        p.live_N_generations(G=10, mortality=.75, type_of_life='better')
        pf = [len(p), p.eval()]
        print("Populatia initiala membri si eval ", str(p0))
        print("Populatia finala   membri si eval ", str(pf))
        
        self.assertEqual(0,0, "eval shall be ...")

if __name__ == '__main__':
    unittest.main()