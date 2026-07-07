from models import GroceryItem, Purchase, User, db


def seed_data():
    if User.query.count() > 1:
        return

    if not User.query.filter_by(username="store_mgr").first():
        db.session.add(
            User(
                username="store_mgr",
                password="pass",
                role="store_manager",
                approved=True,
            )
        )

    if not User.query.filter_by(username="alice").first():
        db.session.add(
            User(username="alice", password="pass", role="user", approved=True)
        )

    if not User.query.filter_by(username="bob").first():
        db.session.add(
            User(username="bob", password="pass", role="user", approved=True)
        )

    db.session.commit()

    if GroceryItem.query.count() == 0:
        items = [
            GroceryItem(name="Apple", price=1.5, description="Fresh red apple", stock=100),
            GroceryItem(name="Banana", price=0.8, description="Ripe banana", stock=150),
            GroceryItem(name="Milk", price=3.2, description="Whole milk 1L", stock=50),
            GroceryItem(name="Bread", price=2.5, description="Whole wheat bread", stock=30),
            GroceryItem(name="Eggs", price=4.0, description=" dozen eggs", stock=20),
            GroceryItem(name="Cheese", price=5.5, description="Cheddar cheese block", stock=15),
            GroceryItem(name="Tomato", price=1.2, description="Fresh tomato", stock=80),
            GroceryItem(name="Potato", price=0.6, description="Bag of potatoes 1kg", stock=0),
        ]
        db.session.add_all(items)
        db.session.commit()

    if Purchase.query.count() == 0:
        alice = User.query.filter_by(username="alice").first()
        apple = GroceryItem.query.filter_by(name="Apple").first()
        milk = GroceryItem.query.filter_by(name="Milk").first()
        bread = GroceryItem.query.filter_by(name="Bread").first()

        if alice and apple and milk and bread:
            db.session.add_all([
                Purchase(
                    user_id=alice.id,
                    grocery_item_id=apple.id,
                    quantity=3,
                    total_price=3 * apple.price,
                ),
                Purchase(
                    user_id=alice.id,
                    grocery_item_id=milk.id,
                    quantity=1,
                    total_price=1 * milk.price,
                ),
                Purchase(
                    user_id=alice.id,
                    grocery_item_id=bread.id,
                    quantity=2,
                    total_price=2 * bread.price,
                ),
            ])
            db.session.commit()
