import streamlit as st
import pandas as pd
import numpy as np
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
import nbformat
import matplotlib


@st.cache_data
def load_doc():
    st.title("MEDBLAST Topic Modeling")

    df2023 = pd.read_csv("clean2023.csv")
    df2022 = pd.read_csv("clean2022.csv")
    df2021 = pd.read_csv("clean2021.csv")
    df2020 = pd.read_csv("clean2020.csv")
    df2019 = pd.read_csv("clean2019.csv")
    df2018 = pd.read_csv("clean2018.csv")

    dfs = [df2023, df2022, df2021, df2020, df2019, df2018]
    df = pd.concat(dfs)
    return list(df["Title_Abstract"].astype(str))[:]


@st.cache_data
def load_model():
    MODEL_NAME = "BERTOPIC_MEDBLAST"
    embeddings = np.load(f"{MODEL_NAME}-embedded.npy")
    topic_model = BERTopic.load(f"{MODEL_NAME}", embedding_model=embeddings)
    return topic_model


@st.cache_data
def load_embed():
    MODEL_NAME = "BERTOPIC_MEDBLAST"
    embeddings = np.load(f"{MODEL_NAME}-embedded.npy")
    return embeddings


docs = load_doc()
topic_model = load_model()
embeddings = load_embed()
MODEL_NAME = "BERTOPIC_MEDBLAST"

st.title("bert topic")

st.subheader("Topics Visualization")

st.write(topic_model.visualize_topics())


# Visualize hierarchy
st.subheader("Hierarchy Visualization")
st.write(topic_model.visualize_hierarchy())


st.subheader("barChart Visualization")
st.write(topic_model.visualize_barchart())

st.subheader("heatMap Visualization")
st.write(topic_model.visualize_heatmap())

st.subheader("termRank Visualization")
st.write(topic_model.visualize_term_rank())
st.write(topic_model.visualize_term_rank(log_scale=True))

st.subheader("hierarchical_topics Visualization")
hierarchical_topics = topic_model.hierarchical_topics(docs)
topic_model.visualize_hierarchical_documents(
    docs, hierarchical_topics, embeddings=embeddings
)
# Reduce dimensionality of embeddings, this step is optional but much faster to perform iteratively:
reduced_embeddings = UMAP(
    n_neighbors=7, n_components=2, min_dist=0.7, metric="cosine",  learning_rate=2, 
).fit_transform(embeddings)
st.write(
    topic_model.visualize_hierarchical_documents(
        docs, hierarchical_topics, reduced_embeddings=reduced_embeddings
    )
)


# st.subheader("Mat Visualization")
# topic_distr, topic_token_distr = topic_model.approximate_distribution(
#     docs, calculate_tokens=True
# )

# # Visualize the token-level distributions
# df = topic_model.visualize_approximate_distribution(docs[1], topic_token_distr[1])
# st.write(df)

# # Visualize documents
# st.subheader("Documents Visualization")
# visualize_documents(df["Title_Abstract"].astype(str), topic_model, embeddings=None)

# # Visualize other aspects (e.g., barchart, heatmap, term rank)
# st.subheader("Other Visualizations")
# visualize_other(topic_model)
