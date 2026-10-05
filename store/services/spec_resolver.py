def normalize(name):
    return name.lower().replace(" ", "").replace("-", "")

def find_specs(product_name, spec_dataset):
    norm_name = normalize(product_name)

    for key, specs in spec_dataset.items():
        if normalize(key) in norm_name or norm_name in normalize(key):
            return specs

    return None
