from django.core.management.base import BaseCommand
from supplements.models import Supplement

class Command(BaseCommand):
    help = 'Populates the database with predefined supplements'

    def handle(self, *args, **kwargs):
        supplements_data = [
            {
                "name": "Vitamin C",
                "description": "Ascorbic acid, an essential nutrient involved in the repair of tissue and the enzymatic production of certain neurotransmitters.",
                "dosage_unit": "mg",
                "default_dosage": 500
            },
            {
                "name": "Vitamin D3",
                "description": "A fat-soluble vitamin involved in calcium absorption, immune function, and bone health.",
                "dosage_unit": "IU",
                "default_dosage": 2000
            },
            {
                "name": "Magnesium",
                "description": "A mineral important for muscle and nerve function, blood sugar control, and blood pressure regulation.",
                "dosage_unit": "mg",
                "default_dosage": 200
            },
            {
                "name": "Zinc",
                "description": "An essential mineral that is naturally present in some foods, added to others, and available as a dietary supplement.",
                "dosage_unit": "mg",
                "default_dosage": 15
            },
            {
                "name": "Omega-3 Fish Oil",
                "description": "Contains DHA and EPA, essential fats that support heart and brain health.",
                "dosage_unit": "mg",
                "default_dosage": 1000
            },
            {
                "name": "Creatine Monohydrate",
                "description": "A substance that is found naturally in muscle cells. It helps your muscles produce energy during heavy lifting or high-intensity exercise.",
                "dosage_unit": "g",
                "default_dosage": 5
            },
            {
                "name": "Whey Protein",
                "description": "A mixture of proteins isolated from whey, the liquid material created as a by-product of cheese production.",
                "dosage_unit": "g",
                "default_dosage": 25
            },
            {
                "name": "Multivitamin",
                "description": "A preparation intended to serve as a dietary supplement with vitamins, dietary minerals, and other nutritional elements.",
                "dosage_unit": "tablet",
                "default_dosage": 1
            },
            {
                "name": "Vitamin B12",
                "description": "A nutrient that helps keep the body's nerve and blood cells healthy and helps make DNA.",
                "dosage_unit": "mcg",
                "default_dosage": 1000
            },
             {
                "name": "Iron",
                "description": "A mineral that the body needs for growth and development. Your body uses iron to make hemoglobin.",
                "dosage_unit": "mg",
                "default_dosage": 18
            }
        ]

        count = 0
        for item in supplements_data:
            obj, created = Supplement.objects.update_or_create(
                name=item['name'],
                defaults={
                    'description': item['description'],
                    'dosage_unit': item['dosage_unit'],
                    'default_dosage': item['default_dosage'],
                    'is_active': True
                }
            )
            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {obj.name}'))
            else:
                self.stdout.write(f'Updated: {obj.name}')

        self.stdout.write(self.style.SUCCESS(f'Successfully processed supplements. Created {count} new ones.'))

