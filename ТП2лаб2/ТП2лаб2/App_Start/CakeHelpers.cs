using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.WebPages;

namespace ТП2лаб2.Helpers
{
    public static class CakeHelpers
    {
        // ВНЕШНИЙ ВСПОМОГАТЕЛЬНЫЙ МЕТОД
        public static HelperResult FormatPriceWithVat(decimal price, decimal vatRate = 0.20m)
        {
            return new HelperResult(async writer =>
            {
                decimal priceWithVat = price * (1 + vatRate);
                await writer.WriteAsync($"{price:F2} руб. (с НДС: {priceWithVat:F2} руб.)");
            });
        }
    }
}