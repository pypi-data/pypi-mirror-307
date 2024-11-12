import os

with open(os.path.join(os.path.dirname(__file__), "version"), mode="r") as fp:
    __version__ = fp.readline().rstrip()

# We import some functions/classes for ease of reference.
from mirabolic.cdf.cdf_tools import cdf_plot
from mirabolic.cdf.qq_plot import qq_plot
from mirabolic.rates.rate_tools import rate_comparison
from mirabolic.llm_embeddings.llm_embedder import llm_embedder
from mirabolic.llm_embeddings.llm_tools import LLM_API
