using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace ТП2лаб3.Controllers
{
    public class CakeController : Controller
    {
        [HttpGet]
        public ActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public ActionResult Index(int id, string name, string type, int weight, decimal price, string ingredients)
        {
            if (id != 0)
            {
                ViewBag.Id = id;
                ViewBag.Name = name;
                ViewBag.Type = type;
                ViewBag.Weight = weight;
                ViewBag.Price = price;
                ViewBag.Ingredients = ingredients;
                return View("Result");
            }
            else
            {
                return RedirectToAction("Index");
            }
        }
    }
}