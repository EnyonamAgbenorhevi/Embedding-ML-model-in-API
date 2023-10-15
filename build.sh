docker build -t sepsis-prediction-app .
docker images
docker run -p 8000:8000 --name sepsis-prediction-app image_id
docker run -p 8000:8000 --name sepsis_tracker sepsis-prediction-app             