tmux kill-session -t portfolio
cd /root/mlh-pe-portfolio 
git fetch && git reset origin/main --hard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
tmux new-session -d -s portfolio "
cd /root/mlh-pe-portfolio
source .venv/bin/activate
flask run --host=0.0.0.0
"


