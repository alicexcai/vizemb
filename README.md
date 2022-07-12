# VizEmbedding

VizEmbedding is a data visualization tool allows users to explore connections betewen items in any kind of database. The tool casts rich statical and semantic data into an embedding space and allows users to explore dimensions along which they want to visualize connections.

Examples of embedding space dimensions include semantics (text and natural language meaning), date / time, location, and other calculated metrics.

## Database Structure

VizEmbedding works for any data formatted with the simple schema:
| Item Title | Item Property #1 | Item Property #2 | Item Property #n |
| ---- | ---- | ---- | ---- |
| ... | ... | ... | ... |


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
* API client to pull data from web databases
* Data processer to standardize data
* Semantic embedder to calculate embeddings for semantic data
* Quantitative embedder to calculate embeddings for quantitative data
* General embedder to integrate embeddings for all data
* Network generator to generate network data from embeddings 