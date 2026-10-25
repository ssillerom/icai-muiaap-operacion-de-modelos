# Un test es un código que comprueba automáticamente que tu código hace
# lo que debería hacer.

# Comprueba que preprocess_wine_request() convirete WineQualityRequest
# en un vector con las 11 características en el orden correcto.
# Es un test que comprueba que el procesado conserva el orden de
# las características

# test_inference_components.py comprueba componentes concretos del 
# sistema de inferencia. Comprueba concretamente: WineQualityRequest,
# preprocess_wine_request() y as_vector()




def test_preprocess_preserves_feature_order() -> None:
    from model_inference.contracts import WineQualityRequest
    from model_inference.preprocess import preprocess_wine_request

    # Crea un vino de prueba y lo pasa a WineQualityRequest para
    # comprobar si el vino creado de prueba es validado por el contrato.
    # Ahora request va a ser el vino creado.
    request = WineQualityRequest(
        fixed_acidity=1.0,
        volatile_acidity=0.5,
        citric_acid=0.2,
        residual_sugar=4.0,
        chlorides=0.05,
        free_sulfur_dioxide=6.0,
        total_sulfur_dioxide=70.0,
        density=0.998,
        ph=3.2,
        sulphates=1.0,
        alcohol=11.0,
    )

    # preprocess_wine_request() coge los valores que tengo dentro de un
    # WineQualityRequest y los prepara para poder obtener un vector con 
    # las 11 características en el orden correcto 
    features = preprocess_wine_request(request)

    # assert comprueba que esto sea verdad
    assert features.as_vector() == [
        1.0,
        0.5,
        0.2,
        4.0,
        0.05,
        6.0,
        70.0,
        0.998,
        3.2,
        1.0,
        11.0,
    ]
