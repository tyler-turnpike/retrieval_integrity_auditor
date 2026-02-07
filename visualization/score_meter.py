import plotly.graph_objects as go


def create_score_meter(score):
    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            gauge={"axis": {"range": [0, 100]}}
        )
    )
