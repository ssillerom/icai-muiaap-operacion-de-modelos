1. ¿Qué campo identifica la muestra?
sample_id
2. ¿Qué once campos consume el modelo?
sample_id,fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,ph,sulphates,alcohol
3. Proponed una nueva columna que el contrato debería
rechazar.
cualquier campo que no esté declarado, por ejemplo chlorides
4. Proponed dos valores inválidos y explicad por qué.
fixed_acidity = 24.0 , ya que está definido que el float entre 0 y 20
sample_id = 3, ya que debe ser un string
