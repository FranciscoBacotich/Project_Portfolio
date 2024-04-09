import os
import random
import re
import sys


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    transition_probabilities = {}
    num_pages = len(corpus)

    # If the current page has no outgoing links, choose randomly among all pages
    if not corpus[page]:
        return {p: 1 / num_pages for p in corpus}

    # Assign probability for choosing any page at random without following a link
    random_prob = (1 - damping_factor) / num_pages
    for p in corpus:
        transition_probabilities[p] = random_prob

    # Assign probabilities for following links from the current page
    links_prob = damping_factor / len(corpus[page])
    for link in corpus[page]:
        transition_probabilities[link] = transition_probabilities.get(link, 0) + links_prob

    # Normalize probabilities
    normalization_factor = sum(transition_probabilities.values())
    transition_probabilities = {p: prob / normalization_factor for p, prob in transition_probabilities.items()}

    return transition_probabilities

    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    visit_count = {page: 0 for page in corpus}

    # Choose a random starting page
    current_page = random.choice(list(corpus.keys()))

    # Perform random walks to generate samples
    for _ in range(n):
        visit_count[current_page] += 1
        transition_probs = transition_model(corpus, current_page, damping_factor)
        next_page = random.choices(list(transition_probs.keys()), weights=transition_probs.values())[0]
        
        # Update the current page for the next iteration
        current_page = next_page

    # Calculate the PageRank estimates based on the visit counts
    pagerank = {page: count / n for page, count in visit_count.items()}

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    num_pages = len(corpus)
    pagerank = {page: 1 / num_pages for page in corpus}

    def calculate_pagerank(page):
        # Calculate the sum of PageRank values from pages that link to the current page
        linking_pageranks = sum(pagerank[link] / len(corpus[link]) for link in corpus if page in corpus[link])

        # Calculate the new PageRank for the current page based on the iterative formula
        new_pagerank = (1 - damping_factor) / num_pages + damping_factor * linking_pageranks

        return new_pagerank

    # Iteratively update PageRank values until convergence
    while True:
        old_pagerank = pagerank.copy()

        pagerank = {page: calculate_pagerank(page) for page in corpus}

        # Check for convergence by comparing old and new PageRank values
        if all(abs(old_pagerank[page] - pagerank[page]) < 0.001 for page in corpus):
            break

    return pagerank


if __name__ == "__main__":
    main()
