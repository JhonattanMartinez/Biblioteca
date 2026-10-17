"""Gráficas del dashboard con Plotly, generadas 100 % en Python."""
import textwrap
import plotly.graph_objects as go
from django.utils.safestring import mark_safe
BLUE = '#2a78d6'
STATUS_COLORS = {
    'active': ('En curso', '#2a78d6'),
    'overdue': ('Vencidos', '#d03b3b'),
    'returned': ('Devueltos', '#0ca30c'),
    'cancelled': ('Cancelados', '#898781'),
}
INK, MUTED, GRID = '#0b0b0b', '#52514e', '#e1e0d9'
def _headroom(values):
    return [0, max(max(values, default=0), 1) * 1.2]
def _layout(fig, height=320):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=30, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='system-ui, -apple-system, "Segoe UI", sans-serif', color=MUTED, size=13),
        showlegend=False,
        bargap=0.45,
        hoverlabel=dict(bgcolor='#fcfcfb', font_color=INK),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, showline=False)
    return fig
def _html(fig, first):
    chart = fig.to_html(
        full_html=False,
        include_plotlyjs='cdn' if first else False,
        config={'displayModeBar': False, 'responsive': True},
        post_script='window.addEventListener("load", function () { Plotly.Plots.resize("{plot_id}"); });',
    )
    return mark_safe(f'<div style="height:{fig.layout.height}px">{chart}</div>')
def loans_per_month(series, first=False):
    fig = go.Figure(go.Bar(
        x=[label for label, _ in series], y=[n for _, n in series],
        marker_color=BLUE, text=[n for _, n in series], textposition='outside',
        hovertemplate='%{x}: %{y} préstamos<extra></extra>', cliponaxis=False,
    ))
    fig.update_yaxes(range=_headroom(n for _, n in series))
    return _html(_layout(fig), first)
def loans_by_status(status_counts, first=False):
    order = ['active', 'overdue', 'returned', 'cancelled']
    fig = go.Figure(go.Bar(
        y=[STATUS_COLORS[k][0] for k in order],
        x=[status_counts[k] for k in order],
        orientation='h',
        marker_color=[STATUS_COLORS[k][1] for k in order],
        text=[status_counts[k] for k in order], textposition='outside',
        hovertemplate='%{y}: %{x}<extra></extra>', cliponaxis=False,
    ))
    fig.update_yaxes(autorange='reversed', gridcolor='rgba(0,0,0,0)')
    fig.update_xaxes(showgrid=True, gridcolor=GRID, range=[0, max(100, _headroom(status_counts.values())[1])])
    return _html(_layout(fig, height=260), first)
def top_books(pairs, first=False):
    pairs = pairs[::-1]
    fig = go.Figure(go.Bar(
        y=['<br>'.join(textwrap.wrap(t, 22)) for t, _ in pairs], x=[n for _, n in pairs],
        orientation='h', marker_color=BLUE,
        text=[n for _, n in pairs], textposition='outside', cliponaxis=False,
        customdata=[t for t, _ in pairs],
        hovertemplate='%{customdata}: %{x} préstamos<extra></extra>',
    ))
    fig.update_yaxes(gridcolor='rgba(0,0,0,0)', automargin=True)
    fig.update_xaxes(showgrid=True, gridcolor=GRID, range=_headroom(n for _, n in pairs))
    return _html(_layout(fig, height=420), first)
def loans_by_category(pairs, first=False):
    fig = go.Figure(go.Bar(
        x=[c for c, _ in pairs], y=[n for _, n in pairs],
        marker_color=BLUE, text=[n for _, n in pairs], textposition='outside',
        hovertemplate='%{x}: %{y} préstamos<extra></extra>', cliponaxis=False,
    ))
    fig.update_yaxes(range=_headroom(n for _, n in pairs))
    return _html(_layout(fig), first)
