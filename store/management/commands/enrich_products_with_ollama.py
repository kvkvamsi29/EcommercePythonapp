from django.core.management.base import BaseCommand
from store.models.product import Products
import ollama
import json
import re


class Command(BaseCommand):
    help = "Update specs, features, description using Ollama AI with strong fallbacks"

    # =====================================================
    # PROMPT BUILDER
    # =====================================================
    def build_prompt(self, model_name, category):
        return f"""
You are a device specification generator.

Generate REALISTIC, PRACTICAL specifications for this device.

Model: {model_name}
Device type: {category}

Rules:
- Real-world specs only
- No marketing buzzwords
- No emojis
- No assumptions beyond common variants
- STRICT JSON ONLY
- If unsure, choose the most common configuration sold in India

Output format (STRICT):

{{
  "description": "Short real-life daily usage description",
  "features": [
    "feature 1",
    "feature 2",
    "feature 3",
    "feature 4"
  ],
  "specifications": {{
    "display": "",
    "processor": "",
    "memory": "",
    "camera": "",
    "battery": "",
    "software": "",
    "connectivity": "",
    "build": ""
  }}
}}
"""

    # =====================================================
    # CALL OLLAMA SAFELY
    # =====================================================
    def ask_ollama(self, prompt):
        try:
            res = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )

            raw = res["message"]["content"]

            # Extract JSON safely
            match = re.search(r"\{.*\}", raw, re.S)
            if not match:
                return None

            data = json.loads(match.group())

            # Validate structure
            if not isinstance(data, dict):
                return None
            if "description" not in data or "features" not in data or "specifications" not in data:
                return None

            return data

        except Exception:
            return None

    # =====================================================
    # DEVICE CATEGORY GUESS
    # =====================================================
    def guess_category(self, name):
        n = name.lower()
        if any(k in n for k in ["macbook", "laptop", "notebook", "thinkpad", "ideapad"]):
            return "laptop"
        if any(k in n for k in ["ipad", "tablet", "tab", "surface"]):
            return "tablet"
        return "smartphone"

    # =====================================================
    # SAFE FALLBACK SPECS (LAST RESORT)
    # =====================================================
    def fallback_specs(self, category):
        if category == "laptop":
            return {
                "description": "Laptop suitable for office work, browsing, online meetings, and media consumption.",
                "features": [
                    "SSD storage",
                    "Wi-Fi and Bluetooth",
                    "Built-in webcam",
                    "Lightweight design"
                ],
                "specifications": {
                    "display": "14-inch Full HD",
                    "processor": "Intel Core i5 / AMD Ryzen 5",
                    "memory": "8GB RAM",
                    "camera": "HD webcam",
                    "battery": "6–8 hours",
                    "software": "Windows",
                    "connectivity": "Wi-Fi, Bluetooth, USB ports",
                    "build": "Plastic / Aluminum"
                }
            }

        if category == "tablet":
            return {
                "description": "Tablet designed for browsing, video streaming, reading, and light productivity.",
                "features": [
                    "Touchscreen display",
                    "Portable design",
                    "Wi-Fi connectivity",
                    "Long battery life"
                ],
                "specifications": {
                    "display": "10-inch IPS LCD",
                    "processor": "Mid-range ARM chipset",
                    "memory": "4GB RAM",
                    "camera": "8MP rear camera",
                    "battery": "7000 mAh",
                    "software": "Android / iPadOS",
                    "connectivity": "Wi-Fi, Bluetooth",
                    "build": "Metal / Plastic body"
                }
            }

        # Smartphone fallback
        return {
            "description": "Smartphone suitable for calls, social media, photography, and daily entertainment.",
            "features": [
                "5G support",
                "Fast charging",
                "Fingerprint sensor",
                "Large display"
            ],
            "specifications": {
                "display": "6.5-inch AMOLED",
                "processor": "Mid-range mobile processor",
                "memory": "8GB RAM",
                "camera": "50MP dual camera",
                "battery": "5000 mAh",
                "software": "Android",
                "connectivity": "5G, Wi-Fi, Bluetooth",
                "build": "Glass / Plastic"
            }
        }

    # =====================================================
    # MAIN EXECUTION
    # =====================================================
    def handle(self, *args, **kwargs):

        # Load grab / derived names if available
        try:
            with open("ai_image_price_updates.json", "r", encoding="utf-8") as f:
                grab_data = json.load(f)
        except Exception:
            grab_data = []

        grab_map = {
            g.get("derived_name", "").lower(): g.get("derived_name")
            for g in grab_data if g.get("derived_name")
        }

        products = Products.objects.all()
        updated = 0
        fallback_used = 0

        for product in products:
            original_name = product.name.strip()
            name_lower = original_name.lower()

            # Resolve better name if exists
            resolved_name = original_name
            for k, v in grab_map.items():
                if k in name_lower or name_lower in k:
                    resolved_name = v
                    break

            category = self.guess_category(resolved_name)

            # Skip ONLY if data already looks good
            if (
                isinstance(product.specifications, dict)
                and product.specifications
                and isinstance(product.features, list)
                and product.features
                and product.description
            ):
                continue

            self.stdout.write(f"🤖 Generating → {resolved_name}")

            # Multiple intelligent attempts
            prompts = [
                resolved_name,
                f"{resolved_name} {category}",
                f"{resolved_name} specifications",
                f"{resolved_name} India variant"
            ]

            data = None
            for p in prompts:
                data = self.ask_ollama(self.build_prompt(p, category))
                if data:
                    break

            # Final fallback
            if not data:
                data = self.fallback_specs(category)
                fallback_used += 1
                self.stdout.write(self.style.WARNING("⚠ Using fallback specs"))

            # Apply ONLY missing fields
            if not product.description:
                product.description = data["description"]

            if not product.features:
                product.features = data["features"]

            if not product.specifications:
                product.specifications = data["specifications"]

            product.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"""
DONE ✅
✔ Products updated: {updated}
⚠ Fallback used: {fallback_used}
"""
        ))
