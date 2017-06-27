# File: genetic.py
#    from chapter 6 of _Genetic Algorithms with Python_
#
# Author: Clinton Sheppard <fluentcoder@gmail.com>
# Copyright (c) 2016 Clinton Sheppard
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.

import random
import statistics
import sys
import time
import math


def _generate_parent( maxGeneGroupSize, geneSet, get_fitness):
    genes = geneSet
#    while len(genes) < length:
#        sampleSize = min(length - len(genes), len(geneSet))
#        genes.extend(random.sample(geneSet, sampleSize))
    fitness = get_fitness(genes, math.ceil(len(genes)/maxGeneGroupSize), maxGeneGroupSize)
    return Chromosome(genes, fitness)


def _mutate(parent, geneSet, get_fitness):
    childGenes = parent.Genes[:]
    index = random.randrange(0, len(parent.Genes))
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    fitness = get_fitness(childGenes)
    return Chromosome(childGenes, fitness)


def _mutate_custom(parent, custom_mutate, get_fitness, maxGeneGroupSize):
    childGenes = parent.Genes[:]
    
    childGenes = custom_mutate(childGenes, maxGeneGroupSize)
    
    fitness = get_fitness(childGenes,math.ceil(len(childGenes)/maxGeneGroupSize), \
                          maxGeneGroupSize)
    return Chromosome(childGenes, fitness)


def get_best(get_fitness, targetLen, maxGeneGroupSize, optimalFitness, geneSet, display,
             custom_mutate=None, maxAge=None):
    if custom_mutate is None:
        def fnMutate(parent, maxGeneGroupSize):
            return _mutate(parent, geneSet, get_fitness, maxGeneGroupSize)
    else:
        def fnMutate(parent, maxGeneGroupSize):
            return _mutate_custom(parent, custom_mutate, get_fitness, maxGeneGroupSize)

    def fnGenerateParent():
        return _generate_parent(maxGeneGroupSize, geneSet, get_fitness)

    for improvement in _get_improvement(fnMutate, fnGenerateParent, maxGeneGroupSize, maxAge):
        display(improvement)
        if not optimalFitness < improvement.Fitness:
            return improvement
        elif (improvement.Age >= maxAge):
            return improvement


def _get_improvement(new_child, generate_parent, maxGeneGroupSize, maxAge):
    bestParent = parent = generate_parent()
    
    while True:
        child = new_child(parent, maxGeneGroupSize)
        
        bestParent.Age += 1
        
        if parent.Fitness < child.Fitness:
            if maxAge is None:
                continue    
            if maxAge > bestParent.Age:
                continue
            else:
                yield bestParent
                break
        
        if parent.Fitness > child.Fitness:
            if bestParent.Fitness > child.Fitness:
                child.Age = bestParent.Age
                bestParent = child    
                yield child
            
            parent = child


class Chromosome:
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness
        self.Age = 0

    def __str__(self):
        return "Fitness : {} Age: {} ".format(
            self.Fitness,
            self.Age)

        

class Benchmark:
    @staticmethod
    def run(function):
        timings = []
        stdout = sys.stdout
        for i in range(100):
            sys.stdout = None
            startTime = time.time()
            function()
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            mean = statistics.mean(timings)
            if i < 10 or i % 10 == 9:
                print("{} {:3.2f} {:3.2f}".format(
                    1 + i, mean,
                    statistics.stdev(timings, mean) if i > 1 else 0))
