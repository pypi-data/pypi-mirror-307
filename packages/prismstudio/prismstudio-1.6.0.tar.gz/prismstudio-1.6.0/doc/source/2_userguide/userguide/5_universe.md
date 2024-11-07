
## Universe
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

Let’s try a bit more realistic filter you might need. Here you want to create an Canadian stock universe with primary stock and you want to exclude any ETFs, REITs, Public Funds, etc:

```python
>>> ps.filter_universe([
        {'attribute': 'Country', 'value': ['CA']},
        {'attribute': 'MIC', 'value': ['XTSE']},
        {'attribute': 'Prism Primary', 'value': ['primary']},
        {'attribute': 'Security Type', 'value': ['Common Equity']},
        {'attribute': 'Company Type', 'value': ['Public Company']},
    ], universename='Canada_primary')
```

In this code, multiple filter conditions are applied. It filters items based on attributes such as Country: Canada, MIC (Exchange Code): XTSE, CIQ primary: primary, Security Type: Common Equity, and Company Type: Public Company. The resulting stocks are stored in the "Canada_primary" universe.

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


### Managing Universe

#### API

PrismStudio also offers functionality to manage universes programmatically using code. This guide will demonstrate how to perform common query management tasks through code.

**Listing Saved Universe:**
To list the universes you have saved using the [prismstudio.list_universe](<#prismstudio.list_universe>) function. This will display the user-created universes along with their details.

```python
>>> ps.list_universe()
```

```python
>>> ps.list_universe(tree=True)

universe/
├── KR_primary
├── KRX 300
└── LSE_primary
```

**Deleting Universe:**
To delete a universe, use the **`delete_universe()`** function, providing the name of the universe to be deleted:

```python
>>> ps.delete_universe(universe="KRX 300")
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

#### Web UI

PrismStudio provides a user-friendly web interface (Web UI) that allows you to conveniently manage your universes. This guide will walk you through the various tasks you can perform on universes using the Web UI.

**Accessing the Web UI**
To access the Web UI, execute the following code in your Python environment:

```python
>>> ps.finder()
```

This will launch the PrismStudio Web UI, where you can manage your univeres.

![../../_static/english_guide/Untitled16.png](../../_static/english_guide/Untitled16.png)

**Managing Universes in the Web UI**

![../../_static/english_guide/Untitled17.png](../../_static/english_guide/Untitled17.png)

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

![../../_static/english_guide/Untitled14.png](../../_static/english_guide/Untitled14.png)
![../../_static/english_guide/Untitled15.png](../../_static/english_guide/Untitled15.png)


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
