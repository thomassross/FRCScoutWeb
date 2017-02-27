function getQueryParams()
{
    var queryString = window.location.search.substr(1);

    var queryParams = queryString.split("&");

    var rtn = {};
    for (var i = 0; i < queryParams.length; i++)
    {
        var param = queryParams[i].split("=");
        rtn[param[0]] = param[1];
    }

    return rtn;
}

window.run_notifications = function()
{
    var queryParams = getQueryParams();

    if ("add_team_success" in queryParams && queryParams["add_team_success"].toLowerCase() == "true" &&
        "add_team_team_number" in queryParams)
    {
        window.snackbar.show({
            message: "Successfully added team " + queryParams["add_team_team_number"]
        });
    }

    if ("edit_team_success" in queryParams && queryParams["edit_team_success"].toLowerCase() == "true" &&
        "edit_team_team_number" in queryParams)
    {
        window.snackbar.show({
            message: "Successfully modified team " + queryParams["edit_team_team_number"]
        });
    }
};