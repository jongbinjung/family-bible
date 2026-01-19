"""Multilingual string maps"""

from src.models import Language

days = {
    Language.EN: "Days",
    Language.KO: "일",
}

leaderboard = {
    Language.EN: "Progress leaderboard",
    Language.KO: "진도 순위표",
}


login = {
    Language.EN: "Log in with Google",
    Language.KO: "구글로 로그인",
}

logout = {
    Language.EN: "Log out",
    Language.KO: "로그아웃",
}


my_progress = {
    Language.EN: "My progress",
    Language.KO: "내 진도",
}

name = {
    Language.EN: "Name",
    Language.KO: "이름",
}

plan = {
    Language.EN: "Plan",
    Language.KO: "진도",
}

read = {
    Language.EN: "Read",
    Language.KO: "읽음",
}

show_completed = {
    Language.EN: "Show past read plans",
    Language.KO: "읽은 지난 진도 보기",
}

title = {
    Language.EN: "Biblical wine",
    Language.KO: "가족 성경통독",
}

update_delay_notice = {
    Language.EN: "Note: Progress updates may take up to a minute to reflect.",
    Language.KO: "참고: 진도 업데이트가 반영되기까지 최대 1분이 걸릴 수 있습니다.",
}

welcome_pattern = {
    Language.EN: "Welcome, {}!",
    Language.KO: "환영합니다, {}님!",
}


def display_name(name: str, lang: Language) -> str:
    """Get display name for a given language"""

    match name:
        case "changkyoon":
            return "정창균"
        case "eunkyoung":
            if lang == Language.EN:
                return "Jessica"
            else:
                return "차은경"
        case "hanbyul":
            if lang == Language.EN:
                return "Hanbyul"
            else:
                return "정한별"
        case "hansol":
            if lang == Language.EN:
                return "Hansol"
            else:
                return "정한솔"
        case "jongbin":
            if lang == Language.EN:
                return "Jongbin"
            else:
                return "정종빈"
        case "lexy":
            return "Lexy"
        case "sangwon":
            return "차상원"
        case "sangyoung":
            return "이상영"
        case "seungho":
            return "한승호"
        case "youngshin":
            return "이영신"
