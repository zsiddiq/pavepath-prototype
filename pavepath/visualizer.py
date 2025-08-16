import matplotlib.pyplot as plt

def visualize_route_scores(segment_scores: list):
    segments = [s['segment'] for s in segment_scores]
    scores = [s['score'] for s in segment_scores]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(segments, scores, color=['red' if s > 6 else 'green' for s in scores])
    plt.axhline(y=6, color='orange', linestyle='--', label='Risk Threshold')
    plt.xlabel('Segment')
    plt.ylabel('Hazard Score')
    plt.title('Route Hazard Analysis')
    plt.legend()
    plt.show()
