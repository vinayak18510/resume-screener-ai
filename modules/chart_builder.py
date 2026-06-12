# modules/chart_builder.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_skill_frequency_chart(skill_freq: dict, title: str = 'Skill Frequency') -> go.Figure:
    """Generates horizontal metrics distributions styled using dark-theme configurations."""
    if not skill_freq:
        fig = go.Figure()
        fig.add_annotation(text='No skills detected', showarrow=False, font=dict(size=16, color='gray'))
        return fig
        
    df = pd.DataFrame(list(skill_freq.items()), columns=['Skill', 'Count'])
    df = df.sort_values('Count', ascending=True)
    
    fig = px.bar(
        df, x='Count', y='Skill', orientation='h', title=title,
        color='Count', color_continuous_scale='Viridis',
        labels={'Count': 'Frequency', 'Skill': 'Skill'}
    )
    
    fig.update_layout(
        paper_bgcolor='#0F172A', plot_bgcolor='#1E293B',
        font=dict(color='white', size=11),
        title_font=dict(size=16, color='#22D3EE'),
        height=max(300, len(df) * 30),
        margin=dict(l=0, r=20, t=40, b=20)
    )
    return fig

def create_match_gauge(score: float) -> go.Figure:
    """Generates a gauge visualization displaying the match percentage."""
    fig = go.Figure(go.Indicator(
        mode='gauge+number', value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': 'Match Score', 'font': {'color': 'white', 'size': 18}},
        number={'suffix': '%', 'font': {'color': 'white', 'size': 40}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'white'},
            'bar': {'color': '#6366F1'},
            'bgcolor': '#1E293B',
            'steps': [
                {'range': [0, 40], 'color': '#EF4444'},
                {'range': [40, 60], 'color': '#F59E0B'},
                {'range': [60, 80], 'color': '#6366F1'},
                {'range': [80, 100], 'color': '#10B981'}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor='#0F172A', height=280, margin=dict(l=20, r=20, t=40, b=20))
    return fig