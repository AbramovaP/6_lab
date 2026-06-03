using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using ТП2лаб2.Models;

namespace ТП2лаб2.Controllers
{
    public class CakeController : Controller
    {
        // Массив для хранения данных (до 10 записей)
        private static Cake[] cakes = new Cake[10];
        private static int nextId = 1;

        // GET: Cake/Index (просмотр всех записей)
        public ActionResult Index()
        {
            // Передаём через ViewData флаг для выбора метода (Часть III)
            ViewData["UseInternalHelper"] = true; // true — внутренний, false — внешний
            return View(cakes.Where(c => c != null).ToArray());
        }

        // GET: Cake/Create (форма добавления)
        public ActionResult Create()
        {
            return View();
        }

        // POST: Cake/Create (обработка добавления)
        [HttpPost]
        public ActionResult Create(Cake cake)
        {
            if (ModelState.IsValid)
            {
                cake.Id = nextId++;
                // Находим первую свободную ячейку в массиве
                for (int i = 0; i < cakes.Length; i++)
                {
                    if (cakes[i] == null)
                    {
                        cakes[i] = cake;
                        break;
                    }
                }
                return RedirectToAction("Index");
            }
            return View(cake);
        }

        // GET: Cake/Edit/5 (форма редактирования)
        public ActionResult Edit(int id)
        {
            Cake cake = cakes.FirstOrDefault(c => c != null && c.Id == id);
            if (cake == null)
                return HttpNotFound();
            return View(cake);
        }

        // POST: Cake/Edit/5 (обработка редактирования)
        [HttpPost]
        public ActionResult Edit(Cake cake)
        {
            if (ModelState.IsValid)
            {
                for (int i = 0; i < cakes.Length; i++)
                {
                    if (cakes[i] != null && cakes[i].Id == cake.Id)
                    {
                        cakes[i] = cake;
                        break;
                    }
                }
                return RedirectToAction("Index");
            }
            return View(cake);
        }
    }
}