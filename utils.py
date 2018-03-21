# Each of the scoring functions calls this function to normalize its result
# Return value between 0 and 1
def normalize_scores(scores, small_is_better = False):
    small = 0.00001 # Avoid division by zero errors    
    if small_is_better:
        min_score = min(scores.values())
        return dict([(key, float(min_score)/max(small, score)) for key, score in scores.items()])
    else:
        max_score = max(scores.values())
        return dict([(key, float(score)/max_score) for key, score in scores.items()])

def unity_based_normalization(scores):
    min_score = min(scores.values())
    max_score = max(scores.values())
    return dict([(key, (float(score)-min_score)/(max_score - min_score)) for key, score in scores.items()])
