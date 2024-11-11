# Sometime you want to do the following:
#   1) You are iterating over a list of text strings X. For
#      each x in X:
#       1) Transform x to f(x) (possibly f()=identity map, or f() uses an LLM)
#       2) Embed f(x) with an LLM
#   2) Map down to 2D with t-SNE or UMAP
#   3) Label some different classes of points, such as a special subset
#   4) Plot the 2D result, color by label, and
#      see if they cluster appealingly.
#
# This module facilitates the bookkeeping behind the preceding steps,
# so you only need to specify an iterable X, an (optional) f, and labels L.
#
# Note: we cram everything into this one module, to handle the likely
# case that the user simply copies this file somewhere else :)

import os
import pickle
import datetime
import time
import dotenv
from collections.abc import Iterable
import hashlib
from openai import OpenAI
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

default_model_dict = dict(OpenAI="text-embedding-3-large")

OpenAIClient = None
query_timestamp = {}
API_keys = {}
initialized_LLMs = {}


def stable_hash(s, out_bytes=10):
    # The intrinsic Python "hash" function is constant across a single process but
    # varies between processes. This function tries to give us a more stable
    # hash value.
    m = hashlib.sha256()
    s = str(s).encode("utf-8")
    m.update(s)
    out = m.hexdigest()
    out = out[:out_bytes]  # Drop to 4*out_bytes bits of entropy
    return out


class llm_embedder:

    def __init__(
        self, X=None, f=None, L=None, max_length=None, data_dir="data", use_cache=True
    ):
        self.X = X
        self.f = f
        self.L = L
        self.max_length = max_length
        self.data_dir = data_dir
        self.use_cache = use_cache

        self.record_x = True
        self.record_t = True
        self.path_list = None
        self.embedding_dimension = None
        self.embeddings = None
        self.labels = None
        self.viz_embeddings = {}

        assert X is not None
        assert isinstance(X, Iterable)
        assert not isinstance(X, str)

        if L is not None:
            assert isinstance(L, Iterable)
            if max_length is None:
                try:
                    len1 = len(X)
                    len2 = len(L)
                    has_length = True
                except:
                    has_length = False
                if has_length:
                    if len1 != len2:
                        raise ValueError(f"Length mismatch: {len1} and {len2}")
        self.cache_dir = os.path.join(data_dir, "cache")
        self.pix_dir = os.path.join(data_dir, "pix")
        for d in [self.data_dir, self.cache_dir, self.pix_dir]:
            os.makedirs(d, exist_ok=True)

    def get_llm_embeddings(self):
        if self.L is None:
            Z = self.X
        else:
            Z = zip(self.X, self.L)
        self.path_list = []
        for i, blob in enumerate(Z):
            if self.max_length is not None:
                if i >= self.max_length:
                    break

            if self.L is None:
                x = blob
                l = 0
            else:
                x, l = blob
            fingerprint = str(x)
            if self.f is not None:
                str_f = self.f.__doc__
                if str_f is None:
                    str_f = "None"
                fingerprint += "__" + str_f
            hash_x = stable_hash(fingerprint)
            path = os.path.join(self.cache_dir, f"{hash_x}_emb.pkl")
            self.path_list.append(path)
            if os.path.exists(path) and self.use_cache:
                continue

            datum = dict(x=None, t=None, label=None, embedding=None)
            if self.f is None:
                t = x
            else:
                t = self.f(x)
            e = embedding_API(t, cache_dir=self.cache_dir)
            if self.embedding_dimension is None:
                self.embedding_dimension = len(e)

            if self.record_x:
                datum["x"] = x
            if self.record_t:
                datum["t"] = t
            datum["label"] = l
            datum["embedding"] = e
            with open(path, "wb") as fp:
                pickle.dump(datum, fp)

    def get_embedding_dimension(self):
        if self.embedding_dimension is not None:
            return self.embedding_dimension

        path = self.path_list[0]
        with open(path, "rb") as fp:
            datum = pickle.load(fp)
        return len(datum["embedding"])

    def reduce_to_2d(
        self,
        flavor="UMAP",
        PCA_reduce=False,
        PCA_dim=32,
        random_seed=None,
        flavor_kwargs=None,
    ):
        assert flavor in ["UMAP", "t-SNE"]
        if flavor_kwargs is None:
            flavor_kwargs = {}

        if self.path_list is None:
            raise ValueError("Must run 'get_llm_embeddings' before 'reduce_to_2d'.")

        d = self.get_embedding_dimension()
        N = len(self.path_list)
        self.d = d
        self.N = N

        if flavor == "t-SNE" and N <= 30:
            # Default perplexity==30, but needs perplexity<=N
            # If very small data set, can be a problem, so fix it
            if "perplexity" not in flavor_kwargs:
                flavor_kwargs["perplexity"] = 0.7 * N

        if PCA_reduce == False:
            PCA_dim == d

        if self.embeddings is None or self.labels is None:
            self.embeddings = np.empty((N, d))
            self.labels = np.empty(N).astype(str)

            for i, path in enumerate(self.path_list):
                with open(path, "rb") as fp:
                    datum = pickle.load(fp)
                self.embeddings[i, :] = datum["embedding"]
                self.labels[i] = str(datum["label"])

        if PCA_reduce:
            pca = PCA(n_components=PCA_dim)
            self.reduced_embeddings = pca.fit_transform(self.embeddings)
        else:
            self.reduced_embeddings = self.embeddings

        viz_key = (flavor, PCA_dim, str(flavor_kwargs))
        if viz_key not in self.viz_embeddings:
            if flavor == "UMAP":
                # kwargs: n_neighbors, min_dist, metric,...
                umap = UMAP(n_components=2, random_state=random_seed, **flavor_kwargs)
                self.viz_embeddings[viz_key] = umap.fit_transform(
                    self.reduced_embeddings
                )
            elif flavor == "t-SNE":
                tsne = TSNE(n_components=2, random_state=random_seed, **flavor_kwargs)
                self.viz_embeddings[viz_key] = tsne.fit_transform(
                    self.reduced_embeddings
                )
            else:
                raise ValueError(f"Unknown flavor {flavor}")

    def plot(
        self,
        figsize=(8, 8),
        colormap="hls",
        legend="infer",
        do_savefig=True,
        dpi=400,
        close_fig=False,
    ):
        assert legend in [True, False, "infer"]
        if len(self.viz_embeddings) == 0:
            raise ValueError("Must run 'reduce_to_2d()' first.")
        for viz_key in self.viz_embeddings:
            V = self.viz_embeddings[viz_key]
            plt.figure(figsize=figsize)
            unique_label_list = np.unique(self.labels)
            num_unique_labels = len(unique_label_list)
            color_list = sns.color_palette(colormap, num_unique_labels)
            if legend == "infer":
                legend = len(unique_label_list) <= 20
            for i, unique_label in enumerate(unique_label_list):
                index = self.labels == unique_label
                plt.scatter(
                    V[index, 0], V[index, 1], label=unique_label, color=color_list[i]
                )
            flavor = viz_key[0]
            plt.title(f"LLM Embeddings reduced via {flavor}")
            plt.gca().set_aspect("equal", adjustable="box")
            if legend:
                plt.legend()
            plt.tight_layout()
            if do_savefig:
                plt.savefig(
                    f"scatter_{colormap}_N{self.N}_d{self.d}_"
                    f"L{num_unique_labels}_{flavor}.png",
                    dpi=dpi,
                )
            if close_fig:
                plt.close()

    def run_all(self, llm_kwargs=None, reduce_kwargs=None, plot_kwargs=None, show=True):
        if llm_kwargs is None:
            llm_kwargs = {}
        if reduce_kwargs is None:
            reduce_kwargs = {}
        if plot_kwargs is None:
            plot_kwargs = {}

        self.get_llm_embeddings(**llm_kwargs)
        self.reduce_to_2d(**reduce_kwargs)
        self.plot(**plot_kwargs)

        if show:
            plt.show()


