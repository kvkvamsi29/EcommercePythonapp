import json
import re
from django.core.management.base import BaseCommand
from store.models.product import Products
from store.models.category import Category
import ollama


class Command(BaseCommand):
    help = "Use Ollama AI to import 5 latest laptops and 5 latest tablets"

    MODEL = "llama3"

    def ask_ollama(self):
        prompt = """
Return STRICT VALID JSON ONLY.

Task:
Provide 5 latest laptops and 5 latest tablets (India market).

Rules:
- Use approximate latest models
- Price must be Indian price (INR, number only)
- Do NOT include explanations
- Do NOT include markdown
- JSON only

Format EXACTLY:

{
  "laptops": [
    {
      "model": "",
      "price": 0,
      "features": [],
      "description": "",
      "specifications": {}
    }
  ],
  "tablets": [
    {
      "model": "",
      "price": 0,
      "features": [],
      "description": "",
      "specifications": {}
    }
  ]
}
"""

        response = ollama.chat(
            model=self.MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response["message"]["content"]

        match = re.search(r"\{.*\}", raw, re.S)
        if not match:
            raise ValueError("Ollama returned invalid JSON")

        return json.loads(match.group())

    def handle(self, *args, **kwargs):
        self.stdout.write("🤖 Asking Ollama for latest laptops & tablets...")

        try:
            data = self.ask_ollama()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"AI failed: {e}"))
            return

        laptop_category, _ = Category.objects.get_or_create(name="Laptop")
        tablet_category, _ = Category.objects.get_or_create(name="Tablet")

        created = 0
        updated = 0

        def save_device(item, device_type, category):
            nonlocal created, updated

            model = item.get("model")
            if not model:
                return

            obj, is_new = Products.objects.get_or_create(
                name=model,
                defaults={
                    "price": item.get("price", 999),
                    "description": item.get("description", ""),
                    "features": item.get("features", []),
                    "specifications": item.get("specifications", {}),
                    "product_type": device_type,
                    "category": category,
                    "is_latest": True
                }
            )

            if not is_new:
                obj.price = item.get("price", obj.price)
                obj.description = item.get("description", obj.description)
                obj.features = item.get("features", obj.features)
                obj.specifications = item.get("specifications", obj.specifications)
                obj.is_latest = True
                obj.save()
                updated += 1
            else:
                created += 1

            self.stdout.write(f"✔ {device_type.upper()} → {model}")

        for laptop in data.get("laptops", []):
            save_device(laptop, "laptop", laptop_category)

        for tablet in data.get("tablets", []):
            save_device(tablet, "tablet", tablet_category)

        self.stdout.write(self.style.SUCCESS(
            f"\nDONE ✅ Created: {created}, Updated: {updated}"
        ))
