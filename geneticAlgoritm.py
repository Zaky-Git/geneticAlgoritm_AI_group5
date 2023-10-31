import random
import math

ra = 10
rb = -10

mutation_rate = 0.1

crossover_rate = 0.7
populasi_size = 10
panjangKromosom = 8
max_generations = 10


# Fungsi untuk menginisialisasi populasi
def inisialisasiPopulasi(sampleSize):
    populasi = []
    for i in range(sampleSize):
        kromosom = []
        for j in range(panjangKromosom):
            kromosom.append(random.randint(0, 9))
        populasi.append(kromosom)
    return populasi

# Fungsi untuk mendekode kromosom menjadi x1 dan x2


def decode(chromosome, ra, rb):
    g = chromosome
    x1 = rb + (((ra-rb)/((9*(10**(-1))) + (9*(10**(-2))) + (9*(10**(-3)))) + (9*(10**(-4))))) * \
        ((g[0]*(10**(-1))) + (g[1]*(10**(-2))) +
         (g[2]*(10**(-3))) + (g[3]*(10**(-4))))
    x2 = rb + (((ra-rb)/((9*(10**(-1))) + (9*(10**(-2))) + (9*(10**(-3)))) + (9*(10**(-4))))) * \
        ((g[4]*(10**(-1))) + (g[5]*(10**(-2))) +
         (g[6]*(10**(-3))) + (g[7]*(10**(-4))))
    return x1, x2


def fitness(x1, x2):
    a = 0.0000001
    if x1 == 0 and x2 == 0:
        return 1/(-(math.sin(x1) * math.cos(x2) + 4/5 * math.exp(1 - math.sqrt(x1**2 + x2**2))) + a)
    else:
        return -(math.sin(x1) * math.cos(x2) + 4/5 * math.exp(1 - math.sqrt(x1**2 + x2**2)))


# Fungsi seleksi orang tua dengan metode roulette wheel


def seleksiOrangTua(population, fitness_values):
    total_fitness = sum(fitness_values)
    roulette_wheel = []

    for i in range(len(population)):
        relative_fitness = fitness_values[i] / total_fitness
        roulette_wheel.append(relative_fitness)

    selected_parents = []
    for j in range(2):
        rand_num = random.random()
        cumulative_prob = 0

        for i in range(len(population)):
            cumulative_prob += roulette_wheel[i]
            if rand_num <= cumulative_prob:
                selected_parents.append(population[i])
                break

    return selected_parents

# Fungsi metode one-point crossover


def crossover(parent1, parent2):
    prob = random.random()
    child1 = []
    child2 = []
    if prob <= crossover_rate:
        i = random.randint(1, 6)
        child1[:i] = parent1[:i]
        child1[i:] = parent2[i:]
        child2[:i] = parent2[:i]
        child2[i:] = parent1[i:]
    else:
        child1 = parent1
        child2 = parent2
    return child1, child2

# Fungsi mutasi metode acak (integer)


def mutasi(chromosome):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = random.randint(0, 9)
    return chromosome


# Fungsi pergantian generasi dengan metode elitisme
def seleksiSurvivorElitisme(populasi):
    new_populasi = []
    fitness_values = [fitness(*decode(chromosome, ra, rb))
                      for chromosome in populasi]

    best_chromosome = populasi[fitness_values.index(max(fitness_values))]
    new_populasi.append(best_chromosome)
    while len(new_populasi) < populasi_size:
        parent1, parent2 = seleksiOrangTua(populasi, fitness_values)
        if random.random() < crossover_rate:
            child1, child2 = crossover(parent1, parent2)
            child1 = mutasi(child1)
            child2 = mutasi(child2)
            new_populasi.extend([child1, child2])

    return new_populasi[:populasi_size]

# Fungsi genetika utama dengan pergantian generasi elitisme


def genetic_algorithm():
    populasi = inisialisasiPopulasi(populasi_size)
    best_chromosome = None
    best_fitness = float('-inf')  # Inisialisasi dengan negatif tak hingga
    best_x1, best_x2 = None, None

    for generation in range(max_generations):
        populasi = seleksiSurvivorElitisme(populasi)
        print("Generasi", generation + 1)
        for i, chromosome in enumerate(populasi):
            x1, x2 = decode(chromosome, ra, rb)
            fit = fitness(x1, x2)
            if fit > best_fitness:
                best_fitness = fit
                best_chromosome = chromosome
                best_x1, best_x2 = x1, x2
            print(
                f"Individu {i + 1} - Chromosome: {chromosome}, x1: {x1}, x2: {x2}, Fitness: {fit}")
        print("")

    return best_chromosome, best_fitness, best_x1, best_x2


best_chromosome, best_fitness, best_x1, best_x2 = genetic_algorithm()

print("Best Chromosome:", best_chromosome)
print("Best Fitness:", best_fitness)
print("Best x1:", best_x1)
print("Best x2:", best_x2)
