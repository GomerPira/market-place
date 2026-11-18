#!/bin/bash
cd /home/gomer/Escritorio/universidad/market-place/fountain-engine
source /home/gomer/Escritorio/universidad/.venv/bin/activate
nohup python -c "from app import create_app; app = create_app(); app.run(host='127.0.0.1', port=5000)" > /home/gomer/Escritorio/universidad/market-place/fountain-engine/server.log 2>&1 &
echo $! > /home/gomer/Escritorio/universidad/market-place/fountain-engine/server.pid
