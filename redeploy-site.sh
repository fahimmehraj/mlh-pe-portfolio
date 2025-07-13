cd /root/mlh-pe-portfolio 
git fetch && git reset origin/main --hard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
systemctl restart myportfolio

