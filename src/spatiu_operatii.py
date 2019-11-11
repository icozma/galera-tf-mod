
class SpatiuOps:

    def __init__(self, operanzi, operatori_unari, operatori_binari):
        self.Space = {}
        self.Space['f1'] = operatori_unari # functii de un param
        # self.Space['f2'] = operatori_binari # functii de doi params
        # self.Space['o0'] = operanzi  # coeficienti
        self.Space['o1'] = operanzi  # features
        # self.Space['o2'] = [(a,b) for a in self.Space['o'] for b in self.Space['o']]
        # self.Space['o3'] = [(a,b,c) for a in self.Space['o'] for b in self.Space['o'] for c in self.Space['o']]


    def val(self):
        ret = 0
        for f in self.Space['o1']:
            ret += 1

        return 0



