using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace ТП2лаб2.Models
{
    public class Cake
    {
        // Свойство 1: ID (числовой тип)
        public int Id { get; set; }

        // Свойство 2: Название (строковый тип)
        [DisplayName("Название изделия")]
        public string Name { get; set; }

        // Свойство 3: Тип изделия (торт, пирожное, печенье и т.д.)
        [DisplayName("Тип изделия")]
        public string Type { get; set; }

        // Свойство 4: Вес в граммах (числовой тип)
        [DisplayName("Вес (г)")]
        public int Weight { get; set; }

        // Свойство 5: Цена (числовой тип decimal)
        [DisplayName("Цена (руб)")]
        public decimal Price { get; set; }

        // Свойство 6: Дата изготовления (DateTime с атрибутом DataType.Date)
        [DisplayName("Дата изготовления")]
        [DataType(DataType.Date)]
        public DateTime ProductionDate { get; set; }

        // Свойство 7: Ингредиенты (строковый тип)
        [DisplayName("Ингредиенты")]
        public string Ingredients { get; set; }
    }
}