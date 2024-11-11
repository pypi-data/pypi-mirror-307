from src.ebat.evaluation.helpers import check_same_length


def false_acceptance_rate(y_true, y_pred):
    """
    How often an attacker is mistaken for a legitimate user.
    :param y_true: bool 1D list of ground truth accepted/rejected authentication requests.
    :param y_pred: bool 1D list of predicted accepted/rejected authentication requests.
    :return: float false acceptance rate.
    """
    check_same_length(y_true, y_pred)
    return sum(
        [1 if not true and pred else 0 for true, pred in zip(y_true, y_pred)]
    ) / len(y_true)


def false_rejection_rate(y_true, y_pred):
    """
    How often a legitimate user is mistaken for an attacker.
    :param y_true: bool 1D list of ground truth accepted/rejected authentication requests.
    :param y_pred: bool 1D list of predicted accepted/rejected authentication requests.
    :return: float false rejection rate.
    """
    check_same_length(y_true, y_pred)
    return sum(
        [1 if true and not pred else 0 for true, pred in zip(y_true, y_pred)]
    ) / len(y_true)


if __name__ == "__main__":
    print(
        false_acceptance_rate([False, False, False, False], [True, False, False, True])
    )
    print(
        false_rejection_rate([False, False, False, False], [True, False, False, True])
    )
    print(false_acceptance_rate([True, True, True, True], [True, False, False, True]))
    print(false_rejection_rate([True, True, True, True], [True, False, False, True]))
