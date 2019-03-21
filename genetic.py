import random
import math

#         Coop | Defect
#    Coop -1,-1| -20,0
#         ------------
#  Defect 0,-20| -10,-10

#   Always Defect
#   Always Coop
#   Random
#   Tit for Tat


# Inputs : Last Resp, 2nd last Resp, 3rd last Resp
# output : Response (defect, Coop)

# Initial output + 2 for 2nd turn + 4 for third turn + 8 for rest

# 1 is coop 2 is defect

# No Offset
# -         0

# Offset 1
# 0         1
# 1         2

# Offset 3
# 00        3
# 01        4
# 10        5
# 11        6

# Offset 7
# 000       7
# 001       8
# 010       9
# 011       10
# 100       11
# 101       12
# 110       13
# 111       14

# the formula for the number of pairs formed by x breeders is y = (x^2 - x) / 2
# this means that to find out the number of breeders needed for x pairs you must
# the mutation rate used when mutating species.
# this is unrelated to the combination process.
mutation_rate = 0.001

# this is the number of instances in each generation
# this tells the program how many instances are needed when combining and mutating instances.
breeder_count = 32
generation_size = ((breeder_count * breeder_count) - breeder_count) / 2

# this is the number of rounds used when simulating
num_rounds = 10

# this is the number of generations we will create
num_generations = 10000
t = 100;


class Instance(object):
    id = 0
    generation = 0
    genes = []
    score = 0

    def to_string(self):
        result = str(self.generation)
        for i in self.genes:
            result += "," + str(i)
        return result

    def from_string(self, string):
        arr = string.split(',')
        self.generation = arr[0]
        self.genes = arr[1::]

    def __init__(self):
        global t
        t = t + 1
        self.id = t
        self.generation = 0
        self.genes = []
        for i in range(0, 15, 1):
            self.genes.append(random.randint(0, 1))
        # print str(len(self.genes))


# Takes two instances as arguments, returns a new instance with a generation number one higher than it's parents
def breed(p, b):
    result = Instance()
    result.generation = p.generation + 1
    result.genes = []
    for i in range(0, 15, 1):
        if random.randint(0, 1) == 1:
            result.genes.append(p.genes[i])
        else:
            result.genes.append(b.genes[i])
        if random.randint(0, math.floor(1.0/mutation_rate)) == 1:
            result.genes[i] = 0 if (result.genes[i] == 1) else 1
    # print "B: " + str(len(result.genes))
    return result


# this simulates "num_rounds" rounds between two instances a and b. returns score
def simulate(p, b):

    p_score = 0;
    b_score = 0;

    def round(x,y):
        if x and y:
            return -1, -1
        if x and not y:
            return -20, 0
        if not x and not y:
            return -20, -20
        if not x and y:
            return 0, -20

    p_resp = []
    b_resp = []
    for i in range(0, num_rounds - 1):
        pa = 0
        ba = 0

        if i == 0:
            pa = p.genes[0]
            ba = b.genes[0]
        if i == 1:
            pa = p.genes[b_resp[0] + 1]
            ba = b.genes[p_resp[0] + 1]
        if i == 2:
            pn = (b_resp[0] * 2) + b_resp[1]
            bn = (p_resp[0] * 2) + p_resp[1]
            pa = p.genes[pn + 3]
            ba = b.genes[bn + 3]
        if i > 2:
            pn = (b_resp[i - 3] * 4) + (b_resp[i - 2] * 2) + b_resp[i - 1]
            bn = (p_resp[i - 3] * 4) + (p_resp[i - 2] * 2) + p_resp[i - 1]
            pa = p.genes[pn + 7]
            ba = b.genes[bn + 7]

        n, m = round(pa, ba)
        p_score += n
        b_score += m
        p_resp.append(pa)
        b_resp.append(ba)

    return p_score, b_score


# running the simulations


generations_a = []
generations_a.append([])
generations_b = []
generations_b.append([])
generations_c = []
generations_c.append([])

for i in range(1, generation_size):
    generations_a[0].append(Instance())
    generations_b[0].append(Instance())
    generations_c[0].append(Instance())

for i in range(0, num_generations):

    for a in range(0, generation_size - 1):

        g, h = simulate(generations_a[i][a], generations_b[i][a])
        generations_a[i][a].score += g
        generations_b[i][a].score += h
        g, h = simulate(generations_a[i][a], generations_c[i][a])
        generations_a[i][a].score += g
        generations_c[i][a].score += h
        g, h = simulate(generations_b[i][a], generations_c[i][a])
        generations_b[i][a].score += g
        generations_c[i][a].score += h

    breeding_pool_a = []
    breeding_pool_b = []
    breeding_pool_c = []

    for j in range(0, breeder_count):

        highest_a = generations_a[i][0]
        highest_b = generations_b[i][0]
        highest_c = generations_c[i][0]

        for k in range(0, generation_size - breeder_count):
            # print str(generation_size) + ":" + str(k)
            if generations_a[i][k].score > highest_a.score:
                highest_a = generations_a[i][k]
            if generations_b[i][k].score > highest_b.score:
                highest_b = generations_b[i][k]
            if generations_c[i][k].score > highest_c.score:
                highest_c = generations_c[i][k]

        breeding_pool_a.append(highest_a)
        breeding_pool_b.append(highest_b)
        breeding_pool_c.append(highest_c)
        if j == 0:
            print "######################"
            print "Generation: " + str(i)
            print "Best A:  " + str((-1.0 * highest_a.score) // (2.0 * num_rounds))
            print "Best B:  " + str((-1.0 * highest_b.score) // (2.0 * num_rounds))
            print "Best C:  " + str((-1.0 * highest_c.score) // (2.0 * num_rounds))
        generations_a[i].remove(highest_a)
        generations_b[i].remove(highest_b)
        generations_c[i].remove(highest_c)

    generations_a.append([])
    generations_b.append([])
    generations_c.append([])
    while len(breeding_pool_a) != 0:

        temp_a = breeding_pool_a[0]
        temp_b = breeding_pool_b[0]
        temp_c = breeding_pool_c[0]

        breeding_pool_a.remove(temp_a)
        breeding_pool_b.remove(temp_b)
        breeding_pool_c.remove(temp_c)

        for inst in breeding_pool_a:
            generations_a[i+1].append(breed(temp_a, inst))
        for inst in breeding_pool_b:
            generations_b[i+1].append(breed(temp_b, inst))
        for inst in breeding_pool_c:
            generations_c[i+1].append(breed(temp_c, inst))
