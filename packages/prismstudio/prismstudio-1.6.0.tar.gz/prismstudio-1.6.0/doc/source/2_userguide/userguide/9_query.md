# Query

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

## Saving Query

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

## Loading Query

PrismStudio provides the capability to load previously saved queries, allowing you to reuse and manipulate them in your data processing tasks. The following guide will walk you through the process of loading queries using the [prismstudio.load_dataquery](<#prismstudio.load_dataquery>) function and how to work with the returned component.

By using the [prismstudio.load_dataquery](<#prismstudio.load_dataquery>) function and specifying the name of the query, a component containing the query is returned. This component is identical to the one you originally created, allowing you to utilize it immediately for further processing. Let's consider an example where we want to load a query named "daily_return":

```python
>>> r = ps.load_dataquery(dataquery="daily_return")
```

Once the query is loaded, you can perform various operations and tasks on the returned component, just like you would with any other component.

## Extracting Query

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

## Managing Query

### Web UI

PrismStudio provides a user-friendly web interface (Web UI) that allows you to conveniently manage your queries. This guide will walk you through the various operations you can perform on queries using the Web UI.

**Accessing the Web UI**

To access the Web UI, execute the following code in your Python environment:

```python
>>> ps.finder()
```

This will launch the PrismStudio Web UI, where you can manage your queries.

![../../_static/english_guide/Untitled12.png](../../_static/english_guide/Untitled12.png)

**Managing Queries in the Web UI**

Once the Web UI is launched, you can perform the following operations on your queries using the right-click menu:

![../../_static/english_guide/Untitled13.png](../../_static/english_guide/Untitled13.png)

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

![../../_static/english_guide/Untitled14.png](../../_static/english_guide/Untitled14.png)

Step 3: The new folder will appear in the Web UI, and you can now move queries into it by dragging and dropping or using the cut/copy and paste operations.

![../../_static/english_guide/Untitled15.png](../../_static/english_guide/Untitled15.png)

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