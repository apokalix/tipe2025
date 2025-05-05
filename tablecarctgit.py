## Création tableau d'young + rep pour chaque classe
import itertools
import copy
import math
N=10 #variable globale pour la table

def hashe(l): #inutile
    res=0
    n=len(l)
    for k in range (n):
        res+=l[k]*(10**(n-k-1))
    return res




#### créer le tableau


def gen_partitions(n):
    #Génère toutes les partitions de n sous forme de listes de taille n avec zéros à droite.
    def helper(n, max_part, current):
        if n == 0:
            partitions.append(current + [0] * (original_n - len(current)))
            return
        for i in range(min(n, max_part), 0, -1):
            helper(n - i, i, current + [i])

    partitions = []
    original_n = n
    helper(n, n, [])
    res=sorted(partitions)
    res.reverse()
    return res


def cycles_to_permutation(cycles, n):
    #Transforme une liste de cycles en une permutation sous forme de liste.
    #Les cycles sont des listes d'entiers.
    perm = list(range(1, n + 1))
    for cycle in cycles:
        if len(cycle) <= 1:
            continue
        for i in range(len(cycle)):
            perm[cycle[i - 1] - 1] = cycle[i]
    return perm

def young_shape_to_cycles(partition):

   # Donne les cycles associés à chaque ligne du diagramme de Young
    # pour une partition donnée, en remplissant ligne par ligne avec 1 à n.

    counter = 1
    cycles = []
    for row_len in partition:
        if row_len > 0:
            cycle = list(range(counter, counter + row_len))
            if len(cycle) > 1:
                cycles.append(cycle)
            counter += row_len
    return cycles

def young_shape_to_permutation(partition):
    n = sum(partition)
    cycles = young_shape_to_cycles(partition)
    perm = cycles_to_permutation(cycles, n)
    return perm



##

def applique(rep,element): #element type set
    res=set()
    for k in range (len(rep)):
        if k+1 in element:
            res.add(rep[k])
    return res

def pseudeq(l1,l2):
    set1=set()
    set2=set()
    for k in l1:
        set1.add(frozenset(k))
    for k in l2:
        set2.add(frozenset(k))
    return set1==set2

def generate_young_partitions(partition): #fait par ia
    n = sum(partition)
    base_set = set(range(1, n + 1))

    # On ignore la première ligne
    sub_partition = partition[1:]
    sub_partition = [k for k in sub_partition if k > 0]

    if not sub_partition:
        return [[]]  # Rien à générer

    def helper(remaining_elements, remaining_sizes):
        if not remaining_sizes:
            return [[]]
        results = []
        first_size = remaining_sizes[0]
        for combo in combinations(remaining_elements, first_size):
            new_remaining = remaining_elements - set(combo)
            for rest in helper(new_remaining, remaining_sizes[1:]):
                results.append([set(combo)] + rest)
        return results

    return helper(base_set, sub_partition)




def nbinvariant(drap,rep): #drap est une liste de drapeaux (set)
    res=0
    for d in drap:
        test=True
        for k in range (len(d)):
            current=set()
            for i in range(N):
                if i+1 in d[k]:
                    current.add(rep[i])
            if current!=d[k]:
                test=False
        if test:
            res+=1
    return res



#### GENERE TOUS LES DRAPEAUX

def generate_flags_from_partition(partition, n=N): #fait par ia
    """
    Génère tous les drapeaux ensemblistes strictement croissants à partir
    d'une partition (en ignorant la première ligne).

    :param partition: Partition de Young, ex: [4,1,1]
    :param n: Taille de l'ensemble {1,..,n}
    :return: Liste des drapeaux
    """
    # Exclure la première ligne
    lines = partition[1:]
    lines = [l for l in lines if l > 0]
    sizes = [sum(lines[:i+1]) for i in range(len(lines))]  # tailles cumulées

    all_flags = []

    # Générer tous les ensembles finaux possibles
    for full_set in itertools.combinations(range(1, n+1), sizes[-1]):
        full_set = set(full_set)

        # Trouver tous les sous-ensembles strictement croissants avec tailles imposées
        def build_flags(prev_set, remaining_sizes, available_elements):
            if not remaining_sizes:
                return [[]]
            current_size = remaining_sizes[0]
            result = []
            for subset in itertools.combinations(available_elements, current_size):
                subset_set = set(subset)
                if prev_set < subset_set:  # inclusion stricte
                    rest_flags = build_flags(subset_set, remaining_sizes[1:], available_elements)
                    for rf in rest_flags:
                        result.append([subset_set] + rf)
            return result

        # Initialiser à ensemble vide
        flags = build_flags(set(), sizes, full_set)
        all_flags.extend(flags)

    return all_flags






## CALCUL KHI PRIME

def khiprime(ty): #ty ligne i<nb de classes d'eq = nb tab young
    classes=gen_partitions(N) #pourrait (devrait) etre variable globale
    representants = [young_shape_to_permutation(k) for k in classes]
    res=[]
    drapo=generate_flags_from_partition(ty,N)
    for j in range(len(classes)): #colonne j de la table de caractere (ligne i)
        r=representants[j]
        u=nbinvariant(drapo,r)
        res.append(u)
    return res


## PRODUIT SCALAIRE DE DEUX CARACTERES


def cardclass(partition):
    n=len(partition)
    res=1
    for k in range (1,n+1):
        u=partition.count(k)
        res*= math.factorial(u)*(k**u)
    return int( math.factorial(n)/res)



def prod(ca,cb): #ca et cb deux listes de caracteres ordonnées ordre young
    classes=gen_partitions(N) #pourrait (devrait) etre variable globale
    res=0
    for i in range (len(classes)):
        res+=cardclass(classes[i])*ca[i]*cb[i]
    return int(res/math.factorial(N))



## Programme recursif pour calculer table entière

def moins(a,b):
    res=[0 for k in range(len(a))]
    for k in range(len(a)):
        res[k]=a[k]-b[k]
    return res

def scal(s,l):
    res=[0 for i in range(len(l))]
    for k in range(len(l)):
        res[k]=s*l[k]
    return res

def tablecaract():
    classes=gen_partitions(N)
    classes=classes[1:]
    res=[[1 for i in range(len(classes)+1)]]
    for k in range(len(classes)):
        print(k)
        khip=khiprime(classes[k])
        khi=khip
        for pred in res:
            scalaire=prod(khip,pred)
            khi=moins(khi,scal(scalaire,pred))
        res.append(khi)

    return res



print(tablecaract())



