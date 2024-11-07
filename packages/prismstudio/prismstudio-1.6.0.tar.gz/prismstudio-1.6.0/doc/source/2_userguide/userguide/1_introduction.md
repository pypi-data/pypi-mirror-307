# Introduction to PrismStudio

## What is PrismStudio?

Welcome to the user guide for PrismStudio, a powerful financial data management and analysis tool. PrismStudio is designed to enable users in efficiently retrieving, managing, and utilizing financial data. With PrismStudio as your financial tool, you can leverage its comprehensive features and functionalities to streamline your financial data management workflow. Whether you are a financial analyst, researcher, or investor, PrismStudio provides the necessary tools to access, analyze, and interpret financial data effectively.

PrismStudio is designed to be a flexible and accessible financial data management solution. One of its key advantages is that you can use it on any hardware with an internet connection, providing you with the convenience of accessing your financial data from anywhere at any time.

This user guide will serve as your roadmap to harness the full potential of PrismStudio, enabling you to make data-driven investment, decision-making, and analysis, and gain valuable insights into the financial markets.

## PrismStudio Structure
![PrismStudio Structure](../../_static/english_guide/PrismStudio.png)

The PrismStudio platform is structured to deliver a seamless and efficient experience in financial data management and analysis. Understanding its architecture will help you navigate and utilize the system effectively.

### Understanding the Resolver in PrismStudio
In the PrismStudio ecosystem, the Resolver plays a critical role in processing and fulfilling user queries. When a user submits a query, which is structured as a complex tree containing various instructions and requests, the Resolver acts as the orchestrator that ensures the precise execution of each step.

Whenever a query comes in, it goes through the following stages facilitated by the Resolver:


#### High-Speed Asynchronous Data Extractor

PrismStudio incorporates asynchronicity into its data extractor to optimize the process of retrieving complex financial data. Here’s how it enhances the system’s efficiency and performance:

Asynchronous Requests: When a user inputs a complex query, which is typically organized in a tree structure with multiple branches requiring various data points and transformations, PrismStudio's data extractor does not operate on a linear, synchronous basis. Instead, it sends out multiple requests to the database simultaneously, rather than waiting for each request to complete before initiating the next. This approach drastically reduces data loading times, allowing for faster access to necessary data.

Intelligent Data Retrieval: To avoid redundant operations, the system is designed to recognize when the same data is needed at different nodes within the query structure. Instead of pulling this data multiple times, PrismStudio’s extractor retrieves it only once and then efficiently distributes it across the various parts of the query tree where it's needed. This not only minimizes the load on the database but also speeds up the data processing time.

#### Security Master Mapper
The Security Master Mapper is a pivotal component in PrismStudio's architecture, especially when it comes to the integration of cross-vendor data. Its role can be understood in several key functions:

Centralizing Security Identifiers: The Mapper creates a "master key" within the security master database, which serves as the central reference point for all security identifiers across different data vendors. Each vendor may have its unique way of identifying securities, such as stocks, bonds, or other financial instruments. The Mapper standardizes these into a single identifier that can be consistently used throughout PrismStudio.

Enabling Cross-Vendor Data Integration: For users to perform comprehensive analyses, they often need to integrate data from various sources. The Mapper allows for this by ensuring that a security identified by different names or codes across various databases is recognized as the same entity in PrismStudio. This seamless integration is essential for users who require a holistic view of the security across different data packages from different vendors.

#### PrismStudio Data Processing Engine
The PrismStudio Data Processing Engine is a sophisticated data integration module designed to convert complex and heterogeneous raw data into a standardized format that is usable and consistent for end-users. Here's how it serves this critical function:

Harmonizing Data from Multiple Vendors: Given that each data vendor can have unique table structures and data presentation methods, the Data Processing Engine acts as a translator. It interprets the various data schemas and harmonizes them into a single, coherent form. This standardization is crucial for analysts who rely on data comparability to make informed decisions.

Establishing a Consistent Data Schema: The Engine is tasked with creating a consistent data schema across all data sources. This means regardless of how the data is initially structured or stored by different vendors, the output that users interact with will follow a uniform format. This uniformity is key to enabling users to perform reliable and accurate analyses without needing to understand the intricacies of each vendor's data setup.

Seamless Data Experience Across Platforms: A key benefit of the Data Processing Engine's integration capability is the seamless experience it provides. Users can switch between different datasets from various vendors without the need to adjust their analysis methodology according to different data formats or structures.

Cross-Vendor Data Integration: The Engine's integration process includes the capability to manage cross-vendor data dependencies. For example, if a particular analysis requires combining ownership data from one vendor with market data from another, the Engine ensures that these diverse data types are compatible and can be integrated smoothly.

#### PrismStudio Data Transform Engine
The Arrow-Based Multithreaded PrismStudio Data Transform Engine is engineered to handle the demanding computational needs inherent in financial time-series data analysis. Here's how its multithreaded capabilities are central to its performance:

Efficiency in Data Transformation: Multithreading allows the Transform Engine to perform numerous operations concurrently. For time-series data that often require complex computations such as rolling window calculations, moving averages, or various other statistical transformations, this capability means that these tasks are completed in a fraction of the time they would take in a single-threaded environment.

Zero-Copy Reads for Speed: Apache Arrow's zero-copy reads capability means that the Data Transform Engine can access large volumes of time-series data quickly without the need for costly memory operations. This enhances the speed at which data can be read and transformed, significantly reducing the time taken from data ingestion to actionable analysis.

#### Investment Analytics Tools in PrismStudio
PrismStudio offers a suite of analytics tools tailored for investment analysis, allowing users to delve deep into financial data and derive actionable insights. These tools are designed to cater to various aspects of investment strategy, from backtesting and risk assessment to portfolio optimization and environmental, social, and governance (ESG) considerations.


### Flexibility in PrismStudio
PrismStudio offers users the flexibility to access processed data directly, bypassing transformation and analytics if they choose. This feature caters to those who may simply require clean, standardized datasets for external use or prefer to perform their own analyses outside the platform. Essentially, PrismStudio accommodates diverse user preferences by providing a streamlined path from data extraction to final output, with optional in-platform transformation and analytics.