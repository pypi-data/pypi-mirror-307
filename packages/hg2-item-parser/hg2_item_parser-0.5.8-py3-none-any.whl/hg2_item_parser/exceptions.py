class BaseItemError(Exception): ...


class ItemNotFoundError(BaseItemError):
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.msg = f"Item with ID={item_id} not found"
        super().__init__(self.msg)
