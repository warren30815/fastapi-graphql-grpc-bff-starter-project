import strawberry
from .types import ProductType, ProductInput

@strawberry.type
class ProductMutations:
    @strawberry.field
    def create_product(self, product_input: ProductInput) -> ProductType:
        return ProductType(
            id=123,
            name=product_input.name,
            price=product_input.price,
            description=product_input.description,
            is_active=True
        )
