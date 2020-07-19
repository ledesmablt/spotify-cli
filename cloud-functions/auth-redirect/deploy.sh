#!/bin/bash
gcloud functions deploy \
	auth-redirect \
	--entry-point main \
	--memory 128MB \
	--project spotify-cli-283006 \
	--region asia-east2 \
	--runtime python37 \
	--trigger-http \
	--allow-unauthenticated
