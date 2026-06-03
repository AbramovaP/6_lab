using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace ТП2лаб1.Models
{
    public class CalculatorModel
    {
        [Required(ErrorMessage = "Пожалуйста, введите первый операнд")]
        public int Operand1 { get; set; }

        [Required(ErrorMessage = "Пожалуйста, введите второй операнд")]
        [StringLength(5, ErrorMessage = "Значение не может быть длиннее 5 символов")]
        public string Operand2 { get; set; }

        public string Operation { get; set; }
        public decimal Result { get; set; }
        public bool IsCalculated { get; set; }
    }
}