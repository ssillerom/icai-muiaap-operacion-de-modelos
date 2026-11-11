from pydantic import BaseModel, Field

class WineQualityInput(BaseModel):
    fixed_acidity: float = Field(..., description="Fixed acidity of the wine")
    volatile_acidity: float = Field(..., description="Volatile acidity of the wine")
    citric_acid: float = Field(..., description="Citric acid content of the wine")
    residual_sugar: float = Field(..., description="Residual sugar content of the wine")
    chlorides: float = Field(..., description="Chloride content of the wine")
    free_sulfur_dioxide: float = Field(..., description="Free sulfur dioxide content of the wine")
    total_sulfur_dioxide: float = Field(..., description="Total sulfur dioxide content of the wine")
    density: float = Field(..., description="Density of the wine")
    ph: float = Field(..., description="pH level of the wine")
    sulphates: float = Field(..., description="Sulphate content of the wine")
    alcohol: float = Field(..., description="Alcohol content of the wine")


FEATURE_NAMES = (
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
)

row = [
    "True", 0.7, 0.0, 1.9, 0.076, 11.0, 34.0, 0.9978, 3.51, 0.56, 9.4
]


def preprocess_wine_request(row):
    """
    Transforms a validated sample into the model's input vector.
    
    Args:
        row (list): A list of feature values corresponding to the wine quality input.
        
    Returns:
        WineQualityInput: An instance of WineQualityInput with the provided feature values.
    """
    print("Esto hace zip:", list(zip(FEATURE_NAMES, row)))
    payload = dict(zip(FEATURE_NAMES, row, strict=True))

    print ("----------------------------------------")

    print ("Lo convierto a dict",payload)
    return WineQualityInput.model_validate(payload)

if __name__ == "__main__":
    # Example usage
    wine_input = preprocess_wine_request(row)

    print("----------RESULTADO DE LA FUNCIÓN-----------------")
    print(wine_input)

