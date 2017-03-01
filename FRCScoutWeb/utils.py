from FRCScoutWeb.config import CURRENT_FRC_YEAR, ALLOWED_YEARS


def get_user_selected_year(request):
    user_selected_year = request.session.get("user_selected_year")
    if not user_selected_year or int(user_selected_year) not in ALLOWED_YEARS:
        request.session["user_selected_year"] = CURRENT_FRC_YEAR
        user_selected_year = CURRENT_FRC_YEAR

    return user_selected_year
