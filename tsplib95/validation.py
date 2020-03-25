

def validate(data):
    errors = []
    if data.get('EDGE_WEIGHT_TYPE') == 'EXPLICIT':
        counts = get_matrix_stream_lengths(data['DIMENSION'])
        if data['EDGE_WEIGHT_FORMAT'] == 'FULL_MATRIX':
            expected = counts['full']
        elif 'DIAG' in data['EDGE_WEIGHT_FORMAT']:
            expected = counts['diag']
        else:
            expected = counts['half']

        num_weights = len(data['EDGE_WEIGHT_SECTION'])
        if num_weights != expected:
            if (num_weights == expected + 1 and
                    data['EDGE_WEIGHT_SECTION'][0] == data['DIMENSION']):
                data['EDGE_WEIGHT_SECTION'].pop(0)
            else:
                message = 'found {num_weights} edge weights (expected {expected})'
                error = ValidationError('EDGE_WEIGHT_SECTION', message)
                errors.append(error)



def get_matrix_stream_lengths(dimension):
    full = dimension * dimension
    half = (full - dimension) // 2
    return {
        'full': full,
        'half': half,
        'diag': half + dimension,
    }
