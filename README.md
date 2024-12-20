
# Saving Christmas - Understanding User Frustration in Wikispeedia

## Datastory 🔗

- https://epfl-ada.github.io/ada-2024-project-leszinzinsdelespace/

## Quick Start 🚀
```bash
# Clone the repository
git clone https://github.com/epfl-ada/ada-2024-project-leszinzinsdelespace.git

# Change into the project directory
cd ada-2024-project-leszinzinsdelespace

# Install dependencies
pip install -r requirements.txt

# Run the main application or script
python results.ipynb

```

## Abstract

Wikispeedia engages users in associative thinking - following hyperlinks trying to reach a target article in the fewest possible clicks. But what happens when the path you think should exist... doesn't?  Players often believe they’re on the brink of victory, only to find a crucial link mysteriously missing. This leads to frustration, as the expected path ends abruptly. Players backtrack and seek an alternative path, since the one they believed to be the obvious shortest path turns out to be a dead-end. This pattern of user behavior points to missing semantic links, in cases where the semantic distance turns out to be very different from the mathematical shortest path. This is incredibly visible in one particular game of Wikispeedia where the player initially started on the Bob Dylan article with “Christmas” as the goal article and went through articles like  “Winter”, “Snow”, “Santa Claus” without ever finding a link to “Christmas”. One can only begin to imagine the frustration and confusion of the player at that point. This situation stemmed from the fact that the “Christmas” article simply does not exist…
  

## Research Questions

**What indicators signal user frustration in information-seeking tasks, and how can these be quantified?**

- How does user backtracking reflect unmet expectations in navigating a hyperlink network?
- What insights can the difficulty rating of a completed path provide about the semantic distance between concepts?
- How do players behave when encountering dead-ends?
- What patterns emerge in backtracking behavior?
- How does game duration correlate with number of backtracks?

**How does the structure of a hyperlink network affect user navigation and the perception of semantic distance?**

- Are high difficulty ratings associated with sparse or missing connections between seemingly related topics?
- To what extent do incomplete paths indicate gaps in semantic linking within the network?
- What percentage of articles are unreachable from the main network?
- How do semantic relationships compare to existing hyperlinks?
- Where are the critical gaps in article connectivity?


**How can semantic distance be used to improve hyperlink networks and enhance user experience?**

- How can we identify missing semantic links?
- How does computed semantic distance between concepts compare to user-perceived similarity in navigation paths?
- What cosine similarity threshold (fixed or variable) can indicate when a link is missing between two concepts, and how might this be applied as a tool for network improvement?
- What criteria should we use for adding new connections?
- How can we maintain game difficulty while eliminating impossible paths?


**What challenges arise in differentiating between genuinely related and superficially similar concepts in a hyperlink network?**

- How might terms with similar titles but different meanings (e.g., “Basil” vs. “Common Basilisk”) affect user navigation and frustration?

**Is there a pattern that can create a feeling of “closeness” to the end? Can this create frustration in the user if there is no ending path ?** 

Other ideas we explored initially but subsequently dropped: 

- We initially considered focusing solely on backtracking behavior, but decided that we wish to deepen our understanding of user behavior. We expanded our search to user frustration in general.
- We considered visualizing the progress of players in real time at each path position as a probability tree.

**With the study of semantic distance and the obvious lack of links, is there a way of improving the game by adding links between pages without altering the game, and therefore reducing player frustration?** 

- Some pages only seem reachable from certain starting points. Would adding links to make them reachable from any starting point improve the game? 
- What criteria should we use to add semantic links between articles? 
- Can we find a way to connect clusters of articles? 
- Would there be a good way of visualizing the new semantic links added? 

## Proposed additional datasets (optional)

We did not use additional external datasets, however we perhaps would have liked having access to more data relative to the “signal missing link” button at the top right of the webpage. This could be used as an additional metric to assess dead-ends and missing connections. 

What would have been really interesting is to have access to the time spent per position in all paths. This combined with our analysis could really help deepen our understanding of user frustration. 

We did create additional datasets ourselves: embeddings - we embedded each article name using OPEN AI model (large one) so that each one of them can be represented as a vector and the semantic distance matrix : cosine similarities between each article to have an idea of the semantic distance between them. $\text{SD} = |1- \text{CS}|$

## Methods

- **Step 1 - Initial Analysis and Data Cleaning**
    - We start by thoroughly examining the dataset and cleaning the data:
        - Cleaning the time : for each one of the unfinished path with a timeout status : subtract 1800s (timeout time) to the duration
        - Merge the dataset properly to have a global overview with all graphs.
    - We determine a broad direction of exploration based on our initial findings.
      
- **Step 2 - Data Exploration**
    - We initially decided to focus our attention on backtracking behavior, and therefore computed various statistics relative to backtracks. We also plotted different metrics with and without backtracks.
    - By diving in deeper, we discover many missing links (”soybean” to “bean”), and, as it turns out, goal articles that do not exist at all (”Christmas”), therefore sending the player on a wild-goose chase and leading to extreme frustration and many consecutive dead-ends.
      
