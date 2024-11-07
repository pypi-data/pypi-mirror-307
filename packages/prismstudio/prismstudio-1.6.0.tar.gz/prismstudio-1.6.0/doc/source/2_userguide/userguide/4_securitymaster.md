# Security Master and Universe
Understanding the Security Master and Universe is crucial as it lays the groundwork for all subsequent financial analysis within PrismStudio. The Security Master serves as the central repository for security identification, a vital reference point when integrating data across various sources or vendors. The Universe, on the other hand, is a dynamic collection of securities defined by user-specified criteria. By starting with these features, you can establish a solid base for accurate and efficient data retrieval.

## Security Master
The Security Master is a comprehensive database that provides detailed identification and meta data for each securities. It includes a wide range of attributes that help identify and categorize securities, enabling users to efficiently manage and analyze their portfolios. This user guide will familiarize you with the available attributes in the Security Master and their corresponding descriptions.

### Security Master Search
When it comes to searching the Security Master, Prism offers two convenient approaches: programmatic searching using the [prismstudio.get_securitymaster_advanced](<#prismstudio.get_securitymaster_advanced>) function and the user-friendly Security Master Search Web UI. Programmatic searching allows for automation and integration within the python environemnt, while the web UI offers a visual interface that simplifies the search process for users who prefer a graphical approach.

#### Search Security Master with Web UI
The Security Master Search Web UI provides a user-friendly interface for searching securities based on specific criteria. You can also open the search page directly using the [prismstudio.securitymaster_search](<#prismstudio.securitymaster_search>) code.

In this example, let's walk through the steps to search for securities headquartered in the US that have "motor" in their company name. Here's a step-by-step guide on how to navigate the Security Master Search Web UI:

**Step 1: Selecting Search Attributes:**
- Use the left side panel to select the attributes for your search.
- For example, choose the "country" attribute and type "US" in the search bar.
- To add additional search criteria, click the (+) button to add a new line of rules.
- Select the "companyname" attribute and enter "motor" in the search bar.

![Untitled](../../_static/english_guide/Untitled8.png)


**Step 2: Managing Search Rules**
- If you make a mistake or want to remove a search rule, click the "X" button on the right side of the rule to delete it.
- To remove all the search rules at once, click the "(-) Remove All" button located in the bottom left corner of the left side panel.

**Step 3: Performing the Search:**
- Once you have entered the desired search criteria, click the "Search" button to initiate the search.
- The side panel will collapse, and the search results will appear if there are no errors.

![Untitled](../../_static/english_guide/Untitled9.png)

**Step 4: Viewing Detailed Security Information:**

- The search results will be displayed on the page.
- You can select a specific security from the list to view its detailed information.
- Upon selecting a security, the right side panel will appear, providing comprehensive details about the selected security, including its attributes and historical values.

![Untitled](../../_static/english_guide/Untitled10.png)

**Step 5: Customizing Viewing Options:**

- To customize your browsing experience, you can adjust the page viewing options.
- Select the number of data items you want to display per page, such as 25, 50, or 100.
- Use the navigation buttons (">", ">>", "<", "<<") to move between pages and explore the search results effectively.
- To download the search results, look for a download button on the web page and click it to initiate the download process.

![Untitled](../../_static/english_guide/Untitled11.png)

#### Search Security Master Programatically

To programmatically search for specific securities in the security master, Prism provides the convenient [prismstudio.get_securitymaster_advanced](<#prismstudio.get_securitymaster_advanced>) function. This powerful feature allows you to retrieve securities that match specific attribute values, enabling targeted searches and providing direct access to the results within your workspace.

To perform a search, you need to specify the attribute and its corresponding search value. The **`attribute`** parameter refers to the specific attribute you want to search for in the security master, such as "country" or "GICS sector". The **`search`** parameter represents the value you want to search for within the chosen attribute.

Additionally, the **`operator`** parameter allows you to specify the logical operator for combining multiple search conditions. By default, the operator is set to "AND", meaning that all specified conditions must be met. You can also explicitly specify "OR" to retrieve securities that match any of the specified conditions.

Let's explore an example where we search for securities that are based in the United States (country) and belong to GICS sector 30 (Consumer Staples).

```python
>>> ps.get_securitymaster_advanced([
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