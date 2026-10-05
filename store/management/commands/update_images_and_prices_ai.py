from django.core.management.base import BaseCommand
from store.models.product import Products
import ollama
import random
import re


MIN_PRICE = 25999
MAX_PRICE = 79999


class Command(BaseCommand):
    help = "Aggressively fetch prices for ALL products using Ollama with guaranteed fallback"

    used_random_prices = set()

    # -----------------------------
    # AI CALL
    # -----------------------------
    def ask_ollama_price(self, query):
        prompt = f"""
Get Indian price for: "{query}"

Rules:
- Output ONLY digits
- No words
- No symbols
- Any variant acceptable
- If unsure, estimate realistic Indian market price

Return ONLY number.
"""
        try:
            res = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )

            raw = res["message"]["content"].strip()
            digits = "".join(filter(str.isdigit, raw))

            if digits:
                price = int(digits)
                if 10000 <= price <= 200000:
                    return price
        except Exception:
            pass

        return None

    # -----------------------------
    # KEYWORD GENERATION
    # -----------------------------
    def build_queries(self, name):
        queries = []

        clean = re.sub(r"[^a-zA-Z0-9 ]", " ", name).strip()
        parts = clean.split()

        brand = parts[0] if parts else clean

        queries.append(clean)
        queries.append(f"{brand} {parts[-1]}" if len(parts) > 1 else brand)
        queries.append(f"{brand} latest device")
        queries.append(f"{brand} smartphone India price")
        queries.append(f"{brand} laptop India price")
        queries.append(f"{brand} tablet India price")

        return list(dict.fromkeys(queries))  # unique order preserved

    # -----------------------------
    # UNIQUE RANDOM PRICE
    # -----------------------------
    def generate_unique_random_price(self):
        while True:
            price = random.randint(MIN_PRICE, MAX_PRICE)
            if price not in self.used_random_prices:
                self.used_random_prices.add(price)
                return price

    # -----------------------------
    # MAIN HANDLER
    # -----------------------------
    def handle(self, *args, **kwargs):
        products = Products.objects.all()

        success = 0
        fallback = 0

        self.stdout.write(self.style.WARNING(
            f"\nStarting aggressive price update for {products.count()} products...\n"
        ))

        for product in products:
            name = product.name.strip()
            self.stdout.write(f"🔍 Pricing → {name}")

            price = None
            queries = self.build_queries(name)

            # TRY HARD — MULTIPLE ATTEMPTS
            for q in queries:
                price = self.ask_ollama_price(q)
                if price:
                    break

            # FALLBACK RANDOM
            if not price:
                price = self.generate_unique_random_price()
                fallback += 1
                self.stdout.write(
                    self.style.WARNING(f"⚠ Fallback random price → ₹{price}")
                )
            else:
                success += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Found price → ₹{price}")
                )

            product.price = price
            product.save()

        self.stdout.write(self.style.SUCCESS(
            f"""
DONE ✅
✔ AI prices fetched: {success}
⚠ Random fallback used: {fallback}
Total updated: {success + fallback}
"""
        ))
