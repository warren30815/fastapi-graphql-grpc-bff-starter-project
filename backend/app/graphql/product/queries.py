import strawberry
from typing import List
from .types import ProductType

@strawberry.type
class ProductQueries:
    @strawberry.field
    def product(self, id: int) -> ProductType:
        return ProductType(id=id, name=f"Product{id}", price=99.9, description=f"Description for Product{id}", is_active=True)

    @strawberry.field
    def products(self) -> List[ProductType]:
        return [ProductType(id=1, name="Product1", price=99.9, description="Sample product", is_active=True)]