from .models import Gist

def search_gists(db_connection, **kwargs):
    from .models import Gist

DATETIME_PREFIXES = ('created_at', 'updated_at')


def is_datetime_param(param):
    for prefix in DATETIME_PREFIXES:
        if param.startswith(prefix):
            return True
    return False
#If no parameter is provided, all the gists in the database should be returned. If `public_id` or `created_at` parameters are provided, you should filter your SELECT query based on them.
def get_operator(comparison):
    return {
        'lt': '<',
        'lte': '<=',
        'gt': '>',
        'gte': '>=',
    }[comparison]

def build_query(**kwargs):
    query = 'SELECT * FROM gists'
    values = {}
    if kwargs:
        filters = []
        for param, value in kwargs.items():
            if is_datetime_param(param):
                if '__' in param:
                    attribute, comparison = param.split('__')
                    operator = get_operator(comparison)
                    filters.append(
                        'datetime(%s) %s datetime(:%s)' % (
                            attribute, operator, param))
                else:
                    attribute = param
                    filters.append(
                        'datetime(%s) == datetime(:%s)' % (
                            attribute, param))
                values[param] = value
            else:
                filters.append(
                    '%s = :%s' % (
                        param, param))
                values[param] = value

        query += ' WHERE '
        query += ' AND '.join(filters)

    return query, values

def search_gists(db_connection, **kwargs):
    query, params = build_query(**kwargs)
    cursor = db_connection.execute(query, params)
    results = []
    for gist in cursor:
        results.append(Gist(gist))
    return results