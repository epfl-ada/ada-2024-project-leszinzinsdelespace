def get_closest_neighbor_similarity(mask, all_words_df, article_similarities):
    """
    Iteratively find the closest neighbor for active points based on a similarity matrix,
    link them, and mark the chosen points as inactive.

    Parameters
    ----------
    mask : array-like of bool
        A boolean array indicating which points are currently active (True = active, False = inactive).
    all_words_df : pandas.DataFrame
        A DataFrame containing at least a column 'article' corresponding to each index.
    article_similarities : pandas.DataFrame
        A DataFrame representing the similarity matrix between articles. It should be aligned with all_words_df.

    Returns
    -------
    links : list of tuples
        Each tuple contains (source_article, target_article) representing the chosen closest pairs.
    """
    # Ensure mask is a boolean array
    mask = mask.astype(bool)
    links = []

    # Continue until no active points remain
    while mask.any():
        similarities = []
        active_points = np.where(mask)[0]

        # Iterate over each active point
        for point in tqdm(active_points, desc="Processing active points"):
            # Get similarity row for this point
            similarity_row = article_similarities.iloc[point]

            sorted_indices = np.argsort(-similarity_row.values)

            # Filter out active indices (we only want neighbors that are not in the mask)
            valid_indices = sorted_indices[~mask[sorted_indices]]

            # Take the nearest valid neighbor
            nearest_index = valid_indices[0]
            nearest_neighbor = all_words_df.iloc[nearest_index]['article']

            # Store tuple: (similarity, source_index, target_article)
            similarities.append((similarity_row.iloc[nearest_index], point, nearest_neighbor))

        # If no similarities found for any active point, break out to avoid infinite loop
        if len(similarities) == 0:
            break

        # Sort by similarity in descending order and select the highest similarity pair
        sorted_similarities = sorted(similarities, key=lambda x: x[0], reverse=True)
        closest_pair = sorted_similarities[0]

        # Add the chosen link
        source_article = all_words_df.iloc[closest_pair[1]]['article']
        target_article = closest_pair[2]
        links.append((source_article, target_article))

        # Deactivate the chosen source point
        mask[closest_pair[1]] = False

    return links