def prepare_API_keys(logger=None):
    global OpenAIClient, initialized_LLMs

    env_str = dict(OpenAI="OPENAI", Google="GEMINI")
    for provider in ["OpenAI"]:
        if initialized_LLMs.get(provider) is not None:
            continue

        # Make sure API key is defined
        if os.environ.get(f"{env_str[provider]}_API_KEY") is None:
            dotenv.load_dotenv(dotenv.find_dotenv())
            API_key = os.environ.get(f"{env_str[provider]}_API_KEY")
            if logger is not None:
                logger.info(f"Loading {provider} API keys to environment...")
            if API_key is None:
                raise ValueError(f"Could not find {provider} API keys")
        # Have to load this again...
        API_key = os.environ.get(f"{env_str[provider]}_API_KEY")

        if provider == "OpenAI":
            OpenAIClient = OpenAI()
        # elif provider == "Google":
        #    genai.configure(api_key=API_key)
        else:
            raise ValueError(f"Unknown provider {provider}")

        initialized_LLMs[provider] = True
    return


model_dict = {}


def get_model(provider=None, model_name=None):
    global model_dict

    if model_dict.get((provider, model_name)) is None:
        raise ValueError("Unspecified provider/model_name")
    return model_dict[(provider, model_name)]


safety_block_string = "Safety Block"


def embedding_API(
    prompt,
    sleep_seconds=0,
    cache=True,
    cache_dir=None,
    provider="OpenAI",
    model_name=None,
    index=0,
    json=False,
    logger=None,
):

    # Note: for OpenAI, response_format = { "type": "json_object" } is useful.
    if model_name is None:
        model_name = default_model_dict[provider]

    if cache:
        os.makedirs(cache_dir, exist_ok=True)

        hash_gpt = stable_hash(
            ":".join(["emb", str(index), provider, model_name, prompt])
        )
        hash_gpt_file = os.path.join(cache_dir, f"{hash_gpt}_gpt.pkl")
        if os.path.exists(hash_gpt_file):
            with open(hash_gpt_file, "rb") as fp:
                blob = pickle.load(fp)
            return blob["reply"]

    prepare_API_keys(logger=logger)

    # Don't flood the LLM server with requests
    now = datetime.datetime.now()

    if query_timestamp.get((provider, model_name)) is not None:
        delay = (
            sleep_seconds
            - (now - query_timestamp[(provider, model_name)]).total_seconds()
        )
        if delay > 0:
            time.sleep(delay)
    query_timestamp[(provider, model_name)] = now

    if provider == "OpenAI":
        if json:
            response_format = {"type": "json_object"}
        else:
            response_format = None

        response = OpenAIClient.embeddings.create(
            model=model_name,
            input=prompt,
            user="SCAMP2024",  # Track what project these tokens are for
        )
        embedding = response.data[0].embedding
    else:
        raise ValueError(f"Unknown provider {provider}")

    if cache:
        with open(hash_gpt_file, "wb") as fp:
            blob = dict(
                prompt=prompt,
                reply=embedding,
                provider=provider,
                model=model_name,
                index=index,
            )
            pickle.dump(blob, fp)
    # Extract text of reply and return it
    return embedding
