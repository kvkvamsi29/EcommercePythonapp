from django.core.management.base import BaseCommand
from store.models.product import Products
import json
import random
import ollama


class Command(BaseCommand):
    help = "Update image first (by original label), then update name, then enrich price"

    # ----------------------------
    # OLLAMA PRICE
    # ----------------------------
    def get_ollama_price(self, model_name):
        prompt = f"""
Get Indian price for: "{model_name}"

Rules:
- Output ONLY digits
- No symbols
- No words
- Any variant acceptable
- Guess realistic Indian market price if unsure

Return ONLY number.
"""
        try:
            res = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )
            raw = res["message"]["content"].strip()
            digits = "".join(filter(str.isdigit, raw))
            return int(digits) if digits else None
        except Exception:
            return None

    # ----------------------------
    # MAIN
    # ----------------------------
    def handle(self, *args, **kwargs):
        with open("ai_image_price_updates.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        updated = 0
        fallback_prices = 0

        for item in data:
            original_label = item["original_label"].strip()
            derived_name = item["derived_name"].strip()
            image_url = item["image_url"]

            # 🔍 MATCH USING ORIGINAL LABEL ONLY
            product = Products.objects.filter(
                name__icontains=original_label
            ).first()

            if not product:
                self.stdout.write(self.style.WARNING(
                    f"❌ No product found for label: {original_label}"
                ))
                continue

            self.stdout.write(f"🖼️ Updating image → {product.name}")

            # ----------------------------
            # STEP 1 — UPDATE IMAGE FIRST
            # ----------------------------
            image_updated = False
            if image_url and product.image != image_url:
                product.image = image_url
                product.save(update_fields=["image"])
                image_updated = True

            if not image_updated:
                self.stdout.write(self.style.WARNING(
                    f"⚠ Image unchanged for {product.name}"
                ))

            # ----------------------------
            # STEP 2 — UPDATE NAME ONLY AFTER IMAGE
            # ----------------------------
            self.stdout.write(f"✏ Renaming → {derived_name}")
            product.name = derived_name

            # ----------------------------
            # STEP 3 — PRICE ENRICHMENT
            # ----------------------------
            price = self.get_ollama_price(derived_name)

            if not price:
                price = random.randint(25999, 79999)
                fallback_prices += 1
                self.stdout.write(self.style.WARNING(
                    f"⚠ Fallback price used: ₹{price}"
                ))

            product.price = price
            product.save(update_fields=["name", "price"])

            self.stdout.write(self.style.SUCCESS(
                f"✅ Updated → {derived_name} | ₹{price}"
            ))

            updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"""
DONE ✅
✔ Products processed: {updated}
⚠ Fallback prices used: {fallback_prices}
"""
        ))
