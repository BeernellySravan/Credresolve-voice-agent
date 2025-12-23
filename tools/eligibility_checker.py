from tools.scheme_db import SCHEMES

def check_eligibility(user_profile):
    eligible = []
    for scheme in SCHEMES:
        match = True
        for k, v in scheme["criteria"].items():
            if user_profile.get(k) != v:
                match = False
        if match:
            eligible.append(scheme["name"])
    return eligible
