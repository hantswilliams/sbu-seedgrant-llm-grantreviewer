# Build Manually
  docker build -t grant-reviewer-app .
  docker run -p 5003:5003 -v $(pwd)/data:/app/data grant-reviewer-app

  # Build and run with docker-compose 
  docker-compose up --build