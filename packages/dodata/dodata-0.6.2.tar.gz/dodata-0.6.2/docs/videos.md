# Videos

## Browse Projects: From Device to Wafer-Level Analysis

### Step 1: Explore the Cell View
- Access the **Cell View** to explore all cells extracted from the **GDS file** or **device manifest**.
- Each cell can include **simulations** or **measurements**, and attributes like **XY coordinates, width,** and **length**.
- **GDS Visualization** (optional): If available, visualize the GDS file, which is particularly useful for collaboration between testers and designers.

### Step 2: View Device Details
- Dive into **device-level measurements and simulations** for insights into performance.
- Observe **measurement variations** across different dies and analyze **die X and Y coordinates**.

### Die-Level Analysis
- Select individual dies (e.g., **die 2,0 on a wafer**) to view **die-level analysis**.
- This helps in detecting performance variations across dies on the same wafer.

### Wafer-Level Analysis
- Analyze **sheet resistance distribution** across the wafer and see **pass/fail results** based on spec limits.
- Non-functional dies outside spec limits are highlighted, aiding quick problem identification.

### Cross-Wafer Comparison
- Compare multiple wafers by creating **comparison plots** (e.g., sheet resistance distribution).
- Set **min/max values** to filter outliers like shorts or open circuits.
- Interactively display and analyze individual wafers’ distributions for greater detail.

### GDS Visualization
- Use **GDS file visualization** to inspect chip layouts, compare designs, or update attributes.
- This feature is valuable for continuous design iteration and detailed analysis.

### Summary
In this video, we covered navigating projects from cells to full-lot analysis. You can now visualize GDS files, analyze devices, compare wafers, and more. We hope this guide has been helpful, and look forward to seeing you next time.

<iframe width="560" height="315" src="https://www.youtube.com/embed/D48N0F8xWtk?si=45zw9Q7_UWvgCfgP" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Upload a New Project and Navigating the Interface

- **Start a New Project**:
  - Click on **"New Project"**.
  - Enter a name for your project.
  - (Optional) Upload a **GDS file** and a **K-layout layer properties file** to visualize the layout and cells.

- **Select Hierarchy Levels**:
  - Choose the hierarchy levels to extract (e.g., one level below the top to extract the first level of cells).
  - Use **regular expressions** to include or exclude specific cells.

- **Upload Project**:
  - Click **"Upload"** to save the project to the database.
  - The project will now appear in the **project dashboard**.

- **Explore Project Features**:
  - Upload a **wafer definition** if needed.
  - View **extracted cells, layout, and design attributes**.
  - For each cell, access **cell properties**, layout details, and associated measurements or simulations.

- **Use Tool Options**:
  - **Zoom in/out**, toggle layers, and inspect metadata for each cell.
  - Select specific cells (e.g., a spiral) to check dimensions like width and extra length.

This guide provides an overview of creating and navigating a new project through the web interface. For instructions on creating your project in Python, please refer to the next video.

<iframe width="560" height="315" src="https://www.youtube.com/embed/bn298jmMa1I?si=8Ybfb5rdyiK5Ccls" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>



## Upload Measurement or Simulation Data

- **Select Device**:
  - Navigate to **Cells** and select the device you want to upload data for.
  - Click **New Data** and choose your data type (e.g., **measurement**).

- **Upload Data**:
  - The tool supports both **CSV** and **JSON** formats for data uploads.

- **Set Details**:
  - Set the **time to now**.
  - (Optional) Add details like **Wafer ID, DieX, DieY**, or other attributes you’d like to track.
  - For example, enter a **temperature** of 25°C, or any other relevant values.

- **Configure Plotting Settings**:
  - Choose **x_col** for the x-axis.
  - Select one or more columns for the **y-axis** from your data.

- **Complete Upload**:
  - Once everything is configured, click **Upload**.

Your data is now uploaded to the database, ready for visualization and analysis. You can view all entered attributes, zoom in to explore details, and multiple channels will be displayed if applicable.


<iframe width="560" height="315" src="https://www.youtube.com/embed/HDLavQPoKGI?si=ZxqiE_dBT470bpg3" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## Trigger an Analysis on Uploaded Data

- **Select Measurement**:
  - Go to **Cells** and select the measurement you uploaded.
  - Click **New Analysis**.

- **Choose Analysis Function**:
  - In the **Analysis** tab, select from available analysis functions.
  - Customize parameters as needed (e.g., for a device power envelope analysis with **10 samples** to create a window average and smooth data).

- **View Results**:
  - Once the analysis is complete, view both the **input parameters** and **output results**.
  - You can download the results as a **ZIP file** containing JSON data and a PNG plot.

- **Run Comparison Analysis**:
  - Trigger a second analysis with **n = 2 samples** to smooth data with fewer samples and compare with the first analysis.

- **Delete Analysis**:
  - Click **Delete** to remove the analysis from the database if needed.

In this video, we covered triggering an analysis, viewing parameters and results, downloading outputs, and deleting an analysis. For custom analysis function uploads, stay tuned for the next video.

<iframe width="560" height="315" src="https://www.youtube.com/embed/HzwniXIKkj4?si=RZq8-ZwhXe5chCAr" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>



## Upload Custom Analysis Functions

- **View Available Analysis Functions**:
  - Go to the **Analysis** tab to see all analysis functions.
  - Three types of functions are available:
    - **Device Analysis** for devices under test
    - **Aggregated Die Analysis** for dies
    - **Aggregated Wafer Analysis** for wafers
  - For each function, you can view the **ID, version,** and **code**.

- **Download Analysis Function**:
  - To download a specific version, click the **Download** button.
  - When triggering an analysis, the **latest version** is used by default.

