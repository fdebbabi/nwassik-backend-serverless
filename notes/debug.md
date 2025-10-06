{
  "title": "Pickup package from post office",
  "description": "Need to pickup a package from La Poste and deliver to my office",
  "dropoff_latitude": 48.8566,
  "dropoff_longitude": 2.3522,
  "pickup_latitude": 48.8584,
  "pickup_longitude": 2.2945,
  "request_type": "pickup_and_delivery",
  "due_date": "2024-12-31"
}



pip install \                             
--platform manylinux2014_x86_64 \
--target=package \
--implementation cp \
--python-version 3.11 \
--only-binary=:all: --upgrade \
pydantic