import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt


def visualize_path(path, reduced_embeddings, all_words_df, target):
    # Create figure if it doesn't exist yet
    if not hasattr(visualize_path, 'fig'):
        visualize_path.fig = go.FigureWidget()
    
    # Clear existing traces
    visualize_path.fig.data = []
    
    # Add all points as background
    visualize_path.fig.add_trace(go.Scatter3d(
        x=reduced_embeddings[:, 0],
        y=reduced_embeddings[:, 1], 
        z=reduced_embeddings[:, 2],
        mode='markers',
        name='All articles',
        marker=dict(
            color='lightgray',
            size=3,
            opacity=0.3
        ),
        text=all_words_df['article'],
        hoverinfo='text'
    ))
    
    # Get indices of path words
    path_indices = []
    target_index = None
    for word in path:
        matches = all_words_df[all_words_df['article'] == word]
        if not matches.empty:
            path_indices.append(matches.index[0])
        else:
            print(f"Warning: Word '{word}' not found in all_words_df")
            return None
    
    target_index = all_words_df[all_words_df['article'] == target].index[0]

    if not path_indices:
        print("No valid words found in path")
        return None
        
    # Add path points
    visualize_path.fig.add_trace(go.Scatter3d(
        x=reduced_embeddings[path_indices, 0],
        y=reduced_embeddings[path_indices, 1],
        z=reduced_embeddings[path_indices, 2],
        mode='markers+lines+text',
        name='Path',
        marker=dict(
            color='red',
            size=5,
            symbol='circle'
        ),
        line=dict(
            color='red',
            width=2
        ),
        text=[f"{p}" for p in path],
        textposition="top center",
        hoverinfo='text'
    ))
    
    # Add start point with larger marker
    visualize_path.fig.add_trace(go.Scatter3d(
        x=[reduced_embeddings[path_indices[0], 0]],
        y=[reduced_embeddings[path_indices[0], 1]],
        z=[reduced_embeddings[path_indices[0], 2]],
        mode='markers+text',
        name='Start',
        marker=dict(
            color='green',
            size=8,
            symbol='circle'
        ),
        text=[f"{path[0]}"],
        textfont=dict(
            color='green',
            size=12
        ),
        textposition="top center",
        hoverinfo='text'
    ))
    
    # Add end point with larger marker
    visualize_path.fig.add_trace(go.Scatter3d(
        x=[reduced_embeddings[target_index, 0]],
        y=[reduced_embeddings[target_index, 1]],
        z=[reduced_embeddings[target_index, 2]],
        mode='markers+text',
        name='End',
        marker=dict(
            color='blue', 
            size=8,
            symbol='circle'
        ),
        text=[f"{target}"],
        textfont=dict(
            color='blue',
            size=12
        ),
        textposition="top center",
        hoverinfo='text'
    ))
    
    # Add arrows using annotations
    for i in range(len(path) - 1):
        # Get start and end points
        x1, y1, z1 = reduced_embeddings[path_indices[i]]
        x2, y2, z2 = reduced_embeddings[path_indices[i + 1]]
        
        # Midpoint of the arrow
        xmid = x2 - 0.1 * (x2 - x1)
        ymid = y2 - 0.1 * (y2 - y1)
        zmid = z2 - 0.1 * (z2 - z1)
        
        # Direction vector
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        
        # Normalize the direction vector to make arrow size consistent
        magnitude = (dx**2 + dy**2 + dz**2)**0.5
        if magnitude > 0:  # Avoid division by zero
            dx_normalized = dx / magnitude
            dy_normalized = dy / magnitude
            dz_normalized = dz / magnitude
        else:
            dx_normalized, dy_normalized, dz_normalized = 0, 0, 0
        
        # Add cone to visualize the arrow
        visualize_path.fig.add_trace(go.Cone(
            x=[xmid],
            y=[ymid],
            z=[zmid],
            u=[dx_normalized],
            v=[dy_normalized],
            w=[dz_normalized],
            colorscale=[[0, 'red'], [1, 'red']],
            showscale=False,
            sizemode="absolute",  # Make size independent of vector length
            sizeref=1  # Adjust for fixed size (tweak as needed)
        ))

    
    visualize_path.fig.update_layout(
        scene=dict(
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                title="",
                backgroundcolor='rgba(0,0,0,0)'
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                title="",
                backgroundcolor='rgba(0,0,0,0)'
            ),
            zaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                title="",
                backgroundcolor='rgba(0,0,0,0)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        legend=dict(
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5,
            orientation="h"
        ),
        showlegend=True,
        width=800,
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return visualize_path.fig


