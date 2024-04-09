import csv
import itertools
import sys


PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set `have_trait` does not have the trait.
    """

    combined_prob = 1

    for person in people:
        mother = people[person]["mother"]
        father = people[person]["father"]

        parent_probs = {mother: 0, father: 0}

        if mother is None and father is None:
            # No parents listed
            copies_of_gene = 0 if person not in one_gene and person not in two_genes else 1 if person in one_gene else 2
            gene_prob = PROBS['gene'][copies_of_gene]

        else:
            # Parents listed
            for parent in parent_probs:
                if parent not in one_gene and parent not in two_genes:
                    parent_probs[parent] = PROBS['mutation']
                elif parent in one_gene:
                    parent_probs[parent] = (1 - PROBS['mutation']) * 0.5
                elif parent in two_genes:
                    parent_probs[parent] = 1 - PROBS['mutation']

            if person not in one_gene and person not in two_genes:
                copies_of_gene = 0
                gene_prob = (1 - parent_probs[mother]) * (1 - parent_probs[father])
            elif person in one_gene:
                copies_of_gene = 1
                prob1 = parent_probs[mother] * (1 - parent_probs[father])
                prob2 = parent_probs[father] * (1 - parent_probs[mother])
                gene_prob = prob1 * prob2
            elif person in two_genes:
                copies_of_gene = 2
                gene_prob = parent_probs[mother] * parent_probs[father]

        trait_prob = PROBS['trait'][copies_of_gene][True] if person in have_trait else PROBS['trait'][copies_of_gene][False]
        combined_prob *= gene_prob * trait_prob

    return combined_prob







def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
    # Update gene distribution
        gene_count = len(one_gene & {person}) + 2 * len(two_genes & {person})
        probabilities[person]["gene"][gene_count] += p

        # Update trait distribution
        trait_value = True if person in have_trait else False
        probabilities[person]["trait"][trait_value] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Normalize gene distribution
        gene_sum = sum(probabilities[person]["gene"].values())
        for gene_count in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_count] /= gene_sum

        # Normalize trait distribution
        trait_sum = sum(probabilities[person]["trait"].values())
        # Check if trait_sum is not zero before normalization
        if trait_sum != 0:
            for trait_value in probabilities[person]["trait"]:
                probabilities[person]["trait"][trait_value] /= trait_sum


if __name__ == "__main__":
    main()
