from django.core.management.base import BaseCommand
from store.models.product import Products
import ollama
import json
import re


class Command(BaseCommand):
    help = "Update REAL specs/features/description for ALL devices using Ollama + fallback"

    # ===============================
    # USER PROMPT TEMPLATE (YOUR PROMPT)
    # ===============================
    def build_prompt(self, model_name, category):
        return f"""
You are a product specification engine.

Generate COMPLETE, REAL-WORLD details for the {category}:

Model: {model_name}

RULES (STRICT):
- Use real-world, realistic specifications
- No marketing fluff
- No emojis
- No assumptions beyond common knowledge
- Output MUST be valid JSON ONLY
- Do NOT include explanations or commentary

RETURN JSON IN THIS EXACT STRUCTURE:

{{
"model": "{model_name}",
"brand": "",
"category": "{category}",
"description": "Real-world usage oriented description explaining performance, battery life, and everyday experience.",
"price_india_estimate": 0,
"features": [
"feature 1",
"feature 2",
"feature 3"
],
"specifications": {{
"display": {{
"size": "",
"type": "",
"resolution": "",
"refresh_rate": ""
}},
"processor": {{
"chipset": "",
"cpu": "",
"gpu": ""
}},
"memory": {{
"ram": "",
"storage_options": []
}},
"camera": {{
"rear": "",
"front": "",
"video": ""
}},
"battery": {{
"capacity": "",
"charging": "",
"real_world_usage": ""
}},
"software": {{
"os": "",
"updates": ""
}},
"connectivity": {{
"5g": "",
"wifi": "",
"bluetooth": "",
"ports": ""
}},
"build": {{
"material": "",
"water_resistance": "",
"dimensions": ""
}}
}},
"use_cases": [
"Daily usage",
"Photography",
"Gaming",
"Content consumption"
],
"pros": [
"pro 1",
"pro 2"
],
"cons": [
"con 1",
"con 2"
]
}}
"""

    # ===============================
    # CATEGORY DETECTION
    # ===============================
    def detect_category(self, name):
        n = name.lower()

        if any(x in n for x in ["laptop", "notebook", "macbook", "thinkpad", "inspiron", "aspire"]):
            return "laptop"

        if any(x in n for x in ["ipad", "tab", "tablet", "surface"]):
            return "tablet"

        return "smartphone"

    # ===============================
    # OLLAMA CALL
    # ===============================
    def ask_ollama(self, prompt):
        try:
            response = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )

            raw = response["message"]["content"]

            match = re.search(r"\{.*\}", raw, re.S)
            if not match:
                return None

            return json.loads(match.group())

        except Exception as e:
       
            return None

    # ===============================
    # FALLBACK REALISTIC SPECS
    # ===============================
    def fallback_data(self, model, category):
        return {
            "description": f"{model} suitable for daily use, productivity, and multimedia consumption.",
            "features": ["Reliable performance", "Wi-Fi connectivity", "Battery efficient"],
            "specifications": {},
            "use_cases": ["Daily usage", "Office work", "Media"],
            "pros": ["Stable performance", "Good usability"],
            "cons": ["Average camera", "Basic build"]
        }

    # ===============================
    # MAIN COMMAND
    # ===============================
    def handle(self, *args, **kwargs):

        products = Products.objects.all()

        updated = 0
        failed = 0

        for product in products:

            model_name = product.name.strip()
            category = self.detect_category(model_name)

            self.stdout.write(f"🤖 Generating → {model_name}")

            # TRY MULTIPLE PROMPTS
            attempts = [
                model_name,
                f"{model_name} full specs",
                f"{model_name} India",
                f"{model_name} real world usage",
                f"{model_name} {category} specifications"
            ]

            data = None

            for attempt in attempts:
                prompt = self.build_prompt(attempt, category)
                data = self.ask_ollama(prompt)
                if data:
                    break

            # FALLBACK IF AI FAILS
            if not data:
                data = self.fallback_data(model_name, category)
                failed += 1
                self.stdout.write(self.style.WARNING(f"⚠ Fallback used → {model_name}"))

            # ======================
            # FORCE UPDATE ALL FIELDS
            # ======================
            product.description = data.get("description", "")
            product.features = data.get("features", [])
            product.specifications = data.get("specifications", {})

            # optional extended fields (safe if exist)
            if hasattr(product, "use_cases"):
                product.use_cases = data.get("use_cases", [])

            if hasattr(product, "pros"):
                product.pros = data.get("pros", [])

            if hasattr(product, "cons"):
                product.cons = data.get("cons", [])

            product.save()
            updated += 1

            self.stdout.write(self.style.SUCCESS(f"✔ Updated → {model_name}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDONE\nUpdated: {updated}\nFallback used: {failed}"
        ))