# Function to create path visualization
def visualize_path_2D(path, reduced_embeddings, all_words_df, target):
    # Create figure
    fig = go.Figure()
    
    # Add all points as background
    fig.add_trace(go.Scatter(
        x=reduced_embeddings[:, 0],
        y=reduced_embeddings[:, 1],
        mode='markers',
        name='All articles',
        marker=dict(
            color='lightgray',
            size=5,
            opacity=0.3
        ),
        text=all_words_df['article'],
        hoverinfo='text'
    ))
    
    # Get indices of path words
    path_indices = []
    target_index = None
    for word in path:
        matches = all_words_df[all_words_df['article'] == word]
        if not matches.empty:
            path_indices.append(matches.index[0])
        else:
            print(f"Warning: Word '{word}' not found in all_words_df")
            return None
    
    target_index = all_words_df[all_words_df['article'] == target].index[0]

    if not path_indices:
        print("No valid words found in path")
        return None
        
    # Add path points
    fig.add_trace(go.Scatter(
        x=reduced_embeddings[path_indices, 0],
        y=reduced_embeddings[path_indices, 1],
        mode='markers+lines',
        name='Path',
        marker=dict(
            color='red',
            size=8,
            symbol='circle'
        ),
        line=dict(
            color='red',
            width=2
        ),
        text=path,
        hoverinfo='text'
    ))
    
    # Add start point with larger marker
    fig.add_trace(go.Scatter(
        x=[reduced_embeddings[path_indices[0], 0]],
        y=[reduced_embeddings[path_indices[0], 1]],
        mode='markers',
        name='Start',
        marker=dict(
            color='green',
            size=15,
            symbol='circle'
        ),
        text=[path[0]],
        hoverinfo='text'
    ))
    
    # Add end point with larger marker
    fig.add_trace(go.Scatter(
        x=[reduced_embeddings[target_index, 0]],
        y=[reduced_embeddings[target_index, 1]],
        mode='markers',
        name='End',
        marker=dict(
            color='blue', 
            size=15,
            symbol='circle'
        ),
        text=[target],
        hoverinfo='text'
    ))
    
    # Add arrows using annotations
    for i in range(len(path)-1):
        x1, y1 = reduced_embeddings[path_indices[i], 0], reduced_embeddings[path_indices[i], 1]
        x2, y2 = reduced_embeddings[path_indices[i+1], 0], reduced_embeddings[path_indices[i+1], 1]
        
        # Calculate arrow position (midpoint)
        fig.add_annotation(
            x=x2,
            y=y2,
            ax=x1,
            ay=y1,
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='red'
        )
    
    # Update layout
    fig.update_layout(
        title=f"Path Visualization in Embedding Space",
        xaxis_title="Dimension 1",
        yaxis_title="Dimension 2",
        showlegend=True,
        width=800,
        height=600
    )
    
    return fig


def draw_condensed_graph(G):
    # Find strongly connected components
    strongly_connected = list(nx.strongly_connected_components(G))

    # Find the largest component
    largest_component = max(range(len(strongly_connected)), key=lambda x: len(strongly_connected[x]))

    # Filter components and identify isolated components
    filtered_components = []
    isolated_nodes_in = set()  # Nodes with only incoming edges to main component
    isolated_nodes_out = set() # Nodes with only outgoing edges from main component
    isolated_nodes_totally = set() # Nodes that are completely isolated

    for i, comp in enumerate(strongly_connected):
        if len(comp) > 1:
            filtered_components.append(comp)
        elif i != largest_component:  # Size 1 component that's not the largest
            # Check direction of connections with largest component
            has_incoming = False
            has_outgoing = False
            for node in comp:
                for main_node in strongly_connected[largest_component]:
                    if G.has_edge(node, main_node):
                        has_outgoing = True
                    if G.has_edge(main_node, node):
                        has_incoming = True
            
            if has_incoming and not has_outgoing:
                isolated_nodes_in.update(comp)
            elif has_outgoing and not has_incoming:
                isolated_nodes_out.update(comp)
            elif not has_incoming and not has_outgoing:
                isolated_nodes_totally.update(comp)
            else:
                filtered_components.append(comp)

    # Add isolated nodes as separate components
    if isolated_nodes_in:
        filtered_components.append(isolated_nodes_in)
    if isolated_nodes_out:
        filtered_components.append(isolated_nodes_out)
    if isolated_nodes_totally:
        filtered_components.append(isolated_nodes_totally)

    # Create a new graph of filtered strongly connected components
    scc_graph = nx.DiGraph()
    for i in range(len(filtered_components)):
        scc_graph.add_node(i)

    # Add edges between components
    for i, comp1 in enumerate(filtered_components):
        for j, comp2 in enumerate(filtered_components):
            if i != j:
                if any(G.has_edge(u, v) for u in comp1 for v in comp2):
                    scc_graph.add_edge(i, j)

    # Draw the condensed graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(scc_graph,k=10,iterations=1000)
    pos = {node: (coords[0]*1.5, coords[1]*1.5) for node, coords in pos.items()}

    # Prepare node colors and sizes
    node_colors = []
    node_sizes = []
    labels = {}
    for n in scc_graph.nodes():
        if filtered_components[n] == isolated_nodes_in:
            node_colors.append('red')
            node_sizes.append(100*len(filtered_components[n]))
            labels[n] = f"incoming isolated\n(size: {len(filtered_components[n])})"
        elif filtered_components[n] == isolated_nodes_out:
            node_colors.append('orange')
            node_sizes.append(2*len(filtered_components[n]))
            labels[n] = f"outgoing isolated\n(size: {len(filtered_components[n])})"
        elif filtered_components[n] == isolated_nodes_totally:
            node_colors.append('gray')
            node_sizes.append(2*len(filtered_components[n]))
            labels[n] = f"totally isolated\n(size: {len(filtered_components[n])})"
        else:
            node_colors.append('lightgreen' if len(filtered_components[n]) > 1 else 'lightblue')
            node_sizes.append(2*len(filtered_components[n]) if len(filtered_components[n]) > 1000 else 100*len(filtered_components[n]))
            labels[n] = str(len(filtered_components[n]))

    nx.draw(scc_graph, pos,
            node_color=node_colors,
            node_size=node_sizes,
            with_labels=False,
            arrows=True,
            edge_color='gray',
            alpha=0.7)

    nx.draw_networkx_labels(scc_graph, pos, labels, font_size=8)

    with open(f'largest_component.txt', 'w') as f:
        for node in strongly_connected[largest_component]:
            f.write(f"{node}\n")

    plt.title("Condensed Graph of Strongly Connected Components")
    plt.show()