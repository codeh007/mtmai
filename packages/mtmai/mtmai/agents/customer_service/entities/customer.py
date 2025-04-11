"""Customer entity module."""

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Address(BaseModel):
    """
    Represents a customer's address.
    """

    street: str
    city: str
    state: str
    zip: str
    model_config = ConfigDict(from_attributes=True)


class Product(BaseModel):
    """
    Represents a product in a customer's purchase history.
    """

    product_id: str
    name: str
    quantity: int
    model_config = ConfigDict(from_attributes=True)


class Purchase(BaseModel):
    """
    Represents a customer's purchase.
    """

    date: str
    items: List[Product]
    total_amount: float
    model_config = ConfigDict(from_attributes=True)


class CommunicationPreferences(BaseModel):
    """
    Represents a customer's communication preferences.
    """

    email: bool = True
    sms: bool = True
    push_notifications: bool = True
    model_config = ConfigDict(from_attributes=True)


class GardenProfile(BaseModel):
    """
    Represents a customer's garden profile.
    """

    type: str
    size: str
    sun_exposure: str
    soil_type: str
    interests: List[str]
    model_config = ConfigDict(from_attributes=True)


class Customer(BaseModel):
    """
    Represents a customer.
    """

    account_number: str
    customer_id: str
    customer_first_name: str
    customer_last_name: str
    email: str
    phone_number: str
    customer_start_date: str
    years_as_customer: int
    billing_address: Address
    purchase_history: List[Purchase]
    loyalty_points: int
    preferred_store: str
    communication_preferences: CommunicationPreferences
    garden_profile: GardenProfile
    scheduled_appointments: Dict = Field(default_factory=dict)
    model_config = ConfigDict(from_attributes=True)

    def to_json(self) -> str:
        """
        Converts the Customer object to a JSON string.

        Returns:
            A JSON string representing the Customer object.
        """
        return self.model_dump_json(indent=4)

    @staticmethod
    def get_customer(current_customer_id: str) -> Optional["Customer"]:
        """
        Retrieves a customer based on their ID.

        Args:
            customer_id: The ID of the customer to retrieve.

        Returns:
            The Customer object if found, None otherwise.
        """
        # In a real application, this would involve a database lookup.
        # For this example, we'll just return a dummy customer.
        return Customer(
            customer_id=current_customer_id,
            account_number="428765091",
            customer_first_name="Alex",
            customer_last_name="Johnson",
            email="alex.johnson@example.com",
            phone_number="+1-702-555-1212",
            customer_start_date="2022-06-10",
            years_as_customer=2,
            billing_address=Address(
                street="123 Main St", city="Anytown", state="CA", zip="12345"
            ),
            purchase_history=[  # Example purchase history
                Purchase(
                    date="2023-03-05",
                    items=[
                        Product(
                            product_id="fert-111",
                            name="All-Purpose Fertilizer",
                            quantity=1,
                        ),
                        Product(
                            product_id="trowel-222",
                            name="Gardening Trowel",
                            quantity=1,
                        ),
                    ],
                    total_amount=35.98,
                ),
                Purchase(
                    date="2023-07-12",
                    items=[
                        Product(
                            product_id="seeds-333",
                            name="Tomato Seeds (Variety Pack)",
                            quantity=2,
                        ),
                        Product(
                            product_id="pots-444",
                            name="Terracotta Pots (6-inch)",
                            quantity=4,
                        ),
                    ],
                    total_amount=42.5,
                ),
                Purchase(
                    date="2024-01-20",
                    items=[
                        Product(
                            product_id="gloves-555",
                            name="Gardening Gloves (Leather)",
                            quantity=1,
                        ),
                        Product(
                            product_id="pruner-666",
                            name="Pruning Shears",
                            quantity=1,
                        ),
                    ],
                    total_amount=55.25,
                ),
            ],
            loyalty_points=133,
            preferred_store="Anytown Garden Store",
            communication_preferences=CommunicationPreferences(
                email=True, sms=False, push_notifications=True
            ),
            garden_profile=GardenProfile(
                type="backyard",
                size="medium",
                sun_exposure="full sun",
                soil_type="unknown",
                interests=["flowers", "vegetables"],
            ),
            scheduled_appointments={},
        )
