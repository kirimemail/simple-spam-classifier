from app import celery


@celery.task
def multiply(a, b):
    """
    Example tasks
    :param a:
    :param b:
    :return:
    """
    return a * b
