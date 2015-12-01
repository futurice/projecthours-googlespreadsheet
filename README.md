# projecthours-googlespreadsheet
A service that pulls projects hours from futuhours and makes a table that can be read into Google spreadsheets

The service generates a html table that google spreadsheets can import
> =IMPORTHTML("https://LOCALHOST/pm_fetch/?id=341765&year=2015&month=11&billableOnly=true", "table", 1)

The serive takes four parameters
id (mandatory) : The project ID in futuhours
year (optional): Specify from what year you want the project hours 
month (optional): Specify from what month you want the project hours 
billableOnly (optional) : Specify if you want to filter out non billable hours (true/false)

> https://LOCALHOST/pm_fetch/?id=341765&year=2015&month=11&billableOnly=true

Needs an API key to pull data from futuhours


