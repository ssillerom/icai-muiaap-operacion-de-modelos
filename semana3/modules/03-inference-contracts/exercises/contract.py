from pydantic import Basemodel, Field, field_validator


class WineInputSchema(Basemodel):
    sample_id: int = Field(..., description="Unique identifier for the wine sample")
    fixed_acidity: float = Field(..., description="Fixed acidity of the wine sample")
    volatile_acidity: float = Field(..., description="Volatile acidity of the wine sample")
    citric_acid: float = Field(..., description="Citric acid content of the wine sample")
    residual_sugar: float = Field(..., description="Residual sugar content of the wine sample")
    chlorides: float = Field(..., description="Chloride content of the wine sample")
    free_sulfur_dioxide: float = Field(..., description="Free sulfur dioxide content of the wine sample")
    total_sulfur_dioxide: float = Field(..., description="Total sulfur dioxide content of the wine sample")
    density: float = Field(..., description="Density of the wine sample")
    ph: float = Field(..., description="pH level of the wine sample")
    sulphates: float = Field(..., description="Sulfate content of the wine sample")
    alcohol: float = Field(..., description="Alcohol content of the wine sample")
    
    
if __name__ == '__main__':
    mi_contrato = WineInputSchema(
        sample_id=1,
        fixed_acidity=7.4,
        volatile_acidity=0.7,
        citric_acid=0.0,
        residual_sugar=1.9,
        chlorides=0.076,
        free_sulfur_dioxide=11.0,
        total_sulfur_dioxide=34.0,
        density=0.9978,
        ph=3.51,
        sulphates=0.56,
        alcohol=9.4
    )