- **Step 3 - Analyzing User Frustration Patterns of Behavior, Building a Semantic Distance Matrix and Finding Missing Links**
    - We use our analysis of backtracking behavior to analyze how players get closer or further away from their target article, and how their frustration manifests itself through their navigation behavior.
    - We use semantic distance computation using OpenAI’s model. We first compared SentenceBERT, CLIP and GloVe’s performance to choose the model that best suited our needs, and OpenAI’s model gave the most coherent results. We used this model to evaluate how when users change pages by clicking forward or backwards they shorten or lengthen the semantic distance. This combined with the actual shortest path provided indicates differences between the way users perceive connections and how the articles are truly connected.
      
- **Step 4 - Semantic Analysis: Linking User Frustration to Semantic Distances**
    - Explored user frustration and precisely computed statistics relative to what makes players give up using information from unfinished paths and combined them with the evolution of the semantic distance to the target article (at what point was the maximum cosine similarity reached). This would potentially allow us to know why each unfinished path remained unfinished, which could be useful for players as well as for the creators of the game.
    - Compared different embedding models (BERT, GloVe, OpenAI)
    - Created semantic distance matrix for all article pairs
    - Visualized article relationships using t-SNE dimensionality reduction

- **Step 5 - Network Optimization: Fixing Missing Links**
    - To address the issue of missing links in Wikispeedia, we used a semantic similarity-based approach and an iterative algorithm in order to contribute to a better experience of the game and a lower frustration of players. We used an approach based on semantic similarity computation, where each article was represented as a vector in semantic space. We used cosine similarity to measure conceptual proximity between articles and identify isolated articles
    - Articles not connected to the main network but showing high semantic similarity to articles in the main cluster were identified as isolated.
    - At each step, we selected the isolated article with the highest semantic similarity to any article in the main cluster. A link was added between the isolated article and the most similar article in the main cluster. The isolated article, along with any articles already connected to it, was integrated into the main cluster. This process was repeated until all articles were connected to the main network. Using this method, we added 525 carefully chosen links, bridging semantic gaps and making navigation smoother and less frustrating for users.
    - Developed criteria for adding new links based on:
     - Semantic similarity (cosine similarity > 0.5)
     - Article name appearances in content
   - Iteratively connected isolated articles to main network
   - Validated new connections through semantic analysis
     
- **Step 6 - Building the Final Narrative**
    - Using all the data relating to backtracking behavior and frustration in general, plus our solution to reduce the frustration of players, we build a datastory around missing semantic links and the dark side of Wikispeedia: links that are mysteriously missing from an article where they most definitely should be present, goal articles that do not exist at all, shortest paths that have little to do with the logical and intuitive connection between concepts, plus a solution to contribute to a better and less frustated experience.
      
- **Step 7 - Wrapping up**
    - Final changes: cleaning the project repository and finalizing the results webpage. 


## Organization within the team

- Albert & Hugo - Data Exploration and Cleaning, Semantic distance analysis, computing the semantic distance matrix, fixing missing links parts. Connection addition algorithm design.
- Elena - Visualizations, building the narrative. Final results webpage design and development.
- Khadija - Data exploration, evaluating the performance of different models, cleaning of the code.
- Tania - Link between hormonal paths and their leading to frustration, backtracks, and giving up on the game. Webpage redaction.

| Team Member/Step | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|-------------------|---|---|---|---|---|---|---|
| Albert            | X | X | X | X | X |   |   |
| Hugo              | X | X | X | X | X |   | X |
| Khadija           | X | X | X |   |   | X | X |
| Elena             | X | X | X |   |   | X | X |
| Tania             | X | X | X |   |   | X | X |


## Project Structure

The directory structure of our project looks like this:

```bash

├── data                                    <- Project data files
├── assets                                  <- Static assets
│   ├── ada.svg
│   ├── algo_animation.gif
│   ├── dataset.svg
│   ├── graphs/
│   │   ├── averageratingvsbacktracks.png
│   │   ├── distribution_added_links.png
│   │   ├── distribution_current_links.png
│   │   ├── final_strongly_connected.png
│   │   ├── initial_strongly_connected.png
│   │   ├── mediangamedurationvsbacktracks.png
│   │   └── strong_similarity_inarticle_strongly_connected.png
│   ├── interactive/
│   │   ├── isolated_words.html
│   │   └── word_embeddings_with_links.html
│   ├── partiemaudite.png
│   ├── path_evolution.gif
│   ├── path_to_christmas.png
│   └── paths_adjusted_for_length.png
├── index.html                             <- Main webpage
├── script.js                              <- JavaScript functionality
├── styles.css                             <- CSS styling
└── README.md                              <- Project documentation

This structure shows the organization of our website:
- `data/`: Contains the project data files
- `assets/`: Contains all static assets including images, animations, and interactive visualizations
- `index.html`: Main webpage file
- `script.js`: JavaScript code for website functionality
- `styles.css`: CSS styling rules

```

