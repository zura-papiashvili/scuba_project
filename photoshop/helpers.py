# Define parameter limits
ALPHA_LIMIT = (1, 8)
OMEGA_VALUES = ["1", "1/r", "G"]
GAUSSIANSTD_LIMIT = (20, 100)
METHOD_VALUES = ["interp", "poly"]
DEGREE_LIMIT = (3, 11)


def validate_parameters(params):
    # Validate parameters and apply default values if out of bounds
    if not ALPHA_LIMIT[0] <= params["alpha"] <= ALPHA_LIMIT[1]:
        params["alpha"] = 5  # Default value if out of bounds

    if params["omega"] not in OMEGA_VALUES:
        params["omega"] = "1/r"  # Default value if invalid

    if not GAUSSIANSTD_LIMIT[0] <= params["gaussianstd"] <= GAUSSIANSTD_LIMIT[1]:
        params["gaussianstd"] = 50  # Default value if out of bounds

    if params["method"] not in METHOD_VALUES:
        params["method"] = "interp"  # Default value if invalid

    if not DEGREE_LIMIT[0] <= params["degree"] <= DEGREE_LIMIT[1]:
        params["degree"] = 9  # Default value if out of bounds

    return params
