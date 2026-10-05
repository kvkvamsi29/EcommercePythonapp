def generate_features_from_specs(specs):
    features = []

    if "Display" in specs:
        features.append(f"Immersive {specs['Display']} display")

    if "Chipset" in specs:
        features.append(f"Powered by {specs['Chipset']}")

    if "Battery" in specs:
        features.append(f"Long-lasting {specs['Battery']} battery")

    if "Camera" in specs:
        features.append("Advanced camera system")

    if "5G" in specs.get("Technology", ""):
        features.append("5G connectivity support")

    return features
