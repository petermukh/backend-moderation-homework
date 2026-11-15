from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr


class PredictionRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    seller_id: StrictInt = Field(gt=0)
    is_verified_seller: StrictBool
    item_id: StrictInt = Field(gt=0)
    name: StrictStr = Field(min_length=1)
    description: StrictStr = Field(min_length=1)
    category: StrictInt = Field(gt=0)
    images_qty: StrictInt = Field(ge=0)
