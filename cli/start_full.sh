#!/bin/bash

bash cli/start_backend.sh

sleep 5

bash cli/start_frontend.sh

echo "Sistema iniciado"
