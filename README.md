
# Saving Christmas - Understanding User Frustration in Wikispeedia

## Abstract

Wikispeedia engages users in associative thinking - following links based on their perception of which concepts they believe are connected. However, players often believe they’re on the brink of victory, only to find a crucial link mysteriously missing. This leads to frustration, as the expected path ends abruptly. Players backtrack and seek an alternative path, since the one they believed to be the obvious shortest path turns out to be a dead-end. This pattern of user behavior points to missing semantic links, in cases where the semantic distance turns out to be very different from the mathematical shortest path. This is incredibly visible in one particular game of Wikispeedia where the player initially started on the Bob Dylan article with “Christmas” as the goal article and went through articles like  “Winter”, “Snow”, “Santa Claus” without ever finding a link to “Christmas”. One can only begin to imagine the frustration and confusion of the player at that point. This situation stemmed from the fact that the “Christmas” article simply does not exist…

## Research Questions

**What indicators signal user frustration in information-seeking tasks, and how can these be quantified?**

- How does user backtracking reflect unmet expectations in navigating a hyperlink network?
- What insights can the difficulty rating of a completed path provide about the semantic distance between concepts?

**How does the structure of a hyperlink network affect user navigation and the perception of semantic distance?**

- Are high difficulty ratings associated with sparse or missing connections between seemingly related topics?
- To what extent do incomplete paths indicate gaps in semantic linking within the network?

**How can semantic distance be used to improve hyperlink networks and enhance user experience?**

- How does computed semantic distance between concepts compare to user-perceived similarity in navigation paths?
- What cosine similarity threshold (fixed or variable) can indicate when a link is missing between two concepts, and how might this be applied as a tool for network improvement?

**What challenges arise in differentiating between genuinely related and superficially similar concepts in a hyperlink network?**

- How might terms with similar titles but different meanings (e.g., “Basil” vs. “Common Basilisk”) affect user navigation and frustration?

**Is there a pattern that can create a feeling of “closeness” to the end ? Can this create frustration in the user if there is no ending path ?** 

Other ideas we explored initially but subsequently dropped: 

- We initially considered focusing solely on backtracking behavior, but decided that we wish to deepen our understanding of user behavior. We expanded our search to user frustration in general.
- We considered visualizing the progress of players in real time at each path position as a probability tree.

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
- **Step 4 - Building the Final Narrative**
    - Using all the data relating to backtracking behavior and frustration in general, we build a datastory around missing semantic links and the dark side of Wikispeedia: links that are mysteriously missing from an article where they most definitely should be present,  goal articles that do not exist at all, shortest paths that have little to do with the logical and intuitive connection between concepts.
- **Step 5 (Optional) - Linking User Frustration to Semantic Distances**
    - If we have sufficient time, we would like to further explore user frustration and precisely compute statistics relative to what makes players give up using information from unfinished paths and combining them with the evolution of the semantic distance to the target article (at what point was the maximum cosine similarity reached). This would potentially allow us to know why each unfinished path remained unfinished, which could be useful for players as well as for the creators of the game.
- **Step 6 - Wrapping up**
    - Final changes: cleaning the project repository and finalizing the results webpage.

## Proposed Timeline

- 18.10.24 - 25.10.14: Step 1 - Initial Data Exploration and Data Cleaning
- 25.10.24 - 08.11.24: Step 2 & 3- Data Exploration, Analyzing Backtracking Behavior
- 08.11.24 - 15.11.24: Step 3 & 4 - Analyzing User Frustration Patterns of Behavior, Building a Semantic Distance Matrix and Finding Missing Links, Building the Final Narrative
- 15.11.24 → : Step (5 &) 6 - Wrapping Up, Final Results Webpage

## Organization within the team

- Albert & Hugo - Data Exploration and Cleaning, Semantic distance analysis, Evaluating the performance of different models, computing the semantic distance matrix.
- Khadija & Elena - Data Exploration and Visualization, Building the narrative, Final Webpage, Wrapping Up.
- Tania - Link between hormonal paths and their leading to frustration, backtracks, and giving up on the game. Webpage redaction.

| Team Member/Step | 1 | 2 | 3 | 4 | 5 (Optional) | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| Albert | X | X | X | X | X |  |
| Hugo | X | X | X | X | X |  |
| Khadija | X | X |  |  | X | X |
| Elena | X | X |  |  | X | X |
| Tania | X | X | X |  | X | X |

## Questions for TAs (optional)

- Is our analysis deep enough or is it too superficial ? How far should we go ?
- Is there something obvious and fundamental in our reasoning and analysis that we have missed ?
- How can we quantitatively distinguish between missing semantic links versus expected detours in user navigation? Are there recommended benchmarks or thresholds for identifying a "critical missing link" in a network?
- Are there established metrics in information-seeking literature that could help quantify user frustration more robustly? Would incorporating path completion times enhance our analysis?

---
