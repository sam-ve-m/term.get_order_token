#!/bin/bash
fission spec init
fission env create --spec --name order-token-env --image nexus.sigame.com.br/fission-async:0.1.9 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name order-token-fn --env order-token-env --src "./func/*" --entrypoint main.sign_term_and_generate_order_token --executortype newdeploy --maxscale 3
fission route create --spec --name order-token-rt --method POST --url /order/generate_token --function order-token-fn