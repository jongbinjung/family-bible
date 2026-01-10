"""Multilingual string maps"""

from src.models import Language

login = {
    Language.EN: "Log in with Google",
    Language.KO: "구글로 로그인",
}

logout = {
    Language.EN: "Log out",
    Language.KO: "로그아웃",
}


welcome_pattern = {
    Language.EN: "Welcome, {}!",
    Language.KO: "환영합니다, {}님!",
}

my_progress = {
    Language.EN: "My progress",
    Language.KO: "내 진도",
}


plan = {
    Language.EN: "Plan",
    Language.KO: "진도",
}


read = {
    Language.EN: "Read",
    Language.KO: "읽음",
}
