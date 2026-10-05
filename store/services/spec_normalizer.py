def normalize_specs(spec_list):
    specs = {}

    for section in spec_list:
        for item in section.get("specs", []):
            key = item.get("key")
            val = item.get("val")
            if key and val:
                specs[key] = ", ".join(val)

    return specs
