"""Information Retrieval metrics

Useful Resources:
http://www.cs.utexas.edu/~mooney/ir-course/slides/Evaluation.ppt
http://www.nii.ac.jp/TechReports/05-014E.pdf
http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
http://hal.archives-ouvertes.fr/docs/00/72/67/60/PDF/07-busa-fekete.pdf
Learning to Rank for Information Retrieval (Tie-Yan Liu)
"""

def mean_reciprocal_rank(rs):
    """Score is reciprocal of the rank of the first relevant item

    First element is 'rank 1'.  Relevance is binary (nonzero is relevant).

    Example from http://en.wikipedia.org/wiki/Mean_reciprocal_rank
    >>> rs = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    >>> mean_reciprocal_rank(rs)
    0.61111111111111105
    >>> from numpy import asarray
    >>> rs = asarray([[0, 0, 0], [0, 1, 0], [1, 0, 0]])
    >>> mean_reciprocal_rank(rs)
    0.5
    >>> rs = [[0, 0, 0, 1], [1, 0, 0], [1, 0, 0]]
    >>> mean_reciprocal_rank(rs)
    0.75

    Args:
        rs: Iterator of relevance scores (list or numpy) in rank order
            (first element is the first item)

    Returns:
        Mean reciprocal rank
    """
    from numpy import asarray, mean
    rs = (asarray(r).nonzero()[0] for r in rs)
    return mean([1. / (r[0] + 1) if r.size else 0. for r in rs])


def r_precision(r):
    """Score is precision after all relevant documents have been retrieved

    Relevance is binary (nonzero is relevant).

    >>> r = [0, 0, 1]
    >>> r_precision(r)
    0.33333333333333331
    >>> r = [0, 1, 0]
    >>> r_precision(r)
    0.5
    >>> r = [1, 0, 0]
    >>> r_precision(r)
    1.0

    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)

    Returns:
        R Precision
    """
    from numpy import asarray, mean
    r = asarray(r) != 0
    z = r.nonzero()[0]
    if not z.size:
        return 0.
    return mean(r[:z[-1] + 1])


def precision_at_k(r, k):
    """Score is precision @ k

    Relevance is binary (nonzero is relevant).

    >>> r = [0, 0, 1]
    >>> precision_at_k(r, 1)
    0.0
    >>> precision_at_k(r, 2)
    0.0
    >>> precision_at_k(r, 3)
    0.33333333333333331
    >>> precision_at_k(r, 4)
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    ValueError: Relevance score length < k


    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)

    Returns:
        Precision @ k

    Raises:
        ValueError: len(r) must be >= k
    """
    from numpy import asarray, mean
    assert k >= 1
    r = asarray(r)[:k] != 0
    if r.size != k:
        raise ValueError('Relevance score length < k')
    return mean(r)


def average_precision(r):
    """Score is average precision (area under PR curve)

    Relevance is binary (nonzero is relevant).

    >>> r = [1, 1, 0, 1, 0, 1, 0, 0, 0, 1]
    >>> delta_r = 1. / sum(r)
    >>> sum([sum(r[:x + 1]) / (x + 1.) * delta_r for x, y in enumerate(r) if y])
    0.7833333333333333
    >>> average_precision(r)
    0.78333333333333333

    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)

    Returns:
        Average precision
    """
    from numpy import asarray, mean
    r = asarray(r) != 0
    out = [precision_at_k(r, k + 1) for k in range(r.size) if r[k]]
    if not out:
        return 0.
    return mean(out)


def mean_average_precision(rs):
    """Score is mean average precision

    Relevance is binary (nonzero is relevant).

    >>> rs = [[1, 1, 0, 1, 0, 1, 0, 0, 0, 1]]
    >>> mean_average_precision(rs)
    0.78333333333333333
    >>> rs = [[1, 1, 0, 1, 0, 1, 0, 0, 0, 1], [0]]
    >>> mean_average_precision(rs)
    0.39166666666666666

    Args:
        rs: Iterator of relevance scores (list or numpy) in rank order
            (first element is the first item)

    Returns:
        Mean average precision
    """
    from numpy import mean
    return mean([average_precision(r) for r in rs])


def dcg_at_k(scores):
    """Score is discounted cumulative gain (dcg)

    Relevance is positive real values.  Can use binary
    as the previous methods.

    Example from
    http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
    >>> scores = [3, 2]
    >>> dcg_at_k(scores)
    5.0
    >>> scores = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
    >>> dcg_at_k(scores)
    9.605117739188811

    Args:
        scores: Relevance scores (list or numpy) in rank order
                (first element is the first item)

    Returns:
        Discounted cumulative gain
    """
    from numpy import log2
    return scores[0] + sum(sc / log2(ind) for sc, ind in zip(scores[1:], range(2, len(scores)+1)))


def ndcg_at_k(predicted_scores, user_scores):
    """Score is normalized discounted cumulative gain (ndcg)

    Relevance is positive real values.  Can use binary
    as the previous methods.

    Example from
    http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf

    >>> predicted1 = [.4, .1, .8]
    >>> predicted2 = [.0, .1, .4]
    >>> predicted3 = [.4, .1, .0]
    >>> actual = [.8, .4, .1, .0]
    >>> ndcg_at_k(predicted1, actual[:3])
    0.7954630596952451
    >>> ndcg_at_k(predicted2, actual[:3])
    0.2789754264360057
    >>> ndcg_at_k(predicted3, actual[:3])
    0.3958536780387228

    Args:
        predicted_scores:   Relevance scores (list or numpy) in rank order
                            (first element is the first item)
        user_scores:        The actual scores

    Returns:
        Normalized discounted cumulative gain
    """
    assert len(predicted_scores) == len(user_scores)
    idcg = dcg_at_k(sorted(user_scores, reverse=True))
    return (dcg_at_k(predicted_scores) / idcg) if idcg > 0.0 else 0.0


if __name__ == "__main__":
    import doctest
    doctest.testmod()
