# PrismStudio User Guide English

## 🚀 Getting Started

### What is PrismStudio?

Welcome to the user guide for PrismStudio, a powerful financial data management and analysis tool. PrismStudio is designed to enable users in efficiently retrieving, managing, and utilizing financial data. With PrismStudio as your financial tool, you can leverage its comprehensive features and functionalities to streamline your financial data management workflow. Whether you are a financial analyst, researcher, or investor, PrismStudio provides the necessary tools to access, analyze, and interpret financial data effectively.

This user guide will serve as your roadmap to harness the full potential of PrismStudio, enabling you to make data-driven investment, decision-making, and analysis, and gain valuable insights into the financial markets.

### Installing PrismStudio

PrismStudio can be installed via pip from [PyPI](https://pypi.org/project/prismstudio/)

```python
pip install prismstudio
```

### How to import PrismStudio

To utilize the functionality of PrismStudio, you can import it into your Python code using the following line:

```python
import prism
```

Thinking About it <span style="color:red">*We have chosen to abbreviate the imported name to `ps` to improve the readability of code that uses PrismStudio. This is a common convention that is widely accepted, so it's recommended that you follow it to ensure that your code can be easily understood by others.*</span>

---

## **📥** Data

### Getting Data

Getting data is one of the most basic tasks in PrismStudio. It allows us to retrieve the desired financial information for analysis and further processing. This guide will walk you through the process of obtaining data using PrismStudio's functionalities.

### Single data

To get started, we need to define a financial component as a variable in Python. In this example, we will retrieve daily closing price by using the [prismstudio.market.close](<#prismstudio.market.close>) function:

```python
import prismstudio as ps

>>> close = ps.market.close()
```

Once you have defined the financial component, there are two methods to retrieve the data: using the [prismstudio.get_data](<#prismstudio.get_data>) function or directly calling the **`get_data`** method on the financial item. In both cases, you need to specify the desired parameters, such as the universe, start date, end date, shown ID, and name.

Here is an example of using the [prismstudio.get_data](<#ps.get_data>) function:

```python
import prismstudio as ps

>>> close_df = ps.get_data(
        component=close,
        universe='KOSPI 200 Index',
        startdate='2015-01-01',
        enddate='2020-12-31',
        shownid=['ticker']
    )
```

Alternatively, you can directly call the **`get_data`** method on the financial item:

```python
>>> close_df = close.get_data(
        universe='KOSPI 200 Index',
        startdate='2015-01-01',
        enddate='2020-12-31',
        shownid=['ticker'],
        name=['my_close']
    )
```

The result of the data query will be directly delivered to your Python environment and stored in the **`close_df`** variable as a pandas DataFrame. This allows you to access, analyze, and manipulate the data using familiar pandas functions for the downstream tasks.

Note that [prismstudio.get_data](<#prismstudio.get_data>) function and the **`get_data`** method have the same functionality and parameters.

### Multiple data

In addition to retrieving single data components, PrismStudio also allows you to retrieve multiple data components simultaneously. This can be useful when you need to obtain multiple sets of data for analysis or model building. The following example demonstrates how to retrieve multiple data components in a single query.

Let's consider a scenario where we want to retrieve the closing prices and 1-day percentage changes for a specific universe of stocks called **`my_snp_500`** between the dates **`2020-01-01`** and **`2020-12-31`**. We also want to include additional information such as company names and ISIN codes for each stock.


**Step 1: Define the Data Components**

First, we need to define the data components we want to retrieve. In this example, we'll use the following components:

```python
>>> c = ps.market.price_close()  # Closing price component (data component)
>>> r = c.n_periods_pct_change(n=1)  # 1-day percentage change component (function component)
```

The **`c`** component represents closing prices, and the **`r`** component calculates the 1-day percentage change based on the closing prices.


**Step 2: Retrieve Single Data (Optional)**

Before retrieving multiple data components, we can also choose to retrieve a single data component for a specific query. Here's an example of retrieving data for the **`r`** component using the **`get_data`** method:

```python
>>> r.get_data(universe='my_snp_500', startdate='2020-01-01', enddate='2020-12-31', name=["daily_return"], shownid=['Company Name', 'ISIN'])
```

This query retrieves the 1-day percentage change data for the specified universe and time period, and includes the company names and ISIN codes in the resulting DataFrame. With in the returned dataframe the data value column is named as **`daily_return`**.


**Step 3: Retrieve Multiple Data**

To retrieve multiple data components in a single query, we can use the [prismstudio.get_data](<#ps.get_data>) function. Here's an example of retrieving both the closing prices (**`c`**) and 1-day percentage changes (**`r`**) for the specified universe and time period:

```python
>>> ps.get_data(
        component=[c, r],
        universe='my_snp_500',
        startdate='2020-01-01',
        enddate='2020-12-31',
        name=["close", "daily_return"],
        shownid=['Company Name', 'ISIN']
    )
```

In this query, we pass a list of data components **`[c, r]`** as the **`component`** parameter. We also provide the universe, start date, end date, name, and shown ID parameters to specify the query details.

```{tip}
When retrieving the data for both components simultaneously, PrismStudio recognizes the dependency and only pulls the necessary data once if there is an overlap. This approach reduces the I/O load and enhances the speed of data retrieval.
```


In the given example, the **`r`** component is derived from the **`c`** component, as it calculates the 1-day percentage change based on the closing prices. PrismStudio recognizes the overlap between **`r`** and **`c`** and only pulls the daily closing price once.

The result will be in a list of DataFrames that includes both the closing prices and 1-day percentage changes, along with the company names and ISIN codes.


### Exporting Data with PrismStudio
#### Data Export

In PrismStudio, you can easily export data using the [prismstudio.export_data](<#prismstudio.export_data>) function, enabling you to save data of specified components results in your cloud space for future use. While utilizing export data typically involves downloading the result, which returns zipped parquet files, you also have the option to directly retrieve the exported data into your Python environment using the **`retrieve_data`** function.

Here's a step-by-step guide on how to export data using Prism:

**Step 1. Define Data:**

Before exporting data, ensure you have defined the necessary data using prismstudio. In the provided code snippet, the **`close`** and **`open`** prices for a market are retrieved using [prismstudio.market.close](<#prismstudio.market.close>) and [prismstudio.market.open](<#prismstudio.market.open>).

```python
>>> close = ps.market.close()
>>> open = ps.market.open()
```

**Step 2. Prepare Export Data Query:**
To export the data, you need to create an export data query. In the provided code, the [prismstudio.export_data](<#prismstudio.export_data>) function is used to define the export query. It takes the following arguments:

```python
ed = ps.export_data([close, open], "KRX_300", "2022-01-01")
```

- Data: Provide the data to be exported as a list. In this case, it includes **`close`** and **`open`**.
- Universe: Specify the universe or group of securities from which the data is extracted. In this example, it is "KRX_300".
- Start Date: Set the start date for the data to be exported. The provided date is **`2022-01-01`**.
- End Date: Since no enddate is given, it defaults to when the export data is run.

**Step 3. Run Export Data Query:**
The export data query is executed using the [prismstudio._ExportData.run](<#prismstudio._ExportData.run>) function on the export data object (**`ed`**). The [prismstudio._ExportData.run](<#prismstudio._ExportData.run>) function takes two parameters:

- Filepath: Specify the filepath where the exported data will be saved. In the given code, the data will be saved in a file named **`open_close`**.
- Filename: Provide a list of file names for the exported data within the zip file. In this case, the filenames are specified as **`close`**, **`open`**.

```python
>>> ed.run("open_close", ["close", "open"])

export_data is added to worker queue!
{'status': 'Pending',
'message': 'export_data is added to worker queue!',
'result': [{'resulttype': 'jobid', 'resultvalue': 465}]}
```

After executing the export data query, Prism will initiate the export job and provide information about the job status. In the provided code snippet, the response contains a dictionary with the following information:

- Status: Indicates the current status of the export data job. It starts as "Pending" and will change to "Completed" once the job is finished.
- Message: Provides a message indicating that the export data job has been added to the worker queue, which includes a job ID (**`jobid`**) for the export data job.
- Check Export Data Job Status: To ensure the export data job is completed, you can check the job status using the job ID. You can monitor the job status periodically until it changes to "Completed".

#### Access Exported Data

**Retrieving Exported Data into Python Workspace**

Once you have exported the data from Prism and saved it in a file, you can access and load the exported data into your Python workspace. The [prismstudio.retrieve_datafiles](<#prismstudio.retrieve_datafiles>) function allows you to retrieve the exported data as a dictionary of DataFrames.

```python
>>> ps.retrieve_datafiles('open_close')

Exported Data test_single_q has components: ['close', 'open']
{'close':
         listingid       date         Close
0         20108704 2022-01-03  16188.903172
1         20108704 2022-01-04  16477.132902
2         20108704 2022-01-05  16092.826595
3         20108704 2022-01-06  15468.328847
4         20108704 2022-01-07  15804.596865
...            ...        ...           ...
666583  1816050654 2023-03-20  31700.000000
666584  1816050654 2023-03-21  31050.000000
666585  1816050654 2023-03-22  31800.000000
666586  1816050654 2023-03-23  34400.000000
666587  1816050654 2023-03-24  35750.000000
,
'open':
         listingid        date          Open
0         20108704  2022-01-03  16092.826595
1         20108704  2022-01-04  16284.979749
2         20108704  2022-01-05  16477.132902
3         20108704  2022-01-06  15852.635154
4         20108704  2022-01-07  15564.405424
...            ...         ...           ...
664804  1816050654  2023-03-20  30300.000000
664805  1816050654  2023-03-21  33050.000000
664806  1816050654  2023-03-22  31900.000000
664807  1816050654  2023-03-23  31350.000000
664808  1816050654  2023-03-24  35000.000000
}
```

In the provided code snippet, the [prismstudio.retrieve_datafiles](<#prismstudio.retrieve_datafiles>) function is used to retrieve the exported data. Pass the name of the exported data file, in this case **`open_close`**, as the argument to the function.

**Downloading Exported Data**

To download exported data from the web UI, you have two methods available. The first method is to use the "Finder" feature, while the second method involves using the "Job Manager" to locate the associated job ID for downloading the desired file. Please note that downloading files is supported exclusively through the web browser.

**Method 1: Using [prismstudio.finder](<#prismstudio.finder>) to Locate the File in the Data Files Tab and Download**

1. Launch the PrismStudio web UI by running the following code: [prismstudio.finder()](<#prismstudio.finder>). This will open the web UI in your default browser.
2. In the web UI, navigate to the "Data Files" tab. This tab is usually located at the top of the page. Click on the "Data Files" tab to access the data files management page.

![Untitled](../_static/english_guide/Untitled.png)

1. Once you have located the desired file, right-click on it to open the menu. From the righ-click menu, select the "Download" option. This will initiate the download process.

![Untitled](../_static/english_guide/Untitled1.png)

**Method 2: Using [prismstudio.job_manager](<#prismstudio.job_manager>) to Locate the Associated Job in the "ALL" Task Tab and "Data Export" Task Tab**

1. Launch the PrismStudio web UI by running the following code: [prismstudio.job_manager](<#prismstudio.job_manager>). This will open the web UI in your default browser.
2. On the job manager page, you will find a list of all the tasks that have been executed. Look for the "Data Export" task tab, which specifically displays the export data tasks.
3. In the "Data Export" task tab, locate the specific job that corresponds to the export data task you initiated. This can be done by searching for the job using filters such as date, task type, or any other available criteria.

![Untitled](../_static/english_guide/Untitled2.png)

1. Look for the download option, which is typically represented by an icon such as a download arrow or a "Download" button. Click on the download option to initiate the download process.

![Untitled](../_static/english_guide/Untitled3.png)

Please note that currently, the exported data file format in PrismStudio is parquet. In later releases, PrismStudio plans to support additional file formats for data export, providing more flexibility for users in choosing the file format that best suits their needs.

### Datasets in PrismStudio

#### Available Datasets and Components

**Market Data**

Market data provides information about the prices, trading volumes, and other relevant data related to various financial instruments. In this user guide, we will explore the different components of market data. Here are the available market data components in PrismStudio:

1. Daily Open Price:
The daily open price refers to the price at which a particular financial instrument started trading at the beginning of a trading day. It is the first recorded price for that day.
2. Daily Close Price:
The daily close price represents the last recorded price of a financial instrument at the end of a trading day. It indicates the price level at which trading activity concluded for that day.
3. Daily High Price:
The daily high price indicates the highest price reached by a financial instrument during a trading day.
4. Daily Low Price:
The daily low price represents the lowest price reached by a financial instrument during a trading day. It gives insights into the lower boundary of price movement.
5. Daily Closing Bid Price:
The daily closing bid price is the highest price at which buyers in the market are willing to purchase a financial instrument at the end of a trading day.
6. Daily Closing Ask Price:
The daily closing ask price is the lowest price at which sellers in the market are willing to sell a financial instrument at the end of a trading day.
7. Daily VWAP (Volume-Weighted Average Price):
The daily VWAP is the average price at which a financial instrument has traded throughout the day, weighted by the corresponding trading volumes. It provides insights into the average price level and trading activity for the day.
8. Daily Short Interest Data:
Short interest data refers to information about the information relating to equity security that have been sold short but not yet covered or closed out. This data can provide insights into market sentiment and potential price movements. You can retrieve specific dataitems relating to short interest for equity securities by specifying a dataitemid.
9. Split:
A split refers to an adjustment made to the price and number of shares of a particular financial instrument. It occurs when a company decides to divide its existing shares into multiple shares, thereby reducing the share price proportionally. Splits are often implemented to make shares more affordable or increase liquidity.
10. Dividend:
Dividends are payments made by a company to its shareholders from its earnings or reserves. They are typically distributed as a portion of the company's profits and are often paid on a regular basis. Dividend payments can provide income to shareholders and may impact the stock price.
11. Exchange Rate:
The exchange rate represents the value of one currency in terms of another currency. In the context of market data, it indicates the rate at which one currency can be exchanged for another. Exchange rates are essential for trading and investment activities involving different currencies.
12. Daily Market Capitalization:
Daily market capitalization refers to the total value of a company's outstanding shares in the market. It is calculated by multiplying the current share price by the number of outstanding shares. Market capitalization is a crucial metric used to assess the size and relative value of a company.
13. Split Adjustment Factor:
The split adjustment factor is a multiplier used to adjust historical prices and data to account for stock splits. It ensures that historical data remains consistent and comparable even after a split occurs. The adjustment factor is applied to adjust the historical prices before the split to reflect the new share prices after the split.
14. Dividend Adjustment Factor:
The dividend adjustment factor is a multiplier used to adjust historical prices and data to account for dividends. It ensures that historical data remains consistent and comparable even after a dividend payment. The adjustment factor is applied to adjust the historical

**Financial Data**

Financial data provides valuable insights into the financial performance and position of a company. It includes various financial statements and metrics that help investors, analysts, and stakeholders assess the company's health and make informed decisions. In this user guide, we will explore the different components of financial data and their meanings. Here are the available financial data components:

1. Balance Sheet:
The balance sheet is a financial statement that provides a snapshot of a company's financial position at a specific point in time. It consists of three main sections: assets, liabilities, and shareholders' equity. The balance sheet highlights the company's assets (such as cash, inventory, and property), its liabilities (such as loans and accounts payable), and the shareholders' equity (the difference between assets and liabilities).
2. Income Statement:
The income statement, also known as the profit and loss statement or statement of operations, summarizes a company's revenues, expenses, gains, and losses over a specific period. It highlights the company's net sales or revenues, cost of goods sold, operating expenses, taxes, and net income or net loss. The income statement helps assess the profitability and performance of a company.
3. Cash Flow Statement:
The cash flow statement reports the cash inflows and outflows of a company during a specific period. It provides information about the company's operating activities (cash generated from core business operations), investing activities (cash spent on investments), and financing activities (cash from or used for financing). The cash flow statement helps evaluate the company's liquidity and ability to generate cash.
4. Earnings Per Share (EPS):
EPS is a financial ratio that indicates the profitability of a company on a per-share basis. It is calculated by dividing the company's net income by the number of outstanding shares. EPS is an important metric for investors as it provides insights into the company's profitability and helps assess its earnings generation capacity.
5. Dividends Per Share (DPS):
DPS represents the amount of dividends paid by a company to its shareholders on a per-share basis. It is calculated by dividing the total dividends paid by the number of outstanding shares. DPS is significant for investors who seek regular income from their investments and want to assess the company's dividend policy and sustainability.
6. Segment Reporting:
Segment reporting refers to the breakdown of a company's financial results and information by its different operating segments or business units. Companies often have multiple business segments that operate in different industries or geographical regions. Segment data allows stakeholders to evaluate the performance and profitability of each business segment separately.

**Estimate Data**

Estimate data provides valuable information regarding market expectations, analyst forecasts, and company guidance. It helps investors and analysts evaluate a company's performance, growth prospects, and potential deviations from expectations. In this user guide, we will explore the different components of estimate data and their meanings. Here are the available estimate data components:

1. Actual:
The actual component refers to the realized or reported value of a specific financial metric, such as revenue, earnings, or other performance indicators. It represents the actual outcome or result achieved by a company during a given period.
2. Consensus:
Consensus refers to the average or median of analysts' forecasts or estimates for a particular financial metric. It provides an aggregated view of market expectations derived from various analysts' assessments. Consensus estimates are often used as benchmarks to evaluate a company's performance relative to market expectations.
3. Guidance:
Guidance is forward-looking information provided by a company regarding its expected future performance. It can include revenue projections, earnings forecasts, or other financial or operational metrics. Guidance is typically issued by company management to provide insights into their expectations and help market participants assess future prospects.
4. Growth:
Growth represents the expected or realized rate of change in a specific financial metric over a given period. It can refer to revenue growth, earnings growth, or other performance indicators. Growth estimates or actuals are used to evaluate the pace of a company's expansion or contraction and its ability to generate sustainable growth.
5. Surprise:
Surprise refers to the difference between the actual reported value and the consensus estimate for a particular financial metric. It indicates whether a company's performance exceeded or fell short of market expectations. A positive surprise occurs when the actual value surpasses the consensus estimate, while a negative surprise indicates underperformance relative to expectations.
6. Revision:
Revision refers to changes made to consensus estimates or guidance by analysts or the company itself over time. Analysts may revise their estimates based on new information, market developments, or changes in the company's outlook. Company guidance revisions occur when management adjusts their previously provided expectations. Revisions help track changes in market sentiment and expectations regarding a company's future performance.

**Event**

Event data provides information about specific occurrences, developments, or news related to companies, industries, or markets. It helps investors, analysts, and stakeholders stay updated on relevant events that can impact investment decisions. In this user guide, we will explore the different components of event data and their meanings. Here are the available event data components:

1. Earnings Transcript:
An earnings transcript is a record or text-based document that provides a written account of a company's earnings conference call or presentation. During earnings calls, company executives discuss financial results, strategies, and outlooks with analysts and investors. Earnings transcripts capture the dialogue, including questions asked by analysts and responses from company representatives.
2. News:
News refers to timely and relevant information about events, developments, or announcements related to companies, industries, or markets. It includes press releases, regulatory filings, business updates, product launches, mergers and acquisitions, regulatory changes, and other significant news items.

**Index**

Index data provides information about specific market indices, which are benchmarks used to measure the performance of a group of stocks or other financial assets. Index data helps investors and analysts track the overall market or specific sectors, evaluate investment strategies, and compare investment performance. In this user guide, we will explore the different components of index data and their meanings. Here are the available index data components:

1. Level:
The level of an index refers to the numerical value that represents the current or historical level of the index. It indicates the aggregate value of the index based on the performance of the constituent securities. The level is often expressed as a price or point value, and it can change over time as the prices of the underlying securities fluctuate.
2. Shares:
Shares, in the context of index data, refers to the number of shares outstanding for each constituent security in the index. It represents the quantity of each stock included in the index, and it helps determine the weight or influence of each security on the index's overall performance. Shares data can be used to assess the liquidity and trading volume of the constituent securities.
3. Weight:
Weight represents the relative importance or contribution of each constituent security to the overall performance of the index. It is typically expressed as a percentage or proportion. Weight is calculated based on various methodologies, including market capitalization, equal weighting, or other customized schemes. The weight of each security determines its impact on the index's movement. Higher-weighted securities have a greater influence on the index's performance.

**Industry Specific**

Industry-specific data provides valuable insights and information about specific sectors or industries. Analyzing industry-specific components is essential for investors, analysts, and stakeholders to understand the unique characteristics, trends, and performance of different sectors.

PrismStudio currently support 19 industries:

Airlines, Bank, Capital Market, Financial Services, Healthcare, Homebuilders, Hotel and Gaming, Insurance, Internet Media, Managed Care, Metals and Mining, Oil and Gas, Pharmaceutical and Biotech, Real Estate, Restaurant, Retail, Semiconductors, Telecom/Cable/Wireless, Utility

#### Searching Dataitems

Data items are specific pieces of information categorized within data components. Searching for data items within a specific data component is essential to navigate through the vast amount of data available and extract the precise information we need.

For example, the income statement component often contains hundreds of data items, including revenue, expenses, and profitability metrics. By specifying our search within the income statement, we can narrow down to the desired dataitems.

PrismStudio provides two ways to search for data items: programmatically using the dataitem function, which returns a Pandas DataFrame, and through the web UI.

**Programmatically Search for DataItems**
To programmatically search for a specific data item within a particular data component, use the dataitem function and provide a search query. The search query typically includes the name or description of the data item you are interested in. By executing the function, you will receive a Pandas DataFrame containing the search results.

In this example, the code [prismstudio.financial.income_statement.dataitems](<#prismstudio.financial.income_statement.dataitems>) is used to search for the specific dataitems related to net income. The returned result is stored in a pandas DataFrame.

```python
>>> ps.financial.income_statement.dataitems("Net Income")

    dataitemid                           dataitemname  ...             packagename
 0    100637                    Net Income to Company  ...  CIQ Premium Financials
 1    100639                               Net Income  ...  CIQ Premium Financials
 2    100644          Other Adjustments to Net Income  ...  CIQ Premium Financials
 3    100645  Net Income Allocable to General Partner  ...  CIQ Premium Financials
 4    100646   Net Income to Common Incl. Extra Items  ...  CIQ Premium Financials
 5    100647   Net Income to Common Excl. Extra Items  ...  CIQ Premium Financials
 6    100703                       Diluted Net Income  ...  CIQ Premium Financials
 7    100829                               Net Income  ...  CIQ Premium Financials
 8    100830               Net Income as per SFAS 123  ...  CIQ Premium Financials
 9    100831  Net Income from Discontinued Operations  ...  CIQ Premium Financials
10    100842                    Normalized Net Income  ...  CIQ Premium Financials

```

**Search for Dataitems in Web UI**

The Web UI provides an intuitive interface for searching and locating data items within the available datasets. Here's a step-by-step example of how to search for revenue data items in the income statement component:

**Navigating the Dataitems search page**

The DataItems search page in the Web UI provides a user-friendly interface for exploring and locating specific data items. Here's a guide on how to navigate the page effectively:

*Side Panel*
The side panel is located on the left-hand side of the page and allows you to categorically narrow down your search. It provides data categories that can be selected to filter the displayed data items.

![Untitled](../_static/english_guide/Untitled4.png)

*Search Bar*
The search bar is located at the top of the page and enables you to enter keywords related to dataitemname, dataitemid, description, datacategory, datamodule, or datacomponent. By entering relevant keywords, you can refine your search results.

![Untitled](../_static/english_guide/Untitled5.png)

```{note}
The search bar will only search for data items within the selected options on the side panel. If you want to search for data items across all categories, make sure to select the "All" option in the side panel.
```

*Displayed DataItems*
The displayed data items section showcases the results of your search. It presents information such as dataitemid, dataitemname, Category, Module, Component, package, and description for each data item. This information helps provide context and assists in identifying the desired data items.

![Untitled](../_static/english_guide/Untitled6.png)

Additionally, you can adjust the page viewing options to customize your browsing experience. You can select the number of data items to display per page, with options such as **`25`**, **`50`**, or **`100`**.

To navigate through the pages, use the **`>`** button to move to the next page, **`>>`** button to move to the last page, the **`<`** symbol to go back one page, and lastly, **`<<`** to move to the first page. These options allow for smooth navigation and efficient exploration of the data items.

![Untitled](../_static/english_guide/Untitled7.png)

*Example: Navigating to Revenue DataItem in the Income Statement Component*

Let’s consider a case where you want to search for revenue dataitem and you only know that revenue dataitem is part of the income statement:

**Approach 1: Using the Search Bar**

1. Open the DataItems search page in the Web UI.
2. In the search bar, enter "revenue" or relevant keywords related to revenue.
3. Search results dynamically updates.
4. Look for the data item that corresponds to revenue in the income statement component. Review the dataitemname, dataitemid, and other relevant information such as description to ensure it is the desired data item.

**Approach 2: Using the Side Panel and Search Bar**

1. Open the DataItems search page in the Web UI.
2. Navigate to the side panel and select the "Financial" data category.
3. Once the “Financial” data category is selected, the available data components within it will be displayed.
4. Choose the "Income Statement" component from the side panel.
5. Utilize the search bar to enter "revenue" or other related keywords.
6. Search results dynamically updates.
7. Look for the data item that corresponds to revenue in the income statement component.

### Data Frequency in PrismStudio

Data frequencies play a crucial role in determining the time intervals at which data is collected, reported, or updated. Here's a guide to help you understand different data frequencies and their meanings:

1. Aperiodic: Aperiodic data refers to information that does not follow a regular or predictable pattern. This type of data does not have a specific frequency or interval associated with it. It may be irregularly collected or updated, making it challenging to determine when new data points will be available.
2. Aperiodic Day: Aperiodic day data indicates that data points are collected or updated on a daily basis, but without a consistent pattern. The updates may occur irregularly or on specific days as determined by the data source. It is essential to check the source or documentation for more information about the specific data collection or update schedule.
3. Daily: Daily data refers to information that is collected, reported, or updated every day.
4. Business Daily: Business daily data focuses on weekdays or business days, excluding weekends and holidays.
5. Weekly: Weekly data indicates that data points are collected, reported, or updated on a weekly basis.
6. Monthly: Monthly data involves data collection, reporting, or updates that occur once a month. It provides a higher-level overview, summarizing information over a one-month period.
7. Business Monthly: Business monthly data follows the same principles as business daily and business weekly data but on a monthly basis. It focuses on business days or weekdays, excluding weekends and holidays. This frequency is ideal for tracking monthly business-related trends, financial reporting, or performance indicators.
8. Quarterly: Quarterly data refers to information that is collected, reported, or updated every three months or once per quarter. It allows for analysis and comparison of performance or trends over a three-month period, providing insights into longer-term patterns.
9. Yearly: Yearly data involves data collection, reporting, or updates that occur once a year. It provides a comprehensive view of trends, changes, or performance over a full calendar year. Yearly data is particularly useful for long-term analysis, trend identification, or annual reporting purposes.

#### Default Frequencies

| Data Category | Data Component Name | Dataitem Input | Data Function | Default Frequency |
| --- | --- | --- | --- | --- |
| ESG | Environmental | ✔️ | `prismstudio.esg.environmental` | Aperiodic Day |
| ESG | Social | ✔️ | `prismstudio.esg.social` | Aperiodic Day |
| ESG | Governance | ✔️ | `prismstudio.esg.governance` | Aperiodic Day |
| ESG | Summary | ✔️ | `prismstudio.esg.summary` | Aperiodic Day |
| Estimate | Actual | ✔️ | `prismstudio.estimate.actual` | Aperiodic |
| Estimate | Consensus | ✔️ | `prismstudio.estimate.consensus` | Aperiodic |
| Estimate | Growth | ✔️ | `prismstudio.estimate.growth` | Aperiodic |
| Estimate | Guidance | ✔️ | `prismstudio.estimate.guidance` | Aperiodic |
| Estimate | Revision | ✔️ | `prismstudio.estimate.revision` | Aperiodic |
| Estimate | Surprise | ✔️ | `prismstudio.estimate.surprise `| Aperiodic |
| Event | Earnings Call | ❌ | `prismstudio.event.earnings_call` | Aperiodic Day |
| Event | News | ✔️ | `prismstudio.event.news` | Aperiodic Day |
| Financial | Balance Sheet | ✔️ | `prismstudio.financial.balance_sheet` | Aperiodic Day |
| Financial | Cash Flow | ✔️ | `prismstudio.financial.cash_flow` | Aperiodic Day |
| Financial | DPS | ✔️ | `prismstudio.financial.dps` | Aperiodic Day |
| Financial | EPS | ✔️ | `prismstudio.financial.eps` | Aperiodic Day |
| Financial | Income Statement | ✔️ | `prismstudio.financial.income_statement` | Aperiodic Day |
| Financial | Segment | ✔️ | `prismstudio.financial.segment` | Aperiodic Day |
| Financial | Ratio | ✔️ | `prismstudio.financial.ratio` | Aperiodic Day |
| Financial | Commitment | ✔️ | `prismstudio.financial.commitment` | Aperiodic Day |
| Financial | Option | ✔️ | `prismstudio.financial.option` | Aperiodic Day |
| Financial | Pension | ✔️ | `prismstudio.financial.pension` | Aperiodic Day |
| Index | Index Level | ✔️ | `prismstudio.index.level` | Business Day |
| Index | Index Share | ✔️ | `prismstudio.index.share` | Business Day |
| Index | Index Weight | ✔️ | `prismstudio.index.weight` | Business Day |
| Industry Financial | Airlines | ✔️ | `prismstudio.industryfin.airlines` | Aperiodic Day |
| Industry Financial | Bank | ✔️ | `prismstudio.industryfin.bank` | Aperiodic Day |
| Industry Financial | Capital Market | ✔️ | `prismstudio.industryfin.capital_market` | Aperiodic Day |
| Industry Financial | Financial Services | ✔️ | `prismstudio.industryfin.financial_services` | Aperiodic Day |
| Industry Financial | Healthcare | ✔️ | `prismstudio.industryfin.healthcare` | Aperiodic Day |
| Industry Financial | Homebuilders | ✔️ | `prismstudio.industryfin.homebuilders` | Aperiodic Day |
| Industry Financial | Hotel and Gaming | ✔️ | `prismstudio.industryfin.hotel` | Aperiodic Day |
| Industry Financial | Insurance | ✔️ | `prismstudio.industryfin.insurance` | Aperiodic Day |
| Industry Financial | Internet Media | ✔️ | `prismstudio.industryfin.internet` | Aperiodic Day |
| Industry Financial | Managed Care | ✔️ | `prismstudio.industryfin.managed_care` | Aperiodic Day |
| Industry Financial | Metals and Mining | ✔️ | `prismstudio.industryfin.mining` | Aperiodic Day |
| Industry Financial | Oil and Gas | ✔️ | `prismstudio.industryfin.oil` | Aperiodic Day |
| Industry Financial | Pharmaceutical and Biotech | ✔️ | `prismstudio.industryfin.biopharma` | Aperiodic Day |
| Industry Financial | Real Estate | ✔️ | `prismstudio.industryfin.real_estate` | Aperiodic Day |
| Industry Financial | Restaurant | ✔️ | `prismstudio.industryfin.restaurant` | Aperiodic Day |
| Industry Financial | Retail | ✔️ | `prismstudio.industryfin.retail` | Aperiodic Day |
| Industry Financial | Semiconductors | ✔️ | `prismstudio.industryfin.semiconductors` | Aperiodic Day |
| Industry Financial | Telecom/Cable/Wireless | ✔️ | `prismstudio.industryfin.telecom` | Aperiodic Day |
| Industry Financial | Utility | ✔️ | `prismstudio.industryfin.utility` | Aperiodic Day |
| Market | High | ❌ | `prismstudio.market.high` | Business Day |
| Market | Low | ❌ | `prismstudio.market.low` | Business Day |
| Market | Open | ❌ | `prismstudio.market.open` | Business Day |
| Market | Close | ❌ | `prismstudio.market.close` | Business Day |
| Market | Ask | ❌ | `prismstudio.market.ask` | Business Day |
| Market | Bid | ❌ | `prismstudio.market.bid` | Business Day |
| Market | Volume | ❌ | `prismstudio.market.volume` | Business Day |
| Market | VWAP | ❌ | `prismstudio.market.vwap` | Business Day |
| Market | Market Capitalization | ❌ | `prismstudio.market.market_cap` | Day |
| Market | Shares Outstanding | ❌ | `prismstudio.market.shares_outstanding` | Day |
| Market | Enterprise Value | ❌ | `prismstudio.market.enterprise_value` | Day |
| Market | Implied Market Capitalization | ❌ | `prismstudio.market.implied_market_cap` | Day |
| Market | Dividend | ❌ | `prismstudio.market.dividend` | Business Day |
| Market | Dividend Adjustment Factor | ❌ | `prismstudio.market.dividend_adjustment_factor` | Business Day |
| Market | Split | ❌ | `prismstudio.market.split` | Aperiodic Day |
| Market | Split Adjustment Factor | ❌ | `prismstudio.market.split_adjustment_factor` | Aperiodic Day |
| Market | Exchange Rate | ❌ | `prismstudio.market.exchange_rate` | Day |
| Market | Short Interest | ✔️ | `prismstudio.market.short_interest` | Business Day |
| Precalculated | Alpha Factor Library | ✔️ | `prismstudio.precalculated.alpha_factor_library` | Business Day |
| Security Master | SecurityMaster | ❌ | `prismstudio.securitymaster.attribute` | Day |
| Transaction | M&A | ✔️ | `prismstudio.transaction.ma` | Aperiodic Day |
| Transaction | Buyback | ❌ | `prismstudio.transaction.buyback` | Aperiodic Day |

#### Data Frequency during Data Tranform

In PrismStudio, data frequency inheritance ensures consistency and coherence in the resulting data components when performing operations between different data components with varying frequencies.

Before explaining how data frequencies are inherited during data operations of different data frequencies, let's define what we mean by "lower frequency" and "higher frequency" in the context of PrismStudio. The lower frequency refers to a data component with a lower temporal resolution, so when comparing yearly and daily frequency, the lower frequency in this case would be the yearly frequency.

When a data component with a higher frequency data is operated with a lower frequency data, the resulting component inherits the frequency of the lower-frequency data. For example, if a daily data component is operated with a monthly frequency data, the resulting component's data frequency will be monthly frequency.

This makes intuitive sense because it aligns with the lower frequency data. Since the monthly frequency is a subset of the daily frequency, the operation considers the available data points at the monthly intervals, resulting in a coherent and meaningful monthly representation.

To demonstrate the data frequency inheritance during operations, let's consider a practical case involving market capitalization data. Suppose we have a daily frequency market capitalization dataset represented by the variable **`mc`**. We want to resample this dataset to a monthly frequency using a lookback window of 31 days, and then perform an addition operation with the original market capitalization dataset.

```python
# Obtain the daily frequency market capitalization dataset
>>> mc = ps.market.market_cap()

# Resample the market capitalization dataset to monthly frequency
>>> mc_monthly = mc.resample('M', lookback=31)

# Perform an addition operation between the daily and monthly market capitalization datasets
>>> mc_operation_result = mc + mc_monthly

# Multiply the monthly market capitalization dataset by 2
>>> mc_monthly_double = mc_monthly * 2
```

In this example, we first resample the daily frequency market capitalization dataset (**`mc`**) to a monthly frequency using a lookback window of 31 days, resulting in the **`mc_monthly`** dataset. Then, we perform an addition operation (**`+`**) between the daily (**`mc`**) and monthly (**`mc_monthly`**) market capitalization datasets, resulting in the **`mc_operation_result`** dataset. Additionally, we multiply the monthly market capitalization dataset (**`mc_monthly`**) by 2, obtaining the **`mc_monthly_double`** dataset.

Since the operation involves adding two datasets of different frequencies, the resulting dataset (**`mc_operation_result`**) will inherit the lower frequency, which is the monthly frequency in this case. Therefore, **`mc_operation_result`** will have a monthly frequency, aligning with the lower frequency dataset (**`mc_monthly`**).

In this specific case, **`mc_monthly_double`** will be the same as **`mc_operation_result`** because both involve the multiplication operation with the same dataset (**`mc_monthly`**).

### Data Transforms in PrismStudio

PrismStudio offers a wide range of data transformation functions to manipulate and analyze your data. Data transformations in PrismStudio are always operated with respect to each specific security and date. This means that the resulting component will have data points corresponding to each month, rather than daily data points.

The functions are grouped into the following categories:

1. Arithmetic (35 functions): This category includes various arithmetic operations, such as addition, subtraction, multiplication, division, and more. It also includes method overrides for seven Python arithmetic operators.
2. Periodic (14 functions): The periodic category provides functions for calculating periodic changes, such as percentage change, rate of change, and moving averages.
3. Cross-Sectional (16 functions): The cross-sectional category offers functions for analyzing data across different entities or groups. It includes functions like rank, percentile, and z-score calculations.
4. Group (16 functions): The group category provides functions for aggregating and summarizing data within groups. It includes functions like group mean, group sum, and group rank.
5. Miscellaneous (4 functions): This category includes miscellaneous data transformation functions that do not fall into other categories. It includes functions like resample, fillna, isin, and map.
6. Financial (12 functions): The financial category offers functions specifically designed for financial data analysis. It includes functions for fiscal quarter operations, such as n_fiscal_quarter_sum, calculating quarter-over-quarter changes(n_fiscal_quarter_pct_change), and more.
7. Ordinary Least Square (6 functions): The Ordinary Least Square category provides functions for regression analysis and modeling. These functions help in estimating relationships between variables and predicting outcomes.

#### Data Structure during Data Transforms

PrismStudio incorporates a hierarchical system of data structures to handle different types of data effectively. Understanding the interactions between these structures during data operations is crucial for effective analysis and processing.

**Hierarchy of Data Structures:** PrismStudio employs a hierarchy of data structures, ranging from simpler to more complex representations:

- Value
- DataFrame
- Time DataFrame = Security DataFrame (same level)
- Security Time DataFrame
- Financial DataFrame

According to this hierarchy, a key principle governs the behavior of these structures:

**Inheritance of Complex Data Structures:** When a simpler data structure is involved in an operation with a more complex data structure, the resulting data structure inherits the data structure of the more complex one. This ensures that the output can fully accommodate the additional associations and functionalities offered by the complex structure.

However, there are exceptions to this general rule that should be considered:

1. **Inoperable Combinations:** Directly operating or combining a Security DataFrame with a Time DataFrame is not possible. These two data structures represent distinct types of data and lack the necessary reference information to perform meaningful operations. A Time DataFrame lacks securities associations, while a Security DataFrame lacks time elements. Consequently, there is no common basis or shared context for conducting operations between these structures.
2. **Financial DataFrame operating with other DataFrame:** When a Financial DataFrame is operated with any other data structure (excluding Value and another Financial DataFrame), the resulting data structure is a Security Time DataFrame. During this operation, the value columns are collapsed into a single column, maintaining the integrity of the financial data while incorporating the necessary time and security associations.
3. **Financial DataFrame operating with Value or Financial DataFrame:** If a Financial DataFrame is operated with a singular Value or another Financial DataFrame, it retains its structure as a Financial DataFrame. Operating with a single value or another Financial DataFrame does not require any structural changes to accommodate the operation.

## 📝 Security Master

The Security Master is a comprehensive database that provides detailed identification and meta data for each securities. It includes a wide range of attributes that help identify and categorize securities, enabling users to efficiently manage and analyze their portfolios. This user guide will familiarize you with the available attributes  in the Security Master and their corresponding descriptions.

### Security Master Attributes

| Attribute Name | Categorical | History | Attribute Level | Description | Available Values |
| --- | --- | --- | --- | --- | --- |
| Security ID | ❌ | N/A | Security | A unique identifier assigned to a security |  |
| Company ID | ❌ | N/A | Company | A unique identifier associated with the company |  |
| Company Name | ❌ | ❌ | Company |  |  |
| Native Company Name | ❌ | ❌ | Company | Company's name in its native language |  |
| Company Type | ✔️ | ❌ | Company | The type of the company. | Company, Investment Firm, Fund |
| Security Type | ✔️ | ❌ | Security | The type of the security. | Common Equity, Preferred Equity, Equity Depositary Receipts, ETF, REITS |
| Prism Active | ✔️ | ✔️ | Listing | An indicator that denotes the current status of a listing and, if the listing is inactive, specifies the start date and end date when it was active. | Active, Inactive |
| Country | ✔️ | ✔️ | Company | Company's denoted country by Prism39 | [ISO country](https://www.iso.org/obp/ui/#search) |
| Headquarter Country | ✔️ | ❌ | Company | Company's headquarter country (ISO 3166 Alpha-2 Code) | [ISO country](https://www.iso.org/obp/ui/#search) |
| Incorporation Country | ✔️ | ❌ | Company | Company's incorporated country (ISO 3166 Alpha-2 Code) | [ISO country](https://www.iso.org/obp/ui/#search) |
| Trade Currency | ✔️ | ❌ | Listing | Currency code - ISO 4217 | [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html) |
| Report Currency | ✔️ | ❌ | Company | Currency code - ISO 4217 | [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html) |
| MIC | ✔️ | ✔️ | Listing | The Market Identifier Code, a unique identifier for a market or exchange. | [ISO](https://www.iso20022.org/market-identifier-codes) |
| Operating MIC | ✔️ | ✔️ | Listing | An operating MIC, also called exchange level MIC, identifies the entity operating an exchange, trading platform, regulated or non-regulated market or a trade reporting facility in a specific country; it is the 'parent' MIC to one or several MICs. | [ISO](https://www.iso20022.org/market-identifier-codes) |
| Prism Primary | ✔️ | ✔️ | Listing | The primary flag made by Prism39. | primary, primary_security |
| CIQ Primary | ✔️ | ❌ | Listing | The primary flag made by Capital IQ databases. | primary, primary_listing, primary_security |
| Compustat Primary | ✔️ | ✔️ | Listing | The primary flag used in Compustat databases. | primary |
| Ticker | ❌ | ✔️ | Listing |  |  |
| GICS Sector | ✔️ | ✔️ | Company | The Global Industry Classification Standard sector to which the security belongs. | [MSCI](https://www.msci.com/our-solutions/indexes/gics) |
| GICS Group | ✔️ | ✔️ | Company | The Global Industry Classification Standard industry group to which the security belongs. | [GICS](https://www.msci.com/our-solutions/indexes/gics) |
| GICS Industry | ✔️ | ✔️ | Company | The Global Industry Classification Standard industry to which the security belongs. | [GICS](https://www.msci.com/our-solutions/indexes/gics) |
| GICS Sub-Industry | ✔️ | ✔️ | Company | The Global Industry Classification Standard sub-industry to which the security belongs. | [GICS](https://www.msci.com/our-solutions/indexes/gics) |
| CIQ Simple Industry | ✔️ | ❌ | Company |  | Same as GICS Sub-Industry |
| SIC | ✔️ | ❌ | Company | Standard Industrial Classification | [SIC](https://www.sec.gov/corpfin/division-of-corporation-finance-standard-industrial-classification-sic-code-list) |
| NAICS | ✔️ | ✔️ | Company | North American Industry Classification System | [NAICS](https://www.census.gov/naics/) |
| Barra ID | ❌ | ✔️ | Listing | An identifier used in Barra risk models. |  |
| CMA Entity ID | ❌ | ❌ | Company | The identifier for the entity in the CMA database. |  |
| CUSIP | ❌ | ❌ | Security | The Committee on Uniform Security Identification Procedures identifier for the security. The 9-character alphanumeric CUSIP code identifies any North American security for the purposes of facilitating clearing and settlement of trades. |  |
| SEDOL | ❌ | ✔️ | Security | Stock Exchange Daily Official List (United Kingdom and Ireland), identifiers used in the United Kingdom and Ireland for clearing purposes. |  |
| ISIN | ❌ | ✔️ | Security | International Securities Identification Number, used worldwide to identify specific securities such as bonds, stocks (common and preferred), futures, warrants, rights, trusts, commercial paper and options. |  |
| CINS | ❌ | ✔️ | Security | The CUSIP International Numbering System identifier for the security. |  |
| VALOR | ❌ | ✔️ | Security | Swiss Valoren |  |
| WKN | ❌ | ✔️ | Security | Wertpapierkennnummer |  |
| FIGI | ❌ | ✔️ | Listing | Financial Instrument Global Identifier, a 12-character alpha-numerical code that does not contain information characterizing financial instruments, but serves for uniform unique global identification. |  |
| Composite FIGI | ❌ | ✔️ | Listing | Composite level FIGI, Composite FIGI is issued to represent unique securities across related exchanges, mainly within a same country. |  |
| Share Class FIGI | ❌ | ✔️ | Security | Security level FIGI |  |
| Fitch Issuer ID | ❌ | ✔️ | Company | The Fitch Issuer Identification Number or FIID is a unique proprietary 12-digit tracking number applied to each issuer of debt rated by Fitch Ratings. |  |
| Moody's Issuer Number | ❌ | ✔️ | Company | The Moody's Issuer Number or MIN is a unique 10-digit identifier applied to each issuer of debt rated by Moody's Investor Services. |  |
| RatingsXpress Entity ID | ❌ | ✔️ | Company | S&P's rating database's entity level identifier. |  |
| IBES Ticker | ❌ | ✔️ | Listing | The ticker symbol used in the Institutional Brokers' Estimate System for the security. |  |
| LEI | ❌ | ✔️ | Company | Legal Entity Identifier, reference code to uniquely identify a legally distinct entity that engages in a financial transaction. |  |
| MarkIt Red Code | ❌ | ✔️ | Company | The identifier assigned by Markit to indicate credit risk. |  |
| SNL Institution ID | ❌ | ✔️ | Company | SNL Financial databases for the institution |  |
| Factset Entity ID | ❌ | ✔️ | Company | Factset entity level identifier. |  |
| Factset Company ID | ❌ | ✔️ | Company | Factset company level identifier. |  |
| Factset Security ID | ❌ | ✔️ | Security | Factset security level identifier. |  |
| Factset Listing ID | ❌ | ✔️ | Listing | Factset listing level identifier. |  |
| GVKEY | ❌ | ✔️ | Company | Compustat Company Level Identifier. |  |
| GVKEYIID | ❌ | ✔️ | Listing | Compustat Listing Level Identifier. |  |
| Trading Item ID | ❌ | N/A | Listing | CIQ listing level identifier. |  |


### Using Securtiy Master Attribute as Data

The [prismstudio.securitymaster.attribute](<#prismstudio.securitymaster.attribute>) function allows you to retrieve the security master attribute and used as a datacomponent just like any other dataset for a given universe.

Here is an example that retrieves the trade currency attribute for the securities in the S&P 500 universe from January 1, 2010, to January 1, 2015. The resulting data frame includes data trade currency for the input period and universe.

```python
>>> tcur = ps.securitymaster.attribute(attribute="Trade Currency")
>>> tcur.get_data(universe="S&P 500", startdate="2010-01-01", enddate="2015-01-01")

        listingid        date  Trade Currency  Company Name
0         2586086  2010-01-01             USD     AFLAC INC
1         2586086  2010-01-02             USD     AFLAC INC
2         2586086  2010-01-03             USD     AFLAC INC
3         2586086  2010-01-04             USD     AFLAC INC
4         2586086  2010-01-05             USD     AFLAC INC
...           ...         ...             ...           ...
914740  344286611  2011-10-27             USD      ITT CORP
914741  344286611  2011-10-28             USD      ITT CORP
914742  344286611  2011-10-29             USD      ITT CORP
914743  344286611  2011-10-30             USD      ITT CORP
914744  344286611  2011-10-31             USD      ITT CORP
```

One common use case for utilizing a Security Master attribute as a data component is when it is employed in the group function.

In the given code snippet, we will demonstrate an example of this scenario using the 'GICS Sector' attribute to calculate GICS sector relative monthly momentum percentile. This will calculate cross-sectional percentile of each security within its corresponding GICS sector.

First, we obtain the 'GICS Sector' data using the code **`gics_sector = ps.securitymaster.attribute('GICS Sector')`**.

```python
>>> gics_sector = ps.securitymaster.attribute('GICS Sector') # data component: GICS Sector
```

Next, prepare monthly momentum with calculating the percentage change over a 21-day period using the **`close.n_periods_pct_change()`** function.

```python
>>> ret_m = close.n_periods_pct_change(21)
```

Finally, we group the results based on the 'GICS Sector' attribute using the **`group_percentile()`** function and inputing it with gics_sector.

```python
>>> ret_m = ret_m.group_percentile(gics_sector)
>>> ret_m.get_data(universe='S&P 500', startdate='2010-01-01', enddate='2015-12-31', shownid=['ticker'])

        listingid        date     value  Ticker
0         2586086  2010-01-04  0.448718     AFL
1         2586086  2010-01-05  0.666667     AFL
2         2586086  2010-01-06  0.782051     AFL
3         2586086  2010-01-07  0.653846     AFL
4         2586086  2010-01-08  0.512821     AFL
...           ...         ...       ...     ...
755337  344286611  2011-10-25  0.166667     ITT
755338  344286611  2011-10-26  0.100000     ITT
755339  344286611  2011-10-27  0.100000     ITT
755340  344286611  2011-10-28  0.133333     ITT
755341  344286611  2011-10-31  0.250000     ITT
```

### Searching Security Master

When it comes to searching the Security Master, Prism offers two convenient approaches: programmatic searching using the [prismstudio.get_securitymaster_advanced](<#prismstudio.get_securitymaster_advanced>) function and the user-friendly Security Master Search Web UI. Programmatic searching allows for automation and integration within custom workflows, while the web UI offers a visual interface that simplifies the search process for users who prefer a graphical approach.

#### Search Security Master Programatically

To programmatically search for specific securities in the security master, Prism provides the convenient [prismstudio.get_securitymaster_advanced](<#prismstudio.get_securitymaster_advanced>) function. This powerful feature allows you to retrieve securities that match specific attribute values, enabling targeted searches and providing direct access to the results within your workspace.

To perform a search, you need to specify the attribute and its corresponding search value. The **`attribute`** parameter refers to the specific attribute you want to search for in the security master, such as "country" or "GICS sector". The **`search`** parameter represents the value you want to search for within the chosen attribute.

Additionally, the **`operator`** parameter allows you to specify the logical operator for combining multiple search conditions. By default, the operator is set to "AND", meaning that all specified conditions must be met. You can also explicitly specify "OR" to retrieve securities that match any of the specified conditions.

Let's explore an example where we search for securities that are based in the United States (country) and belong to GICS sector 30 (Consumer Staples).

```python
ps.get_securitymaster_advanced([
    {'attribute': 'country', 'search': 'US', 'operator': 'AND'},
    {'attribute': 'GICS sector', 'search': '30', 'operator': 'AND'}
])

        listingid      valuetype     value   startdate     enddate
0         2585879  tradingitemid   2585879  1987-05-08  1993-10-15
1         2587041  tradingitemid   2587041  1983-09-20  2002-09-13
2         2588957  tradingitemid   2588957  1984-10-22  1993-02-25
3         2588959  tradingitemid   2588959  1984-10-22  1993-02-25
4         2587848  tradingitemid   2587848  1986-04-23  2003-11-05
   ...        ...            ...       ...         ...         ...
115323   27580549  fsym_entityid  0044NF-E  1700-01-01  2199-12-31
115324   27580549  fsym_entityid  06GRML-E  1700-01-01  2199-12-31
115325   40843715  fsym_entityid  000LNJ-E  1700-01-01  2199-12-31
115326   99731436  fsym_entityid  05N251-E  1700-01-01  2199-12-31
115327  144070140  fsym_entityid  00D843-E  1700-01-01  2199-12-31
```

Running this code will return a pandas dataframe containing the listing ID, value type, value, start date, and end date for each matching security.

#### Search Security Master with Web UI

The Security Master Search Web UI provides a user-friendly interface for searching securities based on specific criteria. You can also open the search page directly using the [prismstudio.securitymaster_search](<#prismstudio.securitymaster_search>) code.

In this example, let's walk through the steps to search for securities headquartered in the US that have "motor" in their company name. Here's a step-by-step guide on how to navigate the Security Master Search Web UI:

**Step 1: Selecting Search Attributes:**

- Use the left side panel to select the attributes for your search.
- For example, choose the "country" attribute and type "US" in the search bar.
- To add additional search criteria, click the (+) button to add a new line of rules.
- Select the "companyname" attribute and enter "motor" in the search bar.

![Untitled](../_static/english_guide/Untitled8.png)

**Step 2: Managing Search Rules**

- If you make a mistake or want to remove a search rule, click the "X" button on the right side of the rule to delete it.
- To remove all the search rules at once, click the "(-) Remove All" button located in the bottom left corner of the left side panel.

**Step 3: Performing the Search:**

- Once you have entered the desired search criteria, click the "Search" button to initiate the search.
- The side panel will collapse, and the search results will appear if there are no errors.

![Untitled](../_static/english_guide/Untitled9.png)

**Step 4: Viewing Detailed Security Information:**

- The search results will be displayed on the page.
- You can select a specific security from the list to view its detailed information.
- Upon selecting a security, the right side panel will appear, providing comprehensive details about the selected security, including its attributes and historical values.

![Untitled](../_static/english_guide/Untitled10.png)

**Step 5: Customizing Viewing Options:**

- To customize your browsing experience, you can adjust the page viewing options.
- Select the number of data items you want to display per page, such as 25, 50, or 100.
- Use the navigation buttons (">", ">>", "<", "<<") to move between pages and explore the search results effectively.
- To download the search results, look for a download button on the web page and click it to initiate the download process.

![Untitled](../_static/english_guide/Untitled11.png)

---

## **⛏️**Query

In part of the user guide, we'll explore how to use queries to retrieve data and perform various data processing tasks.

Firstly, let's define what a query is. It refers to **a request made to the PrismStudio server that contains information on how to retrieve specific data or run a particular task.**

Let's start with a basic example of a query that retrieves a single piece of data without any operations:

```python
>>> c = ps.market.close()
```

The query follows a tree-like structure, which you can inspect by printing it as shown below:

```python
>>> print(c)
==== Close
Query Structure
```

A query can be as simple as a single node or it can be a complex structure with multiple nodes and operations. The example below shows a query with multiple nodes and operations:

```python
>>> c = ps.market.close()
>>> o = ps.market.open()

>>> t_hour_avgret = ((c - o) / o).n_periods_mean(n=21)
>>> print(t_hour_avgret)
==== n_periods_mean
	 ==== __sub__
		 ==== Open
		 ==== Close
Query Structure
```

Components serve as the fundamental building blocks of queries, ranging from basic data components to more sophisticated function and task components. In the context of tree structure, these components act as the nodes.

There are three types of components:

**1. Data Component** - Components that represent data and support various datasets such as market, financial, and outlook.

**2. Function Component** - Components that compute Data Components and provide essential functions for data processing such as arithmetic, cross-sectional, and time-series functions.

**3. Task Component** - Components that execute specific tasks like screening, factor backtesting, and data exporting.

```{warning}
The actual component class name is **`_PrismComponent`**, and it is a private class. It is not recommended to directly create objects using the class constructor.
```

Let’s go back to the example above, we see a more complex query that involves multiple components with operations.

We have the **`sub`** function component, which represents subtraction, and **`Open`** and **`Close`** data components, which represent the market open and close prices, respectively. These components are used in the query to calculate the average return over a 21-day period. The **`n_periods_mean`** function component is used to calculate the mean of the data over a specified number of periods, which is set to **`21`** in this example.

When the query is printed, we can see its tree-like structure, with the n_periods_mean function component at the top, followed by the **`sub`** component, and then the Open and Close data components. This tree-like structure allows us to inspect the query and understand how it retrieves and processes the data.

### Saving Query

PrismStudio provides a convenient way to save and retrieve queries, allowing you to organize and reuse your data retrieval and processing steps. The following guide will walk you through the process of saving queries and accessing them through the web UI or using the [prismstudio.list_dataquery](<#prismstudio.list_dataquery>) function.

**Step 1. Write your query code:**

Begin by writing your query code to retrieve and process the desired data. Let's consider an example:

```python
>>> c = ps.market.close()
>>> o = ps.market.open()

>>> t_hour_avgret = ((c - o) / o).n_periods_mean(n=21)
```

**Step 2. Save the query:**

To save the query for future use, you can use the **`.save()`** method and specify a name for the data query.

For instance, let's save our query as "1M_trading_hour_return":

```python
>>> t_hour_avgret.save(dataqueryname='1M_trading_hour_return')
```

### Loading Query

PrismStudio provides the capability to load previously saved queries, allowing you to reuse and manipulate them in your data processing tasks. The following guide will walk you through the process of loading queries using the [prismstudio.load_dataquery](<#prismstudio.load_dataquery>) function and how to work with the returned component.

By using the [prismstudio.load_dataquery](<#prismstudio.load_dataquery>) function and specifying the name of the query, a component containing the query is returned. This component is identical to the one you originally created, allowing you to utilize it immediately for further processing. Let's consider an example where we want to load a query named "daily_return":

```python
>>> r = ps.load_dataquery(dataquery="daily_return")
```

Once the query is loaded, you can perform various operations and tasks on the returned component, just like you would with any other component.

### Extracting Query

PrismStudio offers a convenient feature that allows you to extract the code for queries stored on the server or queries being worked on in your local environment. The following guide will demonstrate how to use the [extract()](<#prismstudio._AbstractPrismComponent.extract>) function to obtain the code used to create query components.

To extract the code used to create the query component, call the [extract()](<#prismstudio._AbstractPrismComponent.extract>) function on the query component:

```python
>>> c.extract() # Generates code that can recreate the component.
```

The [extract()](<#prismstudio._AbstractPrismComponent.extract>) function will return the code as a string that can be used to recreate the query component. In the example provided, the extracted code is as follows:

```python
>>> x0 = ps.market.close(package="Prism Market")
```

The extracted code can be used to recreate the query component and perform further operations or modifications. You can modify the parameters in the extracted code to customize the query according to your specific requirements.

### Managing Query

#### Web UI

PrismStudio provides a user-friendly web interface (Web UI) that allows you to conveniently manage your queries. This guide will walk you through the various operations you can perform on queries using the Web UI.

**Accessing the Web UI**

To access the Web UI, execute the following code in your Python environment:

```python
>>> ps.finder()
```

This will launch the PrismStudio Web UI, where you can manage your queries.

![../_static/english_guide/Untitled12.png](../_static/english_guide/Untitled12.png)

**Managing Queries in the Web UI**

Once the Web UI is launched, you can perform the following operations on your queries using the right-click menu:

![../_static/english_guide/Untitled13.png](../_static/english_guide/Untitled13.png)

1. Delete: Allows you to delete a selected query from your account.
2. Copy: Enables you to create a copy of a selected query.
3. Cut: Provides the ability to cut (remove) a selected query.
4. Paste: Allows you to paste a previously copied or cut query into a different location.
5. Rename: Allows you to rename a selected query.
6. Share: Enables you to share a query with other users in your account.

```{tip}
When you choose to share a query, it becomes accessible to other users within your PrismStudio account. This allows them to utilize the shared query in their own analysis and data processing tasks.
```

**Creating Folders**
To create a folder and organize your queries within the Web UI, follow these steps:

Step 1: Right-click in the desired location within the Web UI.

Step 2: From the right-click menu, select "New Folder."

![../_static/english_guide/Untitled14.png](../_static/english_guide/Untitled14.png)

Step 3: The new folder will appear in the Web UI, and you can now move queries into it by dragging and dropping or using the cut/copy and paste operations.

![../_static/english_guide/Untitled15.png](../_static/english_guide/Untitled15.png)

By creating folders and organizing your queries within the Web UI, you can easily manage and access your queries based on their respective categories or purposes.

### API

PrismStudio also offers functionality to manage queries programmatically using code. This guide will demonstrate how to perform common query management tasks through code.

**Listing Saved Queries:**
To list the queries that you have saved, use the following code:

```python
>>> ps.list_dataquery() # Lists the queries saved by the user.
```

Additionally, you can use the following code for a better visual representation of the query tree structure:

```python
>>> ps.list_dataquery(tree=True)
dataquery/
└── market cap
```

The output will display the query hierarchy.

**Deleting Queries:**
To delete a query, use the [prismstudio.delete_dataquery](<#prismstudio.delete_dataquery>) function, providing the name of the query to be deleted:

```python
>>> ps.delete_dataquery(dataquery="new_daily_return")
```

**Renaming Queries:**
To rename a query, utilize the [prismstudio.rename_dataquery](<#prismstudio.rename_dataquery>) function, specifying the old name of the query and the desired new name:

```python
>>> ps.rename_dataquery(old="daily_return", new="new_daily_return")
```

---

## **🗺** Universe

Universes in PrismStudio are collections of item identifiers and information about the incorporation period of those items. They are used to define target items when extracting data. This guide will provide instructions on how to create, search, modify, and delete universes using PrismStudio.

### Creating a Universe:

There are three main methods to create a new universe: Universe Filter, Screen Task Utilization, and Index Utilization. In this guide, we will focus on the Universe Filter method.

#### Filter Universe

The Universe Filter method allows you to create a universe by filtering items based on the attributes of the security master. By utilizing metadata among the attributes, you can configure the initial universe with a higher degree of flexibility.

To create a universe using the filtering method, use the [prismstudio.filter_universe](<#prismstudio.filter_universe>) function to apply filters and create a universe.
The following code creates a universe named "Korea and US" that contains both Korean and US stocks based on the "Country" attribute of the security master:

```python
>>> ps.filter_universe(attribute="Country", value=["KR", "US"], universename="Korea and US")
```

```{tip}
You can specify multiple values for an attribute by providing them as a list. For example, **`value=["KR", "US"]`** includes both Korean and US stocks in the "Korea and US" universe.
```

Let’s try a bit more realistic filter you might need. Here you want to create an Australian stock universe with primary stock and you want to exclude any ETFs, REITs, Public Funds, etc:

```python
>>> ps.filter_universe([
        {'attribute': 'Country', 'value': ['CA']},
        {'attribute': 'MIC', 'value': ['XTSE']},
        {'attribute': 'CIQ primary', 'value': ['primary']},
        {'attribute': 'Security Type', 'value': ['Common Equity']},
        {'attribute': 'Company Type', 'value': ['Public Company']},
    ], universename='Canada_primary')
```

In this code, multiple filter conditions are applied. It filters items based on attributes such as Country: Canada, MIC (Exchange Code): XTSE, CIQ primary: primary, Security Type: Common Equity, and Company Type: Public Company. The resulting stocks are stored in the "Canada_primary" universe.


#### Combine Universe

The [prismstudio.combine_universe](<#prismstudio.combine_universe>) function allows you to create a new universe by combining existing universes. This feature enables you to consolidate multiple universes into a single universe.

**Example:**

Let's consider an example scenario where we have the following existing universes:

```python
>>> ps.list_universe()

   universeid                 universename  universetype   startdate     enddate
0           1               Canada_primary        filter  1700-01-01  2199-12-31
1           2                  USA_primary        filter  1700-01-01  2199-12-31
```

Now, let's combine the "Canada_primary" and "USA_primary" universes into a new universe named "NorthAmerica_primary":

```python
>>> ps.combine_universe(["Canada_primary", "USA_primary"], newuniversename="NorthAmerica_primary")
```

The function will return a status dictionary confirming the success of the operation. Upon successful execution, the new combined universe "NorthAmerica_primary" will be created.

```python
>>> ps.list_universe()

   universeid                 universename  universetype   startdate     enddate
0           1               Canada_primary        filter  1700-01-01  2199-12-31
1           2                  USA_primary        filter  1700-01-01  2199-12-31
2           3         NorthAmerica_primary        filter  1700-01-01  2199-12-31

```

As shown in the updated universe list, the "NorthAmerica_primary" universe has been successfully created by combining the "Canada_primary" and "USA_primary" universes. This new universe can now be utilized for further data analysis and extraction.

#### Screen Universe

The screening process allows you to create a filtered universe by applying specific rules and criteria to select only the desired subset of items from an existing universe. This guide will walk you through the steps of screening a universe using prismstudio.

**Define Screening Rules**
Define the screening rules that will be applied to filter the universe. These rules specify the conditions that items must meet to be included in the screened universe. In the following example, three screening rules are defined:

```python
>>> primary_rule = ps.securitymaster.attribute(attribute="CIQ Primary") == "primary" # Include only CIQ Primary items.

>>> non_financial_rule = ps.securitymaster.attribute(attribute="GICS Sector") != "40" # Exclude companies from the Financial sector.

>>>> mcap = ps.market.market_cap()

>>> marketcap_rule = mcap.cross_sectional_rank() <= 1000 # Include the top 1000 items based on market capitalization.
```

Each rule is constructed using the available functions and operators provided by PrismStudio. In this case, the rules focus on including only primary security, excluding companies from the financial sector, and including the top 1000 items based on market capitalization.

**Create the Screening Task**
Create a screening task component using the defined rules. The screening task component will apply the rules to an existing universe and generate the screened universe. In the following code example, the screening task component is created:

```python
>>> NA_1000_screen = ps.screen(
    rule=primary_rule & non_financial_rule & marketcap_rule, # Apply all three rules.
    universename="NorthAmerica_primary", # Use an existing North America universe.
    startdate="2010-01-01",
    enddate="2020-01-01",
    frequency="Q",
)
```

The [prismstudio.screen](<#prismstudio.screen>) function takes the following parameters:

- **`rule`**: The combined set of screening rules. Each rule should evaluate to a boolean value. In this example, all three rules are applied using the logical AND operator (**`&`**).
- **`universename`**: The name of the starting universe to be screened. Here, it is the NorthAmerica_primary universe.
- **`startdate`** and **`enddate`**: The time period during which the screening task is executed.
- **`frequency`**: The frequency at which the screening task is performed (e.g., quarterly).

**Execute the Screening Task**
Run the screening task by specifying a name for the new screened universe. This will create the screened universe based on the applied rules. Here's an example:

```
>>> NA_1000_screen.run(newuniversename="NA_top200_nonfinancial")
```

The **`run`** method is used to execute the screening task and store the resulting screened universe with the specified name (**`NA_top200_nonfinancial`** in this case).

```{tip}
The screening universe functionality in Prism requires an existing universe as a starting point. If you want to create a universe from the entire security master, please refer to the Filter Universe feature.
```

#### Index Universe

Prism provides functionality to create a universe from a stock index, allowing you to work with a specific set of stocks included in the index. Follow the steps below to create a universe from a stock index.

**Step 1. List Available Index Data Items:**
Use the [prismstudio.index.universe.dataitems](<#prismstudio.index.universe.dataitems>) function to list the index data items available for a specific index. For example:

```python
>>> ps.index.universe.dataitems("S&P 500")
```

This will list the index data items that can be used to create a universe containing the stocks from the "S&P 500" index.

**Step 2. Save Index as Universe:**
To create a universe from a specific index, use the [prismstudio.save_index_as_universe](<#prismstudio.save_index_as_universe>) function. Specify the index data item ID, start date, end date, and the desired name for the universe. For example:

```python
>>> ps.save_index_as_universe(dataitemid=4006682, startdate='2020-01-01', enddate='2021-01-01', universename='my_snp_500')
```

This code saves the index with data item ID 4006682 (representing the "S&P 500" index) as a universe named "my_snp_500" for the specified date range.

**Step 3. Verify Saved Universes:**
You can verify the list of universes you have saved using the [prismstudio.list_universe](<#prismstudio.list_universe>) function. This will display the user-created universes along with their details. For example:

```python
>>> ps.list_universe()
```

This will retrieve the list of user-created universes.

```{note}
- The data item ID for an index can be obtained using [prismstudio.index.dataitems](<#prismstudio.index.dataitems>). However, to search for data items specifically for creating universes, you can use [prismstudio.index.universe.dataitems](<#prismstudio.index.universe.dataitems>), which filters the results to index data items that can be used for universe creation.
- Alternatively, you can utilize the Data Item Search GUI page to search for available data items.
```


#### Custom Universe

You can create a custom universe by specifying the constituents using a CSV file. The CSV file should have four columns: valuetype, value, startdate, and enddate. Each column provides specific information about the securities to be included in the universe.

Follow the steps below to create a custom universe using a CSV file:

**Step 1: Prepare the CSV file**

Create a CSV file that includes the universe constituents with the following four columns:

- valuetype: Specifies the Security Master attribute.
- value: Indicates the value of the attribute to include in the universe.
- startdate: Indicates the start date of the specified security's inclusion in the universe.
- enddate: Indicates the end date of the specified security's inclusion in the universe.

Ensure that the CSV file contains the necessary information for each security to be included in the universe.

```python
>>> import pandas as pd
>>> universe_df = pd.read_csv("./my_universe.csv")
>>> print(universe_df) # include all securities being traded in the Korean Exchange

   valuetype  value   startdate     enddate
0        MIC   XKRX  1700-01-01  2999-12-31
```

**Step 2: Upload the universe using the CSV file**

Use the [prismstudio.upload_universe](<#prismstudio.upload_universe>) function to upload the custom universe using the CSV file. Provide the path to the CSV file using the **`universefile`** parameter, and specify a name for the universe using the **`universename`** parameter. In the example code provided, the universe is uploaded with the name "krx" using the file "./my_universe.csv".

```python
>>> ps.upload_universe(universefile="./my_universe.csv", universename="krx")

{'status': 'Success',
 'message': 'Universe saved',
 'result': [{'resulttype': 'universeid', 'resultvalue': 1}]}
```

**Step 3: Verify the custom universe**

Use the [prismstudio.list_universe](<#prismstudio.list_universe>) function to verify that the custom universe has been created successfully. This function will display a list of all saved universes, including the newly created custom universe. Check the **`universename`**, **`universetype`**, **`startdate`**, and **`enddate`** columns to ensure that the universe has the desired properties. In the example code provided, the custom universe "krx" is listed with the specified universetype and time range.

```python
>>> ps.list_universe()

   universeid  universename  universetype   startdate     enddate
0           1           krx        custom  1700-01-01  2199-12-31
```

### Retrieving Universe

The [prismstudio.get_universe](<#prismstudio.get_universe>) function allows you to retrieve data for a specific universe. You can specify the universe by its **`name (str)`** or its **`ID (int)`**. The function returns the universe data in a DataFrame.

Parameters:

- **`universe`**: Accepts a universe name (str) or universe ID (int) as input. This parameter specifies the universe for which you want to retrieve data.
- **`startdate`**: (optional) Specifies the start date of the data. The data includes the start date. If set to **`None`**, the start date of the universe will be used. If the input is earlier than the universe start date, the universe start date will be used instead.
- **`enddate`**: (optional) Specifies the end date of the data. The data excludes the end date. If set to **`None`**, the end date of the universe will be used. If the input is later than the universe end date, the universe end date will be used instead.
- **`frequency`**: (optional) Specifies the desired sampling frequency of universe constituents. This parameter accepts the following values: 'D' (daily), 'W' (weekly), 'MS' (month start), 'SMS' (semi-month start), 'SM' (semi-month), 'M' (monthly), 'Q' (quarterly), 'QS' (quarter start), 'AS' (year start), 'A' (annual). If the **`expand`** parameter is set to **`False`**, this parameter is ignored.
- **`shownid`**: (optional) Accepts a list of Security Master attributes to display with the data. If set to **`None`**, the default attributes set in preferences will be shown. If set to an empty list (**`[]`**), no attributes will be shown.

Example:

The following example demonstrates the usage of [prismstudio.get_universe](<#prismstudio.get_universe>):

1. Retrieve the data for the "Russell 3000 Index" universe:

```python
>>> ps.get_universe(universe='Russell 3000 Index')

          listingid        date
0           2585895  1978-12-29
1           2586016  1978-12-29
2           2586064  1978-12-29
3           2586086  1978-12-29
4           2586118  1978-12-29
...             ...         ...
10110503  701835357  2199-12-31
10110504  701932931  2199-12-31
10110505  703822433  2199-12-31
10110506  704721046  2199-12-31
10110507  706171023  2199-12-31
```

This will return a DataFrame with the listing IDs and dates for the securities in the "Russell 3000 Index" universe.

1. Retrieve the data for the **`Russell 3000 Index`** universe within a specific time range and display only the **`companyname`** attribute:

```python
>>> ps.get_universe('Russell 3000 Index', startdate='2010-01-01', enddate='2015-12-31', shownid=['companyname'])

         listingid        date                   companyname
0          2585893  2010-01-03                      AAON INC
1          2585895  2010-01-03                      AAR CORP
2          2585957  2010-01-03    ADC TELECOMMUNICATIONS INC
3          2586016  2010-01-03            ABM INDUSTRIES INC
4          2586068  2010-01-03            AEP INDUSTRIES INC
...            ...         ...                           ...
2194810  325621650  2015-12-27        AVAGO TECHNOLOGIES LTD
2194811  325832671  2015-12-27                     POZEN INC
2194812  326004249  2015-12-27  LIBERTY INTERACTV CP QVC GRP
2194813  344286611  2015-12-27            ITT INDUSTRIES INC
2194814  365743684  2015-12-27     HERTZ GLOBAL HOLDINGS INC

```

This will return a DataFrame with the listing IDs, dates, and company names of the securities in the **`Russell 3000 Index`** universe between the specified start and end dates.

### Managing Universe

#### Web UI

PrismStudio provides a user-friendly web interface (Web UI) that allows you to conveniently manage your universes. This guide will walk you through the various tasks you can perform on universes using the Web UI.

**Accessing the Web UI**
To access the Web UI, execute the following code in your Python environment:

```python
>>> ps.finder()
```

This will launch the PrismStudio Web UI, where you can manage your queries.

![../_static/english_guide/Untitled16.png](../_static/english_guide/Untitled16.png)

**Managing Queries in the Web UI**

![../_static/english_guide/Untitled17.png](../_static/english_guide/Untitled17.png)

Once the Web UI is launched, you can perform the following operations on your universes using the right-click menu:

1. Delete: Allows you to delete a selected universe from your account.
2. Copy: Enables you to create a copy of a selected universe.
3. Cut: Provides the ability to cut (remove) a selected universe.
4. Paste: Allows you to paste a previously copied or cut universe into a different location.
5. Rename: Allows you to rename a selected universe.
6. Share: Enables you to share a universe with other users in your account.

```{tip}
When you choose to share a universe, it becomes accessible to other users within your PrismStudio account. This allows them to utilize the shared universe in their own analysis and data processing tasks.
```

**Creating Folders**
To create a folder and organize your universes within the Web UI, follow these steps:

1. Right-click in the desired location within the Web UI.
2. From the right-click menu, select **`New Folder`**.
3. The new folder will appear in the Web UI, and you can now move universes into it by dragging and dropping or using the cut/copy and paste operations.

By creating folders and organizing your universes within the Web UI, you can easily manage and access your queries based on their respective categories or purposes.

![../_static/english_guide/Untitled14.png](../_static/english_guide/Untitled14.png)

![../_static/english_guide/Untitled15.png](../_static/english_guide/Untitled15.png)

### API

PrismStudio also offers functionality to manage universes programmatically using code. This guide will demonstrate how to perform common query management tasks through code.

**Listing Saved Universe:**
To list the queries that you have saved, use the following code:

```python
>>> ps.list_universe() # Lists the queries saved by the user in dataframe format
```

```python
>>> ps.list_universe(tree=True) # Lists the queries saved by the user.

universe/
├── KR_primary
├── KRX 300
└── LSE_primary
```

**Deleting Universe:**
To delete a universe, use the **`delete_universe()`** function, providing the name of the query to be deleted:

```python
>>> ps.delete_universe(dataquery="new_daily_return")
```

**Renaming Universe:**
To rename a query, utilize the **`rename_universe()`** function, specifying the old name of the query and the desired new name:

```python
>>> ps.rename_universe(old="daily_return", new="new_daily_return")
```
To rename a universe or data query, you can use the prismstudio.rename_dataquery() function. This function allows you to change the name of a query, and if necessary, move it to a different directory. Specify the old name of the query and the desired new name as arguments to this function. If you want to move the query to a new directory, you can include the directory path as part of the new name.

```python
>>> ps.rename_universe(old="olddirectory/daily_return", new="newdirectory/daily_return")
```
---

## **📈** Backtest

### Factor Backtest

Factor backtest is a task that allows users to evaluate the effectiveness of investment factors. Users can easily experiment with various factors to assess their predictability. This guide provides instructions on how to perform a factor backtest in PrismStudio, with an example of backtesting the Sales to Price factor.

#### Executing Factor Backtest

**Step 1: Factor Input Preparation**
Before performing the factor backtest, we need to prepare the input components for the factor. In this example, we will create the Sales to Price factor. Follow these steps:

1. Generate the component representing total revenue using the [prismstudio.financial.income_statement](<#prismstudio.financial.income_statement>) function. Set the data period as Last Twelve Months (LTM) and the currency as the trading currency:

    ```python
    >>> rev = ps.financial.income_statement(100589, periodtype='LTM', currency='trade')
    ```

    ```{note}
    100589 represents the Dataitem Id for Revenue, Total.
    ```

2. Create the component representing market capitalization using the [prismstudio.market.market_cap](<#prismstudio.market.market_cap>) function:

    ```python
    >>> mcap = ps.market.market_cap()
    ```

3. Resample the revenue data from quarterly to daily frequency:

    ```python
    >>> rev = rev.resample('D')
    ```

4. Calculate the Sales to Price factor by dividing total revenue by market capitalization and store it as **`sp`**:

    ```python
    >>> sp = rev / mcap
    ```


**Step 2: Performing the Factor Backtest**

Now, let's perform the actual factor backtest using the [prismstudio.factor_backtest](<#prismstudio.factor_backtest>) function. We will backtest the Sales to Price factor against the S&P 500 universe. Set the following parameters:

- **`factor`**: The factor to be backtested (in this case, **`sp`**).
- **`universe`**: The universe against which the factor will be tested (e.g., "S&P 500").
- **`frequency`**: The rebalancing frequency (e.g., "M" for monthly).
- **`bins`**: The number of quantiles (e.g., 5).
- **`startdate`**: The start date of the backtest period (e.g., "2016-12-31").
- **`enddate`**: The end date of the backtest period (e.g., "2020-01-01").

Follow these steps:

1. Define the task component **`sp_fb`**:

    ```python
    >>> sp_fb = ps.factor_backtest(factor=sp, universe="S&P 500", frequency="M", bins=5, startdate='2016-12-31', enddate='2020-01-01')
    ```

2. Execute the factor backtest:

    ```python
    >>> sp_fb.run()
    ```

3. Once the factor backtest is complete, a report will be generated, and it will open in a new tab in your browser.

```{note}
In the result, Bin 1 represents the quantile with stocks having higher factor values.
```


#### Walking through a Factor Backtest report

Walking through a resulting factor backtest report involves analyzing various components and understanding their significance. Here is a step-by-step guide to interpreting each section of the report:

> Factor backtest report result
>

[factor_backtest_report.mp4](../_static/english_guide/factor_backtest_report.mp4)

**Summary Table:**
The summary table provides an overview of the inputs used in the factor backtest. It typically includes the following information:

- Universe Name: The name of the universe or group of securities used in the backtest.
- Period: The duration of the backtest period.
- Frequency: The frequency at which the factor is rebalanced (e.g., daily, monthly).
- Bins: The number of quantile portfolios created based on the factor's values.
- Average Turnover: The average turnover rate, indicating how frequently positions are traded.
- Average Information Coefficient: The average correlation between the factor and subsequent returns.
- Top-Bottom Spread: The performance difference between the top and bottom quantile portfolios.

**Annualized Return Table:**
This table displays the annualized return for each quantile portfolio during the factor backtest period. It helps assess the performance of different portfolios based on the factor's ranking. Higher returns typically indicate better performance, while lower returns may suggest inefficiencies in the factor.

**PnL and QR Interactive Graph:**
This interactive graph allows you to explore the profit and loss (cumulative return) and quantile return (period return) for each quantile portfolio. You can select or deselect individual portfolios for display, choose between linear and log scales, and select a specific period of interest to examine. This graph provides insights into the performance and volatility of each portfolio over time.

- PnL: It represents the cumulative return for each rebalancing period for every quantile portfolio. It shows the overall profit or loss generated by each portfolio throughout the backtest period.
- QR (Quantile Return): This indicates the return for each quantile portfolio during each rebalancing period. It reflects the performance of each portfolio over shorter intervals within the backtest period.

**Information Coefficient Line Graph:**
The information coefficient measures the correlation or predictive power of the factor with subsequent returns. The line graph visualizes this coefficient over time. You can choose between linear and log scales and select a specific period for analysis. Higher values of the information coefficient suggest a stronger relationship between the factor and future returns.

**Turnover Line Graph:**
The turnover line graph illustrates the turnover rate for each quantile portfolio over time. Turnover represents the frequency of trading or portfolio rebalancing. This graph helps assess the cost and feasibility of implementing the factor strategy. By selecting a specific period of interest, you can analyze changes in turnover during that timeframe.

**Performance Summary Table:**
The performance summary table combines PnL and QR information into a single table. It provides additional details such as the number of securities included in each rebalancing period for every quantile portfolio. This information helps evaluate the breadth and stability of the factor's performance.

By analyzing each component of the factor backtest report, you can gain insights into the performance, risk, and predictive power of the factor strategy. These insights can guide investment decisions and further refinement of the factor model.

#### Retrieve a Factor Backtest result

To programmatically retrieve a factor backtest result using the [prismstudio.get_factor_backtest_result](<#prismstudio.get_factor_backtest_result>) function, follow this guide:

Call the [prismstudio.get_factor_backtest_result](<#prismstudio.get_factor_backtest_result>) function with the required parameters:

```python
>>> result = ps.get_factor_backtest_result(fbid, data=True, report=False)
```

- **`fbid`**: Provide the factor backtest ID as an integer. This identifies the specific factor backtest you want to retrieve the result for.
- **`data=True`**: Set this parameter to **`True`** to include the dataframe in the returned value. This will provide the factor backtest results as a dictionary of dataframes.
- **`report=False`**: Set this parameter to **`False`** to avoid opening an interactive GUI report in a web browser at the end of the process. If you set it to **`True`**, it will open the interactive Factor Backtest Report.

Retrieve the desired data from the returned result:

```python
>>> summary = result['summary']  # Summary of the factor backtest job
>>> ar = result['ar']  # Annualized return
>>> counts = result['counts']  # Number of securities in each bin
>>> ic = result['ic']  # Information coefficient
>>> pnl = result['pnl']  # Profit & losses
>>> qr = result['qr']  # Quantile return
>>> to = result['to']  # Turnover
```

- **`summary`**: Contains the summary of the factor backtest job.
- **`ar`**: Provides the annualized return for each quantile portfolio.
- **`counts`**: Gives the number of securities in each bin for each rebalancing period.
- **`ic`**: Represents the information coefficient over time.
- **`pnl`**: Holds the profit and losses (cumulative return) for each rebalancing period and quantile portfolio.
- **`qr`**: Contains the quantile return (period return) for each rebalancing period and quantile portfolio.
- **`to`**: Indicates the turnover for each rebalancing period and quantile portfolio.

You can further analyze or process these dataframes according to your requirements.

### Managing Factor Backtest Results

#### Web UI

Managing factor backtest results with a web UI offers convenient control and access to essential information. Here's a guide on managing factor backtest results using the job manager web UI:

> Job Manager Capture
>

![../_static/english_guide/Untitled18.png](../_static/english_guide/Untitled18.png)

Job Display Items:
In the job manager web UI, you will find the following display items for each factor backtest job:

- Job ID: A unique identifier assigned to each factor backtest job.
- Job Name: The name given to the factor backtest job for easy identification.
- Job Status: Indicates the current status of the job, such as completed, failed, canceled, or pending.

Relevant Information:
The job manager web UI provides relevant information about factor backtest inputs and results. This includes:

- Factor Backtest Inputs: Information such as the start and end dates of the backtest, the universe of securities used, the factor being tested, the number of bins, the frequency of rebalancing, and the rank method employed.
- Factor Backtest Results: Key metrics and statistics obtained from the backtest, such as the top-bottom spread (performance difference between top and bottom portfolios), average information coefficient (correlation between the factor and subsequent returns), and average turnover (frequency of portfolio turnover).

Managing Tasks:
The job manager web UI offers several managing tasks to efficiently handle factor backtest jobs. These tasks include:

- Renaming the Job Name:
You can rename the job name to provide a more descriptive or meaningful title. This can be useful for better organization and identification of factor backtest jobs within the job manager. Simply select the desired job and use the provided functionality to rename it.
- Adding Description:
You have the option to add a description or additional notes to a factor backtest job. This feature allows you to provide context, explanations, or any other relevant information associated with the job. It can be helpful for documenting important details or providing additional insights.
- Deleting a Job:
If you want to remove a factor backtest job from the job manager, you can delete it. This action permanently removes the job and its associated data from the system. Exercise caution when deleting a job, as it cannot be undone.
- Reopening the Report Webpage:
By clicking on the report icon associated with a specific factor backtest job, you can reopen the report webpage for that particular job. This allows you to revisit the interactive Factor Backtest Report and review the results, graphs, and data visualizations.
- Extracting Reconstructed Python Codes:
The job manager web UI provides an Extract icon for each factor backtest job. By clicking on this icon, you can extract the reconstructed Python codes associated with that particular job. This can be beneficial for reproducing the analysis, conducting further research, or sharing the code with others.

Utilizing the job manager web UI enhances the management and accessibility of factor backtest results. It offers a user-friendly interface to organize, track, and retrieve crucial information, and provides additional functionalities for customization and exploration of the results.

---