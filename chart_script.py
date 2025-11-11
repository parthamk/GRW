
import plotly.graph_objects as go

# Define component positions (x, y coordinates)
positions = {
    'Dev': (0, 3),
    'GitHub': (1.5, 3),
    'Actions': (3, 3),
    'Render': (4.5, 3),
    'Database': (4.5, 1.5),
    'Disk': (4.5, 4.5),
    'Users': (6, 3)
}

# Define connections with labels
connections = [
    ('Dev', 'GitHub', 'git push'),
    ('GitHub', 'Actions', 'trigger'),
    ('Actions', 'Render', 'webhook<br>Docker build'),
    ('Render', 'Database', 'DB queries'),
    ('Render', 'Disk', 'mount<br>storage'),
    ('Render', 'Users', 'HTTP/HTTPS')
]

# Component details
components = {
    'Dev': {'label': 'Local Dev<br>Machine', 'color': '#1FB8CD'},
    'GitHub': {'label': 'GitHub<br>Repository', 'color': '#DB4545'},
    'Actions': {'label': 'GitHub<br>Actions', 'color': '#2E8B57'},
    'Render': {'label': 'Render Web<br>WordPress', 'color': '#5D878F'},
    'Database': {'label': 'MySQL<br>Database', 'color': '#D2BA4C'},
    'Disk': {'label': 'Persistent<br>Disk 10GB', 'color': '#B4413C'},
    'Users': {'label': 'Internet<br>Users', 'color': '#964325'}
}

fig = go.Figure()

# Add arrows (edges)
for start, end, label in connections:
    x0, y0 = positions[start]
    x1, y1 = positions[end]
    
    # Add arrow line
    fig.add_trace(go.Scatter(
        x=[x0, x1],
        y=[y0, y1],
        mode='lines',
        line=dict(color='#333333', width=2),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Add arrowhead
    fig.add_annotation(
        x=x1, y=y1,
        ax=x0, ay=y0,
        xref='x', yref='y',
        axref='x', ayref='y',
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor='#333333',
        text=''
    )
    
    # Add label on arrow
    mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
    fig.add_annotation(
        x=mid_x, y=mid_y,
        text=label,
        showarrow=False,
        font=dict(size=10, color='#13343b'),
        bgcolor='rgba(243, 243, 238, 0.9)',
        bordercolor='#21808d',
        borderwidth=1,
        borderpad=4
    )

# Add nodes (components)
for comp_name, details in components.items():
    x, y = positions[comp_name]
    
    # Add node shape
    fig.add_trace(go.Scatter(
        x=[x],
        y=[y],
        mode='markers+text',
        marker=dict(size=60, color=details['color'], line=dict(color='#13343b', width=2)),
        text=details['label'],
        textposition='middle center',
        textfont=dict(size=11, color='#13343b', family='Arial Black'),
        hoverinfo='text',
        hovertext=comp_name,
        showlegend=False
    ))

# Update layout
fig.update_layout(
    title='WordPress-Render-GitHub Integration',
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 6.5]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.5, 5.5]),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='#F3F3EE'
)

fig.update_traces(cliponaxis=False)

# Save the figure
fig.write_image('architecture.png')
fig.write_image('architecture.svg', format='svg')
