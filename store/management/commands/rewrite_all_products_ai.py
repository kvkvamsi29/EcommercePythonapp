from django.core.management.base import BaseCommand
from store.models.product import Products
import json
import re
import ollama


class Command(BaseCommand):
    help = "JSON price → else Ollama Indian price + rating + reviews → else ₹999"

    def get_ollama_data(self, model_name):
        prompt = f"""
For the smartphone "{model_name}", return ONLY valid JSON in this EXACT format:

{{
  "price": <NUMBER>,
  "rating": <FLOAT>,
  "reviews": [
    "review 1",
    "review 2",
    "review 3"
  ]
}}

Rules:
- Price must be Indian market estimate
- Price must be ONLY digits (INR)
- Any variant is acceptable
- Rating must be between 1.0 and 5.0
- No currency symbols
- No explanation
- No extra text
"""

        try:
            response = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )

            raw = response["message"]["content"].strip()

            # Extract JSON safely
            match = re.search(r"\{.*\}", raw, re.S)
            if not match:
                return None

            data = json.loads(match.group())

            # Validate numeric price
            price = data.get("price")
            rating = data.get("rating")
            reviews = data.get("reviews", [])

            if not isinstance(price, int):
                return None

            return {
                "price": price,
                "rating": float(rating) if rating else 0,
                "reviews": reviews if isinstance(reviews, list) else []
            }

        except Exception as e:

         return None


    def handle(self, *args, **kwargs):
        path = "strict_100_real_full_specs.json"

        with open(path, "r", encoding="utf-8") as f:
            devices = json.load(f)

        updated = 0
        skipped = 0

        for phone in devices:
            model_name = phone.get("model")
            api_id = phone.get("api_phone_id")

            if not model_name:
                skipped += 1
                continue

            # MATCH DB PRODUCT (UNCHANGED)
            obj = None
            if api_id:
                obj = Products.objects.filter(api_phone_id=api_id).first()
            if not obj:
                obj = Products.objects.filter(name=model_name).first()

            if not obj:
                skipped += 1
                continue

            # ===== STEP 1: JSON PRICE (UNCHANGED LOGIC) =====
            raw_price = (
                phone.get("price")
                or phone.get("price_inr")
                or phone.get("launch_price")
                or phone.get("pricing")
                or phone.get("specifications", {}).get("price")
            )

            price = None
            source = "JSON"

            if raw_price:
                if isinstance(raw_price, str):
                    digits = "".join(filter(str.isdigit, raw_price))
                    price = int(digits) if digits else None
                elif isinstance(raw_price, (int, float)):
                    price = int(raw_price)

            rating = obj.rating
            reviews = obj.reviews

            # ===== STEP 2: OLLAMA AI (ONLY IF JSON FAILED) =====
            if not price:
                self.stdout.write(f"🤖 Asking Ollama → {model_name}")

                ai_data = self.get_ollama_data(model_name)

                if ai_data:
                    price = ai_data["price"]
                    rating = ai_data["rating"]
                    reviews = ai_data["reviews"]
                    source = "Ollama AI"

                    self.stdout.write(self.style.SUCCESS(
                        f"Model: {model_name}\n"
                        f"Price (India): ₹{price}\n"
                        f"Rating: ⭐ {rating}\n"
                        f"Source: Ollama AI\n"
                    ))

            # ===== STEP 3: FALLBACK =====
            if not price:
                price = 999
                source = "Fallback ₹999"

            # ===== UPDATE PRODUCT (SAFE) =====
            old_price = obj.price

            obj.price = price
            obj.rating = rating
            obj.reviews = reviews
            obj.features = phone.get("features", [])
            obj.specifications = phone
            obj.description = ", ".join(obj.features) if isinstance(obj.features, list) else ""
            obj.save()

            updated += 1

            self.stdout.write(
                f"✅ Updated {obj.name}: ₹{old_price} → ₹{price} ({source})"
            )

        self.stdout.write(self.style.SUCCESS(
            f"DONE — {updated} updated, {skipped} skipped"
        ))
