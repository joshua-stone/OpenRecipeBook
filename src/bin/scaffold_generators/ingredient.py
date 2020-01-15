from yaml import safe_dump

class StoreGenerator:
    def __init__(self):
        self.name = None
        self.link = None

    def prompt_name(self):
        self.name = input('Enter store name (leave blank to skip): ')

        return bool(self.name)

    def prompt_link(self):
        self.link = input('Enter store URL: ')

        return True

    def run_prompt_sequence(self):
        return self.prompt_name() and self.prompt_link()

    def to_renderable_dict(self):
        return {
            'name': self.name,
            'link': self.link
        }

class ProductGenerator:
    def __init__(self):
        self.name   = None
        self.stores = []

    def prompt_name(self):
        self.name = input('Enter product name (leave blank to skip): ')

        return bool(self.name)

    def prompt_stores(self):
        while True:
            store = StoreGenerator()
            print(f"Add store for {self.name}?")

            if not store.run_prompt_sequence():
                print(f"Done adding stores to {self.name}.")
                break

            self.stores.append(store)
            print(f"Finished store: {store.name}.\n")

        return True

    def run_prompt_sequence(self):
        return self.prompt_name() and self.prompt_stores()

    def to_renderable_dict(self):
        return {
            'name': self.name,
            'stores': list(map(
                lambda store: store.to_renderable_dict(),
                self.stores
            ))
        }

class IngredientGenerator:
    def __init__(self):
        self.id       = None
        self.name     = None
        self.products = []

    def prompt_id(self):
        while True:
            self.id = input('Enter ingredient ID: ')

            if self.id:
                break

            print("An ingredient ID is required!")

        return True

    def prompt_name(self):
        while True:
            self.name = input('Enter ingredient name: ')

            if self.name:
                break

            print("An ingredient name is required!")

        return True

    def prompt_products(self):
        while True:
            product = ProductGenerator()
            print(f"Add a product listing for {self.name}?")

            if not product.run_prompt_sequence():
                print(f"Done adding products to {self.name}.")
                break

            self.products.append(product)
            print(f"Finished product {product.name}.\n")

        return True

    def run_prompt_sequence(self):
        return self.prompt_id() and self.prompt_name() and self.prompt_products()

    def to_renderable_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'products': list(map(
                lambda product: product.to_renderable_dict(),
                self.products
            ))
        }

INGREDIENTS_ROOT = 'src/config/ingredients'

def run_ingredient_scaffold_generator(file_name):
    output_path = f'{INGREDIENTS_ROOT}/{file_name}.yml'
    ingredient  = IngredientGenerator()

    if not ingredient.run_prompt_sequence():
        return False

    output = safe_dump(ingredient.to_renderable_dict(), sort_keys = False)

    with open(output_path, 'w') as output_file:
        output_file.write(output)

    return True
