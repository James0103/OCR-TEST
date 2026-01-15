#!/bin/bash

# Google Cloud Build 및 Cloud Run 배포 스크립트

PROJECT_ID="YOUR_PROJECT_ID"
SERVICE_NAME="ocr-test-service"
REGION="asia-northeast3"
SERVICE_ACCOUNT="ocr-service-account@${PROJECT_ID}.iam.gserviceaccount.com"

echo "Setting up service account..."
gcloud iam service-accounts create ocr-service-account --display-name="OCR Service Account" 2>/dev/null || true

echo "Granting Vision API permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/vision.imageAnnotator" 2>/dev/null || true

echo "Building Docker image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/ocr-test:latest .

echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/ocr-test:latest \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --service-account=$SERVICE_ACCOUNT \
  --set-env-vars NCP_SECRET_KEY="$NCP_SECRET_KEY",NCP_OCR_URL="$NCP_OCR_URL"

echo "Deployment complete!"
echo "Service URL: $(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')"