# Task and Job

## Task
In PrismStudio, a task refers to a series of activities designed to produce results beyond just data output. Examples include the screen task, which generates a 'universe' object, and the factor backtest task, which produces comprehensive reports. A notable feature of tasks in PrismStudio is their operational design: upon creation, a task initiates and executes a job but does not occupy the Python interpreter until the job's completion. Instead, the task is placed in a queue. The status and results of these queued jobs can be tracked and retrieved through the job manager, accessible via **`ps.job_manager()`**. Currently, PrismStudio offers various types of tasks, such as screen, data export, and factor backtest, each with specific functions and outputs, which are set to be detailed in the following sections.

### Screen
The Screen task is designed to refine the universe of stocks by applying specific screening rules. It allows users to dynamically construct a universe of stocks that meet certain criteria at different points in time. This point-in-time mechanism ensures that the universe of stocks is relevant and accurate for the specific time frame under consideration, reflecting the changing nature of stock characteristics and market conditions. This process is especially crucial for investors and analysts who require a consistent and reliable basis for pulling data and making informed decisions.

For more information regarding screen task, please reference [Screen Universe](<#Screen Universe>)

### Data Export

The Data Export task enables the extraction of data, allowing for its retrieval at a later time. This contrasts with the get_data function, where the outcome is immediately delivered to the Python work environment as soon as it is ready, but can only be accessed once—requiring a new get_data invocation for any subsequent retrievals. Furthermore, the execution of a get_data request occupies the Python interpreter until completion. On the other hand, the Data Export process submits the request to a task queue, freeing up the interpreter almost immediately and initiating a job. Upon completion of the job, the resulting specific data file can be downloaded via the finder or imported directly into Python using [prismstudio.retrieve_datafiles](#prismstudio.retrieve_datafiles). Moreover, the generated data file can be accessed multiple times, provided it has not been deleted.

For more information regarding data export task, please reference [Data Export](<#### Data Export>)

## Job
Job in PrismStudio refers to a specific computational process or task initiated by the user. When a user executes a task, such as a data analysis, screen, or backtest, PrismStudio translates this into a job. This job is then processed asynchronously, meaning it runs independently of the user's immediate interaction. It allows for efficient handling of complex or time-consuming tasks without tying up the user interface or requiring the user to wait for the task to complete. The progress and results of these jobs can be monitored and accessed through the job manager, a feature in PrismStudio that provides visibility and control over the queued and completed jobs.

### Managing Job