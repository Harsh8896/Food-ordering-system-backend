# management/commands/fix_menu_links.py
from django.core.management.base import BaseCommand
from api.models import RestaurantMenuItem, Food

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        items = RestaurantMenuItem.objects.filter(food__isnull=True)
        fixed = 0
        for item in items:
            matching = Food.objects.filter(
                restaurant=item.restaurant,
                item_name__iexact=item.master_food.name
            ).first()
            if matching:
                item.food = matching
                item.save()
                fixed += 1
                self.stdout.write(f"✅ Fixed: {item.restaurant.name} - {item.master_food.name}")
            else:
                self.stdout.write(f"❌ No match: {item.restaurant.name} - {item.master_food.name}")
        
        self.stdout.write(f"\nTotal fixed: {fixed}/{items.count()}")