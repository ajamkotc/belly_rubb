from pathlib import Path
from square import Square
from loguru import logger
from tqdm import tqdm
import typer

from belly_rubb.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

from sqlalchemy.dialects.sqlite import insert
from app.db import Session
from app.db_models import *

app = typer.Typer()

def store_customer_info(customer_info: dict) -> None:
    """
    Stores customer information in the database.
    Args:
        customer_info (dict): A dictionary containing customer details. Expected keys:
            - 'id': Unique identifier for the customer.
            - 'address': A dictionary with 'locality' and 'postal_code'.
            - 'reference_id': Reference identifier for the customer.
            - 'note': Additional notes about the customer.
            - 'creation_source': Source of customer creation.
    Returns:
        None
    """
    session_db = Session()

    stmt = insert(Customer).values(
        id=customer_info.get('id'),
        locality=customer_info.get('address').get('locality'),
        postal_code=customer_info.get('address').get('postal_code'),
        reference_id=customer_info.get('reference_id'),
        note=customer_info.get('note'),
        creation_source=customer_info.get('creation_source')
    )

    update_dict = {col.name: stmt.excluded[col.name] for col in Customer.__table__.columns if col.name != 'id'}

    stmt = stmt.on_conflict_do_update(index_elements=['id'], set_=update_dict)

    logger.debug(f"Storing customer info: {Customer(customer_info)}")

    session_db.execute(stmt)
    session_db.commit()
    session_db.close()

    logger.success("Customer information stored successfully.")

def api_logic():
    cursor = None
    client = Square(token=get_access_token())

    while True:
        customers = client.customers.list(
            limit=50,
            sort_field='created_at',
            sort_order='DESC',
            cursor=cursor
        )

        if customers.is_success():
            for customer in customers:
                store_customer_info(customer)
            cursor = customers.body.cursor
        else:
            break

def store_group_info(group_info: dict) -> None:
    """
    Stores group information in the database.
    Args:
        group_info (dict): A dictionary containing group details. Expected keys:
            - 'id': Unique identifier for the group.
            - 'name': Name of the group.
    Returns:
        None
    """
    session_db = Session()

    group = Group(
        id=group_info.get('id'),
        name=group_info.get('name')
    )
    logger.debug(f"Storing group info: {group}")

    session_db.add(group)
    session_db.commit()
    session_db.close()

    logger.success("Group information stored successfully.")

def store_membership_info(membership_info: dict) -> None:
    """
    Stores membership information in the database.
    Args:
        membership_info (dict): A dictionary containing membership details. Expected keys:
            - 'id': Unique identifier for the membership.
            - 'customer_id': Identifier for the customer.
            - 'group_id': Identifier for the group.
    Returns:
        None
    """
    session_db = Session()

    membership = GroupMembership(
        id=membership_info.get('id'),
        customer_id=membership_info.get('customer_id'),
        group_id=membership_info.get('group_id')
    )
    logger.debug(f"Storing membership info: {membership}")

    session_db.add(membership)
    session_db.commit()
    session_db.close()

    logger.success("Membership information stored successfully.")

@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # ----------------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Processing dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Processing dataset complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
