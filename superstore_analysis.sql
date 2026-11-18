SELECT
    COUNT(*) AS Total_Rows,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM superstore_python;
select category,round(sum(sales),2)as total_sales
from superstore_python
group by category order by total_sales desc;
SELECT
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM superstore_python
GROUP BY Region
ORDER BY Total_Sales DESC;
SELECT
    `Customer Name`,
    ROUND(SUM(Sales), 2) AS Total_Sales
FROM superstore_python
GROUP BY `Customer Name`
ORDER BY Total_Sales DESC
LIMIT 10;
SELECT
    `Sub-Category`,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM superstore_python
GROUP BY `Sub-Category`
HAVING SUM(Profit) < 0
ORDER BY Total_Profit;
SELECT
    YEAR(`Order Date`) AS Year,
    MONTH(`Order Date`) AS Month,
    ROUND(SUM(Sales), 2) AS Monthly_Sales
FROM superstore_python
GROUP BY Year, Month
ORDER BY Year, Month;
CREATE TABLE customers AS
SELECT DISTINCT
    `Customer ID`,
    `Customer Name`,
    Segment,
    Region
FROM superstore_python;
CREATE TABLE orders AS
SELECT
    `Order ID`,
    `Customer ID`,
    `Order Date`,
    Sales,
    Profit,
    Quantity
FROM superstore_python;
SELECT
    c.`Customer Name`,
    o.`Order ID`,
    o.Sales,
    o.Profit
FROM customers c
INNER JOIN orders o
ON c.`Customer ID` = o.`Customer ID`
LIMIT 20;
SELECT
    c.`Customer Name`,
    o.`Order ID`,
    o.Sales
FROM customers c
LEFT JOIN orders o
ON c.`Customer ID` = o.`Customer ID`;
SELECT
    c.`Customer Name`,
    ROUND(SUM(o.Sales), 2) AS Total_Revenue
FROM customers c
INNER JOIN orders o
ON c.`Customer ID` = o.`Customer ID`
GROUP BY c.`Customer Name`
ORDER BY Total_Revenue DESC
LIMIT 10;
SELECT
    c.Segment,
    ROUND(SUM(o.Sales), 2) AS Total_Sales
FROM customers c
INNER JOIN orders o
ON c.`Customer ID` = o.`Customer ID`
GROUP BY c.Segment
ORDER BY Total_Sales DESC;
WITH CategorySales AS (
    SELECT
        Category,
        SUM(Sales) AS Total_Sales
    FROM superstore_python
    GROUP BY Category
)
SELECT *
FROM CategorySales
ORDER BY Total_Sales DESC;
WITH CategorySales AS (
    SELECT
        Category,
        SUM(Sales) AS Total_Sales
    FROM superstore_python
    GROUP BY Category
)
SELECT *
FROM CategorySales
WHERE Total_Sales > (
    SELECT AVG(Total_Sales)
    FROM CategorySales
);
WITH CustomerSales AS (
    SELECT
        `Customer ID`,
        `Customer Name`,
        SUM(Sales) AS Total_Sales
    FROM superstore_python
    GROUP BY `Customer ID`, `Customer Name`
)
SELECT *
FROM CustomerSales
ORDER BY Total_Sales DESC
LIMIT 10;
WITH SubCategoryProfit AS (
    SELECT
        `Sub-Category`,
        SUM(Profit) AS Total_Profit
    FROM superstore_python
    GROUP BY `Sub-Category`
)
SELECT *
FROM SubCategoryProfit
WHERE Total_Profit < 0
ORDER BY Total_Profit;
 
SELECT
    `Customer Name`,
    SUM(Sales) AS Total_Sales,
    RANK() OVER(
        ORDER BY SUM(Sales) DESC
    ) AS Sales_Rank
FROM superstore_python
GROUP BY `Customer Name`
LIMIT 10;
WITH ProductSales AS (
    SELECT
        Category,
        `Product Name`,
        SUM(Sales) AS Total_Sales
    FROM superstore_python
    GROUP BY Category, `Product Name`
)
SELECT *,
    DENSE_RANK() OVER(
        PARTITION BY Category
        ORDER BY Total_Sales DESC
    ) AS Product_Rank
FROM ProductSales;
SELECT
    `Order Date`,
    Sales,
    SUM(Sales) OVER(
        ORDER BY `Order Date`
    ) AS Running_Sales
FROM superstore_python;
WITH MonthlySales AS (
    SELECT
        DATE_FORMAT(`Order Date`, '%Y-%m') AS Sales_Month,
        SUM(Sales) AS Total_Sales
    FROM superstore_python
    GROUP BY DATE_FORMAT(`Order Date`, '%Y-%m')
)
SELECT
    Sales_Month,
    Total_Sales,
    LAG(Total_Sales) OVER(
        ORDER BY Sales_Month
    ) AS Previous_Month_Sales
FROM MonthlySales;