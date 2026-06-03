using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using ТП2лаб1.Models;

namespace ТП2лаб1.Controllers
{
    public class CalculatorController : Controller
    {
        [HttpGet]
        public ActionResult Index()
        {
            return View(new CalculatorModel());
        }

        [HttpPost]
        public ActionResult Index(CalculatorModel model)
        {
            string actionButton = Request.Form["actionButton"];

            // Очистка - ПРИНУДИТЕЛЬНЫЙ способ
            if (actionButton == "Очистить")
            {
                ModelState.Clear(); // Удаляем все сохранённые значения
                var newModel = new CalculatorModel();
                newModel.Operand1 = 0;
                newModel.Operand2 = "";
                newModel.Operation = null;
                newModel.Result = 0;
                newModel.IsCalculated = false;
                return View(newModel);
            }

            // Валидация модели
            if (!ModelState.IsValid)
            {
                model.IsCalculated = false;
                return View(model);
            }

            // Парсинг второго операнда
            int operand2Value = 0;
            if (!int.TryParse(model.Operand2, out operand2Value))
            {
                ModelState.AddModelError("Operand2", "Введите корректное целое число");
                model.IsCalculated = false;
                return View(model);
            }

            // Вычисление
            switch (model.Operation)
            {
                case "+":
                    model.Result = model.Operand1 + operand2Value;
                    break;
                case "-":
                    model.Result = model.Operand1 - operand2Value;
                    break;
                case "*":
                    model.Result = model.Operand1 * operand2Value;
                    break;
                case "/":
                    if (operand2Value != 0)
                        model.Result = (decimal)model.Operand1 / operand2Value;
                    else
                        ModelState.AddModelError("", "Деление на ноль невозможно!");
                    break;
                default:
                    ModelState.AddModelError("", "Выберите операцию");
                    break;
            }

            if (!ModelState.IsValid)
            {
                model.IsCalculated = false;
                return View(model);
            }

            model.IsCalculated = true;
            ViewBag.ExpectedResult = 100;
            ViewBag.ActualResult = model.Result;

            return View(model);
        }

        public ActionResult ShowResult(int operand1, string operand2, string operation, decimal result)
        {
            string expression = $"{operand1} {operation} {operand2} = {result}";
            string processedExpression = ProcessExpression(expression);
            ViewBag.Expression = processedExpression;
            return View();
        }

        private string ProcessExpression(string expression)
        {
            int equalIndex = expression.IndexOf('=');
            if (equalIndex == -1) return expression;

            string leftPart = expression.Substring(0, equalIndex);
            string rightPart = expression.Substring(equalIndex);

            string[] operators = { "+", "-", "*", "/" };
            int lastIndex = -1;
            string foundOperator = "";

            foreach (string op in operators)
            {
                int idx = leftPart.LastIndexOf(op);
                if (idx > lastIndex)
                {
                    lastIndex = idx;
                    foundOperator = op;
                }
            }

            if (lastIndex != -1)
            {
                string wordOperator = "";
                switch (foundOperator)
                {
                    case "+": wordOperator = "плюс"; break;
                    case "-": wordOperator = "минус"; break;
                    case "*": wordOperator = "умножить"; break;
                    case "/": wordOperator = "разделить"; break;
                }

                string beforeOperator = leftPart.Substring(0, lastIndex);
                string afterOperator = leftPart.Substring(lastIndex + 1);
                leftPart = beforeOperator + " " + wordOperator + " " + afterOperator;
            }

            return leftPart + rightPart;
        }
    }
}