- **Upload a Custom Analysis Function**:
  - Click **New Function** to upload custom code.
  - All code is **validated** to ensure safety before execution.

- **Modify Existing Code**:
  - Download the code (e.g., for the device power envelope analysis).
  - Update the code or adjust default parameters as needed.
  - After modifications, select the updated file, specify the **device data type**, and upload it.

- **Test and Validate**:
  - To apply the function to specific data, locate the **Target Model Primary Key** of the measurement.
  - Test the function with various input parameters to preview the output.
  - Once validated, the function is added to the database and ready for use.

- **Trigger and Review Analysis**:
  - Trigger the analysis on uploaded data and review the results.

In this video, we covered uploading analysis functions, downloading and modifying code, validating custom functions, and triggering analysis on data. For performing these actions directly in Python, stay tuned for the next video.

<iframe width="560" height="315" src="https://www.youtube.com/embed/_tsJQ3uIEdc?si=w9zgRy9idhzvstC5" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Upload Data and Analysis Functions Using the Python API

### Step 1: Set Up Jupyter Notebook
- Open the **Jupyter Notebook Interface** in the **Do-Lab tab**.
- Run each cell to generate the **layout** and **device table** by pressing **Shift + Enter**. This process creates both the **GDS file** and **device table CSV file**.

### Step 2: Generate Measurement Data
- In the next notebook, generate the **measurement data** required for upload.
- Run all cells from the **Run tab** to create **JSON files** for each die on the wafer.
- The generated files are saved in folders by **wafer ID**, with subfolders for each die containing JSON data for each spiral cutback length.

### Step 3: Upload Data to the Platform
- In the third notebook, open a new tab to monitor the **creation of a new project**.
- **Upload the Design Manifest** (device details) and **Wafer Definition** (wafer map).
- Upload measurement data:
  - Use **multiple threads** to speed up the process (e.g., 10 threads for faster upload).
  - Monitor the **progress bar** for upload status, which depends on file size and thread count.

### Step 4: Define and Upload Analysis Functions

#### Types of Analysis Functions
- **Device Analysis** for devices under test
- **Die Analysis** for die-level aggregation
- **Wafer Analysis** for wafer-level aggregation

#### Device Analysis
- Upload the **device analysis function** and retrieve the primary key for a single device.
- Set sample size (e.g., **n=10** for averaging, or **n=2** for smaller windows) and validate.
- Use `validate_and_upload` to add the function to the platform.

#### Die Analysis
- Trigger a die analysis for **0.3, 0.5, and 0.8 micrometer** waveguides.
- Set the target model to **die**, validate, and upload.
- Run **63 die analyses** (21 dies x 3 waveguide widths) sequentially and view the results, including **dB/cm loss** based on cutback length.

#### Wafer Analysis
- Aggregate results by uploading the **wafer analysis function**.
- Set spec limits to flag outliers (e.g., **3.13 dB/cm** for 0.3 micrometer waveguides).
- Validate and upload with these spec limits:
  - **3.13 dB/cm** for 0.3 micrometer,
  - **2.31 dB/cm** for 0.5 micrometer,
  - **1.09 dB/cm** for 0.8 micrometer.
- Review yield results for each waveguide width and die, with an overview available in the web interface.

In this video, we demonstrated the use of the Python API for data and function uploads, ideal for automating processes on a lab computer or server. The next video will cover data downloads and advanced queries using Python or SQL.


<iframe width="560" height="315" src="https://www.youtube.com/embed/hULflQoYQfI?si=aUGJikY3dK9mFLIl" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Download Data Using the Python API

### Step 1: Access the Do-Lab Tab
- Open the **Do-Lab tab** to begin downloading data from the "Spiral" project set up in the previous video.

### Step 2: Import the Do-Data Module
- Import the required data module as **TD**.
- Execute each code cell by pressing **Shift + Enter**.

### Understanding the Database Structure
- **Projects**: Every chip belongs to a project.
- **Cells**: Entities within a project.
- **Devices**: Each cell instantiation is a device with **X, Y coordinates**.
- **Device_data**: Stores testing or simulation data.
- **Analysis**: Device data, dies, or wafers can be analyzed with specific functions.
- Data relationships are maintained by linking wafers to projects and dies to wafers.

### Step 3: Querying Data with GetDataByQuery
- Use the **GetDataByQuery** function to filter data with specific clauses.
  - For example, filter by **project ID** (e.g., "Spirals") to retrieve relevant data.
  - Filter data by **project ID** and **device ID** to obtain device-specific data.
  - This data can be stored in a **Pandas DataFrame** with columns like wavelength and output power for easy analysis and plotting.

- **Additional Metadata**:
  - View metadata such as **device ID**, **die origin (x, y coordinates)**, **wafer ID**, **set ID**, and **parent cell**.

### Building a Flat Table for Analysis Tools
- Combine device data into a single **DataFrame** to create a large flat table.
- This table is suitable for exporting to analysis tools like **JMP** or **Excel** for further insights.

### Performing Advanced Queries
- Use the API’s **attribute filter** for advanced data retrieval.
  - Filter by specific **cell attributes** (e.g., settings embedded in GDS or uploaded via CSV).
  - Example: Query devices with a **0.3-micron width** for a specific project and die, yielding six devices with this width.

- **Refining Queries with OR Conditions**:
  - Use OR conditions to filter data from specific dies or other attributes like **length** or **width**.

### Combining Conditional and Attribute Clauses
- Combine **conditional** and **attribute clauses** to create complex queries—all without writing any SQL.

In this video, we demonstrated downloading data using Python, retrieving attributes, performing advanced filtering, and building tables for analysis in tools like JMP or Excel.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Mu_I_ePSieU?si=cYazbvEmKfDKD6L1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
