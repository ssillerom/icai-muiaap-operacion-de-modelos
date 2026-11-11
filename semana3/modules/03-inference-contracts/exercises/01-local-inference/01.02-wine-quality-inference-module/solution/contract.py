from pydantic import BaseModel, ConfigDict, Field, field_validator


class WineQualityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sample_id: str = Field(min_length=1)

    fixed_acidity: float = Field(ge=0, le=20)
    volatile_acidity: float = Field(ge=0, le=2)
    citric_acid: float = Field(ge=0, le=2)
    residual_sugar: float = Field(ge=0, le=3)
    chloride: float = Field(ge=0, le=0.1)
    free_sulfur_dioxide: float = Field(ge=0, le=25)
    total_sulfur_dioxide: float = Field(ge=0, le=70)
    density: float = Field(ge=0, le=1)
    ph: float = Field(ge=3, le=4)
    sulphates : float =Field(ge=0, le=1)
    alcohol: float = Field(ge=0,le=10)