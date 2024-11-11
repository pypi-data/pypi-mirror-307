import mirabolic

# List of common dog breeds
dog_breeds = [
    "Labrador Retriever",
    "German Shepherd",
    "Golden Retriever",
    "Bulldog",
    "Poodle",
    "Beagle",
    "Rottweiler",
    "Yorkshire Terrier",
    "Boxer",
    "Dachshund",
]

# List of common cat breeds
cat_breeds = [
    "Siamese",
    "Persian",
    "Maine Coon",
    "Ragdoll",
    "Bengal",
    "Sphynx",
    "British Shorthair",
    "Abyssinian",
    "Scottish Fold",
    "Russian Blue",
]

common_birds = [
    "Northern Cardinal",
    "American Robin",
    "Blue Jay",
    "House Sparrow",
    "Mourning Dove",
    "European Starling",
    "Black-capped Chickadee",
    "American Goldfinch",
    "Red-winged Blackbird",
    "Downy Woodpecker",
]

data = dog_breeds + cat_breeds + common_birds
labels = (
    len(dog_breeds) * ["dog"]
    + len(cat_breeds) * ["cat"]
    + len(common_birds) * ["birds"]
)


def test1():
    embedder = mirabolic.llm_embedder(X=data, L=labels)
    embedder.run_all()


def test2():
    embedder = mirabolic.llm_embedder(X=data, L=labels)
    # Get embeddings, process, and do UMAP
    embedder.run_all(show=False, plot_kwargs={"close_fig": True})
    # Do t-SNE and plot UMAP + t-SNE
    embedder.run_all(reduce_kwargs={"flavor": "t-SNE"})


def test3():
    # Test out a transformation on the string. Our transformation calls
    # *another* LLM.
    #
    # Note that in order to reduce token costs to LLMs, the code is fairly
    # aggressive about caching. If you change your transformation function,
    # this may be invisible to the system and it will use the previous cached
    # copy instead of applying your new function. To make sure that doesn't
    # happen, the code examines the doc-string for your function, so be sure
    # to change the doc-string when you change the function.
    def f(s):
        """
        Replace the breed or species with a pet name.
        """
        prompt = (
            f"I have a pet {s}. I need a name for my pet that is "
            "some sort of outrageous pun that will reveal its breed or species. "
            "Please reply with one name (and no other text)."
        )
        response = mirabolic.LLM_API(prompt)
        print(f"{s}  =>  {response}")
        return response

    embedder = mirabolic.llm_embedder(X=data, L=labels, f=f)
    embedder.run_all()


if __name__ == "__main__":
    test1()
    test2()
    test3()
