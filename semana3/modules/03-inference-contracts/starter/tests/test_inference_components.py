def test_preprocess_preserves_feature_order() -> None:
    from model_inference.contracts import WineQualityRequest
    from model_inference.preprocess import preprocess_wine_request

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

    features = preprocess_wine_request(request)

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
