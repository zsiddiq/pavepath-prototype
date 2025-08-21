def score_to_color(score):
    if score > 0.75:
        return 'red'
    elif score > 0.5:
        return 'orange'
    elif score > 0.25:
        return 'yellow'
    else:
        return 'green'
