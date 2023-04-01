import numpy as np

class HeapMin(list):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def sift(self, i):
        esq = 2*i+1
        dire = 2*i+2
        maior = i
        if esq < self.__len__() and self[esq][0] < self[i][0]:
            maior = esq
        if dire < self.__len__() and self[dire][0] < self[maior][0]:
            maior = dire
        if maior != i:
            aux = self[i]
            self[i] = self[maior]
            self[maior] = aux
            self.sift(maior)

    def min(self):
        return self[0]
    
    def extract_min(self):
        if self.__len__() < 1:
            raise ValueError()
        else:
            maxi = self[0]
            if self.__len__() > 1:
                self[0] = self.pop()
                self.sift(0)
            else:
                self.pop()
            return maxi
        
    def modify(self, k, x):
        if k >= self.__len__() or k < 0:
            raise IndexError()
        else:
            self[k] = x
            while k > 0 and self[int(np.ceil(k / 2)-1)][0] > self[k][0]:
                aux = self[k]
                self[k] = self[int(np.ceil(k / 2)-1)]
                self[int(np.ceil(k / 2)-1)] = aux
                k = int(np.ceil(k / 2) - 1)
            self.sift(k)

    def insert(self, x):
        self.append(x)
        self.modify(self.__len__()-1, x)

    def find(self, x):
        for i in range(self.__len__()):
            if self[i][1] == x:
                return i
        return None
    
class HeapMax(object):
    # def __init_subclass__(cls) -> None:
    #     return super().__init_subclass__()
    def __init__(self, vector):
        self.heap = vector
    
    def sift(self, i):
        esq = 2*i+1
        dire = 2*i+2
        maior = i
        if esq < self.heap.__len__() and self.heap[esq][0] > self.heap[i][0]:
            maior = esq
        if dire < self.heap.__len__() and self.heap[dire][0] > self.heap[maior][0]:
            maior = dire
        if maior != i:
            aux = self.heap[i]
            self.heap[i] = self.heap[maior]
            self.heap[maior] = aux
            self.sift(maior)

    def max(self):
        return self.heap[0]
    
    def extract_max(self):
        if self.heap.__len__() < 1:
            raise ValueError()
        else:
            maxi = self.heap[0]
            if self.heap.__len__() > 1:
                self.heap[0] = self.heap.pop()
                self.sift(0)
            else:
                self.heap.pop()
            return maxi
        
    def modify(self, k, x):
        if k >= self.heap.__len__() or k < 0:
            raise IndexError()
        else:
            self.heap[k] = x
            while k > 0 and self.heap[int(np.ceil(k / 2)-1)][0] < self.heap[k][0]:
                aux = self.heap[k]
                self.heap[k] = self.heap[int(np.ceil(k / 2)-1)]
                self.heap[int(np.ceil(k / 2)-1)] = aux
                k = int(np.ceil(k / 2) - 1)
            self.sift(k)

    def insert(self, x):
        self.heap.append(x)
        self.modify(self.heap.__len__()-1, x)

    def find(self, x):
        for i in range(self.heap.__len__()):
            if self.heap[i][1] == x:
                return i
        return None