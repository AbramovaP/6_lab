using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;

namespace ТП2лаб3.Controllers
{
    public class FirstController : IController
    {
        public void Execute(RequestContext requestContext)
        {
            string action = requestContext.RouteData.Values["action"]?.ToString() ?? "";
            string idStr = requestContext.RouteData.Values["id"]?.ToString() ?? "0";
            int id = 0;
            int.TryParse(idStr, out id);

            if (action.ToLower() == "start" && id == 0)
            {
                // Полное перенаправление с завершением текущего запроса
                requestContext.HttpContext.Response.Redirect("/Cake/Index", true);
            }
            else
            {
                string fullUrl = requestContext.HttpContext.Request.Url?.ToString() ?? "URL не определён";
                requestContext.HttpContext.Response.Write("<h2>Ошибка!</h2>");
                requestContext.HttpContext.Response.Write($"<p>Условия не выполнены: action = '{action}', id = {id}</p>");
                requestContext.HttpContext.Response.Write($"<p>Полный URL: {fullUrl}</p>");
            }
        }
    }
}