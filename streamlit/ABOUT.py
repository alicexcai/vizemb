import streamlit as st

st.markdown("""
# VizEmb

VizEmb is a data visualization tool allows users to explore connections betewen items in any kind of database. The tool casts rich statical and semantic data into an embedding space and allows users to explore dimensions along which they want to visualize connections.

Examples of embedding space dimensions include semantics (text and natural language meaning), date / time, location, and other calculated metrics.

---
## Database Structure

VizEmb works for any data with a generic item-property schema:
| Item Title | Property #1 | Property #2 | Property #n |
| ---- | ---- | ---- | ---- |
| ... | ... | ... | ... |

---
A little pre-processing is required to make sure the data is in the correct format. 
1. Make sure you have an ID (by index) and TITLE column for each item in your database.
2. If you have a DATE column, make sure it is in an acceptable date format (e.g. YYYY).
3. Make sure all data within each column is formatted consistently.
4. Add a prefix to each column header to indicate what type of data the column contains. The labels are as follows:
    * id - ID column
    * title - TITLE column
    * date - DATE column
    * quant - quantitative data to analyze
    * sem - semantic data to analyze
    * cat - categorical data to analyze
    * info - additional information about the item, not analyzed

Your processed database should look something like this:
| [id] ID | [title] TITLE | [date] DATE | [quant] Property #1 | [sem] Property #2 | [quant] Property #3 | [cat] Property #4 | [info] Property #5 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| ... | ... | ... | ... | ... | ... | ... | ... |

---
## Usage

1. Pre-process your data to make sure it is in a supported format.
2. Load your database into the data directory, or via the web app.
3. Select the properties you would like to include in your visualization.
4. Generate embeddings.
5. Use the parameter module, filtering module, and comparison module to manipulate your visualization as desired.

## Software Architecture

**Frontend components:**
* Parameter module to let users choose parameters for their network
    * Variable weights for each embedding dimension to manipulate their graph (check box toggle dimensions on and off)
    * Variable network visualization parameters, such as number of relevant nodes to show, colors, etc. (include other graph types later?)
* Filtering module to let users filter by item or item properties
    * Search box to let users search for items by name to see their local network graphs
    * Multisearch to highlight item locations within the embedding space
    * Filter by property to only show collections of items with specific properties
* Comparison mmodule to let users compare two items
    * Ordered list of similarity metrics across embedding dimensions with color map representation, normalized against the entire database
* Main network graph
    * Selected item box that displays data on clicked items

**Backend components:**
* Data processer to standardize data
* Semantic embedder to calculate embeddings for semantic data
* Quantitative embedder to calculate embeddings for quantitative data
* General embedder to integrate embeddings for all data
""")